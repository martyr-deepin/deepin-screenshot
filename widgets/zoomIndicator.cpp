#include "zoomIndicator.h"
#include "utils.h"

ZoomIndicator::ZoomIndicator(QWidget *parent)
    : QLabel(parent) {
    setFixedSize(54, 54);
    setStyleSheet(getFileContent(":/resources/qss/zoomindicator.qss"));
}

ZoomIndicator::~ZoomIndicator() {}


void ZoomIndicator::paintEvent(QPaintEvent *) {

}

void ZoomIndicator::showMagnifier(QPoint pos) {
    if (!this->isVisible())
        this->show();
    this->move(pos.x() + 10 , pos.y() + 10);
}
