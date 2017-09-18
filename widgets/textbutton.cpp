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

#include "textbutton.h"

#include "utils/baseutils.h"
#include "utils/configsettings.h"

TextButton::TextButton(int num, QWidget *parent)
    : QPushButton(parent) {
    setObjectName("TextButton");
    m_fontsize = num;
    setText(QString("%1").arg(m_fontsize));

    setFixedSize(24, 26);
    setCheckable(true);

    connect(this, &TextButton::clicked, this, [=]{
        if (this->isChecked()) {
            ConfigSettings::instance()->setValue("text", "fontsize", m_fontsize);
        }
    });
}

TextButton::~TextButton() {}
