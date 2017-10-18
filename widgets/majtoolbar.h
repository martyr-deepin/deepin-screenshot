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

#ifndef MAJTOOLBAR_H
#define MAJTOOLBAR_H

#include <QLabel>
#include <QPushButton>
#include <QHBoxLayout>
#include <QStackedWidget>

class MajToolBar : public QLabel
{
    Q_OBJECT
public:
    MajToolBar(QWidget* parent = 0);
    ~MajToolBar();

signals:
    void buttonChecked(bool checked, QString type);
    void mainColorChanged(QColor currentColor);
    void saveImage();
    void showSaveTooltip(QString tooltips);
    void hideSaveTooltip();
    void shapePressed(QString shape);
    void specificedSavePath();
    void saveSpecificedPath();
    void closed();

public slots:
    void initWidgets();
    bool isButtonChecked();

private:
    QHBoxLayout* m_baseLayout;

    bool m_isChecked;
    bool m_listBtnChecked;
    QString m_currentShape;
};

#endif // MAJTOOLBAR_H
