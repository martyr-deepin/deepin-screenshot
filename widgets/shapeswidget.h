#ifndef SHAPESWIDGET_H
#define SHAPESWIDGET_H

#include <QFrame>
#include <QMouseEvent>

#include "utils/shapesutils.h"
#include "utils/baseutils.h"

class ShapesWidget : public QFrame {
    Q_OBJECT
public:
    ShapesWidget(QWidget* parent = 0);
    ~ShapesWidget();

    enum ClickedKey {
        First,
        Second,
        Third,
        Fourth,
        Fifth,
        Sixth,
        Seventh,
        Eighth,
    };
public slots:
    void setCurrentShape(QString shapeType);

    void handleRotate(QPointF pos);
    void handleResize(QPointF pos, int key);
    bool clickedOnShapes(QPointF pos);
    bool clickedOnRectPoint(QPointF point1, QPointF point2,
                        QPointF point3, QPointF point4, QPointF pos);

    bool clickedOnEllipsePoint(QPointF point1, QPointF point2,
                               QPointF point3, QPointF point4, QPointF pos);
    bool rotateOnPoint(QPointF point1, QPointF point2,
                       QPointF point3, QPointF point4,
                       QPointF pos);
    bool hoverOnRotatePoint(QPointF point1, QPointF point2,
                            QPointF point3, QPointF point4,
                            QPointF pos);
    bool hoverOnShapes(FourPoints fourPoints,
                       QPointF pos);
    bool hoverOnRect(QPointF point1, QPointF point2,
                     QPointF point3, QPointF point4,
                     QPointF pos);
    bool hoverOnEllipse(QPointF point1, QPointF point2,
                        QPointF point3, QPointF point4,
                        QPointF pos);
protected:
    void mousePressEvent(QMouseEvent* e);
    void mouseReleaseEvent(QMouseEvent* e);
    void mouseMoveEvent(QMouseEvent* e);
    void paintEvent(QPaintEvent *);
    bool eventFilter(QObject *watched, QEvent *event);

private:
    QPointF m_pos1 = QPointF(0, 0);
    QPointF m_pos2 = QPointF(0, 0);
    QPointF m_pos3, m_pos4;
    QPointF m_pressedPoint;
    QPointF m_movingPoint;

    bool m_isRecording;
    bool m_isMoving;
    bool m_isSelected;
    bool m_isPressed;
    bool m_isHovered;
    bool m_isRotated;
    bool m_isResize;
    bool m_isShiftPressed;

    ResizeDirection m_resizeDirection;
    ClickedKey m_clickedKey;

    int m_selectedIndex;
    QString m_currentShape = "rectangle";

    DiagPointsList m_diagPointsList;
    DiagPoints m_currentDiagPoints;
    DiagPoints m_currentHoverDiagPoints;
    DiagPoints m_currentSelectedDiagPoints;

    FourPoints m_currentSelectedFPoints;
    FourPoints m_currentHoveredFPoints;
    MPointsList m_mFPointsList;

    void paintImgPoint(QPainter &painter, QPointF pos, QPixmap img, bool isResize = true);
    void paintRect(QPainter &painter, FourPoints rectFPoints);
    void paintEllipse(QPainter &painter, FourPoints ellipseFPoints);
};
#endif // SHAPESWIDGET_H
