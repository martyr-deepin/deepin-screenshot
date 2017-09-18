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

#include "textedit.h"

#include <QDebug>
#include <QPen>
#include <QScrollBar>
#include <QPixmap>
#include <QFontMetricsF>
#include <QApplication>

#include "utils/configsettings.h"
#include "utils/baseutils.h"

const QSize CURSOR_SIZE = QSize(5, 20);
const int TEXT_MARGIN = 10;

TextEdit::TextEdit(int index, QWidget *parent)
    : QPlainTextEdit(parent),
      m_textColor(Qt::red)
{
    m_index = index;
    setLineWrapMode(QPlainTextEdit::NoWrap);
    setContextMenuPolicy(Qt::NoContextMenu);

    int defaultColorIndex = ConfigSettings::instance()->value(
                                               "text", "color_index").toInt();
    QColor defaultColor = colorIndexOf(defaultColorIndex);
    setColor(defaultColor);
    QFont textFont;
    int defaultFontSize = ConfigSettings::instance()->value("text", "fontsize").toInt();
    textFont.setPixelSize(defaultFontSize);
    this->document()->setDefaultFont(textFont);

    QTextCursor cursor = textCursor();
    QTextBlockFormat textBlockFormat = cursor.blockFormat();
    textBlockFormat.setAlignment(Qt::AlignLeft);
    cursor.mergeBlockFormat(textBlockFormat);

     QFontMetricsF m_fontMetric = QFontMetricsF(this->document()->defaultFont());
    QSizeF originSize = QSizeF(m_fontMetric.boundingRect(
                                   "d").width()  + TEXT_MARGIN,  m_fontMetric.boundingRect(
                                   "d").height() + TEXT_MARGIN);
    this->resize(originSize.width(), originSize.height());
    setHorizontalScrollBarPolicy(Qt::ScrollBarAlwaysOff);
    setVerticalScrollBarPolicy(Qt::ScrollBarAlwaysOff);

    connect(this->document(), &QTextDocument::contentsChange, this,  [=]{
        updateContentSize(this->toPlainText());
    });
}

int TextEdit::getIndex()
{
    return m_index;
}

void TextEdit::setColor(QColor c)
{
    m_textColor = c;
    setStyleSheet(QString("TextEdit {background-color:  transparent;"
                                            " color: %1; border: none;}").arg(m_textColor.name()));
    this->updateGeometry();
}

void TextEdit::setFontSize(int fontsize)
{
    QFont font;
    font.setPixelSize(fontsize);
    this->document()->setDefaultFont(font);
    this->updateGeometry();

    updateContentSize(this->toPlainText());
}

void TextEdit::inputMethodEvent(QInputMethodEvent *e)
{
    QPlainTextEdit::inputMethodEvent(e);

    QString virtualStr = this->toPlainText() + e->preeditString();
    updateContentSize(virtualStr);
}

void TextEdit::updateContentSize(QString content)
{
    QFontMetricsF fontMetric = QFontMetricsF(this->document()->defaultFont());
    QSizeF docSize =  fontMetric.size(0,  content);
    this->setMinimumSize(docSize.width() + TEXT_MARGIN, docSize.height() + TEXT_MARGIN);
    this->resize(docSize.width() + TEXT_MARGIN, docSize.height() + TEXT_MARGIN);
    emit  repaintTextRect(this,  QRectF(this->x(), this->y(),
                                            docSize.width() + TEXT_MARGIN, docSize.height() + TEXT_MARGIN));
}

void TextEdit::updateCursor()
{
//    setTextColor(Qt::green);
}

void TextEdit::setCursorVisible(bool visible)
{
    if (visible) {
        setCursorWidth(1);
    } else {
        setCursorWidth(0);
    }
}

void TextEdit::keepReadOnlyStatus()
{
}

void TextEdit::mousePressEvent(QMouseEvent *e)
{
    qDebug() << "TextEdit mousePressEvent" << e->pos();
    if (!this->isReadOnly()) {
        QPlainTextEdit::mousePressEvent(e);
        return;
    }

    if (e->button() == Qt::LeftButton) {
        m_isPressed = true;
        m_pressPoint = QPointF(mapToGlobal(e->pos()));

        if (this->isReadOnly()) {
            emit textEditSelected(getIndex());
        }
    }

    QPlainTextEdit::mousePressEvent(e);
}

void TextEdit::mouseMoveEvent(QMouseEvent *e)
{
    qApp->setOverrideCursor(Qt::ClosedHandCursor);
    QPointF posOrigin = QPointF(mapToGlobal(e->pos()));
    QPointF movePos = QPointF(posOrigin.x(), posOrigin.y());

    if (m_isPressed && movePos != m_pressPoint) {
        this->move(this->x() + movePos.x() - m_pressPoint.x(),
                   this->y() + movePos.y() - m_pressPoint.y());

        emit  repaintTextRect(this,  QRectF(qreal(this->x()), qreal(this->y()),
                                                                        this->width(),  this->height()));
        m_pressPoint = movePos;
    }


    QPlainTextEdit::mouseMoveEvent(e);
}

void TextEdit::mouseReleaseEvent(QMouseEvent *e)
{
    m_isPressed = false;
    if (this->isReadOnly()) {
        setMouseTracking(false);
        return;
    }

    QPlainTextEdit::mouseReleaseEvent(e);
}

void TextEdit::mouseDoubleClickEvent(QMouseEvent *e)
{
    this->setReadOnly(false);
    this->setCursorVisible(true);
    emit backToEditing();
    QPlainTextEdit::mouseDoubleClickEvent(e);
}

void TextEdit::keyPressEvent(QKeyEvent *e)
{
    QPlainTextEdit::keyPressEvent(e);
    if (e->key() == Qt::Key_Escape && !this->isReadOnly()) {
        this->setReadOnly(true);
    }
}

TextEdit::~TextEdit() {}
