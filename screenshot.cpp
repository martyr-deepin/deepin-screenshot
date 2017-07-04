#include "screenshot.h"

#include <QApplication>
#include <QDesktopWidget>
#include <QScreen>
#include <QWindow>

#include "dbusinterface/dbusnotify.h"
#include "utils/screenutils.h"

Screenshot::Screenshot(QWidget *parent)
    : QMainWindow(parent)
{
}

void Screenshot::initUI() {
    setWindowFlags(Qt::X11BypassWindowManagerHint | Qt::WindowStaysOnTopHint |
                   Qt::FramelessWindowHint);
    setAttribute(Qt::WA_TranslucentBackground);

    QPoint curPos = this->cursor().pos();
    ScreenUtils::instance(curPos);
    QRect bgRect = ScreenUtils::instance(curPos)->backgroundRect();

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
    initUI();
    this->show();

    m_window->startScreenshot();
}

void Screenshot::delayScreenshot(int num)
{
    QString summary = QString(tr("Deepin Screenshot will start after %1 second").arg(num));
    QStringList actions = QStringList();
    QVariantMap hints;
    DBusNotify* notifyDBus = new DBusNotify(this);
    if (num >= 2) {
        notifyDBus->Notify("Deepin Screenshot", 0,  "deepin-screenshot", "",
                                    summary, actions, hints, 0);
    }

    QTimer* timer = new QTimer;
    timer->setSingleShot(true);
    timer->start(1000*num);
    connect(timer, &QTimer::timeout, this, [=]{
        notifyDBus->CloseNotification(0);
        startScreenshot();
    });
}

void Screenshot::fullscreenScreenshot()
{
    initUI();
    this->show();
    m_window->fullScreenshot();
}

void Screenshot::topWindowScreenshot()
{
    initUI();
    this->show();
    m_window->topWindow();
}

void Screenshot::noNotifyScreenshot()
{
    initUI();
    this->show();
    m_window->noNotify();
}

void Screenshot::savePathScreenshot(const QString &path)
{
    initUI();
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

