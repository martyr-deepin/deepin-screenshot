#include "calculaterect.h"

const int padding = 2;
const int ROTATEPOINT_PADDING = 30;

/* get a rect by diagPoints */
QRect diagPointsRect(DiagPoints diagPoints) {
    return QRect(std::min(diagPoints.masterPoint.x(), diagPoints.deputyPoint.x()),
                 std::min(diagPoints.masterPoint.y(), diagPoints.deputyPoint.y()),
                 std::abs(diagPoints.masterPoint.x() - diagPoints.deputyPoint.x()),
                 std::abs(diagPoints.masterPoint.y() - diagPoints.deputyPoint.y()));
}

/* judge whether the point1 is on the point2 or not */
bool pointClickIn(QPointF point2, QPointF point1, int padding) {
    if (point2.x() >= point1.x() - padding && point2.x() <= point1.x() + padding &&
            point2.y() >= point1.y() - padding && point2.y() <= point1.y() + padding) {
        return true;
    } else {
        return false;
    }
}

/* judge whether the point3 is on the segment*/
bool pointOnLine(QPointF point1, QPointF point2, QPointF point3) {
    if (point1.x() == point2.x()) {
           if (point3.x() >= point1.x() - padding && point3.x() <= point1.x() + padding &&
           point3.y() >= std::min(point1.y(), point2.y()) - padding && point3.y() <= std::max(point1.y(), point2.y()) + padding) {
               return true;
           }
       } else {
           qreal k =  (point2.y() - point1.y()) / (point2.x() - point1.x());
           qreal b = point1.y() - point1.x()*k;

           if ( point3.x() >= std::min(point1.x(), point2.x()) -padding && point3.x() <= std::max(point1.x(), point2.x() + padding)
           && point3.y() >= k * point3.x() + b - padding && point3.y() <= k * point3.x() + b + padding) {
               return true;
           }
       }
       return false;
}

/* To determine whether a point on the rectangle*/
bool pointOnRect(DiagPoints diagPoints, QPointF pos) {
    QPointF point1 = diagPoints.masterPoint;
    QPointF point3 = diagPoints.deputyPoint;
    QPointF point2 = QPointF(diagPoints.masterPoint.x(), diagPoints.deputyPoint.y());
    QPointF point4 = QPointF(diagPoints.deputyPoint.x(), diagPoints.masterPoint.y());

    if (pointOnLine(point1, point2, pos) || pointOnLine(point1, point4, pos) ||
            pointOnLine(point2, point3, pos) || pointOnLine(point3, point4, pos)) {
        return true;
    } else {
        return false;
    }
}

/* get the point who splid a distance on a line */
QPointF pointSplid(QPointF point1, QPointF point2, int padding) {
    if (point1.x() == point2.x()) {
        return QPointF(0, padding);
    } else {
        int tmpX = padding*std::cos(qAtan2(std::abs(point1.y() - point2.y()), std::abs(point1.x() - point2.x())));
        int tmpY = padding*std::sin(qAtan2(std::abs(point1.y() - point2.y()), std::abs(point1.x() - point2.x())));
        return QPointF(tmpX, tmpY);
    }
}

/* get the rotate point by four points in a rectangle*/
QPointF getRotatePoint(QPointF point1, QPointF point2, QPointF point3, QPointF point4) {
    QPointF leftPoint = QPointF(0, 0);
    QPointF rightPoint = QPointF(0, 0);
    QPointF rotatePoint = QPointF(0, 0);

    QPointF leftSplidPoint = pointSplid(point1, point2, ROTATEPOINT_PADDING);
    QPointF rightSplidPoint = pointSplid(point3, point4, ROTATEPOINT_PADDING);

    /* first position*/
    if (point2.x() - point4.x() <= 0 && point2.y() - point4.y() >= 0) {
        leftPoint = QPointF(point1.x() - leftSplidPoint.x(), point1.y() - leftSplidPoint.y());
        rightPoint = QPointF(point3.x() - rightSplidPoint.x(), point3.y() - rightSplidPoint.y());
        rotatePoint = QPointF((leftPoint.x() + rightPoint.x())/2, (leftPoint.y() + rightPoint.y())/2);
        return rotatePoint;
    }

    /* second position*/
    if (point2.x() - point4.x() > 0 && point2.y() - point4.y() > 0) {
        leftPoint = QPointF(point1.x() - leftSplidPoint.x(), point1.y() + leftSplidPoint.y());
        rightPoint = QPointF(point3.x() - rightSplidPoint.x(), point3.y() + rightSplidPoint.y());
        rotatePoint = QPointF((leftPoint.x() + rightPoint.x())/2, (leftPoint.y() + rightPoint.y())/2);
        return rotatePoint;
    }

    /* third position*/
    if (point2.x() - point4.x() < 0 && point2.y() - point4.y() < 0) {
        leftPoint = QPointF(point1.x() + leftSplidPoint.x(), point1.y() - leftSplidPoint.y());
        rightPoint = QPointF(point3.x() + rightSplidPoint.x(), point3.y() - rightSplidPoint.y());
        rotatePoint = QPointF((leftPoint.x() + rightPoint.x())/2, (leftPoint.y() + rightPoint.y())/2);
        return rotatePoint;
    }

    /* fourth position*/
    if (point2.x() - point4.x() > 0 && point2.y() - point4.y() < 0) {
        leftPoint = QPointF(point1.x() + leftSplidPoint.x(), point1.y() + leftSplidPoint.y());
        rightPoint = QPointF(point3.x() + rightSplidPoint.x(), point3.y() + rightSplidPoint.y());
        rotatePoint = QPointF((leftPoint.x() + rightPoint.x())/2, (leftPoint.y() + rightPoint.y())/2);
        return rotatePoint;
    }

    return rotatePoint;
}

FourPoints fourPointsOnRect(DiagPoints diagPoints) {
    FourPoints  fourPoints;
    QPointF point1 = QPointF(std::min(diagPoints.masterPoint.x(), diagPoints.deputyPoint.x()),
                           std::min(diagPoints.masterPoint.y(), diagPoints.deputyPoint.y()));
    QPointF point2 = QPointF(std::min(diagPoints.masterPoint.x(), diagPoints.deputyPoint.x()),
                           std::max(diagPoints.masterPoint.y(), diagPoints.deputyPoint.y()));
    QPointF point3 = QPointF(std::max(diagPoints.masterPoint.x(), diagPoints.deputyPoint.x()),
                           std::min(diagPoints.masterPoint.y(), diagPoints.deputyPoint.y()));
    QPointF point4 = QPointF(std::max(diagPoints.masterPoint.x(), diagPoints.deputyPoint.x()),
                           std::max(diagPoints.masterPoint.y(), diagPoints.deputyPoint.y()));

    fourPoints.point1 = point1;
    fourPoints.point2 = point2;
    fourPoints.point3 = point3;
    fourPoints.point4 = point4;

    return fourPoints;
}

/*
 *  this function is get the angle of the mouse'moving*/
/* the angle in point3 */

qreal calculateAngle(QPointF point1, QPointF point2, QPointF point3) {
    if (point1 == point2) {
        return 0;
    }

    qreal a = std::pow(point1.x() - point3.x(), 2) + std::pow(point1.y() - point3.y(), 2);
    qreal b = std::pow(point2.x() - point3.x(), 2) + std::pow(point2.y() - point3.y(), 2);
    qreal c = std::pow(point1.x() - point2.x(), 2) + std::pow(point1.y() - point2.y(), 2);

    qreal angle =std::cos(( a + b - c)/(2*std::sqrt(a)*std::sqrt(b)));
    if (point1.x() <= point3.x() && point1.y() < point3.y()) {
        if (point2.x() < point1.x() || point2.y() > point1.y()) {
            angle = - angle;
        }
    }
    if (point1.x() < point3.x() && point1.y() >= point3.y()) {
        if (point2.x() > point1.x() || point2.y() > point1.y()) {
            angle = - angle;
        }
    }
    if (point1.x() >= point3.x() && point1.y() > point3.y()) {
        if (point2.x() > point1.x() || point2.y() < point1.y()) {
            angle = - angle;
        }
    }
    if (point1.x() > point3.x() && point1.y() <= point3.y()) {
        if (point2.x() < point1.x() || point2.y() < point1.y()) {
            angle = - angle;
        }
    }
    return angle;
}

/* point2 is the rotatePoint, point1 is the centerPoint, point3 is point2 who rotate */
QPointF pointRotate(QPointF point1, QPointF point2, qreal angle) {
    QPointF middlePoint = QPointF(point2.x() - point1.x(), point2.y() - point1.y());
    QPointF tmpPoint = QPointF(middlePoint.x() * std::cos(angle) - middlePoint.y() * std::sin(angle),
                             middlePoint.x() * std::sin(angle) + middlePoint.y() * std::cos(angle));
    QPointF point3 = QPointF(tmpPoint.x() + point1.x(), tmpPoint.y() + point1.y());

    return point3;
}

/* the distance from a point(point3) to a line(point1, point2) */
qreal pointToLineDistance(QPoint point1, QPoint point2, QPoint point3) {
    if (point1.x() == point2.x()) {
        return std::abs(point3.x() - point1.x());
    } else {
        qreal k = (point1.y() - point2.y()) / (point1.x() - point2.x());
        qreal b = point1.y() - point1.x() * k;
        return std::abs(point3.x() * k + b - point3.y()) / std::sqrt(std::pow(k, 2) + 1);
    }
}








