#ifndef TOOLBAR_H
#define TOOLBAR_H

#include <QLabel>
#include <QPushButton>
#include <QHBoxLayout>

class ToolButton : public QPushButton {
    Q_OBJECT
public:
    ToolButton(QWidget* parent = 0) {
        Q_UNUSED(parent);
        setFixedSize(22, 22);
        setCheckable(true);
    }
    ~ToolButton(){}
};

class ToolBar : public QLabel {
    Q_OBJECT


public:
    ToolBar(QWidget* parent = 0);
    ~ToolBar();

    void initWidgets();
    void showToolBar(QPoint pos);
    void setExpandMode(bool expand, QString type = "");
protected:
//    void enterEvent(QEvent *event);
//    void leaveEvent(QEvent *event);
//    void paintEvent(QPaintEvent *event);
private:

    QLabel* m_topLabel;
    QLabel* m_separator;
    QLabel* m_bottomLabel;
    QVBoxLayout* m_layout;
    QHBoxLayout* m_baseLayout;
    QHBoxLayout* m_expandLayout;


};

#endif // TOOLBAR_H
