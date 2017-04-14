#include "colorbutton.h"

#include <QPainter>
#include <QDebug>

const QSize BUTTON_SIZE = QSize(13, 13);
const int  ELLIPSE_MARGIN = 1;
ColorButton::ColorButton(QColor bgColor, QWidget *parent)
    : QPushButton(parent) {
    setFixedSize(BUTTON_SIZE);
    setCheckable(true);
    m_bgColor = bgColor;
    m_isChecked = false;
    update();

    connect(this, &ColorButton::clicked, this, &ColorButton::setColorBtnChecked);
}

void ColorButton::setColorBtnChecked() {
    m_isChecked = !m_isChecked;
    setChecked(m_isChecked);
    update();
}

void ColorButton::paintEvent(QPaintEvent *) {
    QPainter painter(this);
    painter.setPen(QPen(QColor(Qt::transparent)));
    painter.setRenderHints(QPainter::Antialiasing | QPainter::SmoothPixmapTransform);
    painter.setBrush(QBrush(QColor(m_bgColor)));
    if (!this->isChecked()) {
        painter.drawRect(this->rect());
    } else {
        QRect ellipseRect = this->rect();
        painter.drawEllipse(QRect(ellipseRect.x() + 2, ellipseRect.y() + 2,
                                  ellipseRect.width() - 4, ellipseRect.height() - 4));

        QPen pen;
        pen.setWidth(1);
        pen.setColor(Qt::white);
        painter.setPen(pen);
        painter.setBrush(QBrush(QColor(Qt::transparent)));
        painter.drawEllipse(QRect(ellipseRect.x() + 1, ellipseRect.y() + 1,
                                  ellipseRect.width() - 2, ellipseRect.height() - 2));
        emit updatePaintColor(m_bgColor);
    }
}

ColorButton::~ColorButton() {}
