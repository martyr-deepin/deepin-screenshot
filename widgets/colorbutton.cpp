#include "colorbutton.h"

#include <QPainter>
#include <QDebug>

const QSize BUTTON_SIZE = QSize(16, 16);
const int  ELLIPSE_MARGIN = 1;
ColorButton::ColorButton(QColor bgColor, QWidget *parent)
    : QPushButton(parent) {
    setFixedSize(BUTTON_SIZE);
    setCheckable(true);
    m_bgColor = bgColor;

    connect(this, &ColorButton::clicked, this, &ColorButton::setColorBtnChecked);
}

void ColorButton::setColorBtnChecked() {
    update();
    if (this->isChecked()) {
        qDebug() << "updatePaintColor:" << m_bgColor;
        emit updatePaintColor(m_bgColor);
    }
}

QColor ColorButton::getColor()
{
    return m_bgColor;
}

//void ColorButton::paintEvent(QPaintEvent *) {
//    QPainter painter(this);
//    painter.setPen(QPen(QColor(Qt::transparent)));
//    painter.setRenderHints(QPainter::Antialiasing| QPainter::SmoothPixmapTransform);
//    painter.setBrush(QBrush(QColor(m_bgColor)));
//    if (!this->isChecked()) {
//        painter.drawRect(QRect(2, 2, this->width() - 4, this->height() - 4));
//        emit updatePaintColor(m_bgColor);
//    } else {
//        painter.drawEllipse(QRect(2, 2, this->width() - 4, this->height() - 4));

//        QPen pen;
//        pen.setWidth(1);
//        pen.setColor(Qt::red);
//        painter.setPen(pen);
//        painter.setBrush(QBrush(QColor(Qt::transparent)));
//        painter.drawEllipse(QRect(1, 1, this->width() - 1, this->height() - 1));
//        emit updatePaintColor(m_bgColor);
//    }
//}

ColorButton::~ColorButton() {}
