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

#ifndef FONTSIZEWIDGET_H
#define FONTSIZEWIDGET_H

#include <QLabel>
#include <QWidget>
#include <QLineEdit>
#include <QPushButton>

class Seperator : public QLabel
{
    Q_OBJECT
public:
    Seperator(QWidget* parent);
    ~Seperator();
};

class FontSizeWidget : public QLabel
{
    Q_OBJECT
public:
    FontSizeWidget(QWidget* parent = 0);
    ~FontSizeWidget();

    void initWidget();
    void adjustFontSize(bool add);
    void setFontSize(int fontSize);

signals:
    void fontSizeChanged(int fontSize);

private:
    QLineEdit* m_fontSizeEdit;
    QPushButton* m_addSizeBtn;
    QPushButton* m_reduceSizeBtn;
    int m_fontSize;
};
#endif // FONTSIZEWIDGET_H
