#ifndef ZOOMINDICATOR_H
#define ZOOMINDICATOR_H

#include <QLabel>
#include <QPainter>
#include <QPaintEvent>

class ZoomIndicator : public QLabel {
    Q_OBJECT
public:
    ZoomIndicator(QWidget* parent = 0);
    ~ZoomIndicator();

    void showMagnifier(QPoint pos);
protected:
    void paintEvent(QPaintEvent *);

    QPoint m_pos;
};

#endif // MAGNIFIER_H
