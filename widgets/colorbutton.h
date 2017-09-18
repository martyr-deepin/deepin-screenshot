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

#ifndef COLORBUTTON_H
#define COLORBUTTON_H

#include <QPushButton>
#include <QPaintEvent>

class ColorButton : public QPushButton {
    Q_OBJECT
public:
    ColorButton(QColor bgColor, QWidget*parent = 0);
    ~ColorButton();

    void setColorBtnChecked();

public slots:
    QColor getColor();

signals:
    void updatePaintColor(QColor paintColor);

//protected:
//    void paintEvent(QPaintEvent *);

private:
    QColor m_bgColor;
};

#endif // COLORBUTTON_H
