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
    void updatePaintEvent();

protected:
    void paintEvent(QPaintEvent *);

private:
    QRect m_centerRect;
    bool m_updatePos;
    QPixmap m_lastPic;
    QBrush m_lastCenterPosBrush;
    QPoint m_pos;
};

#endif // MAGNIFIER_H
