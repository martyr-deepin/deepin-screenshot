#include <gdk/gdk.h>
#include <gtk/gtk.h>
#include <gtk/gtkclipboard.h>
#include "mainwindow.h"

#include <QApplication>
#include <QPainter>
#include <QFileDialog>

namespace {
const int RECORD_MIN_SIZE = 220;
const int DRAG_POINT_RADIUS = 8;
const int CURSOR_BOUND = 5;
const QString TMPFILE_URL = "/tmp/deepin-screenshot.png";
}

MainWindow::MainWindow(QWidget *parent)
    : QWidget(parent)
{
    initUI();
    startScreenshot();
}

MainWindow::~MainWindow()
{
}

void MainWindow::initUI() {
    setWindowFlags(Qt::Tool | Qt::FramelessWindowHint /*|
                   Qt::WindowStaysOnTopHint | Qt::WindowDoesNotAcceptFocus*/);
    setAttribute(Qt::WA_TranslucentBackground, true);
    setMouseTracking(true);   // make MouseMove can response
    m_configSettings =  ConfigSettings::instance();

    m_windowManager = new WindowManager();
    QList<xcb_window_t> windows = m_windowManager->getWindows();
    m_rootWindowRect =  m_windowManager->getRootWindowRect();

    for (int i = 0; i < windows.length(); i++) {
        m_windowRects.append(m_windowManager->adjustRectInScreenArea(
                                 m_windowManager->getWindowRect(windows[i])));
        m_windowNames.append(m_windowManager->getWindowClass(windows[i]));
    }

    //**save tmp image file
    QPixmap tmpImg = qApp->primaryScreen()->grabWindow(windows[windows.length()-1]);
    tmpImg.save(TMPFILE_URL, "png");

    m_sizeTips = new TopTips(this);
    m_sizeTips->hide();
    m_toolBar = new ToolBar(this);
    m_toolBar->hide();
    m_zoomIndicator = new ZoomIndicator(this);
    m_zoomIndicator->hide();
    installEventFilter(this);

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

    m_drawDragPoint = false;
    m_mouseStatus = ShotMouseStatus::Shoting;

    m_selectAreaName = "";

    m_isShapesWidgetExist = false;
    connect(m_toolBar, &ToolBar::buttonChecked, this,  [=](QString shape){
        if (m_isShapesWidgetExist) {
            m_shapesWidget->setCurrentShape(shape);
        } else {
            initShapeWidget(shape);
            m_isShapesWidgetExist = true;
        }
    });
    connect(&m_eventMonitor, SIGNAL(buttonedPress(int, int)), this,
            SLOT(showPressFeedback(int, int)), Qt::QueuedConnection);
    connect(&m_eventMonitor, SIGNAL(buttonedDrag(int, int)), this,
            SLOT(showDragFeedback(int, int)), Qt::QueuedConnection);
    connect(&m_eventMonitor, SIGNAL(buttonedRelease(int, int)), this,
            SLOT(showReleaseFeedback(int, int)), Qt::QueuedConnection);
    connect(&m_eventMonitor, SIGNAL(pressEsc()), this,
            SLOT(responseEsc()), Qt::QueuedConnection);
    m_eventMonitor.start();

    connect(m_toolBar, &ToolBar::updateSaveOption, this, &MainWindow::setSaveOption);
}

bool MainWindow::eventFilter(QObject *, QEvent *event)
{
    if (m_isShapesWidgetExist) {
        return false;
    }
#undef KeyPress
#undef KeyRelease
    if (event->type() == QEvent::MouseButtonDblClick) {
        saveScreenshot();
    }
    bool needRepaint = false;
    if (event->type() ==  QEvent::KeyPress) {
        QKeyEvent* keyEvent = static_cast<QKeyEvent*> (event);
        if (keyEvent->key() == Qt::Key_Escape) {
            qApp->quit();
        }
    }

    if (event->type() == QEvent::KeyPress) {
        QKeyEvent *keyEvent = static_cast<QKeyEvent*>(event);

        if (m_mouseStatus == ShotMouseStatus::Normal) {
            if (/*qApp->keyboardModifiers() & */Qt::ControlModifier) {
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

            if (m_mouseStatus == ShotMouseStatus::Normal && needRepaint) {
//                hideRecordButton();
            }
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
            m_toolBar->showAt(QPoint(m_recordX + m_recordWidth, m_recordY
                                          + m_recordHeight));
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
                        m_selectAreaName = m_windowNames[i];

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
        if (m_recordWidth > 0 && m_recordHeight >0) {
            m_sizeTips->updateTips(QPoint(m_recordX, m_recordY),
                QString("%1X%2").arg(m_recordWidth).arg(m_recordHeight));

            if (m_toolBar->isVisible()) {
                m_toolBar->showAt(QPoint(m_recordX + m_recordWidth,
                                              m_recordY + m_recordHeight));
            } else if (m_isFirstPressButton){
                m_zoomIndicator->showMagnifier(QPoint(m_recordX + m_recordWidth,
                                                     m_recordY + m_recordHeight));
            }
        }

        if (!m_isFirstMove) {
            m_isFirstMove = true;
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
            if (drawPoint != m_drawDragPoint) {
                m_drawDragPoint = drawPoint;
                needRepaint = true;
            }
        } else {
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
        }
    }

    // Use flag instead call `repaint` directly,
    // to avoid repaint many times in one event function.
    if (needRepaint) {
        repaint();
    }

    return false;
}

int MainWindow::getDirection(QEvent *event) {
    QMouseEvent *mouseEvent = static_cast<QMouseEvent*>(event);
    int cursorX = mouseEvent->x();
    int cursorY = mouseEvent->y();

    if (cursorX > m_recordX - CURSOR_BOUND
        && cursorX < m_recordX + CURSOR_BOUND
        && cursorY > m_recordY - CURSOR_BOUND
        && cursorY < m_recordY + CURSOR_BOUND) {
        // Top-Left corner.
        return ResizeDirection::TopLeft;
    } else if (cursorX > m_recordX + m_recordWidth - CURSOR_BOUND
               && cursorX < m_recordX + m_recordWidth + CURSOR_BOUND
               && cursorY > m_recordY + m_recordHeight - CURSOR_BOUND
               && cursorY < m_recordY + m_recordHeight + CURSOR_BOUND) {
        // Bottom-Right corner.
        return  ResizeDirection::BottomRight;
    } else if (cursorX > m_recordX + m_recordWidth - CURSOR_BOUND
               && cursorX < m_recordX + m_recordWidth + CURSOR_BOUND
               && cursorY > m_recordY - CURSOR_BOUND
               && cursorY < m_recordY + CURSOR_BOUND) {
        // Top-Right corner.
        return  ResizeDirection::TopRight;
    } else if (cursorX > m_recordX - CURSOR_BOUND
               && cursorX < m_recordX + CURSOR_BOUND
               && cursorY > m_recordY + m_recordHeight - CURSOR_BOUND
               && cursorY < m_recordY + m_recordHeight + CURSOR_BOUND) {
        // Bottom-Left corner.
        return  ResizeDirection::BottomLeft;
    } else if (cursorX > m_recordX - CURSOR_BOUND
               && cursorX < m_recordX + CURSOR_BOUND) {
        // Left.
        return ResizeDirection::Left;
    } else if (cursorX > m_recordX + m_recordWidth - CURSOR_BOUND
               && cursorX < m_recordX + m_recordWidth + CURSOR_BOUND) {
        // Right.
        return  ResizeDirection::Right;
    } else if (cursorY > m_recordY - CURSOR_BOUND
               && cursorY < m_recordY + CURSOR_BOUND) {
        // Top.
        return ResizeDirection::Top;
    } else if (cursorY > m_recordY + m_recordHeight - CURSOR_BOUND
               && cursorY < m_recordY + m_recordHeight + CURSOR_BOUND) {
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

    if (m_recordWidth > 0 && m_recordHeight > 0) {
        QRect backgroundRect = QRect(m_rootWindowRect.x, m_rootWindowRect.y,
                                     m_rootWindowRect.width, m_rootWindowRect.height);
        QRect frameRect = QRect(m_recordX, m_recordY, m_recordWidth, m_recordHeight);
        qDebug() << frameRect << backgroundRect;
        // Draw background.
        painter.setBrush(QBrush("#000000"));
        painter.setOpacity(0.2);

        painter.setClipping(true);
        painter.setClipRegion(QRegion(backgroundRect).subtracted(QRegion(frameRect)));
        painter.drawRect(backgroundRect);

        // Reset clip.
        painter.setClipRegion(QRegion(backgroundRect));

        // Draw frame.
        if (m_mouseStatus != ShotMouseStatus::Wait) {
            painter.setRenderHint(QPainter::Antialiasing, false);
            QPen framePen(QColor("#01bdff"));
            framePen.setWidth(2);
            painter.setOpacity(1);
            painter.setBrush(QBrush());  // clear brush
            painter.setPen(framePen);
            painter.drawRect(QRect(std::max(frameRect.x(), 1),std::max(frameRect.y(), 1),
                                 std::min(frameRect.width() - 1, m_rootWindowRect.width - 2),
                                 std::min(frameRect.height() - 1, m_rootWindowRect.height - 2)));
            painter.setRenderHint(QPainter::Antialiasing, true);
        }

        // Draw drag pint.
        if (m_mouseStatus != ShotMouseStatus::Wait && m_drawDragPoint) {
            painter.drawPixmap(QPoint(m_recordX - DRAG_POINT_RADIUS,
                               m_recordY - DRAG_POINT_RADIUS), m_resizeBigPix);
            painter.drawPixmap(QPoint(m_recordX - DRAG_POINT_RADIUS + m_recordWidth,
                               m_recordY - DRAG_POINT_RADIUS), m_resizeBigPix);
            painter.drawPixmap(QPoint(m_recordX - DRAG_POINT_RADIUS, m_recordY
                               - DRAG_POINT_RADIUS + m_recordHeight), m_resizeBigPix);
            painter.drawPixmap(QPoint(m_recordX - DRAG_POINT_RADIUS + m_recordWidth,
                               m_recordY - DRAG_POINT_RADIUS + m_recordHeight), m_resizeBigPix);
            painter.drawPixmap(QPoint(m_recordX - DRAG_POINT_RADIUS,
                               m_recordY - DRAG_POINT_RADIUS + m_recordHeight / 2), m_resizeBigPix);
            painter.drawPixmap(QPoint(m_recordX - DRAG_POINT_RADIUS +
                               m_recordWidth, m_recordY - DRAG_POINT_RADIUS + m_recordHeight / 2), m_resizeBigPix);
            painter.drawPixmap(QPoint(m_recordX - DRAG_POINT_RADIUS + m_recordWidth / 2,
                               m_recordY - DRAG_POINT_RADIUS), m_resizeBigPix);
            painter.drawPixmap(QPoint(m_recordX - DRAG_POINT_RADIUS + m_recordWidth / 2,
                               m_recordY - DRAG_POINT_RADIUS + m_recordHeight), m_resizeBigPix);

            painter.drawPixmap(QPoint(m_recordX - DRAG_POINT_RADIUS,
                               m_recordY - DRAG_POINT_RADIUS), m_resizeSmallPix);
            painter.drawPixmap(QPoint(m_recordX - DRAG_POINT_RADIUS +
                               m_recordWidth, m_recordY - DRAG_POINT_RADIUS),  m_resizeSmallPix);
            painter.drawPixmap(QPoint(m_recordX - DRAG_POINT_RADIUS,
                               m_recordY - DRAG_POINT_RADIUS + m_recordHeight), m_resizeSmallPix);
            painter.drawPixmap(QPoint(m_recordX - DRAG_POINT_RADIUS +
                               m_recordWidth, m_recordY - DRAG_POINT_RADIUS + m_recordHeight), m_resizeSmallPix);
            painter.drawPixmap(QPoint(m_recordX - DRAG_POINT_RADIUS, m_recordY -
                               DRAG_POINT_RADIUS + m_recordHeight / 2), m_resizeSmallPix);
            painter.drawPixmap(QPoint(m_recordX - DRAG_POINT_RADIUS + m_recordWidth,
                               m_recordY - DRAG_POINT_RADIUS + m_recordHeight / 2), m_resizeSmallPix);
            painter.drawPixmap(QPoint(m_recordX - DRAG_POINT_RADIUS + m_recordWidth / 2,
                               m_recordY - DRAG_POINT_RADIUS), m_resizeSmallPix);
            painter.drawPixmap(QPoint(m_recordX - DRAG_POINT_RADIUS + m_recordWidth / 2,
                               m_recordY - DRAG_POINT_RADIUS + m_recordHeight), m_resizeSmallPix);
        }
    }
}

void MainWindow::initShapeWidget(QString type) {
    qDebug() << "show shapesWidget";
    m_shapesWidget = new ShapesWidget(this);
    m_shapesWidget->setCurrentShape(type);
    m_shapesWidget->setFixedSize(m_recordWidth, m_recordHeight);
    m_shapesWidget->move(m_recordX, m_recordY);
    m_shapesWidget->show();
    update();

    connect(m_toolBar,  &ToolBar::updateColor, m_shapesWidget, &ShapesWidget::setPenColor);
}

void MainWindow::updateCursor(QEvent *event)
{
    if (m_mouseStatus == ShotMouseStatus::Normal) {
        QMouseEvent *mouseEvent = static_cast<QMouseEvent*>(event);
        int cursorX = mouseEvent->x();
        int cursorY = mouseEvent->y();

        if (cursorX > m_recordX - CURSOR_BOUND
            && cursorX < m_recordX + CURSOR_BOUND
            && cursorY > m_recordY - CURSOR_BOUND
            && cursorY < m_recordY + CURSOR_BOUND) {
            // Top-Left corner.
            qApp->setOverrideCursor(Qt::SizeFDiagCursor);
        } else if (cursorX > m_recordX + m_recordWidth - CURSOR_BOUND
                   && cursorX < m_recordX + m_recordWidth + CURSOR_BOUND
                   && cursorY > m_recordY + m_recordHeight - CURSOR_BOUND
                   && cursorY < m_recordY + m_recordHeight + CURSOR_BOUND) {
            // Bottom-Right corner.
            qApp->setOverrideCursor(Qt::SizeFDiagCursor);
        } else if (cursorX > m_recordX + m_recordWidth - CURSOR_BOUND
                   && cursorX < m_recordX + m_recordWidth + CURSOR_BOUND
                   && cursorY > m_recordY - CURSOR_BOUND
                   && cursorY < m_recordY + CURSOR_BOUND) {
            // Top-Right corner.
            qApp->setOverrideCursor(Qt::SizeBDiagCursor);
        } else if (cursorX > m_recordX - CURSOR_BOUND
                   && cursorX < m_recordX + CURSOR_BOUND
                   && cursorY > m_recordY + m_recordHeight - CURSOR_BOUND
                   && cursorY < m_recordY + m_recordHeight + CURSOR_BOUND) {
            // Bottom-Left corner.
            qApp->setOverrideCursor(Qt::SizeBDiagCursor);
        } else if (cursorX > m_recordX - CURSOR_BOUND
                   && cursorX < m_recordX + CURSOR_BOUND) {
            // Left.
            qApp->setOverrideCursor(Qt::SizeHorCursor);
        } else if (cursorX > m_recordX + m_recordWidth - CURSOR_BOUND
                   && cursorX < m_recordX + m_recordWidth + CURSOR_BOUND) {
            // Right.
            qApp->setOverrideCursor(Qt::SizeHorCursor);
        } else if (cursorY > m_recordY - CURSOR_BOUND
                   && cursorY < m_recordY + CURSOR_BOUND) {
            // Top.
            qApp->setOverrideCursor(Qt::SizeVerCursor);
        } else if (cursorY > m_recordY + m_recordHeight - CURSOR_BOUND
                   && cursorY < m_recordY + m_recordHeight + CURSOR_BOUND) {
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

void MainWindow::setSaveOption(int saveOption) {
    m_saveIndex = saveOption;
    saveScreenshot();
}

void MainWindow::saveScreenshot() {
    QDateTime currentDate;
    QPixmap screenShotPix(TMPFILE_URL);
    screenShotPix = screenShotPix.copy(QRect(m_recordX + 2, m_recordY + 2,
        m_recordWidth - 4 , m_recordHeight - 4));
    QString currentTime =  currentDate.currentDateTime().toString("yyyyMMddHHmmss");
    QString fileName = "";
    QStandardPaths::StandardLocation saveOption = QStandardPaths::TempLocation;
    bool copyToClipboard = false;

    switch (m_saveIndex) {
    case 0: {
        saveOption = QStandardPaths::DesktopLocation;
        break;
    }
    case 1: {
        saveOption = QStandardPaths::PicturesLocation;
        break;
    }
    case 2: {
        QFileDialog fileDialog;
        fileName =  fileDialog.getSaveFileName(NULL, "Save");
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
    if (saveOption != QStandardPaths::TempLocation || fileName.isEmpty()) {
        fileName = QString("%1/DeepinScreenshot%2.png").arg(
                    QStandardPaths::writableLocation(saveOption)).arg(currentTime);
                     screenShotPix.save(fileName, "PNG");
    }
    if (copyToClipboard) {
        GError *err = NULL;
        screenShotPix.save("/tmp/deepin-screenshot.png", "PNG");
        GdkPixbuf*   pixbuf =  gdk_pixbuf_new_from_file(QString(
            "/tmp/deepin-screenshot.png").toLatin1().data(), &err);
        GtkClipboard* clipboard = gtk_clipboard_get(GDK_SELECTION_CLIPBOARD);
        gtk_clipboard_set_image(clipboard, pixbuf);
        gtk_clipboard_store(clipboard);
    }
    qApp->quit();
}
