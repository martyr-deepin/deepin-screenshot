#ifndef TOOLBAR_H
#define TOOLBAR_H

#include <QLabel>

#include "majtoolbar.h"
#include "subtoolbar.h"

class ToolBar : public QLabel {
    Q_OBJECT
public:
    ToolBar(QWidget* parent = 0);
    ~ToolBar();

signals:
    void buttonChecked(QString shapeType);
    void updateColor(QColor color);

public slots:
    bool isButtonChecked();
    void setExpand(bool expand, QString shapeType);
    void showAt(QPoint pos);

private:
    MajToolBar* m_majToolbar;
    QLabel* m_hSeperatorLine;
    SubToolBar* m_subToolbar;

    bool m_isChecked;
};

#endif // TOOLBAR_H
