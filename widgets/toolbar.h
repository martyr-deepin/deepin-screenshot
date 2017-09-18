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

#ifndef TOOLBAR_H
#define TOOLBAR_H

#include <QLabel>
#include <QPainter>
#include <DBlurEffectWidget>
#include <QEvent>
#include <QLabel>
#include <QDebug>

#include "majtoolbar.h"
#include "subtoolbar.h"

DWIDGET_USE_NAMESPACE

class ToolBarWidget : public DBlurEffectWidget {
    Q_OBJECT
public:
    ToolBarWidget(QWidget* parent = 0);
    ~ToolBarWidget();

signals:
    void buttonChecked(QString shapeType);
    void expandChanged(bool expand,  QString shapeType);
    void colorChanged(QColor color);
    void saveImage();
    void shapePressed(QString tool);
    void saveBtnPressed(int index = 0);
    void saveSpecifiedPath();
    void closed();

public slots:
    bool isButtonChecked();
    void setExpand(bool expand, QString shapeType);
    void specifiedSavePath();

protected:
    void paintEvent(QPaintEvent *e);

private:
    MajToolBar* m_majToolbar;
    QLabel* m_hSeperatorLine;
    SubToolBar* m_subToolbar;

    bool  m_expanded;
};

class ToolBar : public QLabel {
    Q_OBJECT
public:
    ToolBar(QWidget* parent = 0);
    ~ToolBar();

signals:
    void heightChanged();
    void buttonChecked(QString shape);
    void updateColor(QColor color);
    void requestSaveScreenshot();
    void shapePressed(QString tool);
    void saveBtnPressed(int index = 0);
    void saveSpecifiedPath();
    void closed();

public slots:
    bool isButtonChecked();
    void setExpand(bool expand, QString shapeType);
    void showAt(QPoint pos);
    void specificedSavePath();

protected:
    void paintEvent(QPaintEvent *e);
    void enterEvent(QEvent *e);

private:
    ToolBarWidget* m_toolbarWidget;

    bool m_expanded;
};
#endif // TOOLBAR_H
