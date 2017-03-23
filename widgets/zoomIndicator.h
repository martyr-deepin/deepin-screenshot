#ifndef ZOOMINDICATOR_H
#define ZOOMINDICATOR_H

#include <QLabel>
#include <QPaintEvent>

class ZoomIndicator : public QLabel {
    Q_OBJECT
public:
    ZoomIndicator(QWidget* parent = 0);
    ~ZoomIndicator();

    void showMagnifier(QPoint pos);
protected:
    void paintEvent(QPaintEvent *);
};

#endif // MAGNIFIER_H
