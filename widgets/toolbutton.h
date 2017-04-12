#ifndef TOOLBUTTON_H
#define TOOLBUTTON_H

#include <QPushButton>

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
#endif // TOOLBUTTON_H
