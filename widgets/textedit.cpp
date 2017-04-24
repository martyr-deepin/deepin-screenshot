#include "textedit.h"

#include <QDebug>
#include <QPen>
#include <QScrollBar>
#include <QFontMetricsF>

TextEdit::TextEdit(int index, QWidget *parent)
    : QPlainTextEdit(parent) {
    m_index = index;
     setLineWrapMode(QPlainTextEdit::NoWrap);
    setContentsMargins(0, 0, 0, 0);
    setAutoFillBackground(true);

    QTextCursor cursor = textCursor();
    QTextBlockFormat textBlockFormat = cursor.blockFormat();
    textBlockFormat.setAlignment(Qt::AlignLeft);
    cursor.mergeBlockFormat(textBlockFormat);

    setStyleSheet("background-color:  transparent; color: white; border: none;");
    QFontMetricsF fontMetric(this->document()->defaultFont());
    QSizeF originSize = QSizeF(fontMetric.boundingRect(this->toPlainText()).width() + 10, 30);
    this->resize(originSize.width(), originSize.height());

    connect(this->document(), &QTextDocument::contentsChange, [=]{
        QSizeF docSize =  fontMetric.size(0, this->toPlainText());

        this->setMinimumSize(docSize.width() + 10, docSize.height() + 10);
        this->resize(docSize.width() + 10, docSize.height() + 10);
        emit  repaintTextRect(this,  docSize.width() + 10, docSize.height() + 10);
    });
}

int TextEdit::getIndex() {
    return m_index;
}

void TextEdit::setColor(QColor c) {
//    setTextColor(c);
}

TextEdit::~TextEdit() {}
