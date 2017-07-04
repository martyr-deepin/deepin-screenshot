#include "screenutils.h"

#include <QApplication>
#include <QDesktopWidget>
#include <QScreen>

ScreenUtils* ScreenUtils::m_screenUtils = nullptr;
ScreenUtils* ScreenUtils::instance(QPoint pos) {
    if (!m_screenUtils) {
        m_screenUtils = new ScreenUtils(pos);
    }

    return m_screenUtils;
}

ScreenUtils::ScreenUtils(QPoint pos, QObject *parent)
    : QObject(parent) {
    QList<QScreen*> screenList = qApp->screens();
    m_screenNum = qApp->desktop()->screenNumber(pos);
    m_rootWindowId = qApp->desktop()->screen(m_screenNum)->winId();
    m_primaryScreen = screenList[m_screenNum];
    if (m_screenNum != 0 && m_screenNum < screenList.length()) {
        m_backgroundRect = screenList[m_screenNum]->geometry();
    } else {
        m_backgroundRect = qApp->primaryScreen()->geometry();
    }

}

ScreenUtils::~ScreenUtils() {}

int ScreenUtils::getScreenNum() {
    return m_screenNum;
}

QRect ScreenUtils::backgroundRect() {
    return m_backgroundRect;
}

WId ScreenUtils::rootWindowId() {
    return m_rootWindowId;
}

QScreen* ScreenUtils::primaryScreen() {
    return m_primaryScreen;
}
