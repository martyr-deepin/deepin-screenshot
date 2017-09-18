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

#ifndef ZOOMINDICATOR_H
#define ZOOMINDICATOR_H

#include <QLabel>
#include <QPainter>
#include <QPaintEvent>

class ZoomIndicator : public QLabel {
    Q_OBJECT
public:
    ZoomIndicator(QWidget* parent = 0);
    ~ZoomIndicator();

    void showMagnifier(QPoint pos);
    void updatePaintEvent();

protected:
    void paintEvent(QPaintEvent *);

private:
    QRect m_centerRect;
    bool m_updatePos;
    QPixmap m_lastPic;
    QBrush m_lastCenterPosBrush;
    QPoint m_pos;
};

#endif // MAGNIFIER_H
