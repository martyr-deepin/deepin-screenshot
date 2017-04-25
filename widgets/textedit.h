#ifndef TEXTEDIT_H
#define TEXTEDIT_H

#include <QWidget>
#include <QTextEdit>
#include <QPainter>
#include <QMouseEvent>

class TextEdit : public QTextEdit {
    Q_OBJECT
public:
    TextEdit(int index, QWidget* parent);
    ~TextEdit();

    void setColor(QColor c);
     int getIndex();
    void updateCursor();
    void setCursorVisible(bool visible);
    void keepReadOnlyStatus();

signals:
     void repaintTextRect(TextEdit* edit,  QRectF newPositiRect);

protected:
    void mousePressEvent(QMouseEvent* e);
    void enterEvent(QEnterEvent* e);
    void mouseMoveEvent(QMouseEvent* e);
    void mouseReleaseEvent(QMouseEvent* e);
    bool eventFilter(QObject* watched, QEvent* event);

private:
     int m_index;
     QColor m_textColor;
     QPainter* m_painter;

     QPointF m_pressPoint;
};

#endif // TEXTEDIT_H
