#include "calculaterect.h"

const int padding = 2;

QRect diagPointsRect(DiagPoints diagPoints) {
    return QRect(qMin(diagPoints.masterPoint.x(), diagPoints.deputyPoint.x()),
                 qMin(diagPoints.masterPoint.y(), diagPoints.deputyPoint.y()),
                 qAbs(diagPoints.masterPoint.x() - diagPoints.deputyPoint.x()),
                 qAbs(diagPoints.masterPoint.y() - diagPoints.deputyPoint.y()));
}

bool pointOnLine(QPoint point1, QPoint point2, QPoint point3) {
    if (point1.x() == point2.x()) {
           if (point3.x() >= point1.x() - padding && point3.x() <= point1.x() + padding &&
           point3.y() >= qMin(point1.y(), point2.y()) - padding && point3.y() <= qMax(point1.y(), point2.y()) + padding) {
               return true;
           }
       } else {
           qreal k =  (point2.y() - point1.y()) / (point2.x() - point1.x());
           qreal b = point1.y() - point1.x()*k;

           if ( point3.x() >= qMin(point1.x(), point2.x()) -padding && point3.x() <= qMax(point1.x(), point2.x() + padding)
           && point3.y() >= k * point3.x() + b - padding && point3.y() <= k * point3.x() + b + padding) {
               return true;
           }
       }
       return false;
}

bool pointOnRect(DiagPoints diagPoints, QPoint pos) {
    QPoint point1 = diagPoints.masterPoint;
    QPoint point3 = diagPoints.deputyPoint;
    QPoint point2 = QPoint(diagPoints.masterPoint.x(), diagPoints.deputyPoint.y());
    QPoint point4 = QPoint(diagPoints.deputyPoint.x(), diagPoints.masterPoint.y());

    if (pointOnLine(point1, point2, pos) || pointOnLine(point1, point4, pos) ||
            pointOnLine(point2, point3, pos) || pointOnLine(point3, point4, pos)) {
        return true;
    } else {
        return false;
    }
}

QList<QPoint> fourPointsOnRect(DiagPoints diagPoints) {
    QList<QPoint>  fourPoints;
    QPoint point1 = QPoint(qMin(diagPoints.masterPoint.x(), diagPoints.deputyPoint.x()),
                           qMin(diagPoints.masterPoint.y(), diagPoints.deputyPoint.y()));
    QPoint point2 = QPoint(qMin(diagPoints.masterPoint.x(), diagPoints.deputyPoint.x()),
                           qMax(diagPoints.masterPoint.y(), diagPoints.deputyPoint.y()));
    QPoint point3 = QPoint(qMax(diagPoints.masterPoint.x(), diagPoints.deputyPoint.x()),
                           qMin(diagPoints.masterPoint.y(), diagPoints.deputyPoint.y()));
    QPoint point4 = QPoint(qMax(diagPoints.masterPoint.x(), diagPoints.deputyPoint.x()),
                           qMax(diagPoints.masterPoint.y(), diagPoints.deputyPoint.y()));
    fourPoints.clear();
    fourPoints.append(point1);
    fourPoints.append(point2);
    fourPoints.append(point3);
    fourPoints.append(point4);
    return fourPoints;
}
