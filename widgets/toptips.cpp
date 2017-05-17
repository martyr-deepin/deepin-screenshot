#include "toptips.h"

#include "utils/baseutils.h"
#include <QDebug>

TopTips::TopTips(QWidget *parent)
    : QLabel(parent) {
    this->setStyleSheet(" TopTips { background-color: transparent;"
                        "border-image: url(:/resources/images/action/sizetip.png) stretch;"
                        "color: white;}");
}

void TopTips::setContent(QString widthXHeight) {
    int minWidth = stringWidth(this->font(),
                               widthXHeight);

    this->setMinimumWidth(minWidth + 30);
    setText(widthXHeight);
    setAlignment(Qt::AlignCenter);
}

void TopTips::updateTips(QPoint pos, QString text) {
    if (!this->isVisible())
        this->show();

    QPoint startPoint = pos;

    startPoint.setX(pos.x() + 3);

    if (pos.y() > this->height()) {
        startPoint.setY(pos.y() - this->height() - 5);
    } else {
        startPoint.setY(pos.y() + 5);
    }

    this->move(startPoint);
    setContent(text);
 }

TopTips::~TopTips() {}
