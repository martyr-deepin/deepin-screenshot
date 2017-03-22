#ifndef TOOLBAR_H
#define TOOLBAR_H

#include <QLabel>
#include <QHBoxLayout>

class ToolBar : public QLabel {
    Q_OBJECT


public:
    ToolBar(QWidget* parent = 0);
    ~ToolBar();

    void initWidgets();
    void showToolBar(QPoint pos);
protected:
//    void enterEvent(QEvent *event);
//    void leaveEvent(QEvent *event);
//    void paintEvent(QPaintEvent *event);
private:

    QHBoxLayout* m_layout;
//    QHBoxLayout* m_expandLayout;


};

#endif // TOOLBAR_H
