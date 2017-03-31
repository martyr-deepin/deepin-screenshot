#include "shapeswidget.h"

#include "utils/calculaterect.h"

#include <QApplication>
#include <QPainter>
#include <QDebug>

const int DRAG_BOUND_RADIUS = 8;

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

void ShapesWidget::updateCursor() {
    if (m_resizeDirection == Rotate) {
        qApp->setOverrideCursor(setCursorShape("rotate"));
    } else if (m_resizeDirection == TopLeft) {
        qApp->setOverrideCursor(Qt::SizeFDiagCursor);
    } else if (m_resizeDirection == BottomLeft) {
        qApp->setOverrideCursor(Qt::SizeBDiagCursor);
    } else if (m_resizeDirection == TopRight) {
        qApp->setOverrideCursor(Qt::SizeBDiagCursor);
    } else if (m_resizeDirection == BottomRight) {
        qApp->setOverrideCursor(Qt::SizeFDiagCursor);
    } else if (m_resizeDirection == Left) {
        qApp->setOverrideCursor(Qt::SizeHorCursor);
    } else if (m_resizeDirection == Right) {
        qApp->setOverrideCursor(Qt::SizeHorCursor);
    } else if (m_resizeDirection == Top) {
        qApp->setOverrideCursor(Qt::SizeVerCursor);
    } else if (m_resizeDirection == Bottom) {
        qApp->setOverrideCursor(Qt::SizeVerCursor);
    } else {
        qApp->setOverrideCursor(Qt::ClosedHandCursor);
    }
}

void ShapesWidget::mousePressEvent(QMouseEvent *e) {

    m_pressedPoint = e->pos();
    m_isPressed = true;
    m_isSelected = false;
    m_isMoving = false;

    for(int i = 0; i < m_diagPointsList.length(); i++) {
        if (pointOnRect(m_diagPointsList[i], e->pos())) {
            m_currentSelectedDiagPoints = m_diagPointsList[i];
            m_currentHoverDiagPoints = m_diagPointsList[i];
            m_selectedIndex = i;
            m_isSelected = true;
            update();
            break;
        } else {
            continue;
        }
    }

    if (!m_isSelected) {
        m_isRecording = true;
        m_currentSelectedDiagPoints.deputyPoint = QPoint(0, 0);
        m_currentSelectedDiagPoints.masterPoint = QPoint(0, 0);

        if (m_pos1 == QPoint(0, 0)) {
            m_pos1 = e->pos();
            qDebug() << "m_pos1:" << m_pos1;
            m_currentDiagPoints.masterPoint = m_pos1;
            m_shapesMap.insert(m_shapesMap.count(), m_currentShape);
        }
    } else {
        m_isRecording = false;
        m_pos1 = QPoint(0, 0);
    }

    QFrame::mousePressEvent(e);
}

void ShapesWidget::mouseReleaseEvent(QMouseEvent *e) {
    m_isMoving = false;
    m_isPressed = false;

    if (!m_isSelected && m_isRecording) {
        m_isRecording = false;

        m_currentDiagPoints.deputyPoint = m_pos2;
        m_diagPointsList.append(m_currentDiagPoints);
    }

    m_pos1 =QPoint(0, 0);
    m_pos2 = QPoint(0, 0);
    update();

    QFrame::mouseMoveEvent(e);
}

void ShapesWidget::mouseMoveEvent(QMouseEvent *e) {
    m_pos2 = e->pos();
    m_movingPoint = e->pos();
    m_currentDiagPoints.deputyPoint = m_pos2;
    m_isMoving = true;

    if (m_isSelected && !m_isRecording && m_isPressed) {
        m_diagPointsList[m_selectedIndex].masterPoint = QPoint(
                    m_diagPointsList[m_selectedIndex].masterPoint.x() + (m_movingPoint.x() - m_pressedPoint.x()),
                    m_diagPointsList[m_selectedIndex].masterPoint.y() + (m_movingPoint.y() - m_pressedPoint.y()));
        m_diagPointsList[m_selectedIndex].deputyPoint = QPoint(
                    m_diagPointsList[m_selectedIndex].deputyPoint.x() + (m_movingPoint.x() - m_pressedPoint.x()),
                    m_diagPointsList[m_selectedIndex].deputyPoint.y() + (m_movingPoint.y() - m_pressedPoint.y()));
        m_currentSelectedDiagPoints = m_diagPointsList[m_selectedIndex];

        m_pressedPoint = e->pos();
        update();
    }

    if (m_isRecording) {
        update();
    } else {
        m_currentHoverDiagPoints.masterPoint = QPoint(0, 0);
        m_currentHoverDiagPoints.deputyPoint = QPoint(0, 0);

        if (m_diagPointsList.length() != 0) {
            bool hasHovered = false;

            for(int i = 0; i < m_diagPointsList.length(); i++) {
                if (pointOnRect(m_diagPointsList[i], e->pos())) {
                    m_currentHoverDiagPoints = m_diagPointsList[i];
                    hasHovered = true;
                    QList<QPoint> fourHoveredPoint = fourPointsOnRect(m_diagPointsList[i]);
                    getResizeDirection(fourHoveredPoint[0], fourHoveredPoint[1],
                            fourHoveredPoint[2], fourHoveredPoint[3], e->pos());
                    updateCursor();
                    update();
                    break;

                } else {
                    continue;
                    qDebug() << "!!!!!!!!!!!!!!!";
                }
            }

            if (!hasHovered && m_isSelected) {
                QList<QPoint> selectedFourPoints = fourPointsOnRect(m_currentSelectedDiagPoints);
                getResizeDirection(selectedFourPoints[0], selectedFourPoints[1],
                        selectedFourPoints[2], selectedFourPoints[3], e->pos());
                updateCursor();
            }
            update();
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

    if (m_pos1 != QPoint(0, 0)) {
        QRect curRect = diagPointsRect(m_currentDiagPoints);
        painter.drawRect(curRect);
    }

    for(int i = 0; i < m_diagPointsList.length(); i++) {
        QRect diagRect = diagPointsRect(m_diagPointsList[i]);
        painter.drawRect(diagRect);
    }


    if (m_currentSelectedDiagPoints.masterPoint != QPoint(0, 0)) {
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
