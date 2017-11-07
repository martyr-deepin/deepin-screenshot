/*
 * Copyright (C) 2017 ~ 2017 Deepin Technology Co., Ltd.
 *
 * Maintainer: Peng Hui<penghui@deepin.com>
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

#include "mainwindow.h"

#include <QDesktopWidget>
#include <QPainter>
#include <QFileDialog>
#include <QClipboard>
#include <QAction>
#include <QMap>
#include <QStyleFactory>
#include <QShortcut>
#include <QKeySequence>
#include <QApplication>
#include <QCommandLineParser>
#include <QCommandLineOption>

#include <DApplication>

//The deepin-tool-kit didn't update...
//#include <DDesktopServices>

//DCORE_USE_NAMESPACE

#include "utils/screenutils.h"
#include "utils/tempfile.h"

DWIDGET_USE_NAMESPACE

namespace {
const int RECORD_MIN_SIZE = 10;
const int SPACING = 5;
const int TOOLBAR_Y_SPACING = 8;
const int CURSOR_WIDTH = 8;
const int CURSOR_HEIGHT = 18;
const int INDICATOR_WIDTH =  59;
const qreal RESIZEPOINT_WIDTH = 15;
}

MainWindow::MainWindow(QWidget *parent)
    : QLabel(parent)
{
//     startScreenshot();
}

MainWindow::~MainWindow()
{
}

void MainWindow::initOriginUI()
{
    this->setFocus();
    setMouseTracking(true);

    QPoint curPos = this->cursor().pos();

    m_swUtil = DScreenWindowsUtil::instance(curPos);
    m_screenNum =  m_swUtil->getScreenNum();
    m_backgroundRect = m_swUtil->backgroundRect();
    this->move(m_backgroundRect.x(), m_backgroundRect.y());
    this->setFixedSize(m_backgroundRect.size());
    initBackground();

    m_sizeTips = new TopTips(this);
    m_sizeTips->hide();
    m_zoomIndicator = new ZoomIndicator(this);
    m_zoomIndicator->hide();
    m_updateZoomTimer = new QTimer(this);

    connect(m_updateZoomTimer, &QTimer::timeout,
            m_zoomIndicator, &ZoomIndicator::updatePaintEvent);


    m_isFirstDrag = false;
    m_isFirstMove = false;
    m_isFirstPressButton = false;
    m_isFirstReleaseButton = false;

    m_recordX = 0;
    m_recordY = 0;
    m_recordWidth = 0;
    m_recordHeight = 0;

    qreal ration =  this->devicePixelRatioF();
    QIcon icon(":/image/icons/resize_handle_big.svg");
    m_resizeBigPix = icon.pixmap(QSize(RESIZEPOINT_WIDTH,RESIZEPOINT_WIDTH));
    m_resizeBigPix.setDevicePixelRatio(ration);

    m_dragRecordX = -1;
    m_dragRecordY = -1;

    m_needDrawSelectedPoint = false;
    m_mouseStatus = ShotMouseStatus::Shoting;

    m_selectAreaName = "";

    m_isShapesWidgetExist = false;

}

void MainWindow::initSecondUI()
{
    if (m_screenNum == 0) {
        m_windowRects = m_swUtil->windowsRect();
        m_windowNames = m_swUtil->windowsName();
    }
    m_configSettings =  ConfigSettings::instance();
    m_toolBar = new ToolBar(this);
    m_toolBar->hide();
    m_menuController = new MenuController(this);

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
    connect(m_menuController, &MenuController::shapePressed, m_toolBar,
            &ToolBar::shapePressed);
    connect(m_menuController, &MenuController::saveBtnPressed, m_toolBar,
            &ToolBar::saveBtnPressed);
    connect(m_toolBar, &ToolBar::heightChanged, this, &MainWindow::updateToolBarPos);
    connect(m_menuController, &MenuController::menuNoFocus, this, &MainWindow::activateWindow);
    connect(m_toolBar, &ToolBar::closed, this, &MainWindow::exitApp);
}

void MainWindow::initDBusInterface()
{
    m_controlCenterDBInterface = new DBusControlCenter(this);
    m_notifyDBInterface = new DBusNotify(this);
    m_notifyDBInterface->CloseNotification(0);
    m_hotZoneInterface = new DBusZone(this);
    if (m_hotZoneInterface->isValid())
        m_hotZoneInterface->asyncCall("EnableZoneDetected", false);
    m_interfaceExist = true;
}

void MainWindow::initShortcut()
{
    QShortcut* rectSC = new QShortcut(QKeySequence("Alt+1"), this);
    QShortcut* ovalSC = new QShortcut(QKeySequence("Alt+2"), this);
    QShortcut* arrowSC = new QShortcut(QKeySequence("Alt+3"), this);
    QShortcut* lineSC = new QShortcut(QKeySequence("Alt+4"), this);
    QShortcut* textSC = new QShortcut(QKeySequence("Alt+5"), this);
    QShortcut* colorSC = new QShortcut(QKeySequence("Alt+6"), this);

    connect(rectSC, &QShortcut::activated, this, [=]{
        emit m_toolBar->shapePressed("rectangle");
    });
    connect(ovalSC, &QShortcut::activated, this, [=]{
        emit m_toolBar->shapePressed("oval");
    });
    connect(arrowSC, &QShortcut::activated, this, [=]{
        emit m_toolBar->shapePressed("arrow");
    });
    connect(lineSC, &QShortcut::activated, this, [=]{
        emit m_toolBar->shapePressed("line");
    });
    connect(textSC, &QShortcut::activated, this, [=]{
        emit m_toolBar->shapePressed("text");
    });
    connect(colorSC, &QShortcut::activated, this, [=]{
        emit m_toolBar->shapePressed("color");
    });

    if (isCommandExist("dman")) {
        QShortcut* helpSC = new QShortcut(QKeySequence("F1"), this);
        helpSC->setAutoRepeat(false);
        connect(helpSC,  SIGNAL(activated()), this, SLOT(onHelp()));
    }
}

void MainWindow::keyPressEvent(QKeyEvent *keyEvent)
{
    if (keyEvent->key() == Qt::Key_Escape ) {
        if (m_isShapesWidgetExist) {
            if (m_shapesWidget->textEditIsReadOnly()) {
                return;
            }
        }
        qDebug() << "Key_Escape pressed: app quit!";
        exitApp();
    } else if (keyEvent->modifiers() == (Qt::ShiftModifier | Qt::ControlModifier)) {
        if (keyEvent->key() == Qt::Key_Question) {
            onViewShortcut();
        }
    } else if (qApp->keyboardModifiers() & Qt::ControlModifier) {
        if (keyEvent->key() == Qt::Key_Z) {
            qDebug() << "SDGF: ctrl+z !!!";
            emit unDo();
        }
    }

    bool needRepaint = false;
    if (m_isShapesWidgetExist) {
        if (keyEvent->key() == Qt::Key_Escape) {
            exitApp();
            return  ;
        }

        if (keyEvent->key() == Qt::Key_Shift) {
            m_isShiftPressed =  true;
            m_shapesWidget->setShiftKeyPressed(m_isShiftPressed);
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
            if (keyEvent->key() == Qt::Key_Left) {
                m_shapesWidget->microAdjust("Ctrl+Left");
            } else if (keyEvent->key() == Qt::Key_Right) {
                m_shapesWidget->microAdjust("Ctrl+Right");
            } else if (keyEvent->key() == Qt::Key_Up) {
                m_shapesWidget->microAdjust("Ctrl+Up");
            } else if (keyEvent->key() == Qt::Key_Down) {
                m_shapesWidget->microAdjust("Ctrl+Down");
            } else if (keyEvent->key() == Qt::Key_C) {
                ConfigSettings::instance()->setValue("save", "save_op", 3);
                saveScreenshot();
            } else if (keyEvent->key() == Qt::Key_S) {
                expressSaveScreenshot();
            }
        }  else {
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

        if (keyEvent->key() == Qt::Key_Delete || keyEvent->key() == Qt::Key_Backspace) {
            emit  deleteShapes();
        } else {
            qDebug() << "ShapeWidget Exist keyEvent:" << keyEvent->key();
        }
        return  ;
    }

    if (m_mouseStatus == ShotMouseStatus::Normal) {
        if (keyEvent->modifiers() == (Qt::ShiftModifier | Qt::ControlModifier)) {

            if (keyEvent->key() == Qt::Key_Left) {
                m_recordX = std::max(0, m_recordX + 1);
                m_recordWidth = std::max(std::min(m_recordWidth - 1,
                                                  m_backgroundRect.width()), RECORD_MIN_SIZE);

                needRepaint = true;
            } else if (keyEvent->key() == Qt::Key_Right) {
                m_recordWidth = std::max(std::min(m_recordWidth - 1,
                                                  m_backgroundRect.width()), RECORD_MIN_SIZE);

                needRepaint = true;
            } else if (keyEvent->key() == Qt::Key_Up) {
                m_recordY = std::max(0, m_recordY + 1);
                m_recordHeight = std::max(std::min(m_recordHeight - 1,
                                                   m_backgroundRect.height()), RECORD_MIN_SIZE);

                needRepaint = true;
            } else if (keyEvent->key() == Qt::Key_Down) {
                m_recordHeight = std::max(std::min(m_recordHeight - 1,
                                                   m_backgroundRect.height()), RECORD_MIN_SIZE);

                needRepaint = true;
            }
        } else if (qApp->keyboardModifiers() & Qt::ControlModifier) {
            if (keyEvent->key() == Qt::Key_S) {
                expressSaveScreenshot();
            }

            if (keyEvent->key() == Qt::Key_C) {
                ConfigSettings::instance()->setValue("save", "save_op", 3);
                saveScreenshot();
            }

            if (keyEvent->key() == Qt::Key_Left) {
                m_recordX = std::max(0, m_recordX - 1);
                m_recordWidth = std::max(std::min(m_recordWidth + 1,
                                                  m_backgroundRect.width()), RECORD_MIN_SIZE);

                needRepaint = true;
            } else if (keyEvent->key() == Qt::Key_Right) {
                m_recordWidth = std::max(std::min(m_recordWidth + 1,
                                                  m_backgroundRect.width()), RECORD_MIN_SIZE);

                needRepaint = true;
            } else if (keyEvent->key() == Qt::Key_Up) {
                m_recordY = std::max(0, m_recordY - 1);
                m_recordHeight = std::max(std::min(m_recordHeight + 1,
                                                   m_backgroundRect.height()), RECORD_MIN_SIZE);

                needRepaint = true;
            } else if (keyEvent->key() == Qt::Key_Down) {
                m_recordHeight = std::max(std::min(m_recordHeight + 1,
                                                   m_backgroundRect.height()), RECORD_MIN_SIZE);

                needRepaint = true;
            }
        } else {
            if (keyEvent->key() == Qt::Key_Left) {
                m_recordX = std::max(0, m_recordX - 1);

                needRepaint = true;
            } else if (keyEvent->key() == Qt::Key_Right) {
                m_recordX = std::min(m_backgroundRect.width() - m_recordWidth,
                                     m_recordX + 1);

                needRepaint = true;
            } else if (keyEvent->key() == Qt::Key_Up) {
                m_recordY = std::max(0, m_recordY - 1);

                needRepaint = true;
            } else if (keyEvent->key() == Qt::Key_Down) {
                m_recordY = std::min(m_backgroundRect.height() -
                                     m_recordHeight, m_recordY + 1);

                needRepaint = true;
            }
        }

        if ( !m_needSaveScreenshot) {
            m_sizeTips->updateTips(QPoint(m_recordX, m_recordY),
                                   QString("%1X%2").arg(m_recordWidth).arg(m_recordHeight));
            updateToolBarPos();
        }
    }

    if (needRepaint) {
        update();
    }

    QLabel::keyPressEvent(keyEvent);
}

void MainWindow::keyReleaseEvent(QKeyEvent *keyEvent)
{
    // NOTE: must be use 'isAutoRepeat' to filter KeyRelease event
    //send by Qt.
    bool needRepaint = false;
    //    if(keyEvent->modifiers() == Qt::NoModifier) {
    //        QProcess::startDetached("deepin-shortcut-viewer");
    //    }

    if (m_isShapesWidgetExist) {
        if (keyEvent->key() == Qt::Key_Shift) {
            m_isShiftPressed =  false;
            m_shapesWidget->setShiftKeyPressed(m_isShiftPressed);
        }
    }

    if (!keyEvent->isAutoRepeat()) {
        if (keyEvent->key() == Qt::Key_Left || keyEvent->key()
                == Qt::Key_Right || keyEvent->key() == Qt::Key_Up ||
                keyEvent->key() == Qt::Key_Down) {
            needRepaint = true;
        }
    }
    if (needRepaint) {
        update();
    }
    QLabel::keyReleaseEvent(keyEvent);
}

void MainWindow::mousePressEvent(QMouseEvent *ev)
{
    if (!m_isShapesWidgetExist) {
        m_dragStartX = ev->x();
        m_dragStartY = ev->y();

        if (ev->button() == Qt::RightButton) {
            m_moving = false;
            if (!m_isFirstPressButton) {
                exitApp();
            }

            m_menuController->showMenu(QPoint(mapToGlobal(ev->pos())));
        }

        if (!m_isFirstPressButton) {
            m_isFirstPressButton = true;
        } else if (ev->button() == Qt::LeftButton) {
            m_moving = true;
            m_dragAction = getDirection(ev);

            m_dragRecordX = m_recordX;
            m_dragRecordY = m_recordY;
            m_dragRecordWidth = m_recordWidth;
            m_dragRecordHeight = m_recordHeight;
        }

        m_isPressButton = true;
        m_isReleaseButton = false;
    }
    QLabel::mousePressEvent(ev);
}

void MainWindow::mouseDoubleClickEvent(QMouseEvent *ev)
{
    expressSaveScreenshot();
    QLabel::mouseDoubleClickEvent(ev);
}

void MainWindow::mouseReleaseEvent(QMouseEvent *ev)
{
    bool needRepaint = false;

    if (!m_isShapesWidgetExist) {
        m_moving = false;

        if (m_sizeTips->isVisible()) {
            m_sizeTips->updateTips(QPoint(m_recordX, m_recordY),
                                   QString("%1X%2").arg(m_recordWidth).arg(m_recordHeight));
        }

        if (m_toolBar->isVisible()) {
            updateToolBarPos();
        }

        if (!m_isFirstReleaseButton) {
            m_isFirstReleaseButton = true;

            m_mouseStatus = ShotMouseStatus::Normal;
            m_zoomIndicator->hide();

            qDebug() << "MainWindow mouseReleaseEvent";
            updateToolBarPos();
            updateCursor(ev);

            // Record select area name with window name if just click (no drag).
            if (!m_isFirstDrag) {
                for (int i = 0; i < m_windowRects.length(); i++) {
                    int wx = m_windowRects[i].x();
                    int wy = m_windowRects[i].y();
                    int ww = m_windowRects[i].width();
                    int wh = m_windowRects[i].height();
                    int ex = ev->x();
                    int ey = ev->y();
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

                if (m_recordX + m_recordWidth > m_backgroundRect.width()) {
                    m_recordX = m_backgroundRect.width() - m_recordWidth;
                }

                if (m_recordY + m_recordHeight > m_backgroundRect.height()) {
                    m_recordY = m_backgroundRect.height() - m_recordHeight;
                }
            }

            needRepaint = true;
        }

        m_isPressButton = false;
        m_isReleaseButton = true;

        needRepaint = true;
    }

    if (needRepaint) {
        update();
    }

    QLabel::mouseReleaseEvent(ev);
}

void MainWindow::hideEvent(QHideEvent *event)
{
    qApp->setOverrideCursor(Qt::ArrowCursor);
    QLabel::hideEvent(event);
}

void MainWindow::mouseMoveEvent(QMouseEvent *ev)
{
    bool needRepaint = false;

    m_updateZoomTimer->start(200);

    if (!m_isShapesWidgetExist) {
        if (m_recordWidth > 0 && m_recordHeight >0 && !m_needSaveScreenshot && this->isVisible()) {
            m_sizeTips->updateTips(QPoint(m_recordX, m_recordY),
                                                         QString("%1X%2").arg(m_recordWidth).arg(m_recordHeight));

            if (m_toolBar->isVisible()) {
                updateToolBarPos();
                m_zoomIndicator->hide();
            }
        }

        if (m_isFirstMove) {
            if (!m_toolBar->isVisible() && !m_isFirstReleaseButton) {
                QPoint curPos = this->cursor().pos();
                QPoint tmpPos;
                if (curPos.x() + INDICATOR_WIDTH + CURSOR_WIDTH > m_backgroundRect.x()
                        + m_backgroundRect.width()) {
                      tmpPos.setX(curPos.x() - INDICATOR_WIDTH);
                } else {
                    tmpPos.setX(curPos.x() + CURSOR_WIDTH);
                }

                if (curPos.y() + INDICATOR_WIDTH > m_backgroundRect.y() + m_backgroundRect.height()) {
                    tmpPos.setY(curPos.y() - INDICATOR_WIDTH);
                } else {
                    tmpPos.setY(curPos.y() + CURSOR_HEIGHT);
                }

                m_zoomIndicator->showMagnifier(QPoint(
                    std::max(tmpPos.x() - m_backgroundRect.x(), 0),
                    std::max(tmpPos.y() - m_backgroundRect.y(), 0)));
            }
        } else {
            m_isFirstMove = true;
            needRepaint = true;
        }

        if (m_isFirstPressButton) {
            if (!m_isFirstReleaseButton) {
                if (m_isPressButton && !m_isReleaseButton) {
                    m_recordX = std::min(m_dragStartX, ev->x());
                    m_recordY = std::min(m_dragStartY, ev->y());
                    m_recordWidth = std::abs(m_dragStartX - ev->x());
                    m_recordHeight = std::abs(m_dragStartY - ev->y());

                    needRepaint = true;
                }
            } else if (m_isPressButton) {
                if (m_mouseStatus != ShotMouseStatus::Wait && m_dragRecordX >= 0
                && m_dragRecordY >= 0) {
                    if (m_dragAction == ResizeDirection::Moving && m_moving) {
                        m_recordX = std::max(std::min(m_dragRecordX + ev->x() - m_dragStartX,
                                                                                  m_backgroundRect.width() - m_recordWidth), 1);
                        m_recordY = std::max(std::min(m_dragRecordY + ev->y() - m_dragStartY,
                                                                                  m_backgroundRect.height() - m_recordHeight), 1);

                    } else if (m_dragAction == ResizeDirection::TopLeft) {
                        resizeDirection(ResizeDirection::Top, ev);
                        resizeDirection(ResizeDirection::Left, ev);
                    } else if (m_dragAction == ResizeDirection::TopRight) {
                        resizeDirection(ResizeDirection::Top, ev);
                        resizeDirection(ResizeDirection::Right, ev);
                    } else if (m_dragAction == ResizeDirection::BottomLeft) {
                        resizeDirection(ResizeDirection::Bottom, ev);
                        resizeDirection(ResizeDirection::Left, ev);
                    } else if (m_dragAction == ResizeDirection::BottomRight) {
                        resizeDirection(ResizeDirection::Bottom, ev);
                        resizeDirection(ResizeDirection::Right, ev);
                    } else if (m_dragAction == ResizeDirection::Top) {
                        resizeDirection(ResizeDirection::Top, ev);
                    } else if (m_dragAction == ResizeDirection::Bottom) {
                        resizeDirection(ResizeDirection::Bottom, ev);
                    } else if (m_dragAction == ResizeDirection::Left) {
                        resizeDirection(ResizeDirection::Left, ev);
                    } else if (m_dragAction == ResizeDirection::Right) {
                        resizeDirection(ResizeDirection::Right, ev);
                    }

                    needRepaint = true;
                }
            }

            updateCursor(ev);
            int mousePosition =  getDirection(ev);
            bool drawPoint = mousePosition != ResizeDirection::Moving;
            if (drawPoint != m_needDrawSelectedPoint) {
                m_needDrawSelectedPoint = drawPoint;
                needRepaint = true;
            }
        } else {
            if (m_screenNum == 0) {
                for (int i = 0; i < m_windowRects.length(); i++) {
                    int wx = m_windowRects[i].x();
                    int wy = m_windowRects[i].y();
                    int ww = m_windowRects[i].width();
                    int wh = m_windowRects[i].height();
                    int ex = ev->x();
                    int ey = ev->y();
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
                m_recordWidth = m_backgroundRect.width();
                m_recordHeight = m_backgroundRect.height();
                needRepaint = true;
            }
        }

        if (m_isPressButton && m_isFirstPressButton) {
            if (!m_isFirstDrag) {
                m_isFirstDrag = true;

                m_selectAreaName = tr("select-area");
            }
        }
    }

    if (needRepaint) {
        update();
    }

    QLabel::mouseMoveEvent(ev);
}

int MainWindow::getDirection(QEvent *event)
{
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
    } else if (cursorX > m_recordX && cursorX < m_recordX + m_recordWidth
               && cursorY > m_recordY && cursorY < m_recordY + m_recordHeight) {
        return ResizeDirection::Moving;
    } else {
        return ResizeDirection::Outting;
    }
}

void MainWindow::paintEvent(QPaintEvent *event)
{
    Q_UNUSED(event);
    QPainter painter(this);
    painter.setRenderHint(QPainter::Antialiasing, true);

    QRect backgroundRect = QRect(0, 0,
                                 m_backgroundRect.width(), m_backgroundRect.height());

    m_backgroundPixmap.setDevicePixelRatio(devicePixelRatioF());
    painter.drawPixmap(backgroundRect, m_backgroundPixmap);

    // Draw background.
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

            qreal margin =  qreal(RESIZEPOINT_WIDTH / 2);
            qreal paintX = frameRect.x() - margin;
            qreal paintY = frameRect.y() - margin;
            qreal paintWidth = frameRect.x() + frameRect.width() - margin;
            qreal paintHeight = frameRect.y() + frameRect.height() - margin;
            qreal paintHalfWidth = frameRect.x() + frameRect.width()/2 - margin;
            qreal paintHalfHeight = frameRect.y() + frameRect.height()/2 - margin;
            paintSelectedPoint(painter, QPointF(paintX, paintY), m_resizeBigPix);
            paintSelectedPoint(painter, QPointF(paintWidth, paintY), m_resizeBigPix);
            paintSelectedPoint(painter, QPointF(paintX, paintHeight), m_resizeBigPix);
            paintSelectedPoint(painter, QPointF(paintWidth, paintHeight), m_resizeBigPix);

            paintSelectedPoint(painter, QPointF(paintX, paintHalfHeight), m_resizeBigPix);
            paintSelectedPoint(painter, QPointF(paintHalfWidth, paintY), m_resizeBigPix);
            paintSelectedPoint(painter, QPointF(paintWidth, paintHalfHeight), m_resizeBigPix);
            paintSelectedPoint(painter, QPointF(paintHalfWidth, paintHeight), m_resizeBigPix);
        }
    }
}

void MainWindow::initShapeWidget(QString type)
{
    qDebug() << "show shapesWidget";
    m_shapesWidget = new ShapesWidget(this);
    m_shapesWidget->setShiftKeyPressed(m_isShiftPressed);

    if (type != "color")
        m_shapesWidget->setCurrentShape(type);

    m_shapesWidget->show();
    m_shapesWidget->setFixedSize(m_recordWidth - 4, m_recordHeight - 4);
    m_shapesWidget->move(m_recordX + 2, m_recordY + 2);

    updateToolBarPos();
    m_toolBar->raise();
    m_needDrawSelectedPoint = false;
    update();

    connect(m_toolBar, &ToolBar::updateColor,
            m_shapesWidget, &ShapesWidget::setPenColor);
    connect(m_shapesWidget, &ShapesWidget::reloadEffectImg,
            this, &MainWindow::reloadImage);
    connect(this, &MainWindow::deleteShapes, m_shapesWidget,
            &ShapesWidget::deleteCurrentShape);
    connect(m_shapesWidget, &ShapesWidget::requestScreenshot,
            this, &MainWindow::saveScreenshot);
    connect(m_shapesWidget, &ShapesWidget::shapePressed,
            m_toolBar, &ToolBar::shapePressed);
    connect(m_shapesWidget, &ShapesWidget::saveBtnPressed,
            m_toolBar, &ToolBar::saveBtnPressed);
    connect(m_shapesWidget, &ShapesWidget::requestExit, this, &MainWindow::exitApp);
    connect(this, &MainWindow::unDo, m_shapesWidget, &ShapesWidget::undoDrawShapes);
    connect(this, &MainWindow::saveActionTriggered,
            m_shapesWidget, &ShapesWidget::saveActionTriggered);
    connect(m_shapesWidget, &ShapesWidget::menuNoFocus, this, &MainWindow::activateWindow);
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
        } else {
            if (m_isPressButton) {
                qApp->setOverrideCursor(Qt::ClosedHandCursor);
            } else if (cursorX >= m_recordX - SPACING && cursorX <= m_recordX + m_recordWidth + SPACING
                       && cursorY >= m_recordY - SPACING && cursorY < m_recordY + m_recordHeight + SPACING) {
                qApp->setOverrideCursor(Qt::OpenHandCursor);
            } else {
                qApp->setOverrideCursor(Qt::ArrowCursor);
            }
        }
    }
}

void MainWindow::resizeDirection(ResizeDirection direction, QMouseEvent *e)
{
    int offsetX = e->x() - m_dragStartX;
    int offsetY = e->y() - m_dragStartY;

    switch (direction) {
    case ResizeDirection::Top: {
        m_recordY = std::max(std::min(m_dragRecordY + offsetY,
                                      m_dragRecordY + m_dragRecordHeight - RECORD_MIN_SIZE), 1);
        m_recordHeight = std::max(std::min(m_dragRecordHeight -
                                           offsetY, m_backgroundRect.height()), RECORD_MIN_SIZE);
        break;
    };
    case ResizeDirection::Bottom: {
        m_recordHeight = std::max(std::min(m_dragRecordHeight + offsetY,
                                           m_backgroundRect.height()), RECORD_MIN_SIZE);
        break;
    };
    case ResizeDirection::Left: {
        m_recordX = std::max(std::min(m_dragRecordX + offsetX,
                                      m_dragRecordX + m_dragRecordWidth - RECORD_MIN_SIZE), 1);
        m_recordWidth = std::max(std::min(m_dragRecordWidth - offsetX,
                                          m_backgroundRect.width()), RECORD_MIN_SIZE);
        break;
    };
    case ResizeDirection::Right: {
        m_recordWidth = std::max(std::min(m_dragRecordWidth + offsetX,
                                          m_backgroundRect.width()), RECORD_MIN_SIZE);
        break;
    };
    default:break;
    }
}

void MainWindow::fullScreenshot()
{
    m_mouseStatus = ShotMouseStatus::Shoting;
    repaint();
    qApp->setOverrideCursor(setCursorShape("start"));
    initDBusInterface();
    this->setFocus();
    m_configSettings =  ConfigSettings::instance();
    installEventFilter(this);

    if (m_hotZoneInterface->isValid())
        m_hotZoneInterface->asyncCall("EnableZoneDetected", false);

    QPoint curPos = this->cursor().pos();
    m_swUtil = DScreenWindowsUtil::instance(curPos);
    m_screenNum = m_swUtil->getScreenNum();
    m_backgroundRect = m_swUtil->backgroundRect();

    this->move(m_backgroundRect.x(), m_backgroundRect.y());
    this->setFixedSize(m_backgroundRect.size());
    m_needSaveScreenshot = true;
    shotFullScreen();
    m_toolBar = new ToolBar(this);
    m_toolBar->hide();

    if (m_hotZoneInterface->isValid())
        m_hotZoneInterface->asyncCall("EnableZoneDetected",  true);

    emit this->hideScreenshotUI();
//    DDesktopServices::playSystemSoundEffect(DDesktopServices::SSE_Screenshot);
//    using namespace utils;
    QPixmap screenShotPix(TempFile::instance()->getFullscreenFileName());
    saveAction(screenShotPix);
    sendNotify(m_saveIndex, m_saveFileName);
}

void MainWindow::savePath(const QString &path)
{
    if (!QFileInfo(path).dir().exists()) {
        exitApp();
    }

    qDebug() << "path exist!";
    startScreenshot();
    m_toolBar->specificedSavePath();
    m_specificedPath = path;

    connect(m_toolBar, &ToolBar::saveSpecifiedPath, this, [=]{
        emit releaseEvent();
        emit saveActionTriggered();
        m_needSaveScreenshot = true;
        qDebug() << "toolBar" << m_specificedPath;
        saveSpecificedPath(m_specificedPath);
    });
}

void MainWindow::saveSpecificedPath(QString path)
{
    QString savePath;
    QString baseName = QFileInfo(path).baseName();
    QString suffix = QFileInfo(path).completeSuffix();

    if (!QFileInfo(path).isDir() && !baseName.isEmpty())
    {
        if (isValidFormat(suffix)) {
            savePath = path;
        } else if (suffix.isEmpty()) {
            savePath = path + ".png";
        } else {
            qWarning() << "Invalid image format! Screenshot will quit, suffix:" << suffix;
            exitApp();
        }
        qDebug() << "process savepath1:" << savePath;
    } else {
        if (QFileInfo(path).isDir() && !path.endsWith("/")) {
            path = path + "/";
        }
        qDebug() << "path isEmpty!";

        QDateTime currentDate;
        QString currentTime =  currentDate.currentDateTime().
                toString("yyyyMMddHHmmss");
        if (m_selectAreaName.isEmpty()) {
            savePath = path + QString("%1_%2.png").arg(tr("DeepinScreenshot")).arg(currentTime);
        } else {
            savePath = path + QString("%1_%2_%3.png").arg(tr("DeepinScreenshot")).arg(
                                                                                       m_selectAreaName).arg(currentTime);
        }
        qDebug() << "process savepath2: " << savePath;
    }

    if (m_hotZoneInterface->isValid())
        m_hotZoneInterface->asyncCall("EnableZoneDetected",  true);
//    using namespace utils;
    m_toolBar->setVisible(false);
    m_sizeTips->setVisible(false);

    shotCurrentImg();
//    DDesktopServices::playSystemSoundEffect(DDesktopServices::SSE_Screenshot);

    QPixmap screenShotPix(TempFile::instance()->getTmpFileName());
    screenShotPix.save(savePath);
    QStringList actions;
    actions << "_open" << tr("View");
    QVariantMap hints;
    QString fileDir = QUrl::fromLocalFile(QFileInfo(savePath).absoluteDir().absolutePath()).toString();
    QString filePath =  QUrl::fromLocalFile(savePath).toString();
    QString command;
    if (QFile("/usr/bin/dde-file-manager").exists()) {
        command = QString("/usr/bin/dde-file-manager,%1?selectUrl=%2"
                          ).arg(fileDir).arg(filePath);
    } else {
        command = QString("xdg-open,%1").arg(filePath);
    }

    hints["x-deepin-action-_open"] = command;

    QString summary = QString(tr("Picture has been saved to %1")).arg(savePath);

    m_notifyDBInterface->Notify("Deepin Screenshot", 0,  "deepin-screenshot", "",
                                summary, actions, hints, 0);
    exitApp();
}

//void MainWindow::delayScreenshot(int num) {
//    initDBusInterface();
//    QString summary = QString(tr("Deepin Screenshot will start after %1 second.").arg(num));
//    QStringList actions = QStringList();
//    QVariantMap hints;
//    if (num >= 2) {
//        m_notifyDBInterface->Notify("Deepin Screenshot", 0,  "deepin-screenshot", "",
//                                    summary, actions, hints, 0);
//        QTimer* timer = new QTimer;
//        timer->setSingleShot(true);
//        timer->start(1000*num);
//        connect(timer, &QTimer::timeout, this, [=]{
//            m_notifyDBInterface->CloseNotification(0);
//            initUI();
//            initShortcut();
//            this->show();
//        });
//    } else {
//        initUI();
//        initShortcut();
//        this->show();
//    }
//}

void MainWindow::noNotify()
{
    m_controlCenterDBInterface = new DBusControlCenter(this);
    m_hotZoneInterface = new DBusZone(this);
    m_interfaceExist = true;
    m_noNotify = true;

    initOriginUI();
    this->show();
    initSecondUI();
    initShortcut();
}

void MainWindow::topWindow()
{
    initOriginUI();
    this->show();
    initSecondUI();
    initDBusInterface();

    if (m_screenNum == 0) {
        m_windowRects  = m_swUtil->windowsRect();

        m_recordX = m_windowRects[0].x();
        m_recordY = m_windowRects[0].y();
        m_recordWidth = m_windowRects[0].width();
        m_recordHeight = m_windowRects[0].height();
    } else {
        m_recordX = m_backgroundRect.x();
        m_recordY = m_backgroundRect.y();
        m_recordWidth = m_backgroundRect.width();
        m_recordHeight = m_backgroundRect.height();
    }

    this->hide();
    emit this->hideScreenshotUI();
//    using namespace utils;
    QPixmap screenShotPix = QPixmap(TempFile::instance()->getFullscreenFileName()).copy(
                m_recordX, m_recordY, m_recordWidth, m_recordHeight);

    m_needSaveScreenshot = true;
//    DDesktopServices::playSystemSoundEffect(DDesktopServices::SSE_Screenshot);
    saveAction(screenShotPix);
    sendNotify(m_saveIndex, m_saveFileName);
}

void MainWindow::expressSaveScreenshot()
{
    if (m_specificedPath.isEmpty()) {
        qDebug() << "specificedPath isEmpty!";
        saveScreenshot();
    } else {
        qDebug() << "specificedPath isEmpty!XCVBN";
        m_toolBar->specificedSavePath();
        emit m_toolBar->saveSpecifiedPath();
    }
}

void MainWindow::startScreenshot()
{
    initOriginUI();
    m_mouseStatus = ShotMouseStatus::Shoting;
    qApp->setOverrideCursor(setCursorShape("start"));
    this->show();

    initSecondUI();

    initDBusInterface();
    initShortcut();
}

QPixmap MainWindow::getPixmapofRect(const QRect &rect)
{
    const qreal dpr = qApp->devicePixelRatio();
    return m_swUtil->primaryScreen()->grabWindow(
                m_swUtil->rootWindowId(),
               rect.x() / dpr, rect.y() / dpr, rect.width(), rect.height());
}

void MainWindow::initBackground()
{
    m_backgroundPixmap = getPixmapofRect(m_backgroundRect);
}

void MainWindow::shotFullScreen() {
    QPixmap tmpImg =  getPixmapofRect(m_backgroundRect);

    //    using namespace utils;
    tmpImg.save(TempFile::instance()->getFullscreenFileName(), "png");
}

void MainWindow::shotCurrentImg()
{
    if (m_recordWidth == 0 || m_recordHeight == 0)
        return;

    m_needDrawSelectedPoint = false;
    m_drawNothing = true;
    update();

    QEventLoop eventloop1;
    QTimer::singleShot(100, &eventloop1, SLOT(quit()));
    eventloop1.exec();

    qDebug() << "shotCurrentImg shotFullScreen";
//    using namespace utils;
    shotFullScreen();
    if (m_isShapesWidgetExist) {
        m_shapesWidget->hide();
    }

    this->hide();
    emit hideScreenshotUI();

    const qreal ratio = this->devicePixelRatioF();
    QRect target( m_recordX * ratio,
                  m_recordY * ratio,
                  m_recordWidth * ratio,
                  m_recordHeight * ratio );

    QPixmap tmpImg(TempFile::instance()->getFullscreenFileName());
    tmpImg = tmpImg.copy(target);

    tmpImg.save(TempFile::instance()->getTmpFileName(), "png");
}

void MainWindow::shotImgWidthEffect()
{
    if (m_recordWidth == 0 || m_recordHeight == 0)
        return;

    update();

//    QEventLoop eventloop;
//    QTimer::singleShot(100, &eventloop, SLOT(quit()));
//    eventloop.exec();

    qDebug() << m_toolBar->isVisible() << m_sizeTips->isVisible();
    QPixmap tmpImg =    getPixmapofRect(m_shapesWidget->geometry());

    qDebug() << tmpImg.isNull() << tmpImg.size();

//    using namespace utils;
    tmpImg.save(TempFile::instance()->getTmpFileName(), "png");
    m_drawNothing = false;
    update();
}

void MainWindow::saveScreenshot()
{
    emit releaseEvent();
    emit saveActionTriggered();

//    DDesktopServices::playSystemSoundEffect(DDesktopServices::SSE_Screenshot);
    if (m_hotZoneInterface->isValid())
        m_hotZoneInterface->asyncCall("EnableZoneDetected",  true);
    m_needSaveScreenshot = true;

    m_toolBar->setVisible(false);
    m_sizeTips->setVisible(false);

    shotCurrentImg();

//    using namespace utils;
    saveAction(TempFile::instance()->getTmpFileName());
    sendNotify(m_saveIndex, m_saveFileName);
}

void MainWindow::saveAction(QPixmap pix)
{
    emit releaseEvent();

//    using namespace utils;
    QPixmap screenShotPix = pix;
    QDateTime currentDate;
    QString currentTime =  currentDate.currentDateTime().
            toString("yyyyMMddHHmmss");
    m_saveFileName = "";

    QStandardPaths::StandardLocation saveOption = QStandardPaths::TempLocation;
    bool copyToClipboard = false;
    m_saveIndex =  ConfigSettings::instance()->value("save", "save_op").toInt();
    switch (m_saveIndex) {
    case 0: {
        saveOption = QStandardPaths::DesktopLocation;
        ConfigSettings::instance()->setValue("common", "default_savepath", QStandardPaths::writableLocation(
                                                 QStandardPaths::DesktopLocation));
        break;
    }
    case 1: {
        QString defaultSaveDir = ConfigSettings::instance()->value("common", "default_savepath").toString();
        if (defaultSaveDir.isEmpty()) {
            saveOption = QStandardPaths::DesktopLocation;
        } else if (defaultSaveDir == "clipboard") {
            copyToClipboard = true;
            m_saveIndex = 3;
        } else {
            if (m_selectAreaName.isEmpty()) {
                m_saveFileName = QString("%1/%2_%3.png").arg(defaultSaveDir).arg(tr(
                                                                                     "DeepinScreenshot")).arg(currentTime);
            } else {
                m_saveFileName = QString("%1/%2_%3_%4.png").arg(defaultSaveDir).arg(tr(
                                                                                        "DeepinScreenshot")).arg(m_selectAreaName).arg(currentTime);
            }
        }
        break;
    }
    case 2: {
        this->hide();
        this->releaseKeyboard();
        QFileDialog fileDialog;
        QString  lastFileName;
        if (m_selectAreaName.isEmpty()) {
            lastFileName = QString("%1/%2_%3.png").arg(QStandardPaths::writableLocation(
                                        QStandardPaths::PicturesLocation)).arg(tr("DeepinScreenshot")).arg(currentTime);
        } else {
            lastFileName = QString("%1/%2_%3_%4.png").arg(QStandardPaths::writableLocation(
                                         QStandardPaths::PicturesLocation)).arg(tr("DeepinScreenshot")
                                                                                                     ).arg(m_selectAreaName).arg(currentTime);
        }

        m_saveFileName =  fileDialog.getSaveFileName(this, "Save",  lastFileName,
                                                     tr("PNG (*.png);;JPEG (*.jpg *.jpeg);; BMP (*.bmp);; PGM (*.pgm);;"
                                                        "XBM (*.xbm);;XPM(*.xpm)"));


        if (QFileInfo(m_saveFileName).isDir()) {
            qDebug() << "empty fileName";
            exitApp();
        }

        QString fileSuffix = QFileInfo(m_saveFileName).completeSuffix();
        if (fileSuffix.isEmpty()) {
                    m_saveFileName = m_saveFileName + ".png";
        } else if ( !isValidFormat(fileSuffix)) {
            qWarning() << "The fileName has invalid suffix!" << fileSuffix << m_saveFileName;
            exitApp();
        }

        ConfigSettings::instance()->setValue("common", "default_savepath",
                                             QFileInfo(m_saveFileName).dir().absolutePath());
        break;
    }
    case 3: {
        copyToClipboard = true;
        ConfigSettings::instance()->setValue("common", "default_savepath",   "clipboard");
        break;
    }
    case 4: {
        copyToClipboard = true;
        QString defaultSaveDir = ConfigSettings::instance()->value("common", "default_savepath").toString();
        if (defaultSaveDir.isEmpty()) {
            saveOption = QStandardPaths::DesktopLocation;
        } else if (defaultSaveDir == "clipboard") {
            m_saveIndex = 3;
        } else  {
            if (m_selectAreaName.isEmpty()) {
                m_saveFileName = QString("%1/%2_%3.png").arg(defaultSaveDir).arg(tr(
                                                                                     "DeepinScreenshot")).arg(currentTime);
            } else {
                m_saveFileName = QString("%1/%2_%3_%4.png").arg(defaultSaveDir).arg(tr(
                                                                                        "DeepinScreenshot")).arg(m_selectAreaName).arg(currentTime);
            }
        }
        break;
    }
    default:
        break;
    }

    int toolBarSaveQuality = std::min(ConfigSettings::instance()->value("save",
                                                            "save_quality").toInt(), 100);

    if (toolBarSaveQuality != 100) {
       qreal saveQuality = qreal(toolBarSaveQuality)*5/1000 + 0.5;

       int pixWidth = screenShotPix.width();
       int pixHeight = screenShotPix.height();
        screenShotPix = screenShotPix.scaled(pixWidth*saveQuality, pixHeight*saveQuality,
                                                                             Qt::KeepAspectRatio, Qt::FastTransformation);
        screenShotPix = screenShotPix.scaled(pixWidth,  pixHeight,
                                                                            Qt::KeepAspectRatio, Qt::FastTransformation);
    }

    if (m_saveIndex ==2 && m_saveFileName.isEmpty()) {
        exitApp();
        return;
    } else if (m_saveIndex == 2 || !m_saveFileName.isEmpty()) {
        screenShotPix.save(m_saveFileName,  QFileInfo(m_saveFileName).suffix().toLocal8Bit());
    } else if (saveOption != QStandardPaths::TempLocation || m_saveFileName.isEmpty()) {
        if (m_selectAreaName.isEmpty()) {
            m_saveFileName = QString("%1/%2_%3.png").arg(QStandardPaths::writableLocation(
                             saveOption)).arg(tr("DeepinScreenshot")).arg(currentTime);
        } else {
            m_saveFileName = QString("%1/%2_%3_%4.png").arg(QStandardPaths::writableLocation(
                             saveOption)).arg(tr("DeepinScreenshot")).arg(m_selectAreaName).arg(currentTime);
        }
        screenShotPix.save(m_saveFileName,  "PNG");
    }

    if (copyToClipboard) {
        Q_ASSERT(!screenShotPix.isNull());
        QClipboard* cb = qApp->clipboard();
        cb->setPixmap(screenShotPix, QClipboard::Clipboard);
    }
}

void MainWindow::sendNotify(int saveIndex, QString saveFilePath)
{
    QStringList actions;
    actions << "_open" << tr("View");
    QVariantMap hints;
    QString fileDir = QUrl::fromLocalFile(QFileInfo(saveFilePath).absoluteDir().absolutePath()).toString();
    QString filePath =  QUrl::fromLocalFile(saveFilePath).toString();
    QString command;
    if (QFile("/usr/bin/dde-file-manager").exists()) {
        command = QString("/usr/bin/dde-file-manager,%1?selectUrl=%2"
                          ).arg(fileDir).arg(filePath);
    } else {
        command = QString("xdg-open,%1").arg(filePath);
    }

    hints["x-deepin-action-_open"] = command;

    qDebug() << "saveFilePath:" << saveFilePath;

    QString summary;
    if (saveIndex == 3) {
        summary = QString(tr("Picture has been saved to clipboard"));
    } else {
        summary = QString(tr("Picture has been saved to %1")).arg(saveFilePath);
    }

    if (saveIndex == 3 && !m_noNotify) {
        QVariantMap emptyMap;
        m_notifyDBInterface->Notify("Deepin Screenshot", 0,  "deepin-screenshot", "",
                                    summary,  QStringList(), emptyMap, 0);
    }  else if ( !m_noNotify &&  !(m_saveIndex == 2 && m_saveFileName.isEmpty())) {
        m_notifyDBInterface->Notify("Deepin Screenshot", 0,  "deepin-screenshot", "",
                                    summary, actions, hints, 0);
    }

    QTimer::singleShot(2, [=]{
        exitApp();
    });

}

void MainWindow::reloadImage(QString effect)
{
    //*save tmp image file
    shotImgWidthEffect();
    //using namespace utils;
    const int radius = 10;
    QPixmap tmpImg(TempFile::instance()->getTmpFileName());
    int imgWidth = tmpImg.width();
    int imgHeight = tmpImg.height();
    if (effect == "blur") {
        if (!tmpImg.isNull()) {
            tmpImg = tmpImg.scaled(imgWidth/radius, imgHeight/radius,
                                   Qt::IgnoreAspectRatio, Qt::SmoothTransformation);
            tmpImg = tmpImg.scaled(imgWidth, imgHeight, Qt::IgnoreAspectRatio,
                                   Qt::SmoothTransformation);
            tmpImg.save(TempFile::instance()->getBlurFileName(), "png");
        }
    } else {
        if (!tmpImg.isNull()) {
            tmpImg = tmpImg.scaled(imgWidth/radius, imgHeight/radius,
                                   Qt::IgnoreAspectRatio, Qt::SmoothTransformation);
            tmpImg = tmpImg.scaled(imgWidth, imgHeight);
            tmpImg.save(TempFile::instance()->getMosaicFileName(), "png");
        }
    }
}

void MainWindow::onViewShortcut()
{
    QRect rect = window()->geometry();
    QPoint pos(rect.x() + rect.width()/2, rect.y() + rect.height()/2);
    Shortcut sc;
    QStringList shortcutString;
    QString param1 = "-j=" + sc.toStr();
    QString param2 = "-p=" + QString::number(pos.x()) + "," + QString::number(pos.y());
    shortcutString << "-b" << param1 << param2;

    QProcess* shortcutViewProc = new QProcess(this);
    shortcutViewProc->startDetached("killall deepin-shortcut-viewer");
    shortcutViewProc->startDetached("deepin-shortcut-viewer", shortcutString);

    connect(shortcutViewProc, SIGNAL(finished(int)), shortcutViewProc, SLOT(deleteLater()));
}

void MainWindow::onHelp()
{
//    using namespace utils;
    if (m_manualPro.isNull()) {
        const QString pro = "dman";
        const QStringList args("deepin-screenshot");
        m_manualPro = new QProcess();
        connect(m_manualPro.data(), SIGNAL(finished(int)),
                m_manualPro.data(), SLOT(deleteLater()));
        this->hide();
        m_manualPro->start(pro, args);

        exitApp();
    }
}

void MainWindow::exitApp()
{
    if (m_interfaceExist && nullptr != m_hotZoneInterface)
    {
        if (m_hotZoneInterface->isValid())
            m_hotZoneInterface->asyncCall("EnableZoneDetected",  true);
    }
    qApp->quit();
}

void MainWindow::updateToolBarPos()
{
    QPoint toolbarPoint;
    toolbarPoint = QPoint(m_recordX + m_recordWidth - m_toolBar->width(),
                          std::max(m_recordY + m_recordHeight + TOOLBAR_Y_SPACING, 0));

    if (m_toolBar->width() > m_recordX + m_recordWidth) {
        toolbarPoint.setX(m_recordX + 8);
    }
    if (toolbarPoint.y()>= m_backgroundRect.y() + m_backgroundRect.height()
            - m_toolBar->height() - 28) {
        if (m_recordY > 28*2 + 10) {
            toolbarPoint.setY(m_recordY - m_toolBar->height() - TOOLBAR_Y_SPACING);
        } else {
            toolbarPoint.setY(m_recordY + TOOLBAR_Y_SPACING);
        }
    }
    m_toolBar->showAt(toolbarPoint);
}
