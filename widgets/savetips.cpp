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

#include "savetips.h"
#include "utils/baseutils.h"

#include <QDebug>

SaveTips::SaveTips(QWidget *parent)
    : QLabel(parent) {
    setStyleSheet(getFileContent(":/resources/qss/savetips.qss"));
    setTipWidth(0);
    setFixedWidth(0);
    m_startAni = new QPropertyAnimation(this, "tipWidth");
    m_stopAni = new QPropertyAnimation(this, "tipWidth");

    connect(m_startAni, &QPropertyAnimation::valueChanged, [=](QVariant value){
        emit tipWidthChanged(std::max(value.toInt(), this->width()));
        setFixedWidth(value.toInt());
    });
    connect(m_stopAni, &QPropertyAnimation::valueChanged, [=](QVariant value){
        emit tipWidthChanged(std::max(value.toInt(), this->width()));
        setFixedWidth(value.toInt());
    });
    connect(m_stopAni, &QPropertyAnimation::finished, this, [=]{
        this->clear();
        m_text = "";
    });
}

void SaveTips::setSaveText(QString text) {
    m_text = "   " + text;
   setTipWidth(stringWidth(this->font(), m_text) + 10);
//   setText(text);
}

int SaveTips::tipWidth() const {
    return  this->width();
}

void SaveTips::setTipWidth(int tipsWidth) {
    m_tipsWidth = tipsWidth;
}

SaveTips::~SaveTips() {
}

void SaveTips::startAnimation() {
    m_stopAni->stop();
    m_startAni->stop();
    m_startAni->setDuration(220);
    m_startAni->setStartValue(this->width());
    m_startAni->setEasingCurve(QEasingCurve::OutSine);
    m_startAni->setEndValue(m_tipsWidth);
    m_startAni->start();
    setText(m_text);
}

void SaveTips::endAnimation() {
    m_stopAni->setDuration(220);
    m_stopAni->setStartValue(m_tipsWidth);
    m_stopAni->setEndValue(0);
    m_stopAni->setEasingCurve(QEasingCurve::OutSine);

    m_stopAni->start();
}
