#include "mainwindow.h"

#include <QApplication>
#include <QDesktopWidget>
#include <QPainter>
#include <QFileDialog>
#include <QClipboard>
#include <QAction>
#include <QMap>
#include <QStyleFactory>

namespace {
const int RECORD_MIN_SIZE = 220;
const int SPACING = 5;
}

MainWindow::MainWindow(QWidget *parent)
    : QLabel(parent)
{
    initDBusInterface();
     initUI();
     startScreenshot();
}

MainWindow::~MainWindow()
{
}

void MainWindow::initUI() {
    setWindowFlags(Qt::X11BypassWindowManagerHint | Qt::Tool | Qt::WindowStaysOnTopHint);
    setMouseTracking(true);   // make MouseMove can response

    m_configSettings =  ConfigSettings::instance();
    installEventFilter(this);
    m_hotZoneInterface->asyncCall("EnableZoneDetected", false);

    QPoint curPos = this->cursor().pos();
     m_screenNum = qApp->desktop()->screenNumber(curPos);
     QList<QScreen*> screenList = qApp->screens();
     if (m_screenNum != 0 && m_screenNum < screenList.length()) {
        m_backgroundRect = screenList[m_screenNum]->geometry();
     } else {
         m_backgroundRect =  qApp->primaryScreen()->geometry();
     }
     qDebug() << "this screen geometry:" << m_screenNum << m_backgroundRect;
     this->move(m_backgroundRect.x(), m_backgroundRect.y());
     this->setFixedSize(m_backgroundRect.size());
     shotFullScreen();

    m_windowManager = new WindowManager();
    m_windowManager->setRootWindowRect(m_backgroundRect);

    m_rootWindowRect.x = 0;
    m_rootWindowRect.y = 0;
    m_rootWindowRect.width = m_backgroundRect.width();
    m_rootWindowRect.height = m_backgroundRect.height();

    if (m_screenNum == 0) {
        QList<xcb_window_t> windows = m_windowManager->getWindows();
        for (int i = 0; i < windows.length(); i++) {
            m_windowRects.append(m_windowManager->adjustRectInScreenArea(
                                     m_windowManager->getWindowRect(windows[i])));
        }
    }

    m_sizeTips = new TopTips(this);
    m_sizeTips->hide();
    m_toolBar = new ToolBar(this);
    m_toolBar->hide();
    m_zoomIndicator = new ZoomIndicator(this);
    m_zoomIndicator->hide();

    m_menuController = new MenuController;

    m_isFirstDrag = false;
    m_isFirstMove = false;
    m_isFirstPressButton = false;
    m_isFirstReleaseButton = false;

    m_recordX = 0;
    m_recordY = 0;
    m_recordWidth = 0;
    m_recordHeight = 0;

    m_resizeBigPix = QPixmap(":/image/icons/resize_handle_big.png");
    m_resizeSmallPix = QPixmap(":/image/icons/resize_handle_small.png");

    m_dragRecordX = -1;
    m_dragRecordY = -1;

    m_needDrawSelectedPoint = false;
    m_mouseStatus = ShotMouseStatus::Shoting;

    m_selectAreaName = "";

    m_isShapesWidgetExist = false;
    connect(m_toolBar, &ToolBar::buttonChecked, this,  [=](QString shape){
        if (m_isShapesWidgetExist && shape != "color") {
            m_shapesWidget->setCurrentShape(shape);
        } else if (shape != "color") {
            initShapeWidget(shape);
            m_isShapesWidgetExist = true;
        }
    });

    connect(m_toolBar, &ToolBar::requestSaveScreenshot, this,
            &MainWindow::saveScreenshot);
}

void MainWindow::initDBusInterface() {
    m_controlCenterDBInterface = new DBusControlCenter(this);
    m_notifyDBInterface = new DBusNotify(this);
    m_soundEffectInterface = new DBusSoundEffect(this);
    m_hotZoneInterface = new DBusZone(this);
}

bool MainWindow::eventFilter(QObject *, QEvent *event)
{
#undef KeyPress
#undef KeyRelease
    if (m_isShapesWidgetExist) {
        if (event->type() == QEvent::KeyPress) {
            QKeyEvent *keyEvent = static_cast<QKeyEvent*>(event);
            if (keyEvent->key() == Qt::Key_Escape) {
                m_hotZoneInterface->asyncCall("EnableZoneDetected",  true);
                qApp->quit();
                return false;
            }

            if (keyEvent->modifiers() == (Qt::ShiftModifier | Qt::ControlModifier)) {
                if (keyEvent->key() == Qt::Key_Left) {
                    m_shapesWidget->microAdjust("Ctrl+Shift+Left");
                } else if (keyEvent->key() == Qt::Key_Right) {
                    m_shapesWidget->microAdjust("Ctrl+Shift+Right");
                } else if (keyEvent->key() == Qt::Key_Up) {
                    m_shapesWidget->microAdjust("Ctrl+Shift+Up");
                } else if (keyEvent->key() == Qt::Key_Down) {
                    m_shapesWidget->microAdjust("Ctrl+Shift+Down");
                }
            } else if (qApp->keyboardModifiers() & Qt::ControlModifier) {
                qDebug() << "Control";
                if (keyEvent->key() == Qt::Key_Left) {
                    m_shapesWidget->microAdjust("Ctrl+Left");
                } else if (keyEvent->key() == Qt::Key_Right) {
                    m_shapesWidget->microAdjust("Ctrl+Right");
                } else if (keyEvent->key() == Qt::Key_Up) {
                    m_shapesWidget->microAdjust("Ctrl+Up");
                } else if (keyEvent->key() == Qt::Key_Down) {
                    m_shapesWidget->microAdjust("Ctrl+Down");
                }
            }  else {
                qDebug() << "left micro";
                if (keyEvent->key() == Qt::Key_Left) {
                    m_shapesWidget->microAdjust("Left");
                } else if (keyEvent->key() == Qt::Key_Right) {
                    m_shapesWidget->microAdjust("Right");
                } else if (keyEvent->key() == Qt::Key_Up) {
                    m_shapesWidget->microAdjust("Up");
                } else if (keyEvent->key() == Qt::Key_Down) {
                    m_shapesWidget->microAdjust("Down");
                }
            }

            if (keyEvent->key() == Qt::Key_Delete) {
                emit  deleteShapes();
            } else {
                qDebug() << "keyEvent:" << keyEvent->key();
            }
            return false;
        }
        return false;
    }

    if (event->type() == QEvent::MouseButtonDblClick) {
        saveScreenshot();
    }
    bool needRepaint = false;

    if (event->type() == QEvent::KeyPress) {
        QKeyEvent *keyEvent = static_cast<QKeyEvent*>(event);
        if (keyEvent->key() == Qt::Key_Escape) {
            qApp->quit();
        }

        if (m_mouseStatus == ShotMouseStatus::Normal) {
              if (keyEvent->modifiers() == (Qt::ShiftModifier | Qt::ControlModifier)) {
                  if (keyEvent->key() == Qt::Key_Left) {
                      m_recordX = std::max(0, m_recordX + 1);
                      m_recordWidth = std::min(m_recordWidth - 1,
                                                        m_rootWindowRect.width);

                      needRepaint = true;
                  } else if (keyEvent->key() == Qt::Key_Right) {
                      m_recordWidth = std::min(m_recordWidth - 1,
                                               m_rootWindowRect.width);

                      needRepaint = true;
                  } else if (keyEvent->key() == Qt::Key_Up) {
                      m_recordY = std::max(0, m_recordY + 1);
                      m_recordHeight = std::min(m_recordHeight - 1,
                                                m_rootWindowRect.height);

                      needRepaint = true;
                  } else if (keyEvent->key() == Qt::Key_Down) {
                      m_recordHeight = std::min(m_recordHeight - 1,
                                                m_rootWindowRect.height);

                      needRepaint = true;
                  }
              } else if (qApp->keyboardModifiers() & Qt::ControlModifier) {
                if (keyEvent->key() == Qt::Key_Left) {
                    m_recordX = std::max(0, m_recordX - 1);
                    m_recordWidth = std::min(m_recordWidth + 1,
                                                      m_rootWindowRect.width);

                    needRepaint = true;
                } else if (keyEvent->key() == Qt::Key_Right) {
                    m_recordWidth = std::min(m_recordWidth + 1,
                                             m_rootWindowRect.width);

                    needRepaint = true;
                } else if (keyEvent->key() == Qt::Key_Up) {
                    m_recordY = std::max(0, m_recordY - 1);
                    m_recordHeight = std::min(m_recordHeight + 1,
                                              m_rootWindowRect.height);

                    needRepaint = true;
                } else if (keyEvent->key() == Qt::Key_Down) {
                    m_recordHeight = std::min(m_recordHeight + 1,
                                              m_rootWindowRect.height);

                    needRepaint = true;
                }
            } else {
                if (keyEvent->key() == Qt::Key_Left) {
                    m_recordX = std::max(0, m_recordX - 1);

                    needRepaint = true;
                } else if (keyEvent->key() == Qt::Key_Right) {
                    m_recordX = std::min(m_rootWindowRect.width - m_recordWidth,
                                         m_recordX + 1);

                    needRepaint = true;
                } else if (keyEvent->key() == Qt::Key_Up) {
                    m_recordY = std::max(0, m_recordY - 1);

                    needRepaint = true;
                } else if (keyEvent->key() == Qt::Key_Down) {
                    m_recordY = std::min(m_rootWindowRect.height -
                                         m_recordHeight, m_recordY + 1);

                    needRepaint = true;
                }
            }

           m_sizeTips->updateTips(QPoint(m_recordX, m_recordY),
               QString("%1X%2").arg(m_recordWidth).arg(m_recordHeight));
            if (m_mouseStatus == ShotMouseStatus::Normal && needRepaint) {
//                hideRecordButton();
            }

            QPoint toolbarPoint;
            toolbarPoint = QPoint(m_recordX + m_recordWidth - m_toolBar->width() - 5,
                                                    std::max(m_recordY + m_recordHeight + 5, 0));

            if (m_toolBar->width() > m_recordX + m_recordWidth) {
                toolbarPoint.setX(m_recordX + 5);
            }
            if (toolbarPoint.y()>= m_backgroundRect.y() + m_backgroundRect.height()
                    - m_toolBar->height() - 28) {
                if (m_recordY > 28*2 + 10) {
                    toolbarPoint.setY(m_recordY - m_toolBar->height() - 5);
                } else {
                    toolbarPoint.setY(m_recordY + 5);
                }
            }
            m_toolBar->showAt(toolbarPoint);
        }
    } else if (event->type() == QEvent::KeyRelease) {
        QKeyEvent *keyEvent = static_cast<QKeyEvent*>(event);

        // NOTE: must be use 'isAutoRepeat' to filter KeyRelease event
        //send by Qt.
        if (!keyEvent->isAutoRepeat()) {
            if (keyEvent->key() == Qt::Key_Left || keyEvent->key()
                == Qt::Key_Right || keyEvent->key() == Qt::Key_Up ||
                keyEvent->key() == Qt::Key_Down) {
                needRepaint = true;
            }

            if (m_mouseStatus == ShotMouseStatus::Normal && needRepaint) {
//                showRecordButton();
            }
        }

    }

    if (event->type() == QEvent::MouseButtonPress) {
        QMouseEvent *mouseEvent = static_cast<QMouseEvent*>(event);
        m_dragStartX = mouseEvent->x();
        m_dragStartY = mouseEvent->y();

        if (mouseEvent->button() == Qt::RightButton) {
            m_menuController->showMenu(mouseEvent->pos());
        }

        if (!m_isFirstPressButton) {
            m_isFirstPressButton = true;
        } else {
            m_dragAction = getDirection(event);

            m_dragRecordX = m_recordX;
            m_dragRecordY = m_recordY;
            m_dragRecordWidth = m_recordWidth;
            m_dragRecordHeight = m_recordHeight;

            if (m_mouseStatus == ShotMouseStatus::Normal) {
//                hideRecordButton();
            }
        }

        m_isPressButton = true;
        m_isReleaseButton = false;
    } else if (event->type() == QEvent::MouseButtonRelease) {
        if (!m_isFirstReleaseButton) {
            m_isFirstReleaseButton = true;

            m_mouseStatus = ShotMouseStatus::Normal;
            m_zoomIndicator->hide();

            QPoint toolbarPoint;
            toolbarPoint = QPoint(m_recordX + m_recordWidth - m_toolBar->width() - 5,
                                                    std::max(m_recordY + m_recordHeight + 5, 0));

            if (m_toolBar->width() > m_recordX + m_recordWidth) {
                toolbarPoint.setX(m_recordX + 5);
            }
            if (toolbarPoint.y()>= m_backgroundRect.y() + m_backgroundRect.height()
                    - m_toolBar->height() - 28) {
                if (m_recordY > 28*2 + 10) {
                    toolbarPoint.setY(m_recordY - m_toolBar->height() - 5);
                } else {
                    toolbarPoint.setY(m_recordY + 5);
                }
            }

            m_toolBar->showAt(toolbarPoint);
            updateCursor(event);

            // Record select area name with window name if just click (no drag).
            if (!m_isFirstDrag) {
                QMouseEvent *mouseEvent = static_cast<QMouseEvent*>(event);
                for (int i = 0; i < m_windowRects.length(); i++) {
                    int wx = m_windowRects[i].x;
                    int wy = m_windowRects[i].y;
                    int ww = m_windowRects[i].width;
                    int wh = m_windowRects[i].height;
                    int ex = mouseEvent->x();
                    int ey = mouseEvent->y();
                    if (ex > wx && ex < wx + ww && ey > wy && ey < wy + wh) {
//                        m_selectAreaName = m_windowNames[i];

                        break;
                    }
                }

            } else {
                // Make sure record area not too small.
                m_recordWidth = m_recordWidth < RECORD_MIN_SIZE ?
                            RECORD_MIN_SIZE : m_recordWidth;
                m_recordHeight = m_recordHeight < RECORD_MIN_SIZE ?
                            RECORD_MIN_SIZE : m_recordHeight;

                if (m_recordX + m_recordWidth > m_rootWindowRect.width) {
                    m_recordX = m_rootWindowRect.width - m_recordWidth;
                }

                if (m_recordY + m_recordHeight > m_rootWindowRect.height) {
                    m_recordY = m_rootWindowRect.height - m_recordHeight;
                }
            }

            needRepaint = true;
        } else {
            if (m_mouseStatus == ShotMouseStatus::Normal) {
//                showRecordButton();
            }
        }

        m_isPressButton = false;
        m_isReleaseButton = true;

        needRepaint = true;
    } else if (event->type() == QEvent::MouseMove) {
        qDebug() <<QDateTime::currentDateTime() << "event filter mouse move";
        if (m_recordWidth > 0 && m_recordHeight >0) {
            m_sizeTips->updateTips(QPoint(m_recordX, m_recordY),
                QString("%1X%2").arg(m_recordWidth).arg(m_recordHeight));

            if (m_toolBar->isVisible() && m_isPressButton) {
                QPoint toolbarPoint;
                toolbarPoint = QPoint(m_recordX + m_recordWidth - m_toolBar->width() - 5,
                                                        std::max(m_recordY + m_recordHeight + 5, 0));
                if (m_toolBar->width() > m_recordX + m_recordWidth) {
                    toolbarPoint.setX(m_recordX + 5);
                }

                if (toolbarPoint.y()>= m_backgroundRect.y() + m_backgroundRect.height()
                        - m_toolBar->height() - 28 ) {
                    if (m_recordY > 28*2 + 10) {
                        toolbarPoint.setY(m_recordY - m_toolBar->height() - 5);
                    } else {
                        toolbarPoint.setY(m_recordY + 5);
                    }
                }

                m_toolBar->showAt(toolbarPoint);

            } else if (m_isFirstPressButton && !m_toolBar->isVisible()) {
                QPoint curPos = this->cursor().pos();
                QPoint tmpPoint;
                tmpPoint = QPoint(std::min(curPos.x() + 5 - m_backgroundRect.x(), curPos.x() + 5),
                                  curPos.y() + 5);

                if (curPos.x() >= m_backgroundRect.x() + m_backgroundRect.width() - m_zoomIndicator->width()) {
                    tmpPoint.setX(std::min(m_backgroundRect.width() - m_zoomIndicator->width() - 5, curPos.x() + 5));
                }

                if (curPos.y() >= m_backgroundRect.y() + m_backgroundRect.height() - m_zoomIndicator->height()) {
                    tmpPoint.setY(curPos.y()  - m_zoomIndicator->height() - 5);
                }

                m_zoomIndicator->showMagnifier(tmpPoint);

                qDebug() << "ZoomIndicator showsAt:" << tmpPoint << m_backgroundRect;
            }
        }

        if ( !m_isFirstMove) {
            m_isFirstMove = true;
            needRepaint = true;
        } else {
            if (!m_toolBar->isVisible()) {
                QPoint curPos = this->cursor().pos();
                QPoint tmpPoint;
                tmpPoint = QPoint(std::min(curPos.x() + 5 - m_backgroundRect.x(), curPos.x() + 5),
                                  curPos.y() + 5);

                if (curPos.x() >= m_backgroundRect.x() + m_backgroundRect.width() - m_zoomIndicator->width()) {
                    tmpPoint.setX(std::min(m_backgroundRect.width() - m_zoomIndicator->width() - 5, curPos.x() + 5));
                }

                if (curPos.y() >= m_backgroundRect.y() + m_backgroundRect.height() - m_zoomIndicator->height()) {
                    tmpPoint.setY(curPos.y()  - m_zoomIndicator->height() - 5);
                }

                qDebug() << "show zoomIndicator:" << tmpPoint;
                m_zoomIndicator->showMagnifier(tmpPoint);
            }
        }

        if (m_isPressButton && m_isFirstPressButton) {
            if (!m_isFirstDrag) {
                m_isFirstDrag = true;

                m_selectAreaName = tr("Select area");
            }
        }

        QMouseEvent *mouseEvent = static_cast<QMouseEvent*>(event);

        if (m_isFirstPressButton) {
            if (!m_isFirstReleaseButton) {
                if (m_isPressButton && !m_isReleaseButton) {
                    m_recordX = std::min(m_dragStartX, mouseEvent->x());
                    m_recordY = std::min(m_dragStartY, mouseEvent->y());
                    m_recordWidth = std::abs(m_dragStartX - mouseEvent->x());
                    m_recordHeight = std::abs(m_dragStartY - mouseEvent->y());

                    needRepaint = true;
                }
            } else if (m_isPressButton) {
                if (m_mouseStatus != ShotMouseStatus::Wait && m_dragRecordX >= 0
                        && m_dragRecordY >= 0) {
                    if (m_dragAction == ResizeDirection::Moving) {
                        m_recordX = std::max(std::min(m_dragRecordX +
                            mouseEvent->x() - m_dragStartX, m_rootWindowRect.width
                            - m_recordWidth), 1);
                        m_recordY = std::max(std::min(m_dragRecordY + mouseEvent->y()
                            - m_dragStartY, m_rootWindowRect.height - m_recordHeight), 1);
                    } else if (m_dragAction == ResizeDirection::TopLeft) {
                        resizeDirection(ResizeDirection::Top, mouseEvent);
                        resizeDirection(ResizeDirection::Left, mouseEvent);
                    } else if (m_dragAction == ResizeDirection::TopRight) {
                        resizeDirection(ResizeDirection::Top, mouseEvent);
                        resizeDirection(ResizeDirection::Right, mouseEvent);
                    } else if (m_dragAction == ResizeDirection::BottomLeft) {
                        resizeDirection(ResizeDirection::Bottom, mouseEvent);
                        resizeDirection(ResizeDirection::Left, mouseEvent);
                    } else if (m_dragAction == ResizeDirection::BottomRight) {
                        resizeDirection(ResizeDirection::Bottom, mouseEvent);
                        resizeDirection(ResizeDirection::Right, mouseEvent);
                    } else if (m_dragAction == ResizeDirection::Top) {
                        resizeDirection(ResizeDirection::Top, mouseEvent);
                    } else if (m_dragAction == ResizeDirection::Bottom) {
                        resizeDirection(ResizeDirection::Bottom, mouseEvent);
                    } else if (m_dragAction == ResizeDirection::Left) {
                        resizeDirection(ResizeDirection::Left, mouseEvent);
                    } else if (m_dragAction == ResizeDirection::Right) {
                        resizeDirection(ResizeDirection::Right, mouseEvent);
                    }
                    needRepaint = true;
                }
            }

            updateCursor(event);

            int mousePosition =  getDirection(event);
            bool drawPoint = mousePosition != ResizeDirection::Moving;
            if (drawPoint != m_needDrawSelectedPoint) {
                m_needDrawSelectedPoint = drawPoint;
                needRepaint = true;
            }
        } else {
            if (m_screenNum == 0) {
                for (int i = 0; i < m_windowRects.length(); i++) {
                    int wx = m_windowRects[i].x;
                    int wy = m_windowRects[i].y;
                    int ww = m_windowRects[i].width;
                    int wh = m_windowRects[i].height;
                    int ex = mouseEvent->x();
                    int ey = mouseEvent->y();
                    if (ex > wx && ex < wx + ww && ey > wy && ey < wy + wh) {
                        m_recordX = wx;
                        m_recordY = wy;
                        m_recordWidth = ww;
                        m_recordHeight = wh;

                        needRepaint = true;

                        break;
                    }
                }
            } else {
                m_recordX = 0;
                m_recordY = 0;
                m_recordWidth = m_rootWindowRect.width;
                m_recordHeight = m_rootWindowRect.height;
                needRepaint = true;
            }
        }
    }

    // Use flag instead call `repaint` directly,
    // to avoid repaint many times in one event function.
    this->grabKeyboard();
    if (needRepaint) {
        repaint();
        return false;
    } else {
        return false;
    }

//    return  true;
}

int MainWindow::getDirection(QEvent *event) {
    QMouseEvent *mouseEvent = static_cast<QMouseEvent*>(event);
    int cursorX = mouseEvent->x();
    int cursorY = mouseEvent->y();

    if (cursorX > m_recordX - SPACING
        && cursorX < m_recordX + SPACING
        && cursorY > m_recordY - SPACING
        && cursorY < m_recordY + SPACING) {
        // Top-Left corner.
        return ResizeDirection::TopLeft;
    } else if (cursorX > m_recordX + m_recordWidth - SPACING
               && cursorX < m_recordX + m_recordWidth + SPACING
               && cursorY > m_recordY + m_recordHeight - SPACING
               && cursorY < m_recordY + m_recordHeight + SPACING) {
        // Bottom-Right corner.
        return  ResizeDirection::BottomRight;
    } else if (cursorX > m_recordX + m_recordWidth - SPACING
               && cursorX < m_recordX + m_recordWidth + SPACING
               && cursorY > m_recordY - SPACING
               && cursorY < m_recordY + SPACING) {
        // Top-Right corner.
        return  ResizeDirection::TopRight;
    } else if (cursorX > m_recordX - SPACING
               && cursorX < m_recordX + SPACING
               && cursorY > m_recordY + m_recordHeight - SPACING
               && cursorY < m_recordY + m_recordHeight + SPACING) {
        // Bottom-Left corner.
        return  ResizeDirection::BottomLeft;
    } else if (cursorX > m_recordX - SPACING
               && cursorX < m_recordX + SPACING) {
        // Left.
        return ResizeDirection::Left;
    } else if (cursorX > m_recordX + m_recordWidth - SPACING
               && cursorX < m_recordX + m_recordWidth + SPACING) {
        // Right.
        return  ResizeDirection::Right;
    } else if (cursorY > m_recordY - SPACING
               && cursorY < m_recordY + SPACING) {
        // Top.
        return ResizeDirection::Top;
    } else if (cursorY > m_recordY + m_recordHeight - SPACING
               && cursorY < m_recordY + m_recordHeight + SPACING) {
        // Bottom.
        return  ResizeDirection::Bottom;
    } else {
        return ResizeDirection::Moving;
    }
}
void MainWindow::paintEvent(QPaintEvent *event)  {
    Q_UNUSED(event);
    QPainter painter(this);
    painter.setRenderHint(QPainter::Antialiasing, true);

    QRect backgroundRect = QRect(m_rootWindowRect.x, m_rootWindowRect.y,
                                                              m_rootWindowRect.width, m_rootWindowRect.height);
    // Draw background.
    qDebug() << "backgroundRect" << backgroundRect;
    if (!m_isFirstMove) {
        painter.setBrush(QBrush("#000000"));
        painter.setOpacity(0.5);
        painter.drawRect(backgroundRect);
    } else if (m_recordWidth > 0 && m_recordHeight > 0 && !m_drawNothing) {
        QRect frameRect = QRect(m_recordX + 1, m_recordY + 1, m_recordWidth - 2, m_recordHeight - 2);
        // Draw frame.
        if (m_mouseStatus != ShotMouseStatus::Wait) {
            painter.setRenderHint(QPainter::Antialiasing, false);
            painter.setBrush(QBrush("#000000"));
            painter.setOpacity(0.2);
            painter.setClipping(true);
            painter.setClipRegion(QRegion(backgroundRect).subtracted(QRegion(frameRect)));
            painter.drawRect(backgroundRect);

            painter.setClipRegion(backgroundRect);
            QPen framePen(QColor("#01bdff"));
            framePen.setWidth(2);
            painter.setOpacity(1);
            painter.setBrush(Qt::transparent);
            painter.setPen(framePen);
            painter.drawRect(QRect(frameRect.x(), frameRect.y(), frameRect.width(), frameRect.height()));
            painter.setClipping(false);
        }

        // Draw drag pint.
        if (m_mouseStatus != ShotMouseStatus::Wait && m_needDrawSelectedPoint) {
            painter.setOpacity(1);
            int margin = m_resizeBigPix.width() / 2 + 1;
            int paintX = frameRect.x() - margin;
            int paintY = frameRect.y() - margin;
            int paintWidth = frameRect.x() + frameRect.width() - margin;
            int paintHeight = frameRect.y() + frameRect.height() - margin;
            int paintHalfWidth = frameRect.x() + frameRect.width()/2 - margin;
            int paintHalfHeight = frameRect.y() + frameRect.height()/2 - margin;
            paintSelectedPoint(painter, QPoint(paintX, paintY), m_resizeBigPix);
            paintSelectedPoint(painter, QPoint(paintWidth, paintY), m_resizeBigPix);
            paintSelectedPoint(painter, QPoint(paintX, paintHeight), m_resizeBigPix);
            paintSelectedPoint(painter, QPoint(paintWidth, paintHeight), m_resizeBigPix);

            paintSelectedPoint(painter, QPoint(paintX, paintHalfHeight), m_resizeBigPix);
            paintSelectedPoint(painter, QPoint(paintHalfWidth, paintY), m_resizeBigPix);
            paintSelectedPoint(painter, QPoint(paintWidth, paintHalfHeight), m_resizeBigPix);
            paintSelectedPoint(painter, QPoint(paintHalfWidth, paintHeight), m_resizeBigPix);
        }
    }

}

void MainWindow::initShapeWidget(QString type) {
    qDebug() << "show shapesWidget";
    this->releaseKeyboard();
    m_shapesWidget = new ShapesWidget(this);
    if (type != "color")
        m_shapesWidget->setCurrentShape(type);

    m_shapesWidget->show();
    m_shapesWidget->setFixedSize(m_recordWidth - 4, m_recordHeight - 4);
    m_shapesWidget->move(m_recordX + 2, m_recordY + 2);

    QPoint toolbarPoint;
    toolbarPoint = QPoint(m_recordX + m_recordWidth - m_toolBar->width() - 5,
                          std::max(m_recordY + m_recordHeight + 5, 0));

    if (m_toolBar->width() > m_recordX + m_recordWidth) {
        toolbarPoint.setX(m_recordX + 5);
    }
    if (toolbarPoint.y()>= m_backgroundRect.y() + m_backgroundRect.height()
            - m_toolBar->height() - 28) {
        if (m_recordY > 28*2 + 10) {
            toolbarPoint.setY(m_recordY - m_toolBar->height() - 5);
        } else {
            toolbarPoint.setY(m_recordY + 5);
        }
    }

    m_toolBar->showAt(toolbarPoint);
    m_toolBar->raise();

    update();

    connect(m_toolBar, &ToolBar::updateColor,
            m_shapesWidget, &ShapesWidget::setPenColor);
    connect(m_shapesWidget, &ShapesWidget::reloadEffectImg,
            this, &MainWindow::reloadImage);
    connect(this, &MainWindow::deleteShapes, m_shapesWidget,
            &ShapesWidget::deleteCurrentShape);
    connect(m_shapesWidget, &ShapesWidget::requestScreenshot,
            this, &MainWindow::saveScreenshot);
}

void MainWindow::updateCursor(QEvent *event)
{
    if (m_mouseStatus == ShotMouseStatus::Normal) {
        QMouseEvent *mouseEvent = static_cast<QMouseEvent*>(event);
        int cursorX = mouseEvent->x();
        int cursorY = mouseEvent->y();

        if (cursorX > m_recordX - SPACING
            && cursorX < m_recordX + SPACING
            && cursorY > m_recordY - SPACING
            && cursorY < m_recordY + SPACING) {
            // Top-Left corner.
            qApp->setOverrideCursor(Qt::SizeFDiagCursor);
        } else if (cursorX > m_recordX + m_recordWidth - SPACING
                   && cursorX < m_recordX + m_recordWidth + SPACING
                   && cursorY > m_recordY + m_recordHeight - SPACING
                   && cursorY < m_recordY + m_recordHeight + SPACING) {
            // Bottom-Right corner.
            qApp->setOverrideCursor(Qt::SizeFDiagCursor);
        } else if (cursorX > m_recordX + m_recordWidth - SPACING
                   && cursorX < m_recordX + m_recordWidth + SPACING
                   && cursorY > m_recordY - SPACING
                   && cursorY < m_recordY + SPACING) {
            // Top-Right corner.
            qApp->setOverrideCursor(Qt::SizeBDiagCursor);
        } else if (cursorX > m_recordX - SPACING
                   && cursorX < m_recordX + SPACING
                   && cursorY > m_recordY + m_recordHeight - SPACING
                   && cursorY < m_recordY + m_recordHeight + SPACING) {
            // Bottom-Left corner.
            qApp->setOverrideCursor(Qt::SizeBDiagCursor);
        } else if (cursorX > m_recordX - SPACING
                   && cursorX < m_recordX + SPACING) {
            // Left.
            qApp->setOverrideCursor(Qt::SizeHorCursor);
        } else if (cursorX > m_recordX + m_recordWidth - SPACING
                   && cursorX < m_recordX + m_recordWidth + SPACING) {
            // Right.
            qApp->setOverrideCursor(Qt::SizeHorCursor);
        } else if (cursorY > m_recordY - SPACING
                   && cursorY < m_recordY + SPACING) {
            // Top.
            qApp->setOverrideCursor(Qt::SizeVerCursor);
        } else if (cursorY > m_recordY + m_recordHeight - SPACING
                   && cursorY < m_recordY + m_recordHeight + SPACING) {
            // Bottom.
            qApp->setOverrideCursor(Qt::SizeVerCursor);
        } /*else if (recordButton->geometry().contains(cursorX, cursorY) ||
             recordOptionPanel->geometry().contains(cursorX, cursorY)) {
            // Record area.
            qApp->setOverrideCursor(Qt::ArrowCursor);
        }*/ else {
            if (m_isPressButton) {
                qApp->setOverrideCursor(Qt::ClosedHandCursor);
            } else {
                qApp->setOverrideCursor(Qt::OpenHandCursor);
            }
        }
    }
}

void MainWindow::resizeDirection(ResizeDirection direction,
                                 QMouseEvent *e) {
    int offsetX = e->x() - m_dragStartX;
    int offsetY = e->y() - m_dragStartY;

    switch (direction) {
    case ResizeDirection::Top: {
        m_recordY = std::max(std::min(m_dragRecordY + offsetY,
                    m_dragRecordY + m_dragRecordHeight - RECORD_MIN_SIZE), 1);
        m_recordHeight = std::max(std::min(m_dragRecordHeight -
                      offsetY, m_rootWindowRect.height), RECORD_MIN_SIZE);
        break;
    };
    case ResizeDirection::Bottom: {
        m_recordHeight = std::max(std::min(m_dragRecordHeight + offsetY,
                                         m_rootWindowRect.height), RECORD_MIN_SIZE);
        break;
    };
    case ResizeDirection::Left: {
        m_recordX = std::max(std::min(m_dragRecordX + offsetX,
                    m_dragRecordX + m_dragRecordWidth - RECORD_MIN_SIZE), 1);
        m_recordWidth = std::max(std::min(m_dragRecordWidth - offsetX,
                    m_rootWindowRect.width), RECORD_MIN_SIZE);
        break;
    };
    case ResizeDirection::Right: {
        m_recordWidth = std::max(std::min(m_dragRecordWidth + offsetX,
                        m_rootWindowRect.width), RECORD_MIN_SIZE);
        break;
    };
    default:break;
    }

}

void MainWindow::startScreenshot() {
    m_mouseStatus = ShotMouseStatus::Shoting;
    repaint();
    qApp->setOverrideCursor(setCursorShape("start"));
}

void MainWindow::showPressFeedback(int x, int y)
{
    if (m_mouseStatus == ShotMouseStatus::Shoting) {
//        buttonFeedback->showPressFeedback(x, y);
    }
}

void MainWindow::showDragFeedback(int x, int y)
{
    if (m_mouseStatus == ShotMouseStatus::Shoting) {
//        buttonFeedback->showDragFeedback(x, y);
    }
}

void MainWindow::showReleaseFeedback(int x, int y)
{
    if (m_mouseStatus == ShotMouseStatus::Shoting) {
//        buttonFeedback->showReleaseFeedback(x, y);
    }
}

void MainWindow::responseEsc()
{
//    if (recordButtonStatus != ShotMouseStatus::Shoting) {
        qApp->quit();
//    }
}

void MainWindow::shotFullScreen() {
    QList<QScreen*> screenList = qApp->screens();
    QPixmap tmpImg =  screenList[m_screenNum]->grabWindow(
                qApp->desktop()->screen(m_screenNum)->winId(),
                m_backgroundRect.x(), m_backgroundRect.y(),
                m_backgroundRect.width(), m_backgroundRect.height());

    using namespace utils;
    tmpImg.save(TMP_FULLSCREEN_FILE, "png");
    this->setStyleSheet(QString("MainWindow{ border-image: url(%1);}"
                                       ).arg(TMP_FULLSCREEN_FILE));
}

void MainWindow::shotCurrentImg() {
    if (m_recordWidth == 0 || m_recordHeight == 0)
        return;

    m_needDrawSelectedPoint = false;
    m_drawNothing = true;
    update();

    QEventLoop eventloop;
    QTimer::singleShot(100, &eventloop, SLOT(quit()));
    eventloop.exec();

    qDebug() << m_toolBar->isVisible() << m_sizeTips->isVisible();
    QList<QScreen*> screenList = qApp->screens();
    QPixmap tmpImg =  screenList[m_screenNum]->grabWindow(
                qApp->desktop()->screen(m_screenNum)->winId(),
                m_recordX + m_backgroundRect.x(), m_recordY, m_recordWidth, m_recordHeight);
    qDebug() << tmpImg.isNull() << tmpImg.size();

    using namespace utils;
    tmpImg.save(TMP_FILE, "png");
}

void MainWindow::shotImgWidthEffect() {
    if (m_recordWidth == 0 || m_recordHeight == 0)
        return;

    m_needDrawSelectedPoint = false;
    m_drawNothing = true;
    update();

    qDebug() << m_toolBar->isVisible() << m_sizeTips->isVisible();
    QList<QScreen*> screenList = qApp->screens();
    QPixmap tmpImg =  screenList[m_screenNum]->grabWindow(
                qApp->desktop()->screen(m_screenNum)->winId(),
                m_recordX + m_backgroundRect.x(), m_recordY, m_recordWidth, m_recordHeight);
    qDebug() << tmpImg.isNull() << tmpImg.size();

    using namespace utils;
    tmpImg.save(TMP_FILE, "png");
    m_drawNothing = false;
    update();
}

void MainWindow::saveScreenshot() {
    m_hotZoneInterface->asyncCall("EnableZoneDetected",  true);
    QDateTime currentDate;
    using namespace utils;
    m_toolBar->setVisible(false);
    m_sizeTips->setVisible(false);

    shotCurrentImg();

    QPixmap screenShotPix(TMP_FILE);
    QString currentTime =  currentDate.currentDateTime().
            toString("yyyyMMddHHmmss");
    QString fileName = "";
    QStandardPaths::StandardLocation saveOption = QStandardPaths::TempLocation;
    bool copyToClipboard = false;
    int saveIndex =  ConfigSettings::instance()->value(
                                   "save", "save_op").toInt();
    switch (saveIndex) {
    case 0: {
        saveOption = QStandardPaths::DesktopLocation;
        break;
    }
    case 1: {
        saveOption = QStandardPaths::PicturesLocation;
        break;
    }
    case 2: {
        this->hide();
        QFileDialog fileDialog;
        QString  lastFileName = QString("%1DeepinScreenshot%2.png").arg(QStandardPaths::writableLocation(
                                                                            QStandardPaths::PicturesLocation)).arg(currentTime);
        fileName =  fileDialog.getSaveFileName(NULL, "Save",  lastFileName,  tr("")) + ".png";

        break;
    }
    case 3: {
        copyToClipboard = true;
        break;
    }
    case 4: {
        copyToClipboard = true;
        break;
    }
    default:
        break;
    }

    if (saveIndex == 2) {
        screenShotPix.save(fileName, "PNG");
        if (m_soundEffectInterface->enabled()) {
            m_soundEffectInterface->asyncCall("PlaySystemSound", "camera-shutter");
        }
    } else if (saveOption != QStandardPaths::TempLocation || fileName.isEmpty()) {
        fileName = QString("%1/DeepinScreenshot%2.png").arg(
                    QStandardPaths::writableLocation(saveOption)).arg(currentTime);
        screenShotPix.save(fileName, "PNG");
        if (m_soundEffectInterface->enabled()) {
            m_soundEffectInterface->asyncCall("PlaySystemSound", "camera-shutter");
        }
    }

    if (copyToClipboard) {
        Q_ASSERT(!screenShotPix.isNull());
        QClipboard* cb = qApp->clipboard();
        cb->setPixmap(screenShotPix, QClipboard::Clipboard);
    }


    QStringList actions;
    actions << "_open" << tr("View");
    QVariantMap hints;
    QString fileDir = QUrl::fromLocalFile(QFileInfo(fileName).absoluteDir().absolutePath()).toString();
    QString filePath =  QUrl::fromLocalFile(fileName).toString();
    QString command;
    if (QFile("/usr/bin/dde-file-manager").exists()) {
        command = QString("/usr/bin/dde-file-manager,%1?selectUrl=%2"
                          ).arg(fileDir).arg(filePath);
    } else {
        command = QString("xdg-open,%1").arg(filePath);
    }

    hints["x-deepin-action-_open"] = command;

   QString summary = QString("Picture has been saved to %1").arg(fileName);
   m_notifyDBInterface->Notify("Deepin Screenshot", 0,  "deepin-screenshot", "",
                               summary, actions, hints, 0);
    qApp->quit();
}

void MainWindow::reloadImage(QString effect) {
    //**save tmp image file
    shotImgWidthEffect();
    using namespace utils;
    const int radius = 10;
    QPixmap tmpImg(TMP_FILE);
    int imgWidth = tmpImg.width();
    int imgHeight = tmpImg.height();
    if (effect == "blur") {
        if (!tmpImg.isNull()) {
            tmpImg = tmpImg.scaled(imgWidth/radius, imgHeight/radius,
                                     Qt::IgnoreAspectRatio, Qt::SmoothTransformation);
            tmpImg = tmpImg.scaled(imgWidth, imgHeight, Qt::IgnoreAspectRatio,
                                     Qt::SmoothTransformation);
            tmpImg.save(TMP_BLUR_FILE, "png");
        }
    } else {
        if (!tmpImg.isNull()) {
            tmpImg = tmpImg.scaled(imgWidth/radius, imgHeight/radius,
                                   Qt::IgnoreAspectRatio, Qt::SmoothTransformation);
            tmpImg = tmpImg.scaled(imgWidth, imgHeight);
            tmpImg.save(TMP_MOSA_FILE, "png");
        }
    }
}
