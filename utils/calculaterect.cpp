#include "calculaterect.h"

const int padding = 2;
const int ROTATEPOINT_PADDING = 30;

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

QPoint      pointSplid(QPoint point1, QPoint point2, int padding) {
    if (point1.x() == point2.x()) {
        return QPoint(0, padding);
    } else {
        int tmpX = padding*qAcos(qAtan2(qAbs(point1.y() - point2.y()), qAbs(point1.x() - point2.x())));
        int tmpY = padding*qAsin(qAtan2(qAbs(point1.y() - point2.y()), qAbs(point1.x() - point2.x())));
        return QPoint(tmpX, tmpY);
    }
}

QPoint       getRotatePoint(QPoint point1, QPoint point2, QPoint point3, QPoint point4) {
    QPoint leftPoint = QPoint(0, 0);
    QPoint rightPoint = QPoint(0, 0);
    QPoint rotatePoint = QPoint(0, 0);

    QPoint leftSplidPoint = pointSplid(point1, point2, ROTATEPOINT_PADDING);
    QPoint rightSplidPoint = pointSplid(point3, point4, ROTATEPOINT_PADDING);

    /* first position*/
    if (point2.x() - point4.x() <= 0 && point2.y() - point4.y() >= 0) {
        leftPoint = QPoint(point1.x() - leftSplidPoint.x(), point1.y() - leftSplidPoint.y());
        rightPoint = QPoint(point3.x() - rightSplidPoint.x(), point3.y() - rightSplidPoint.y());
        rotatePoint = QPoint((leftPoint.x() + rightPoint.x())/2, (leftPoint.y() + rightPoint.y())/2);
        return rotatePoint;
    }

    /* second position*/
    if (point2.x() - point4.x() > 0 && point2.y() - point4.y() > 0) {
        leftPoint = QPoint(point1.x() - leftSplidPoint.x(), point1.y() + leftSplidPoint.y());
        rightPoint = QPoint(point3.x() - rightSplidPoint.x(), point3.y() + rightSplidPoint.y());
        rotatePoint = QPoint((leftPoint.x() + rightPoint.x())/2, (leftPoint.y() + rightPoint.y())/2);
        return rotatePoint;
    }

    /* third position*/
    if (point2.x() - point4.x() < 0 && point2.y() - point4.y() < 0) {
        leftPoint = QPoint(point1.x() + leftSplidPoint.x(), point1.y() - leftSplidPoint.y());
        rightPoint = QPoint(point3.x() + rightSplidPoint.x(), point3.y() - rightSplidPoint.y());
        rotatePoint = QPoint((leftPoint.x() + rightPoint.x())/2, (leftPoint.y() + rightPoint.y())/2);
        return rotatePoint;
    }

    /* fourth position*/
    if (point2.x() - point4.x() > 0 && point2.y() - point4.y() < 0) {
        leftPoint = QPoint(point1.x() + leftSplidPoint.x(), point1.y() + leftSplidPoint.y());
        rightPoint = QPoint(point3.x() + rightSplidPoint.x(), point3.y() + rightSplidPoint.y());
        rotatePoint = QPoint((leftPoint.x() + rightPoint.x())/2, (leftPoint.y() + rightPoint.y())/2);
        return rotatePoint;
    }

    return rotatePoint;
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
