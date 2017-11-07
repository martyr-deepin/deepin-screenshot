/*
 * Copyright (C) 2017 ~ 2017 Deepin Technology Co., Ltd.
 *
 * Maintainer: Peng Hui<penghui@deepin.com>
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

#include "zoomIndicator.h"
#include "utils/baseutils.h"
#include "utils/tempfile.h"

#include <QCursor>
#include <QTextOption>
#include <QDebug>
#include <QRgb>

namespace {
const QSize BACKGROUND_SIZE = QSize(59, 59);
const int SCALE_VALUE = 4;
const int IMG_WIDTH =  12;
const int INDICATOR_WIDTH = 49;
const int CENTER_RECT_WIDTH = 12;
const int BOTTOM_RECT_HEIGHT = 14;
}
ZoomIndicator::ZoomIndicator(QWidget *parent)
    : QLabel(parent)
    , m_updatePos(true)
{
    setFixedSize(BACKGROUND_SIZE);
    setStyleSheet(getFileContent(":/resources/qss/zoomindicator.qss"));
    setAttribute(Qt::WA_TransparentForMouseEvents);

    m_centerRect = QRect((BACKGROUND_SIZE.width() - CENTER_RECT_WIDTH)/2 + 1,
                             (BACKGROUND_SIZE.width() - CENTER_RECT_WIDTH)/2 + 1,
                             CENTER_RECT_WIDTH, CENTER_RECT_WIDTH);
}

ZoomIndicator::~ZoomIndicator() {}


void ZoomIndicator::paintEvent(QPaintEvent *) {
//    using namespace utils;
    QPoint centerPos =  this->cursor().pos();
    centerPos = QPoint(std::max(centerPos.x() - this->window()->x(), 0),
                           std::max(centerPos.y(), 0));

    QPainter painter(this);
    if (m_updatePos) {
        QString fullscreenImgFile = TempFile::instance()->getFullscreenFileName();
        qreal ration = this->devicePixelRatioF();
        QImage fullscreenImg = QImage(fullscreenImgFile);
        fullscreenImg =  fullscreenImg.scaled(fullscreenImg.width()/ration,
                                              fullscreenImg.height()/ration, Qt::KeepAspectRatio);
        const QRgb centerRectRgb = fullscreenImg.pixel(centerPos);
        QPixmap zoomPix = QPixmap(fullscreenImgFile).scaled(
            fullscreenImg.width(), fullscreenImg.height()).copy(
            centerPos.x() - IMG_WIDTH/2, centerPos.y() - IMG_WIDTH/2, IMG_WIDTH, IMG_WIDTH);

        zoomPix = zoomPix.scaled(QSize(INDICATOR_WIDTH,  INDICATOR_WIDTH),
                                 Qt::KeepAspectRatio);
        m_lastPic = zoomPix;

        painter.drawPixmap(QRect(5, 5, INDICATOR_WIDTH, INDICATOR_WIDTH), zoomPix);


        painter.drawPixmap(m_centerRect, QPixmap(":/resources/images/action/center_rect.png"));
        m_lastCenterPosBrush = QBrush(QColor(qRed(centerRectRgb),
                                             qGreen(centerRectRgb), qBlue(centerRectRgb)));
        painter.fillRect(QRect(INDICATOR_WIDTH/2 + 2, INDICATOR_WIDTH/2 + 2,
                               CENTER_RECT_WIDTH - 4, CENTER_RECT_WIDTH - 4), m_lastCenterPosBrush);

        painter.fillRect(QRect(5, INDICATOR_WIDTH - 9, INDICATOR_WIDTH, BOTTOM_RECT_HEIGHT),
                         QBrush(QColor(0, 0, 0, 125)));
        QFont posFont;
        posFont.setPixelSize(9);
        painter.setFont(posFont);
        painter.setPen(QColor(Qt::white));
        QTextOption posTextOption;
        posTextOption.setAlignment(Qt::AlignHCenter | Qt::AlignTop);
        painter.drawText(QRectF(5, INDICATOR_WIDTH - 10, INDICATOR_WIDTH, INDICATOR_WIDTH),
                         QString("%1, %2").arg(centerPos.x()).arg(centerPos.y()), posTextOption);
        m_updatePos = false;
    } else {
        painter.drawPixmap(QRect(5, 5, INDICATOR_WIDTH, INDICATOR_WIDTH), m_lastPic);
        painter.drawPixmap(m_centerRect, QPixmap(":/resources/images/action/center_rect.png"));

        painter.fillRect(QRect(INDICATOR_WIDTH/2 + 2, INDICATOR_WIDTH/2 + 2,
                               CENTER_RECT_WIDTH - 4, CENTER_RECT_WIDTH - 4), m_lastCenterPosBrush);
    }
}

void ZoomIndicator::updatePaintEvent() {
    m_updatePos = true;
    update();
}

void ZoomIndicator::showMagnifier(QPoint pos) {
    this->show();

    this->move(pos);
}
