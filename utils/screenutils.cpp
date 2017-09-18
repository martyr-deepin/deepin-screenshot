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
