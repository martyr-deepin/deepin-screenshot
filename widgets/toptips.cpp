#include "toptips.h"

#include "utils/baseutils.h"
#include <QDebug>

TopTips::TopTips(QWidget *parent)
    : QLabel(parent) {
    setFixedSize(75, 20);
    this->setStyleSheet(" TopTips { background-color: transparent;"
                        "border-image: url(:/resources/images/action/sizetip.png)  no-repeat;"
                        "color: white;"
                        "font-size: 12px;}");
}

void TopTips::setContent(QString widthXHeight) {
    setText(widthXHeight);
    setAlignment(Qt::AlignCenter);
}

void TopTips::updateTips(QPoint pos, QString text) {
    if (!this->isVisible())
        this->show();

    QPoint startPoint = pos;

    startPoint.setX(pos.x());

    if (pos.y() > this->height()) {
        startPoint.setY(pos.y() - this->height() - 3);
    } else {
        startPoint.setY(pos.y() + 3);
    }

    this->move(startPoint);
    setContent(text);
 }

TopTips::~TopTips() {}
