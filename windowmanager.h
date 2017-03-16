/* -*- Mode: C++; indent-tabs-mode: nil; tab-width: 4 -*-
 * -*- coding: utf-8 -*-
 *
 * Copyright (C) 2011 ~ 2017 Deepin, Inc.
 *               2011 ~ 2017 Wang Yong
 *
 * Author:     Wang Yong <wangyong@deepin.com>
 * Maintainer: Wang Yong <wangyong@deepin.com>
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

#ifndef WINDOWMANAGER_H
#define WINDOWMANAGER_H

#include <QObject>
#include <xcb/xcb.h>
#include <xcb/xcb_aux.h>

struct WindowRect {
    int x;
    int y;
    int width;
    int height;
};

class WindowManager : public QObject
{
    Q_OBJECT

public:
    WindowManager(QObject *parent = 0);
    ~WindowManager();

    QList<int> getWindowFrameExtents(xcb_window_t window);
    QList<xcb_window_t> getWindows();
    QString getAtomName(xcb_atom_t atom);
    QString getWindowName(xcb_window_t window);
    QString getWindowClass(xcb_window_t window);
    QStringList getWindowTypes(xcb_window_t window);
    QStringList getWindowStates(xcb_window_t window);
    WindowRect getRootWindowRect();
    WindowRect getWindowRect(xcb_window_t window);
    int getCurrentWorkspace(xcb_window_t window);
    int getWindowWorkspace(xcb_window_t window);
    xcb_atom_t getAtom(QString name);
    xcb_get_property_reply_t* getProperty(xcb_window_t window, QString propertyName, xcb_atom_t type);
    void setWindowBlur(int wid, QVector<uint32_t> &data);
    void translateCoords(xcb_window_t window, int32_t& x, int32_t& y);
    WindowRect adjustRectInScreenArea(WindowRect rect);

    xcb_window_t rootWindow;
    
private:
    xcb_connection_t* conn;
};

#endif
