#include "shapeswidget.h"

#include "utils/calculaterect.h"

#include <QApplication>
#include <QPainter>
#include <QDebug>

const int DRAG_BOUND_RADIUS = 8;
const int SPACING = 12;

ShapesWidget::ShapesWidget(QWidget *parent)
    : QFrame(parent),
      m_selectedIndex(-1),
      m_isMoving(false),
      m_isSelected(false),
      m_isShiftPressed(false)
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
    qDebug() << "shape" << m_currentShape;
    qApp->setOverrideCursor(setCursorShape(m_currentShape));
}

bool ShapesWidget::clickedOnShapes(QPointF pos) {
    bool onShapes = false;
    m_currentDiagPoints.masterPoint = QPointF(0, 0);
    m_currentDiagPoints.deputyPoint = QPointF(0, 0);
    m_selectedIndex = -1;

    for (int i = 0; i < m_mFPointsList.length(); i++) {
        bool currentOnShape = false;
        if (m_mFPointsList[i].shapeType == "rectangle") {
            if (clickedOnRectPoint(m_mFPointsList[i].point1, m_mFPointsList[i].point2,
                                   m_mFPointsList[i].point3, m_mFPointsList[i].point4, pos)) {
                currentOnShape = true;
            }
        }
        if (m_mFPointsList[i].shapeType == "oval") {
            if (clickedOnEllipsePoint(m_mFPointsList[i].point1, m_mFPointsList[i].point2,
                                      m_mFPointsList[i].point3, m_mFPointsList[i].point4, pos)) {
                currentOnShape = true;
            }
        }

        if (currentOnShape) {
            m_currentSelectedDiagPoints.masterPoint = m_mFPointsList[i].point1;
            m_currentSelectedDiagPoints.deputyPoint = m_mFPointsList[i].point4;
            m_currentSelectedFPoints.point1 = m_mFPointsList[i].point1;
            m_currentSelectedFPoints.point2 = m_mFPointsList[i].point2;
            m_currentSelectedFPoints.point3 = m_mFPointsList[i].point3;
            m_currentSelectedFPoints.point4 = m_mFPointsList[i].point4;
            m_selectedIndex = i;

            onShapes = true;
            break;
        } else {
            update();
            continue;
        }
    }
        return onShapes;
}



    //TODO: selectUnique
bool ShapesWidget::clickedOnRectPoint(QPointF point1, QPointF point2,
                                  QPointF point3, QPointF point4, QPointF pos) {
    m_isSelected = false;
    m_isResize = false;
    m_isRotated = false;

    m_pressedPoint = QPoint(0, 0);
    FourPoints otherFPoints = getAnotherFPoints(point1, point2, point3, point4);
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
    }  else if (pointClickIn(otherFPoints.point1, pos)) {
        m_isSelected = true;
        m_isResize = true;
        m_clickedKey = Fifth;
        m_resizeDirection = Left;
        m_pressedPoint = pos;
        return true;
    } else if (pointClickIn(otherFPoints.point2, pos)) {
        m_isSelected = true;
        m_isResize = true;
        m_clickedKey = Sixth;
        m_resizeDirection = Top;
        m_pressedPoint = pos;
        return true;
    } else if (pointClickIn(otherFPoints.point3, pos)) {
        m_isSelected = true;
        m_isResize = true;
        m_clickedKey = Seventh;
        m_resizeDirection = Right;
        m_pressedPoint = pos;
        return true;
    } else if (pointClickIn(otherFPoints.point4, pos)) {
        m_isSelected = true;
        m_isResize = true;
        m_clickedKey = Eighth;
        m_resizeDirection = Bottom;
        m_pressedPoint = pos;
        return true;
    } else if (rotateOnPoint(point1, point2, point3, point4, pos)) {
        m_isSelected = true;
        m_isRotated = true;
        m_isResize = false;
        m_resizeDirection = Rotate;
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

bool ShapesWidget::clickedOnEllipsePoint(QPointF point1, QPointF point2,
                                         QPointF point3, QPointF point4, QPointF pos) {
    m_isSelected = false;
    m_isResize = false;
    m_isRotated = false;

    m_pressedPoint = QPoint(0, 0);
    FourPoints mainFPoints;
    mainFPoints.point1 = point1;
    mainFPoints.point2 = point2;
    mainFPoints.point3 = point3;
    mainFPoints.point4 = point4;
    FourPoints otherFPoints = getAnotherFPoints(point1, point2, point3, point4);
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
    }  else if (pointClickIn(otherFPoints.point1, pos)) {
        m_isSelected = true;
        m_isResize = true;
        m_clickedKey = Fifth;
        m_resizeDirection = Left;
        m_pressedPoint = pos;
        return true;
    } else if (pointClickIn(otherFPoints.point2, pos)) {
        m_isSelected = true;
        m_isResize = true;
        m_clickedKey = Sixth;
        m_resizeDirection = Top;
        m_pressedPoint = pos;
        return true;
    } else if (pointClickIn(otherFPoints.point3, pos)) {
        m_isSelected = true;
        m_isResize = true;
        m_clickedKey = Seventh;
        m_resizeDirection = Right;
        m_pressedPoint = pos;
        return true;
    } else if (pointClickIn(otherFPoints.point4, pos)) {
        m_isSelected = true;
        m_isResize = true;
        m_clickedKey = Eighth;
        m_resizeDirection = Bottom;
        m_pressedPoint = pos;
        return true;
    } else if (rotateOnPoint(point1, point2, point3, point4, pos)) {
        m_isSelected = true;
        m_isRotated = true;
        m_isResize = false;
        m_resizeDirection = Rotate;
        m_pressedPoint = pos;
        return true;
    } else if (pointOnLine(point1, point2, pos) || pointOnLine(point1, point3, pos)
             || pointOnLine(point2, point4, pos) || pointOnLine(point3, point4, pos)) {
        m_isSelected = true;
        m_isResize = false;
        m_resizeDirection = Moving;
        m_pressedPoint = pos;
        return true;
    } else if (pointOnEllipse(mainFPoints, pos)) {
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

bool ShapesWidget::hoverOnRect(QPointF point1, QPointF point2,
                               QPointF point3, QPointF point4, QPointF pos) {
    FourPoints tmpFPoints = getAnotherFPoints(point1, point2, point3, point4);
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
    }  else if (pointClickIn(tmpFPoints.point1, pos)) {
        m_resizeDirection = Left;
        return true;
    } else if (pointClickIn(tmpFPoints.point2, pos)) {
        m_resizeDirection = Top;
        return true;
    }  else if (pointClickIn(tmpFPoints.point3, pos)) {
        m_resizeDirection = Right;
        return true;
    } else if (pointClickIn(tmpFPoints.point4, pos)) {
        m_resizeDirection = Bottom;
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

bool ShapesWidget::hoverOnEllipse(QPointF point1, QPointF point2,
                                  QPointF point3, QPointF point4, QPointF pos) {
    FourPoints mainFPoints;
    mainFPoints.point1 = point1;
    mainFPoints.point2 = point2;
    mainFPoints.point3 = point3;
    mainFPoints.point4 = point4;
    FourPoints tmpFPoints = getAnotherFPoints(point1, point2, point3, point4);
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
    }  else if (pointClickIn(tmpFPoints.point1, pos)) {
        m_resizeDirection = Left;
        return true;
    } else if (pointClickIn(tmpFPoints.point2, pos)) {
        m_resizeDirection = Top;
        return true;
    }  else if (pointClickIn(tmpFPoints.point3, pos)) {
        m_resizeDirection = Right;
        return true;
    } else if (pointClickIn(tmpFPoints.point4, pos)) {
        m_resizeDirection = Bottom;
        return true;
    } else if (pointOnLine(point1, point2, pos) || pointOnLine(point1, point3, pos)
               || pointOnLine(point2, point4, pos) || pointOnLine(point3, point4, pos)) {
        m_resizeDirection = Moving;
        return true;
    }  else if (pointOnEllipse(mainFPoints, pos)) {
        m_isSelected = true;
        m_isResize = false;

        m_resizeDirection = Moving;
        m_pressedPoint = pos;
        return true;
   } else {
        m_resizeDirection = Outting;
    }
    return false;
}
bool ShapesWidget::hoverOnShapes(FourPoints fourPoints, QPointF pos) {
    if (fourPoints.shapeType == "rectangle") {
        return hoverOnRect(fourPoints.point1, fourPoints.point2,
                           fourPoints.point3, fourPoints.point4, pos);
    } else if (fourPoints.shapeType == "oval") {
        return hoverOnEllipse(fourPoints.point1, fourPoints.point2,
                              fourPoints.point3, fourPoints.point4, pos);
    }

    return false;
}

bool ShapesWidget::rotateOnPoint(QPointF point1, QPointF point2,
                                 QPointF point3, QPointF point4,
                                 QPointF pos) {
    bool result = hoverOnRotatePoint(point1, point2, point3, point4, pos);
    return result;
}

bool ShapesWidget::hoverOnRotatePoint(QPointF point1, QPointF point2,
                                      QPointF point3, QPointF point4,
                                      QPointF pos) {
    QPointF rotatePoint = getRotatePoint(point1, point2, point3, point4);
    rotatePoint = QPointF(rotatePoint.x() - 5, rotatePoint.y() - 5);
    bool result = false;
    if (pos.x() >= rotatePoint.x() - SPACING && pos.x() <= rotatePoint.x() + SPACING
            && pos.y() >= rotatePoint.y() - SPACING && pos.y() <= rotatePoint.y() + SPACING) {
        result = true;
    } else {
        result = false;
    }

    m_pressedPoint = rotatePoint;
    return result;
}

////////////////////TODO: perfect handleRotate..
void ShapesWidget::handleRotate(QPointF pos) {
    QList<QPointF> tmpFourPoint;
    tmpFourPoint.append(m_currentSelectedFPoints.point1);
    tmpFourPoint.append(m_currentSelectedFPoints.point2);
    tmpFourPoint.append(m_currentSelectedFPoints.point3);
    tmpFourPoint.append(m_currentSelectedFPoints.point4);

    QPointF centerInPoint = QPointF((m_currentSelectedFPoints.point1.x() + m_currentSelectedFPoints.point4.x())/2,
                                  (m_currentSelectedFPoints.point1.y() + m_currentSelectedFPoints.point4.y())/2);

    qreal angle = calculateAngle(m_pressedPoint, pos, centerInPoint)/35;
    for (int i = 0; i < 4; i++) {
        tmpFourPoint[i] = pointRotate(centerInPoint, tmpFourPoint[i], angle);
    }  
    m_diagPointsList[m_selectedIndex].masterPoint = tmpFourPoint[0];
    m_diagPointsList[m_selectedIndex].deputyPoint = tmpFourPoint[3];

    m_mFPointsList[m_selectedIndex].point1 = tmpFourPoint[0];
    m_mFPointsList[m_selectedIndex].point2 = tmpFourPoint[1];
    m_mFPointsList[m_selectedIndex].point3 = tmpFourPoint[2];
    m_mFPointsList[m_selectedIndex].point4 = tmpFourPoint[3];

    m_currentSelectedFPoints.point1 = tmpFourPoint[0];
    m_currentSelectedFPoints.point2 = tmpFourPoint[1];
    m_currentSelectedFPoints.point3 = tmpFourPoint[2];
    m_currentSelectedFPoints.point4 = tmpFourPoint[3];

    m_currentHoveredFPoints.point1 = tmpFourPoint[0];
    m_currentHoveredFPoints.point2 = tmpFourPoint[1];
    m_currentHoveredFPoints.point3 = tmpFourPoint[2];
    m_currentHoveredFPoints.point4 = tmpFourPoint[3];

    m_pressedPoint = pos;
}

void ShapesWidget::handleResize(QPointF pos, int key) {
        if (m_isResize) {
            QList<QPointF> tmpFourPoint;
            tmpFourPoint.append(m_currentSelectedFPoints.point1);
            tmpFourPoint.append(m_currentSelectedFPoints.point2);
            tmpFourPoint.append(m_currentSelectedFPoints.point3);
            tmpFourPoint.append(m_currentSelectedFPoints.point4);
            FourPoints newResizeFPoints = resizePointPosition(tmpFourPoint[0], tmpFourPoint[1],
                    tmpFourPoint[2], tmpFourPoint[3], pos, key,  m_isShiftPressed);
            m_mFPointsList[m_selectedIndex].point1 = newResizeFPoints.point1;
            m_mFPointsList[m_selectedIndex].point2 = newResizeFPoints.point2;
            m_mFPointsList[m_selectedIndex].point3 = newResizeFPoints.point3;
            m_mFPointsList[m_selectedIndex].point4 = newResizeFPoints.point4;
            m_currentSelectedFPoints.point1 = newResizeFPoints.point1;
            m_currentSelectedFPoints.point2 = newResizeFPoints.point2;
            m_currentSelectedFPoints.point3 = newResizeFPoints.point3;
            m_currentSelectedFPoints.point4 = newResizeFPoints.point4;
            m_currentHoveredFPoints.point1 = newResizeFPoints.point1;
            m_currentHoveredFPoints.point2 = newResizeFPoints.point2;
            m_currentHoveredFPoints.point3 = newResizeFPoints.point3;
            m_currentHoveredFPoints.point4 = newResizeFPoints.point4;
        }
}

void ShapesWidget::mousePressEvent(QMouseEvent *e) {
    m_pressedPoint = e->pos();
    m_isPressed = true;
    if (!clickedOnShapes(m_pressedPoint)) {
        qDebug() << "no one shape be clicked!";
        m_currentDiagPoints.masterPoint = QPoint(0, 0);
        m_currentDiagPoints.deputyPoint = QPoint(0, 0);
        m_currentSelectedFPoints.point1 = QPoint(0, 0);
        m_currentSelectedFPoints.point2 = QPoint(0, 0);
        m_currentSelectedFPoints.point3 = QPoint(0, 0);
        m_currentSelectedFPoints.point4 = QPoint(0, 0);
        m_currentSelectedFPoints.shapeType = m_currentShape;
        m_selectedIndex = -1;
        m_isRecording = true;
        if (m_pos1 == QPointF(0, 0)) {

            m_pos1 = e->pos();
            m_currentDiagPoints.masterPoint = m_pos1;
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
    if (m_isRecording && !m_isSelected && m_pos2 != QPointF(0, 0)) {
        m_currentDiagPoints.deputyPoint = m_pos2;
        m_diagPointsList.append(m_currentDiagPoints);

        FourPoints tmpPoints = fourPointsOnRect(m_currentDiagPoints);
        tmpPoints.shapeType = m_currentShape;
        m_mFPointsList.append(tmpPoints);
        m_isRecording = false;
        m_isMoving = false;
        m_currentDiagPoints.masterPoint = QPoint(0, 0);
        m_currentDiagPoints.deputyPoint = QPoint(0, 0);
        m_currentSelectedFPoints.point1 = QPoint(0, 0);
        m_currentSelectedFPoints.point2 = QPoint(0, 0);
        m_currentSelectedFPoints.point3 = QPoint(0, 0);
        m_currentSelectedFPoints.point4 = QPoint(0, 0);
    }

    m_pos1 = QPointF(0, 0);
    m_pos2 = QPointF(0, 0);


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
            // resize function
             handleResize(QPointF(e->pos()), m_clickedKey);
            update();
            return;
        }

        if (m_isSelected && m_isPressed && m_selectedIndex != -1) {
            m_mFPointsList[m_selectedIndex].point1 = QPointF(
                        m_mFPointsList[m_selectedIndex].point1.x() + (m_movingPoint.x() - m_pressedPoint.x()),
                        m_mFPointsList[m_selectedIndex].point1.y() + (m_movingPoint.y() - m_pressedPoint.y()));
            m_mFPointsList[m_selectedIndex].point2 = QPointF(
                        m_mFPointsList[m_selectedIndex].point2.x() + (m_movingPoint.x() - m_pressedPoint.x()),
                        m_mFPointsList[m_selectedIndex].point2.y() + (m_movingPoint.y() - m_pressedPoint.y()));
            m_mFPointsList[m_selectedIndex].point3 = QPointF(
                        m_mFPointsList[m_selectedIndex].point3.x() + (m_movingPoint.x() - m_pressedPoint.x()),
                        m_mFPointsList[m_selectedIndex].point3.y() + (m_movingPoint.y() - m_pressedPoint.y()));
            m_mFPointsList[m_selectedIndex].point4 = QPointF(
                        m_mFPointsList[m_selectedIndex].point4.x() + (m_movingPoint.x() - m_pressedPoint.x()),
                        m_mFPointsList[m_selectedIndex].point4.y() + (m_movingPoint.y() - m_pressedPoint.y()));

            m_currentSelectedFPoints = m_mFPointsList[m_selectedIndex];
            m_currentHoveredFPoints = m_mFPointsList[m_selectedIndex];
            m_currentSelectedFPoints.shapeType = m_mFPointsList[m_selectedIndex].shapeType;
            m_currentSelectedDiagPoints.masterPoint = m_mFPointsList[m_selectedIndex].point1;
            m_currentSelectedDiagPoints.deputyPoint = m_mFPointsList[m_selectedIndex].point4;

            m_pressedPoint = e->pos();
            update();
        }
    } else {
        if (!m_isRecording) {
            m_isHovered = false;
            for (int i = 0; i < m_mFPointsList.length(); i++) {
                 FourPoints tmpHoverFPoints =  m_mFPointsList[i];
                 if (hoverOnShapes(tmpHoverFPoints,  e->pos())) {
                     m_isHovered = true;
                     m_currentHoverDiagPoints = m_diagPointsList[i];
                     m_currentHoveredFPoints = tmpHoverFPoints;
                     if (m_resizeDirection == Left) {
                         if (m_isSelected || m_isRotated) {
                            qApp->setOverrideCursor(Qt::SizeHorCursor);
                         } else {
                            qApp->setOverrideCursor(Qt::ClosedHandCursor);
                         }
                     } else if (m_resizeDirection == Top) {
                         if (m_isSelected || m_isRotated) {
                            qApp->setOverrideCursor(Qt::SizeVerCursor);
                         } else {
                            qApp->setOverrideCursor(Qt::ClosedHandCursor);
                         }
                     } else if (m_resizeDirection == Right) {
                         if (m_isSelected || m_isRotated) {
                            qApp->setOverrideCursor(Qt::SizeHorCursor);
                         } else {
                            qApp->setOverrideCursor(Qt::ClosedHandCursor);
                         }
                     } else if (m_resizeDirection == Bottom) {
                         if (m_isSelected || m_isRotated) {
                            qApp->setOverrideCursor(Qt::SizeVerCursor);
                         } else {
                            qApp->setOverrideCursor(Qt::ClosedHandCursor);
                         }
                     }  else if (m_resizeDirection == TopLeft) {
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
                m_currentHoveredFPoints.point1 = QPointF(0, 0);
                m_currentHoveredFPoints.point2 = QPointF(0, 0);
                m_currentHoveredFPoints.point3 = QPointF(0, 0);
                m_currentHoveredFPoints.point4 = QPointF(0, 0);
                m_currentHoverDiagPoints.masterPoint = QPointF(0, 0);
                m_currentHoverDiagPoints.deputyPoint = QPointF(0, 0);
                update();
            }
            if (m_mFPointsList.length() == 0) {
                qApp->setOverrideCursor(setCursorShape(m_currentShape));
            }
        } else {
            //TODO text
        }
    }

    QFrame::mouseMoveEvent(e);
}

void ShapesWidget::paintImgPoint(QPainter &painter, QPointF pos, QPixmap img, bool isResize) {
        if (isResize) {
                painter.drawPixmap(QPoint(pos.x() - DRAG_BOUND_RADIUS,
                                  pos.y() - DRAG_BOUND_RADIUS), img);
        } else {
            painter.drawPixmap(QPoint(pos.x() - 12,
                              pos.y() - 12), img);
        }
}

void ShapesWidget::paintRect(QPainter &painter, FourPoints rectFPoints) {
    painter.drawLine(rectFPoints.point1, rectFPoints.point2);
    painter.drawLine(rectFPoints.point2, rectFPoints.point4);
    painter.drawLine(rectFPoints.point4, rectFPoints.point3);
    painter.drawLine(rectFPoints.point3, rectFPoints.point1);
}

void ShapesWidget::paintEllipse(QPainter &painter, FourPoints ellipseFPoints) {
    FourPoints minorPoints = getAnotherFPoints(ellipseFPoints.point1, ellipseFPoints.point2,
                         ellipseFPoints.point3, ellipseFPoints.point4);
    QList<QPointF> eightControlPoints = getEightControlPoint(ellipseFPoints);
    QPainterPath ellipsePath;
    ellipsePath.moveTo(minorPoints.point1.x(), minorPoints.point1.y());
    ellipsePath.cubicTo(eightControlPoints[0], eightControlPoints[1], minorPoints.point2);
    ellipsePath.cubicTo(eightControlPoints[4], eightControlPoints[5], minorPoints.point3);
    ellipsePath.cubicTo(eightControlPoints[6], eightControlPoints[7], minorPoints.point4);
    ellipsePath.cubicTo(eightControlPoints[3], eightControlPoints[2], minorPoints.point1);
    painter.drawPath(ellipsePath);
}

void ShapesWidget::paintEvent(QPaintEvent *) {
    QPainter painter(this);
    painter.setRenderHints(QPainter::Antialiasing);
    QPen pen;
    pen.setColor(Qt::red);
    pen.setWidth(3);
    painter.setPen(pen);

    if (m_currentDiagPoints.masterPoint != QPointF(0, 0) &&
            m_currentDiagPoints.deputyPoint != QPointF(0, 0)) {
        FourPoints currentFPoint = fourPointsOnRect(m_currentDiagPoints);
        if (m_currentShape == "rectangle") {
            paintRect(painter, currentFPoint);
        } else if (m_currentShape == "oval") {
            paintEllipse(painter, currentFPoint);
        }
    }

    for(int i = 0; i < m_mFPointsList.length(); i++) {
        if (m_mFPointsList[i].shapeType == "rectangle") {
            paintRect(painter, m_mFPointsList[i]);
        } else if (m_mFPointsList[i].shapeType == "oval") {
            paintEllipse(painter, m_mFPointsList[i]);
        }
    }

    if (m_currentSelectedDiagPoints.masterPoint != QPointF(0, 0) &&
            m_currentSelectedDiagPoints.deputyPoint != QPointF(0, 0)) {
        QPixmap resizePointImg(":/resources/images/size/resize_handle_big.png");
        paintImgPoint(painter, m_currentSelectedFPoints.point1, resizePointImg);
        paintImgPoint(painter, m_currentSelectedFPoints.point2, resizePointImg);
        paintImgPoint(painter, m_currentSelectedFPoints.point3, resizePointImg);
        paintImgPoint(painter, m_currentSelectedFPoints.point4, resizePointImg);

        FourPoints anotherFPoints = getAnotherFPoints(m_currentSelectedFPoints.point1,
       m_currentSelectedFPoints.point2, m_currentSelectedFPoints.point3, m_currentSelectedFPoints.point4);
        paintImgPoint(painter, anotherFPoints.point1, resizePointImg);
        paintImgPoint(painter, anotherFPoints.point2, resizePointImg);
        paintImgPoint(painter, anotherFPoints.point3, resizePointImg);
        paintImgPoint(painter, anotherFPoints.point4, resizePointImg);


        QPointF rotatePoint = getRotatePoint(m_currentSelectedFPoints.point1, m_currentSelectedFPoints.point2,
                m_currentSelectedFPoints.point3, m_currentSelectedFPoints.point4);
        QPointF middlePoint((m_currentSelectedFPoints.point1.x() + m_currentSelectedFPoints.point3.x())/2,
                           (m_currentSelectedFPoints.point1.y() + m_currentSelectedFPoints.point3.y())/2);
        painter.setPen(QColor(Qt::white));
        painter.drawLine(rotatePoint, middlePoint);
        QPixmap rotatePointImg(":/resources/images/size/rotate.png");
        paintImgPoint(painter, rotatePoint, rotatePointImg, false);

        if (m_currentSelectedFPoints.shapeType == "oval") {
            paintRect(painter, m_currentSelectedFPoints);
        }
    }

    if (m_currentHoverDiagPoints.masterPoint != QPointF(0, 0)) {
        pen.setWidth(1);
        pen.setColor(QColor(Qt::white));
        painter.setPen(pen);
        if (m_currentHoveredFPoints.shapeType == "rectangle") {
            paintRect(painter, m_currentHoveredFPoints);
        } else if (m_currentHoveredFPoints.shapeType == "oval") {
            paintEllipse(painter, m_currentHoveredFPoints);
        }
    }
}

bool ShapesWidget::eventFilter(QObject *watched, QEvent *event) {
    Q_UNUSED(watched);

    if (event->type() == QEvent::Enter) {
        qApp->setOverrideCursor(setCursorShape(m_currentShape));
    }

    if (event->type() == QKeyEvent::KeyPress) {
        QKeyEvent* keyEvent = static_cast<QKeyEvent*>(event);
        if (keyEvent->key() == Qt::Key_Escape) {
            qApp->quit();
        }
    }
    return false;

}
