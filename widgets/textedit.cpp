#include "textedit.h"

#include <QDebug>
#include <QPen>
#include <QScrollBar>
#include <QPixmap>
#include <QFontMetricsF>
#include <QApplication>

const QSize CURSOR_SIZE = QSize(5, 20);

TextEdit::TextEdit(int index, QWidget *parent)
    : QTextEdit(parent),
      m_textColor(Qt::red)
{
    m_index = index;
    setLineWrapMode(QTextEdit::NoWrap);

    QTextCursor cursor = textCursor();
    QTextBlockFormat textBlockFormat = cursor.blockFormat();
    textBlockFormat.setAlignment(Qt::AlignLeft);
    cursor.mergeBlockFormat(textBlockFormat);

    setStyleSheet("background-color:  transparent; color: white; border: none;");
    QFontMetricsF fontMetric(this->document()->defaultFont());
    QSizeF originSize = QSizeF(fontMetric.boundingRect(this->toPlainText()).width() + 10, 30);
    this->resize(originSize.width(), originSize.height());
    updateCursor();
    installEventFilter(this);

    setHorizontalScrollBarPolicy(Qt::ScrollBarAlwaysOff);
    setVerticalScrollBarPolicy(Qt::ScrollBarAlwaysOff);

    connect(this->document(), &QTextDocument::contentsChange, [=]{
        QSizeF docSize =  fontMetric.size(0, this->toPlainText());

        this->setMinimumSize(docSize.width() + 10, docSize.height() + 10);
        this->resize(docSize.width() + 10, docSize.height() + 10);
        emit  repaintTextRect(this,  QRectF(this->x(), this->y(), docSize.width() + 10, docSize.height() + 10));
    });
}

int TextEdit::getIndex() {
    return m_index;
}

void TextEdit::setColor(QColor c) {
    m_textColor = c;
}

void TextEdit::updateCursor() {
    setTextColor(Qt::green);
}

void TextEdit::setCursorVisible(bool visible) {
    if (visible) {
        setCursorWidth(0);
    } else {
        setCursorWidth(2);
    }
}

void TextEdit::keepReadOnlyStatus() {

}

bool TextEdit::eventFilter(QObject *watched, QEvent *event) {
    Q_UNUSED(watched);
    if (event->type() == QEvent::Enter) {
        qApp->setOverrideCursor(Qt::ClosedHandCursor);
    }

    if (event->type() == QKeyEvent::KeyPress) {
        QKeyEvent* keyEvent = static_cast<QKeyEvent*>(event);
        if (keyEvent->key() == Qt::Key_Escape) {
            qApp->quit();
        }
    }

    return false;
}

void TextEdit::mousePressEvent(QMouseEvent *e) {
    if (this->isReadOnly()) {
        setMouseTracking(false);
        setCursorVisible(false);
        return;
    }

    m_pressPoint = e->pos();
    QTextEdit::mousePressEvent(e);
}

void TextEdit::mouseMoveEvent(QMouseEvent *e) {
    QPoint movePos = e->pos();
    this->move(this->x() + movePos.x() - m_pressPoint.x(),
                         this->y() + movePos.y() - m_pressPoint.y());

    emit  repaintTextRect(this,  QRectF(this->x(), this->y(),
                                           this->width(),  this->height()));
}

void TextEdit::mouseReleaseEvent(QMouseEvent *e) {
    if (this->isReadOnly()) {
        setMouseTracking(false);
        return;
    }

    QTextEdit::mouseReleaseEvent(e);
}

void TextEdit::enterEvent(QEnterEvent *e) {
    if (this->isReadOnly()) {
        setCursorVisible(false);
        this->selectAll();
        qApp->setOverrideCursor(Qt::ClosedHandCursor);
    } else {
        qApp->setOverrideCursor(Qt::ArrowCursor);
    }

    QTextEdit::enterEvent(e);
}

TextEdit::~TextEdit() {}
