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
    };
public slots:
    void setCurrentShape(QString shapeType);
    ResizeDirection getResizeDirection(QPoint point1, QPoint point2,
                                       QPoint point3, QPoint point4,
                                       QPoint pos);

    void handleRotate(QPoint pos);
    bool clickedOnShapes(QPoint pos);
    bool clickedOnPoint(QPoint point1, QPoint point2,
                        QPoint point3, QPoint point4,
                        QPoint pos);
    bool rotateOnPoint(QPoint point1, QPoint point2,
                       QPoint point3, QPoint point4,
                       QPoint pos);
    bool hoverOnRotatePoint(QPoint point1, QPoint point2,
                            QPoint point3, QPoint point4,
                            QPoint pos);
    bool hoverOnShapes(QPoint point1, QPoint point2,
                       QPoint point3, QPoint point4,
                       QPoint pos);

protected:
    void mousePressEvent(QMouseEvent* e);
    void mouseReleaseEvent(QMouseEvent* e);
    void mouseMoveEvent(QMouseEvent* e);
    void paintEvent(QPaintEvent *);
    bool eventFilter(QObject *watched, QEvent *event);

private:

    QPoint m_pos1 = QPoint(0, 0);
    QPoint m_pos2 = QPoint(0, 0);
    QPoint m_pos3, m_pos4;
    QPoint m_pressedPoint;
    QPoint m_movingPoint;

    bool m_isRecording;
    bool m_isMoving;
    bool m_isSelected;
    bool m_isPressed;
    bool m_isHovered;
    bool m_isRotated;

    bool m_isResize;
    ResizeDirection m_resizeDirection;
    ClickedKey m_clickedKey;

    int m_selectedIndex;
    QString m_currentShape = "rect";
    QMap<int, QString> m_shapesMap;

    DiagPointsList m_diagPointsList;
    DiagPoints m_currentDiagPoints;
    DiagPoints m_currentHoverDiagPoints;
    DiagPoints m_currentSelectedDiagPoints;

    MPointsList m_mFourPointList;
};
#endif // SHAPESWIDGET_H
