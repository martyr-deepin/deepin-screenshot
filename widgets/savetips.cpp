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
