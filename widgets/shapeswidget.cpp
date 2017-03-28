#include "shapeswidget.h"

#include <QApplication>
#include <QPainter>
#include <QDebug>

ShapesWidget::ShapesWidget(QWidget *parent)
    : QFrame(parent),
      m_shapesMap(QMap<int ,QString>())
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
    m_isRecording = true;

    if (m_pos1 == QPoint(0, 0)) {
        m_pos1 = QPoint(e->x(), e->y());
        qDebug() << "m_pos1:" << m_pos1;
        m_currentDiagPoints.masterPoint = m_pos1;
        m_shapesMap.insert(m_shapesMap.count(), m_currentShape);
    }

    QFrame::mousePressEvent(e);
}

void ShapesWidget::mouseReleaseEvent(QMouseEvent *e) {
    m_isRecording = false;

    m_pos2 = QPoint(e->x(), e->y());
    m_currentDiagPoints.deputyPoint = m_pos2;
    m_diagPointsList.append(m_currentDiagPoints);
    m_pos1 =QPoint(0, 0);
    m_pos2 = QPoint(0, 0);
    update();


    QFrame::mouseMoveEvent(e);
}

void ShapesWidget::mouseMoveEvent(QMouseEvent *e) {
    m_pos2 = QPoint(e->x(), e->y());
    m_currentDiagPoints.deputyPoint = m_pos2;

    if (m_isRecording)
        update();

    QFrame::mouseMoveEvent(e);
}

void ShapesWidget::paintEvent(QPaintEvent *) {
    QPainter painter(this);

    QPen pen;
    pen.setColor(Qt::red);
    pen.setWidth(2);
    painter.setPen(pen);

    if (m_pos1 != QPoint(0, 0)) {
        QRect curRect = QRect(qMin(m_currentDiagPoints.masterPoint.x(), m_currentDiagPoints.deputyPoint.x()),
                              qMin(m_currentDiagPoints.masterPoint.y(), m_currentDiagPoints.deputyPoint.y()),
                              qAbs(m_currentDiagPoints.masterPoint.x() - m_currentDiagPoints.deputyPoint.x()),
                              qAbs(m_currentDiagPoints.masterPoint.y() - m_currentDiagPoints.deputyPoint.y()));
        painter.drawRect(curRect);
    }

    for(int i = 0; i < m_diagPointsList.length(); i++) {
        QRect diagRect = QRect(qMin(m_diagPointsList[i].masterPoint.x(), m_diagPointsList[i].deputyPoint.x()),
                               qMin(m_diagPointsList[i].masterPoint.y(), m_diagPointsList[i].deputyPoint.y()),
                               qAbs(m_diagPointsList[i].masterPoint.x() - m_diagPointsList[i].deputyPoint.x()),
                               qAbs(m_diagPointsList[i].masterPoint.y() - m_diagPointsList[i].deputyPoint.y()));
        painter.drawRect(diagRect);
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
