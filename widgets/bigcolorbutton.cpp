#include "bigcolorbutton.h"
#include <QDebug>

const int COLOR_RADIUS = 4;

BigColorButton::BigColorButton(QWidget *parent)
    : QPushButton(parent),
      m_color(QColor(Qt::red)),
      m_isHover(false),
      m_isChecked(false)
{
    setFixedSize(21, 21);
    setCheckable(true);

    connect(this, &QPushButton::clicked, this,
            &BigColorButton::setCheckedStatus);
}

BigColorButton::~BigColorButton() {

}

void BigColorButton::paintEvent(QPaintEvent *) {
    QPainter painter(this);
    painter.setRenderHints(QPainter::Antialiasing);
    painter.setPen(Qt::transparent);

    painter.setBrush(QBrush(QColor(0, 0, 0, 80)));
    if (m_isHover) {
        painter.drawRoundedRect(rect(), 4, 4);
    }

    painter.setBrush(QBrush(QColor(m_color)));
    painter.drawEllipse(QPoint(11, 10),
                        COLOR_RADIUS, COLOR_RADIUS);

    if (m_isChecked) {
        painter.drawPixmap(rect(), QPixmap(
                               ":/resources/images/action/colors_checked.png"));
    } else if (m_isHover && !m_isChecked) {
        painter.drawPixmap(rect(), QPixmap(
                               ":/resources/images/action/colors_hover.png"));
    } else {
         painter.drawPixmap(rect(), QPixmap(
                                ":/resources/images/action/colors_normal.png"));
    }


}

void BigColorButton::setColor(QColor color) {
    m_color = color;
    update();
}

void BigColorButton::setCheckedStatus(bool checked) {
    if (m_isChecked != checked) {
        m_isChecked = checked;
        update();
    }
}

void BigColorButton::enterEvent(QEvent *) {
    if (!m_isHover) {
        m_isHover = true;
        update();
    }
}

void BigColorButton::leaveEvent(QEvent *) {
    if (m_isHover) {
        m_isHover = false;
        update();
    }
}
