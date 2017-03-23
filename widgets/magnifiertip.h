#ifndef MAGNIFIERTIP_H
#define MAGNIFIERTIP_H

#include <QLabel>
#include <QPaintEvent>

class MagnifierTip : public QLabel {
    Q_OBJECT
public:
    MagnifierTip(QWidget* parent = 0);
    ~MagnifierTip();

    void showMagnifier(QPoint pos);
protected:
    void paintEvent(QPaintEvent *);
};

#endif // MAGNIFIER_H
