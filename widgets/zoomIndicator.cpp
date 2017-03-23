#include "zoomIndicator.h"
#include "utils.h"

#include <QCursor>
#include <QDebug>
#include <QRgb>

namespace {
const QString TMPFILE_URL = "/tmp/deepin-screenshot.png";
const QSize BACKGROUND_SIZE = QSize(59, 59);
const int SCALE_VALUE = 4;
const int IMG_WIDTH =  12;
const int INDICATOR_WIDTH = 49;
const int CENTER_RECT_WIDTH = 12;
}
ZoomIndicator::ZoomIndicator(QWidget *parent)
    : QLabel(parent) {
    setFixedSize(BACKGROUND_SIZE);
    setStyleSheet(getFileContent(":/resources/qss/zoomindicator.qss"));
}

ZoomIndicator::~ZoomIndicator() {}


void ZoomIndicator::paintEvent(QPaintEvent *) {
    QPoint centerPos = this->cursor().pos();
    QRgb centerRectRgb = QImage(TMPFILE_URL).pixel(centerPos);
    QPixmap zoomPix = QPixmap(TMPFILE_URL).copy(centerPos.x() - IMG_WIDTH/2,
            centerPos.y() - IMG_WIDTH/2, IMG_WIDTH, IMG_WIDTH);

    zoomPix = zoomPix.scaled(QSize(INDICATOR_WIDTH,  INDICATOR_WIDTH),
                             Qt::KeepAspectRatio);

    QPainter painter(this);
    painter.drawPixmap(QRect(5, 5, INDICATOR_WIDTH, INDICATOR_WIDTH), zoomPix);

    QRect centerRect = QRect((BACKGROUND_SIZE.width() - CENTER_RECT_WIDTH)/2 + 1,
                             (BACKGROUND_SIZE.width() - CENTER_RECT_WIDTH)/2 + 1,
                             CENTER_RECT_WIDTH, CENTER_RECT_WIDTH);
    painter.drawPixmap(centerRect, QPixmap(":/resources/images/action/center_rect.png"));
    painter.fillRect(QRect(INDICATOR_WIDTH/2 + 2, INDICATOR_WIDTH/2 + 2,
            CENTER_RECT_WIDTH - 4, CENTER_RECT_WIDTH - 4), QBrush(QColor(qRed(centerRectRgb),
             qGreen(centerRectRgb), qBlue(centerRectRgb))));
}

void ZoomIndicator::showMagnifier(QPoint pos) {
    if (!this->isVisible())
        this->show();

    QPoint movePos = cursor().pos();
    this->move(movePos.x() + 10 , movePos.y() + 10);
    update();
}
