/*
 * Copyright (C) 2017 ~ 2018 Deepin Technology Co., Ltd.
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

#include "screenshot.h"

#include <QApplication>
#include <QDesktopWidget>
#include <QScreen>
#include <QWindow>

#include "dbusinterface/dbusnotify.h"

#include <dscreenwindowsutil.h>

DWM_USE_NAMESPACE

Screenshot::Screenshot(QObject *parent)
    : QObject(parent)
{
}

void Screenshot::initUI() {
    m_eventContainer = new EventContainer(this);
    m_window = new MainWindow;
    if (m_noNotify) {
        m_window->noNotify();
    }
}

void Screenshot::noNotify()
{
    m_noNotify = true;
}

void Screenshot::startScreenshot()
{
    initUI();
    m_window->show();

    m_window->startScreenshot();
}

void Screenshot::delayScreenshot(double num)
{
    QString summary = QString(tr("Deepin Screenshot will start after %1 seconds").arg(num));
    QStringList actions = QStringList();
    QVariantMap hints;
    DBusNotify* notifyDBus = new DBusNotify(this);
    if (num >= 2 && !m_noNotify) {
        notifyDBus->Notify("Deepin Screenshot", 0,  "deepin-screenshot", "",
                                    summary, actions, hints, 0);
    }

    QTimer* timer = new QTimer;
    timer->setSingleShot(true);
    timer->start(int(1000*num));
    connect(timer, &QTimer::timeout, this, [=]{
        notifyDBus->CloseNotification(0);
        startScreenshot();
    });
}

void Screenshot::fullscreenScreenshot()
{
    initUI();
    m_window->show();
    m_window->fullScreenshot();
}

void Screenshot::topWindowScreenshot()
{
    initUI();
    m_window->show();
    m_window->topWindow();
}

void Screenshot::savePathScreenshot(const QString &path)
{
    initUI();
    m_window->show();
    m_window->savePath(path);
}

Screenshot::~Screenshot() {}
