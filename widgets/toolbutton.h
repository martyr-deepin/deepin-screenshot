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

#ifndef TOOLBUTTON_H
#define TOOLBUTTON_H

#include <QPushButton>
#include <QApplication>

class ToolButton : public QPushButton {
    Q_OBJECT
public:
    ToolButton(QWidget* parent = 0) {
        Q_UNUSED(parent);
        setFixedSize(32, 26);
        setCheckable(true);
        m_tips = "";
    }
    ~ToolButton(){}

public slots:
    void setTips(QString tips) {
        m_tips = tips;
    }

    QString getTips() {
        return m_tips;
    }

signals:
    void onEnter();
    void onExist();

protected:
    void enterEvent(QEvent* e) {
        emit onEnter();
        QPushButton::enterEvent(e);
    }

    void leaveEvent(QEvent* e) {
        emit onExist();
        QPushButton::leaveEvent(e);
    }

private:
    QString m_tips;

};
#endif // TOOLBUTTON_H
