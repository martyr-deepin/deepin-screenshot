#include "shapeswidget.h"

#include <QApplication>
#include <QPainter>
#include <QDebug>

ShapesWidget::ShapesWidget(QWidget *parent)
    : QFrame(parent),
      m_shapesMap(QMap<int ,QString>())
{
//    setStyleSheet("background-color: rgba(255, 0, 0, 100);");
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
        m_shapesMap.insert(m_shapesMap.count(), m_currentShape);
    }

    QFrame::mousePressEvent(e);
}

void ShapesWidget::mouseReleaseEvent(QMouseEvent *e) {
    m_isRecording = false;

    m_pos2 = QPoint(e->x(), e->y());
    update();

    QFrame::mouseMoveEvent(e);
}

void ShapesWidget::mouseMoveEvent(QMouseEvent *e) {
    m_pos2 = QPoint(e->x(), e->y());
    if (m_isRecording)
        update();

    QFrame::mouseMoveEvent(e);
}

void ShapesWidget::paintEvent(QPaintEvent *) {
    QPainter painter(this);

    QRect mainRect(m_pos1.x(), m_pos1.y(), m_pos2.x() - m_pos1.x(),
                   m_pos2.y() - m_pos1.y());

    painter.drawRect(mainRect);
}

bool ShapesWidget::eventFilter(QObject *watched, QEvent *event) {
    Q_UNUSED(watched);

    if (event->type() == QEvent::Enter) {
        setCursor(Qt::ArrowCursor);
        qApp->setOverrideCursor(Qt::ArrowCursor);
    }
    return false;
}
