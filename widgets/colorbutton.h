#ifndef COLORBUTTON_H
#define COLORBUTTON_H

#include <QPushButton>
#include <QPaintEvent>

class ColorButton : public QPushButton {
    Q_OBJECT
public:
    ColorButton(QColor bgColor, QWidget*parent = 0);
    ~ColorButton();

    void setColorBtnChecked();

public slots:
    QColor getColor();

signals:
    void updatePaintColor(QColor paintColor);

//protected:
//    void paintEvent(QPaintEvent *);

private:
    QColor m_bgColor;
};

#endif // COLORBUTTON_H
