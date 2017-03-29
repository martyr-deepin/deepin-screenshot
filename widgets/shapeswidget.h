#ifndef SHAPESWIDGET_H
#define SHAPESWIDGET_H

#include <QFrame>
#include <QMouseEvent>

#include "utils/shapesutils.h"

class ShapesWidget : public QFrame {
    Q_OBJECT
public:
    ShapesWidget(QWidget* parent = 0);
    ~ShapesWidget();

public slots:
    void setCurrentShape(QString shapeType);

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
    bool m_isRecording;

    QString m_currentShape;
    QMap<int, QString> m_shapesMap;

    DiagPointsList m_diagPointsList;
    DiagPoints m_currentDiagPoints;
    DiagPoints m_currentHoverDiagPoints;
};
#endif // SHAPESWIDGET_H
