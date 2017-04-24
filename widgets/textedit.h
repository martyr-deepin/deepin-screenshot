#ifndef TEXTEDIT_H
#define TEXTEDIT_H

#include <QWidget>
#include <QPlainTextEdit>
#include <QPainter>
#include <QKeyEvent>

class TextEdit : public QPlainTextEdit {
    Q_OBJECT
public:
    TextEdit(int index, QWidget* parent);
    ~TextEdit();

    void setColor(QColor c);
     int getIndex();

signals:
     void repaintTextRect(TextEdit* edit, int contentWidth, int contentHeight);

protected:
     void keyPressEvent();

private:
     int m_index;
     QPainter* m_painter;
};

#endif // TEXTEDIT_H
