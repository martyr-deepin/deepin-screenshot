#ifndef TEXTBUTTON_H
#define TEXTBUTTON_H

#include <QPushButton>

class TextButton : public QPushButton {
    Q_OBJECT
public:
    TextButton(int num, QWidget* parent = 0);
    ~TextButton();

private:
    int m_fontsize;
};

#endif // TEXTBUTTON_H
