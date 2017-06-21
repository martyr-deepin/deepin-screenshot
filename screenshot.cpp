#include "screenshot.h"

#include <QApplication>
#include <QDesktopWidget>
#include <QScreen>
#include <QWindow>

Screenshot::Screenshot(QWidget *parent)
    : QMainWindow(parent)
{
    setWindowFlags(Qt::X11BypassWindowManagerHint | Qt::WindowStaysOnTopHint |
                   Qt::FramelessWindowHint);
    setAttribute(Qt::WA_TranslucentBackground);

    QPoint curPos = this->cursor().pos();
     int screenNum = qApp->desktop()->screenNumber(curPos);
     QList<QScreen*> screenList = qApp->screens();
     QRect bgRect;
     if (screenNum != 0 && screenNum < screenList.length()) {
        bgRect = screenList[screenNum]->geometry();
     } else {
         bgRect =  qApp->primaryScreen()->geometry();
     }
    qDebug() << "MainWindow bgRect:" << bgRect;
     this->move(bgRect.x(), bgRect.y());
     this->setFixedSize(bgRect.size());

    m_eventContainer = new EventContainer(this);
    m_window = new MainWindow(m_eventContainer);

    setCentralWidget(m_window);
    this->installEventFilter(this);

    connect(m_window, &MainWindow::releaseEvent, this, [=]{
        qDebug() << "relase event !!!";
        m_keyboardReleased = true;
        m_keyboardGrabbed =  this->windowHandle()->setKeyboardGrabEnabled(false);
        qDebug() << "keyboardGrabbed:" << m_keyboardGrabbed;
        removeEventFilter(this);
    });
    connect(m_window, &MainWindow::hideScreenshotUI, this, [=]{
        this->hide();
    });
}

void Screenshot::startScreenshot()
{
    this->show();
    m_window->startScreenshot();
}

void Screenshot::delayScreenshot(int num)
{
    this->show();
    m_window->delayScreenshot(num);
}

void Screenshot::fullscreenScreenshot()
{
    this->show();
    m_window->fullScreenshot();
}

void Screenshot::topWindowScreenshot()
{
    this->show();
    m_window->topWindow();
}

void Screenshot::noNotifyScreenshot()
{
    this->show();
    m_window->noNotify();
}

void Screenshot::savePathScreenshot(const QString &path)
{
    this->show();
    m_window->savePath(path);
}

bool Screenshot::eventFilter(QObject* watched, QEvent *event)
{
    Q_UNUSED(watched);
#undef KeyPress
#undef KeyRelease
    if (!m_keyboardGrabbed &&this->windowHandle() != NULL)
    {
        m_keyboardGrabbed = this->windowHandle()->setKeyboardGrabEnabled(true);
        qDebug() << "m_keyboardGrabbed:" << m_keyboardGrabbed;
    }

    if (m_keyboardGrabbed)
    {
        if (event->type() == QEvent::KeyPress || event->type() == QEvent::KeyRelease) {
            m_eventContainer->handleEvent(event);

            return true;
        }

        if (event->type() == QEvent::Paint) {
            m_eventContainer->handleEvent(event);
            return true;
        }
    }

    return false;
}

Screenshot::~Screenshot() {}

