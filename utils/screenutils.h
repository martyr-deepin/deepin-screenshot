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

#ifndef SCREENUTILS_H
#define SCREENUTILS_H

#include <QObject>
#include <QWindow>

class ScreenUtils : public QObject {
    Q_OBJECT
public:
    static ScreenUtils *instance(QPoint pos);

public slots:
    int getScreenNum();
    QRect backgroundRect();
    WId rootWindowId();
    QScreen* primaryScreen();

private:
     static ScreenUtils* m_screenUtils;
     ScreenUtils(QPoint pos, QObject* parent = 0);
     ~ScreenUtils();

    QRect m_backgroundRect;
    int m_screenNum;
    WId m_rootWindowId;
    QScreen* m_primaryScreen;
};

#endif // SCREENUTILS_H
