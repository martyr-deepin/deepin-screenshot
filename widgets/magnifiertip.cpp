#include "magnifiertip.h"
#include "utils.h"

MagnifierTip::MagnifierTip(QWidget *parent)
    : QLabel(parent) {
    setFixedSize(54, 54);
    setStyleSheet(getFileContent(":/resources/qss/magnifiertip.qss"));
}

MagnifierTip::~MagnifierTip() {}


void MagnifierTip::paintEvent(QPaintEvent *) {

}

void MagnifierTip::showMagnifier(QPoint pos) {
    if (!this->isVisible())
        this->show();
    this->move(pos.x() + 10 , pos.y() + 10);
}
