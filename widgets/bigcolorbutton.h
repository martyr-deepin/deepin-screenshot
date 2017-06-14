#ifndef BIGCOLORBUTTON_H
#define BIGCOLORBUTTON_H

#include <QPushButton>
#include <QPainter>
#include <QPaintEvent>

class BigColorButton : public QPushButton {
    Q_OBJECT
public:
    BigColorButton(QWidget* parent = 0);
    ~BigColorButton();

    void setColor(QColor color);
    void setColorIndex();
    void setCheckedStatus(bool checked);
    void updateConfigColor(const QString &shape,  const QString &key, int index);

protected:
    void paintEvent(QPaintEvent *);
    void enterEvent(QEvent *);
    void leaveEvent(QEvent *);

private:
    QColor m_color;
    bool m_isHover;
    bool m_isChecked;
};

#endif // BIGCOLORBUTTON_H
