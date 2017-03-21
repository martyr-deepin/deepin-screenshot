#include "toptips.h"

#include "utils.h"
#include <QDebug>

TopTips::TopTips(QWidget *parent)
    : QLabel(parent) {
    setStyleSheet("color: white;"
                  "background-color: rgba(0, 0, 0, 100); "
                  "border: 1px solid rgba(255, 255, 255, 100);"
                  "border-radius: 4px;");
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
    if (pos.x() > this->width()) {
        startPoint.setX(pos.x() - this->width());
    }

    if (pos.y() > this->height()) {
        startPoint.setY(pos.y() - this->height());
    }

    this->move(startPoint);
    setContent(text);
 }

TopTips::~TopTips() {}
