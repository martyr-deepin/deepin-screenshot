#include "savetips.h"
#include "utils/baseutils.h"

#include <QDebug>

SaveTips::SaveTips(QWidget *parent)
    : QLabel(parent) {
    setStyleSheet(getFileContent(":/resources/qss/savetips.qss"));
    setTipWidth(0);
    m_animation = new QPropertyAnimation(this, "tipWidth");

    connect(m_animation, &QPropertyAnimation::valueChanged, [=](QVariant value){
        emit tipWidthChanged(value.toInt());
    });
}

void SaveTips::setSaveText(QString text) {
   setTipWidth(stringWidth(this->font(), text) + 10);
   setFixedWidth(m_tipsWidth);
   setText(text);
}

int SaveTips::tipWidth() const {
    return m_tipsWidth;
}

void SaveTips::setTipWidth(int tipsWidth) {
    m_tipsWidth = tipsWidth;
    setFixedWidth(m_tipsWidth);
}

SaveTips::~SaveTips() {
}

void SaveTips::startAnimation() {
    m_animation->stop();
    m_animation->setDuration(150);
    m_animation->setStartValue(0);
    m_animation->setEndValue(m_tipsWidth);
    m_animation->setEasingCurve(QEasingCurve::OutSine);
    m_animation->start();
}

void SaveTips::endAnimation() {
    m_animation->stop();
    m_animation->setDuration(150);
    m_animation->setStartValue(m_tipsWidth);
    m_animation->setEndValue(0);
    m_animation->setEasingCurve(QEasingCurve::OutSine);

    m_animation->start();
}
