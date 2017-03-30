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
        m_currentHoverDiagPoints = m_diagPointsList[m_selectedIndex];
        m_currentSelectedDiagPoints = m_diagPointsList[m_selectedIndex];
        m_pressedPoint = e->pos();
        update();
    }

    if (m_isRecording) {
        update();
    } else if (!m_isSelected){
        m_currentHoverDiagPoints.masterPoint = QPoint(0, 0);
        m_currentHoverDiagPoints.deputyPoint = QPoint(0, 0);

        if (m_diagPointsList.length() != 0) {

            for(int i = 0; i < m_diagPointsList.length(); i++) {
                if (pointOnRect(m_diagPointsList[i], e->pos())) {
                    m_currentHoverDiagPoints = m_diagPointsList[i];
                    update();
                    break;

                } else {
                    continue;
                    qDebug() << "!!!!!!!!!!!!!!!";
                }
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


    if (m_currentHoverDiagPoints.masterPoint != QPoint(0, 0)) {
        pen.setWidth(1);
        pen.setColor(QColor(0, 0, 255));
        painter.setPen(pen);
        painter.drawRect(diagPointsRect(m_currentHoverDiagPoints));
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
        painter.drawLine(rotatePoint, middlePoint);
        painter.drawPixmap(QPoint(rotatePoint.x() - 12, rotatePoint.y() - 12),
                           QPixmap(":/resources/images/size/rotate.png"));
    }
}

bool ShapesWidget::eventFilter(QObject *watched, QEvent *event) {
    Q_UNUSED(watched);

    if (event->type() == QEvent::Enter) {
        setCursor(Qt::ArrowCursor);
        qApp->setOverrideCursor(Qt::ArrowCursor);
    }

    return false;
}
