#include "shapeswidget.h"

#include "utils/calculaterect.h"

#include <QApplication>
#include <QPainter>
#include <QDebug>

const int DRAG_BOUND_RADIUS = 8;
const int SPACING = 12;

ShapesWidget::ShapesWidget(QWidget *parent)
    : QFrame(parent),
      m_shapesMap(QMap<int ,QString>()),
      m_isMoving(false),
      m_isSelected(false)
{
    setFocusPolicy(Qt::StrongFocus);
    setMouseTracking(true);
    setAcceptDrops(true);
    installEventFilter(this);
}

ShapesWidget::~ShapesWidget() {

}

void ShapesWidget::setCurrentShape(QString shapeType) {
    m_currentShape = shapeType;
}

ResizeDirection ShapesWidget::getResizeDirection(QPoint point1, QPoint point2,
                                    QPoint point3, QPoint point4, QPoint pos) {

    QPoint rotatePoint = getRotatePoint(point1, point2, point3, point4);
    rotatePoint = QPoint(rotatePoint.x() - 5, rotatePoint.y() - 5);

    if (pointClickIn(rotatePoint, pos)) {
        m_isResize = true;
        m_resizeDirection = Rotate;
    } else if (pointClickIn(point1, pos)) {
        m_isResize = true;
        m_resizeDirection = TopLeft;
    } else if (pointClickIn(point2, pos)) {
        m_isResize = true;
        m_resizeDirection = BottomLeft;
    } else if (pointClickIn(point3, pos)) {
        m_isResize = true;
        m_resizeDirection = TopRight;
    } else if (pointClickIn(point4, pos)) {
        m_isResize = true;
        m_resizeDirection = BottomRight;
    }/* else if (pointOnLine(point1, point2, pos)) {
        m_isResize = true;
//        m_resizeDirection = Left;
        m_resizeDirection == Moving;
    } else if (pointOnLine(point1, point3, pos)) {
        m_isResize = true;
//        m_resizeDirection = Top;
        m_resizeDirection = Moving;
    } else if (pointOnLine(point3, point4, pos)) {
        m_isResize = true;
//        m_resizeDirection = Right;
        m_resizeDirection = Moving;
    } else if (pointOnLine(point2, point4, pos)) {
        m_isResize = true;
//        m_resizeDirection = Bottom;
        m_resizeDirection = Moving;
    }*/
    else {
        m_resizeDirection = Moving;
    }

    return m_resizeDirection;
}

bool ShapesWidget::clickedOnShapes(QPoint pos) {
    bool onShapes = false;
    m_currentDiagPoints.masterPoint = QPoint(0, 0);
    m_currentDiagPoints.deputyPoint = QPoint(0, 0);
    m_selectedIndex = 0;
    for (int i = 0; i < m_mFourPointList.length(); i++) {
        if (clickedOnPoint(m_mFourPointList[i].point1, m_mFourPointList[i].point2,
                           m_mFourPointList[i].point3, m_mFourPointList[i].point4, pos)) {
            m_currentSelectedDiagPoints.masterPoint = m_mFourPointList[i].point1;
            m_currentSelectedDiagPoints.deputyPoint = m_mFourPointList[i].point4;
            m_selectedIndex = i;

            onShapes = true;
            break;
        } else {
            continue;
        }
    }
    update();
    return onShapes;

    //TODO: selectUnique
}

bool ShapesWidget::clickedOnPoint(QPoint point1, QPoint point2,
                                  QPoint point3, QPoint point4, QPoint pos) {
    m_isSelected = false;
    m_isResize = false;
    m_isRotated = false;

    if (pointClickIn(point1, pos)) {
        m_isSelected = true;
        m_isResize = true;
        m_clickedKey = First;
        m_resizeDirection = TopLeft;
        m_pressedPoint = pos;
        return true;
    } else if (pointClickIn(point2, pos)) {
        m_isSelected = true;
        m_isResize = true;
        m_clickedKey = Second;
        m_resizeDirection = BottomLeft;
        m_pressedPoint = pos;
        return true;
    } else if (pointClickIn(point3, pos)) {
        m_isSelected = true;
        m_isResize = true;
        m_clickedKey = Third;
        m_resizeDirection = TopRight;
        m_pressedPoint = pos;
        return true;
    } else if (pointClickIn(point4, pos)) {
        m_isSelected = true;
        m_isResize = true;
        m_clickedKey = Fourth;
        m_resizeDirection = BottomRight;
        m_pressedPoint = pos;
        return true;
    } else if (pointOnLine(point1, point2, pos) || pointOnLine(point1, point3, pos)
             || pointOnLine(point2, point4, pos) || pointOnLine(point3, point4, pos)) {
        m_isSelected = true;
        m_isResize = false;
        m_resizeDirection = Moving;
        m_pressedPoint = pos;
        return true;
    } else {
        m_isSelected = false;
        m_isResize = false;
        m_isRotated = false;
    }

    return false;
}

bool ShapesWidget::hoverOnShapes(QPoint point1, QPoint point2,
                                  QPoint point3, QPoint point4, QPoint pos) {
    if (pointClickIn(point1, pos)) {
        m_resizeDirection = TopLeft;
        return true;
    } else if (pointClickIn(point2, pos)) {
        m_resizeDirection = BottomLeft;
        return true;
    } else if (pointClickIn(point3, pos)) {
        m_resizeDirection = TopRight;
        return true;
    } else if (pointClickIn(point4, pos)) {
        m_resizeDirection = BottomRight;
        return true;
    } else if (rotateOnPoint(point1, point2, point3, point4, pos)) {
        m_resizeDirection = Rotate;
        return true;
    } else if (pointOnLine(point1, point2, pos) || pointOnLine(point1, point3, pos)
             || pointOnLine(point2, point4, pos) || pointOnLine(point3, point4, pos)) {
        m_resizeDirection = Moving;
        return true;
    } else {
        m_resizeDirection = Outting;
    }
    return false;
}

bool ShapesWidget::rotateOnPoint(QPoint point1, QPoint point2,
                                 QPoint point3, QPoint point4,
                                 QPoint pos) {
    bool result = hoverOnRotatePoint(point1, point2, point3, point4, pos);
    return result;
}

bool ShapesWidget::hoverOnRotatePoint(QPoint point1, QPoint point2,
                                      QPoint point3, QPoint point4,
                                      QPoint pos) {
    QPoint rotatePoint = getRotatePoint(point1, point2, point3, point4);
    rotatePoint = QPoint(rotatePoint.x() - 5, rotatePoint.y() - 5);
    bool result = false;
    if (pos.x() >= rotatePoint.x() - SPACING && pos.x() <= rotatePoint.x() + SPACING
            && pos.y() >= rotatePoint.y() - SPACING && pos.y() <= rotatePoint.y() + SPACING) {
        result = true;
    } else {
        result = false;
    }

    return result;
}

void ShapesWidget::handleRotate(QPoint pos) {
    QList<QPoint> tmpFourPoint = fourPointsOnRect(m_currentDiagPoints);
    QPoint centerInPoint = QPoint((tmpFourPoint[0].x() + tmpFourPoint[3].x())/2,
                                  (tmpFourPoint[1].x() + tmpFourPoint[4].x())/2);
    QPoint rotatePoint = getRotatePoint(tmpFourPoint[0], tmpFourPoint[1],
                                        tmpFourPoint[2], tmpFourPoint[2]);
    qreal angle = calculateAngle(m_pressedPoint, pos, centerInPoint);
    for (int i = 0; i < 4; i++) {
        tmpFourPoint[i] = pointRotate(centerInPoint, tmpFourPoint[i], angle);
    }

    m_pressedPoint = pos;
    m_diagPointsList[m_selectedIndex].masterPoint = tmpFourPoint[0];
    m_diagPointsList[m_selectedIndex].deputyPoint = tmpFourPoint[3];

    m_mFourPointList[m_selectedIndex].point1 = tmpFourPoint[0];
    m_mFourPointList[m_selectedIndex].point2 = tmpFourPoint[1];
    m_mFourPointList[m_selectedIndex].point3 = tmpFourPoint[2];
    m_mFourPointList[m_selectedIndex].point4 = tmpFourPoint[3];
}

void ShapesWidget::mousePressEvent(QMouseEvent *e) {
    m_pressedPoint = e->pos();
    m_isPressed = true;
    if (!clickedOnShapes(m_pressedPoint)) {
        qDebug() << "no one shape be clicked!";
        m_isRecording = true;
        if (m_pos1 == QPoint(0, 0)) {

            m_pos1 = e->pos();
            qDebug() << "m_pos1:" << m_pos1;
            m_currentDiagPoints.masterPoint = m_pos1;
            m_shapesMap.insert(m_shapesMap.count(), m_currentShape);
            update();
        }
    } else {
        m_isRecording = false;
        qDebug() << "some on shape be clicked!";
    }


    QFrame::mousePressEvent(e);
}

void ShapesWidget::mouseReleaseEvent(QMouseEvent *e) {
    m_isPressed = false;
    if (m_isRecording && !m_isSelected && m_pos2 != QPoint(0, 0)) {
        m_currentDiagPoints.deputyPoint = m_pos2;
        m_diagPointsList.append(m_currentDiagPoints);

        QList<QPoint> fourPointList = fourPointsOnRect(m_currentDiagPoints);
        FourPoints tmpPoints;
        tmpPoints.point1 = fourPointList[0];
        tmpPoints.point2 = fourPointList[1];
        tmpPoints.point3 = fourPointList[2];
        tmpPoints.point4 = fourPointList[3];

        m_mFourPointList.append(tmpPoints);
        m_isRecording = false;
        m_isMoving = false;
    }

    m_pos1 =QPoint(0, 0);
    m_pos2 = QPoint(0, 0);
    update();

    QFrame::mouseMoveEvent(e);
}

void ShapesWidget::mouseMoveEvent(QMouseEvent *e) {
    m_isMoving = true;
    m_movingPoint = e->pos();

    if (m_isRecording && m_isPressed) {
        m_pos2 = e->pos();
        m_currentDiagPoints.deputyPoint = m_pos2;
        update();
    } else if (!m_isRecording && m_isPressed) {
        if (m_isRotated && m_isPressed) {
            handleRotate(e->pos());
            update();
        }

        if (m_isResize && m_isPressed) {
            //TODO resize function
            //handleResize(e->pos, m_clickedKey);
            update();
        }

        if (m_isSelected && m_isPressed) {
            m_diagPointsList[m_selectedIndex].masterPoint = QPoint(
                        m_diagPointsList[m_selectedIndex].masterPoint.x() + (m_movingPoint.x() - m_pressedPoint.x()),
                        m_diagPointsList[m_selectedIndex].masterPoint.y() + (m_movingPoint.y() - m_pressedPoint.y()));
            m_diagPointsList[m_selectedIndex].deputyPoint = QPoint(
                        m_diagPointsList[m_selectedIndex].deputyPoint.x() + (m_movingPoint.x() - m_pressedPoint.x()),
                        m_diagPointsList[m_selectedIndex].deputyPoint.y() + (m_movingPoint.y() - m_pressedPoint.y()));
            m_currentSelectedDiagPoints = m_diagPointsList[m_selectedIndex];
            m_currentHoverDiagPoints = m_diagPointsList[m_selectedIndex];
            m_pressedPoint = e->pos();
            update();
        }
    } else {
        if (!m_isRecording) {
            m_isHovered = false;
            for (int i = 0; i < m_diagPointsList.length(); i++) {
                 QList<QPoint> tmpHoverPoints = fourPointsOnRect(m_diagPointsList[i]);
                 if (hoverOnShapes(tmpHoverPoints[0], tmpHoverPoints[1],
                     tmpHoverPoints[2], tmpHoverPoints[3], e->pos())) {
                     m_isHovered = true;
                     m_currentHoverDiagPoints = m_diagPointsList[i];
                     if (m_resizeDirection == TopLeft) {
                         if (m_isSelected || m_isRotated) {
                            qApp->setOverrideCursor(Qt::SizeFDiagCursor);
                         } else {
                            qApp->setOverrideCursor(Qt::ClosedHandCursor);
                         }
                     } else if (m_resizeDirection == BottomLeft) {
                         if (m_isSelected || m_isRotated) {
                            qApp->setOverrideCursor(Qt::SizeBDiagCursor);
                         } else {
                            qApp->setOverrideCursor(Qt::ClosedHandCursor);
                         }
                     } else if (m_resizeDirection == TopRight) {
                         if (m_isSelected || m_isRotated) {
                            qApp->setOverrideCursor(Qt::SizeBDiagCursor);
                         } else {
                            qApp->setOverrideCursor(Qt::ClosedHandCursor);
                         }
                     } else if (m_resizeDirection == BottomRight) {
                         if (m_isSelected || m_isRotated) {
                            qApp->setOverrideCursor(Qt::SizeFDiagCursor);
                         } else {
                            qApp->setOverrideCursor(Qt::ClosedHandCursor);
                         }
                     } else if (m_resizeDirection == Rotate) {
                         qApp->setOverrideCursor(setCursorShape("rotate"));
                     } else if (m_resizeDirection == Moving) {
                         qApp->setOverrideCursor(Qt::ClosedHandCursor);
                     } else {
                         qApp->setOverrideCursor(setCursorShape("rect"));
                     }
                     update();
                     break;
                 } else {
                     qApp->setOverrideCursor(setCursorShape(m_currentShape));
                     update();
                 }
            }
            if (!m_isHovered) {
                m_currentHoverDiagPoints.masterPoint = QPoint(0, 0);
                m_currentHoverDiagPoints.deputyPoint = QPoint(0, 0);
            }
            if (m_diagPointsList.length() == 0) {
                qApp->setOverrideCursor(setCursorShape(m_currentShape));
            }
            update();
        } else {
            //TODO text
        }
    }

    QFrame::mouseMoveEvent(e);
}

void ShapesWidget::paintEvent(QPaintEvent *) {
    QPainter painter(this);

    QPen pen;
    pen.setColor(Qt::red);
    pen.setWidth(3);
    painter.setPen(pen);

    if (m_pos1 != QPoint(0, 0) && m_pos2 != QPoint(0, 0)) {
        QRect curRect = diagPointsRect(m_currentDiagPoints);
        painter.drawRect(curRect);
    }

    for(int i = 0; i < m_diagPointsList.length(); i++) {
        QRect diagRect = diagPointsRect(m_diagPointsList[i]);
        painter.drawRect(diagRect);
    }


    if (m_currentSelectedDiagPoints.masterPoint != QPoint(0, 0) &&
            m_currentSelectedDiagPoints.deputyPoint != QPoint(0, 0)) {
        qDebug() << "currentSelected " << m_currentSelectedDiagPoints.masterPoint
                 << m_currentSelectedDiagPoints.deputyPoint;
        QList<QPoint> tmpPoints = fourPointsOnRect(m_currentSelectedDiagPoints);
        for(int i = 0; i < tmpPoints.length(); i++) {
            painter.drawPixmap(QPoint(tmpPoints[i].x() - DRAG_BOUND_RADIUS,
                                      tmpPoints[i].y() - DRAG_BOUND_RADIUS),
                    QPixmap(":/resources/images/size/resize_handle_big.png"));

            qDebug() << "i =" << i << tmpPoints[i];
        }

        QPoint rotatePoint = getRotatePoint(tmpPoints[0], tmpPoints[1],
                tmpPoints[2], tmpPoints[3]);
        QPoint middlePoint((tmpPoints[0].x() + tmpPoints[2].x())/2,
                           (tmpPoints[0].y() + tmpPoints[2].y())/2);
        painter.setPen(QColor(Qt::white));
        painter.drawLine(rotatePoint, middlePoint);
        painter.drawPixmap(QPoint(rotatePoint.x() - 12, rotatePoint.y() - 12),
                           QPixmap(":/resources/images/size/rotate.png"));
    }

    if (m_currentHoverDiagPoints.masterPoint != QPoint(0, 0)) {
        pen.setWidth(1);
        pen.setColor(QColor(Qt::white));
        painter.setPen(pen);
        painter.drawRect(diagPointsRect(m_currentHoverDiagPoints));
    }

}

bool ShapesWidget::eventFilter(QObject *watched, QEvent *event) {
    Q_UNUSED(watched);

    if (event->type() == QEvent::Enter) {
        if (m_currentShape == "rect") {
            qApp->setOverrideCursor(setCursorShape("rect"));
        }
    }

    return false;
}
