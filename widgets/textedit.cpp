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
    this->setFont(textFont);

    QTextCursor cursor = textCursor();
    QTextBlockFormat textBlockFormat = cursor.blockFormat();
    textBlockFormat.setAlignment(Qt::AlignLeft);
    cursor.mergeBlockFormat(textBlockFormat);


    QFontMetricsF fontMetric(this->document()->defaultFont());
    QSizeF originSize = QSizeF(fontMetric.boundingRect(
                                   this->toPlainText()).width() + 10, 30);
    this->resize(originSize.width(), originSize.height());
    this->viewport()->installEventFilter(this);

    setHorizontalScrollBarPolicy(Qt::ScrollBarAlwaysOff);
    setVerticalScrollBarPolicy(Qt::ScrollBarAlwaysOff);

    connect(this->document(), &QTextDocument::contentsChange, [=]{
        QSizeF docSize =  fontMetric.size(0, this->toPlainText());
        this->setMinimumSize(docSize.width() + TEXT_MARGIN, docSize.height() + TEXT_MARGIN);
        this->resize(docSize.width() + TEXT_MARGIN, docSize.height() + TEXT_MARGIN);
        emit  repaintTextRect(this,  QRectF(this->x(), this->y(),
                                                docSize.width() + TEXT_MARGIN, docSize.height() + TEXT_MARGIN));
    });
}

int TextEdit::getIndex() {
    return m_index;
}

void TextEdit::setColor(QColor c) {
    m_textColor = c;
    setStyleSheet(QString("TextEdit {background-color:  transparent;"
                                            " color: %1; border: none;}").arg(m_textColor.name()));
}

void TextEdit::updateCursor() {
//    setTextColor(Qt::green);
}

void TextEdit::setCursorVisible(bool visible) {
    if (visible) {
        setCursorWidth(1);
    } else {
        setCursorWidth(0);
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

    if (event->type() == QMouseEvent::MouseButtonDblClick) {
        this->setReadOnly(false);
        this->setCursorVisible(true);
        this->grabKeyboard();
        emit backToEditing();
    }

    return false;
}

void TextEdit::mousePressEvent(QMouseEvent *e) {
    m_isPressed = true;
    m_pressPoint = QPointF(mapToGlobal(e->pos()));

    QPlainTextEdit::mousePressEvent(e);
}

void TextEdit::mouseMoveEvent(QMouseEvent *e) {
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

void TextEdit::mouseReleaseEvent(QMouseEvent *e) {
    m_isPressed = false;
    if (this->isReadOnly()) {
        setMouseTracking(false);
        return;
    }

    QPlainTextEdit::mouseReleaseEvent(e);
}

//void TextEdit::enterEvent(QEnterEvent *e) {
//    if (this->isReadOnly()) {
//        setCursorVisible(false);
//        this->selectAll();
//        qApp->setOverrideCursor(Qt::ClosedHandCursor);
//    } else {
//        qApp->setOverrideCursor(Qt::ArrowCursor);
//    }

//    QPlainTextEdit::enterEvent(e);
//}

TextEdit::~TextEdit() {}
