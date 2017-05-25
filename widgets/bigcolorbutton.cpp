#include "bigcolorbutton.h"

#include "utils/baseutils.h"
#include "utils/configsettings.h"

#include <QDebug>

const qreal COLOR_RADIUS = 4;

BigColorButton::BigColorButton(QWidget *parent)
    : QPushButton(parent),
      m_color(QColor(Qt::red)),
      m_isHover(false),
      m_isChecked(false)
{
    setFixedSize(22, 22);
    setCheckable(true);
    int colIndex = ConfigSettings::instance()->value(
                              "common", "color_index").toInt();
    m_color = colorIndexOf(colIndex);

    connect(this, &QPushButton::clicked, this,
            &BigColorButton::setCheckedStatus);
}

BigColorButton::~BigColorButton() {

}

void BigColorButton::paintEvent(QPaintEvent *) {
    QPainter painter(this);
    painter.setRenderHints(QPainter::Antialiasing);
    painter.setPen(Qt::transparent);

    painter.setBrush(QBrush(QColor(0, 0, 0, 20.4)));
    if (m_isHover) {
        painter.drawRoundedRect(rect(), 4, 4);
    }

    painter.setBrush(QBrush(QColor(m_color)));
    painter.drawEllipse(QPointF(11, 11),
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
    int colorNum = colorIndex(color);
    ConfigSettings::instance()->setValue("common", "color_index", colorNum);
    update();
}

void BigColorButton::setColorIndex() {
   int colorNum = ConfigSettings::instance()->value("common", "color_index").toInt();
    m_color = colorIndexOf(colorNum);
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
