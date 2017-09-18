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

#ifndef SAVEBUTTON_H
#define SAVEBUTTON_H

#include "toolbutton.h"

class SaveButton : public QPushButton {
    Q_OBJECT
public:
    SaveButton(QWidget* parent = 0);
    ~SaveButton();

signals:
    void saveAction();
    void expandSaveOption(bool expand);

private:
    ToolButton* m_saveBtn;
    ToolButton* m_listBtn;
};

#endif // SAVEBUTTON_H
