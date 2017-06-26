#include "calculaterect.h"
#include <cmath>

const int padding = 2;
const int ROTATEPOINT_PADDING = 30;
const int TANT_EDGEVALUE = 0.78539;
const int TANT2_EDGEVALUE = 2.35619;
const int MIN_PADDING = 3;
const qreal SLOPE = 0.5522848;

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

/* get the distance between two points*/
qreal getDistance(QPointF point1, QPointF point2) {
    return std::sqrt(std::pow(point1.x() - point2.x(), 2) + std::pow(point1.y() - point2.y(), 2));
}

/* get the point who splid a distance on a line */
QPointF pointSplid(QPointF point1, QPointF point2, qreal padding) {
    if (point1.x() == point2.x()) {
        return QPointF(0, padding);
    } else {
        qreal tmpX = padding*std::cos(std::atan2(std::abs(point1.y() - point2.y()), std::abs(point1.x() - point2.x())));
        qreal tmpY = padding*std::sin(std::atan2(std::abs(point1.y() - point2.y()), std::abs(point1.x() - point2.x())));
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

/* get the four points from a line */
FourPoints fourPointsOfLine(QList<QPointF> points) {
    FourPoints resultFPoint;
    const int MIN_PADDING = 10;
    resultFPoint = initFourPoints(resultFPoint);
    if (points.length() < 2) {
        return initFourPoints(resultFPoint);
    }

    QPointF minPointF = points[0];
    QPointF maxPointF = points[0];
    foreach (QPointF point, points) {
        minPointF = QPointF(std::min(minPointF.x(), point.x()), std::min(minPointF.y(), point.y()));
        maxPointF = QPointF(std::max(maxPointF.x(), point.x()), std::max(maxPointF.y(), point.y()));
    }

    resultFPoint[0] = QPointF(minPointF.x() - MIN_PADDING, minPointF.y() - MIN_PADDING);
    resultFPoint[1] = QPointF(minPointF.x() - MIN_PADDING, maxPointF.y() + MIN_PADDING);
    resultFPoint[2] = QPointF(maxPointF.x() + MIN_PADDING, minPointF.y() - MIN_PADDING);
    resultFPoint[3] = QPointF(maxPointF.x() + MIN_PADDING, maxPointF.y() + MIN_PADDING);
    return resultFPoint;
}
FourPoints getAnotherFPoints(FourPoints mainPoints) {
FourPoints  otherFPoints;
otherFPoints = initFourPoints(otherFPoints);
if (mainPoints.length() != 4) {
    return otherFPoints;
}
otherFPoints[0] = QPoint((mainPoints[0].x() + mainPoints[1].x())/2,
                                              (mainPoints[0].y() + mainPoints[1].y())/2);
otherFPoints[1] = QPoint((mainPoints[0].x() + mainPoints[2].x())/2,
                                              (mainPoints[0].y() + mainPoints[2].y())/2);
otherFPoints[2] = QPoint((mainPoints[2].x() + mainPoints[3].x())/2,
                                              (mainPoints[2].y() + mainPoints[3].y())/2);
otherFPoints[3] = (QPoint((mainPoints[1].x() + mainPoints[3].x())/2,
                                              (mainPoints[1].y() + mainPoints[3].y())/2));
return otherFPoints;
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
qreal pointToLineDistance(QPointF point1, QPointF point2, QPointF point3) {
    if (point1.x() == point2.x()) {
        return std::abs(point3.x() - point1.x());
    } else {
        qreal k = (point1.y() - point2.y())/(point1.x() - point2.x());
        qreal b = point1.y() - point1.x() * k;
        return std::abs(point3.x() * k + b - point3.y()) / std::sqrt(std::pow(k, 2) + 1);
    }
}

/* judge the direction of point3 of line(point1, point2) */
qreal pointLineDir(QPointF point1, QPointF point2, QPointF point3) {
    if (point1.x() == point2.x()) {
        if (point3.x() <= point1.x()) {
            return -1;
        } else {
            return 1;
        }
    } else {
        qreal k = (point1.y() - point2.y()) / (point1.x() - point2.x());
        qreal b = point1.y() - point1.x() * k;
        if (point3.y() <= point3.x() * k + b) {
            return -1;
        } else {
            return 1;
        }
    }
 }

/* calculate the control point of the beizer */
QPointF getControlPoint(QPointF point1, QPointF point2, bool direction)  {
    qreal k1 = SLOPE;
    qreal k2 = 1 - SLOPE;
    qreal k3;

    if (direction) {
        k3 = k2/k1;
    } else {
        k3 = k1/k2;
    }
    QPointF resultPoint = QPoint((point1.x() + k3*point2.x())/(1+k3),
                                                         (point1.y() + k3*point2.y())/(1+k3));
    return resultPoint;
}

/* get eight control points */
QList<QPointF> getEightControlPoint(FourPoints rectFPoints) {
    FourPoints anotherFPoints = getAnotherFPoints(rectFPoints);

    QList<QPointF> resultPointList;
    resultPointList.append(getControlPoint(rectFPoints[0], anotherFPoints[0], true));
    resultPointList.append(getControlPoint(rectFPoints[0], anotherFPoints[1], true));
    resultPointList.append(getControlPoint(anotherFPoints[0], rectFPoints[1], false));
    resultPointList.append(getControlPoint(rectFPoints[1], anotherFPoints[3], true));
    resultPointList.append(getControlPoint(anotherFPoints[1], rectFPoints[2], false));
    resultPointList.append(getControlPoint(rectFPoints[2], anotherFPoints[2], true));
    resultPointList.append(getControlPoint(anotherFPoints[2], rectFPoints[3], false));
    resultPointList.append(getControlPoint(rectFPoints[3], anotherFPoints[3], true));

    return resultPointList;
}

/* judge whether the clickOnPoint is on the bezier */
/* 0 <= pos.x() <= 1*/
bool pointOnBezier(QPointF point1, QPointF point2, QPointF point3, QPointF point4, QPointF pos) {
    const int MIN_PADDING = 10;
    for (qreal t = 0; t <= 1; t = t + 0.1) {
        qreal bx = point1.x()*(1-t)*std::pow(1-t, 2) + 3*point2.x()*t*std::pow(1-t, 2)
                + 3*point3.x()*std::pow(t, 2)*(1-t) + point4.x()*t*std::pow(t, 2);
        qreal by = point1.y()*(1-t)*std::pow(1-t, 2) + 3*point2.y()*t*std::pow(1-t, 2)
                + 3*point3.y()*std::pow(t, 2)*(1-t) + point4.y()*t*std::pow(t, 2);
        if (pos.x() >= bx - MIN_PADDING && pos.x() <= bx + MIN_PADDING &&
                pos.y() >= by - MIN_PADDING && pos.y() <= by + MIN_PADDING) {
            return true;
        }
    }
    return false;
}

/* judge whether the clickOnPoint is on the ellipse */
bool pointOnEllipse(FourPoints rectFPoints, QPointF pos) {
    FourPoints anotherFPoints = getAnotherFPoints(rectFPoints);
    QList<QPointF> controlPointList;
    controlPointList.append(getControlPoint(rectFPoints[0], anotherFPoints[0], true));
    controlPointList.append(getControlPoint(rectFPoints[0], anotherFPoints[1], true));
    controlPointList.append(getControlPoint(anotherFPoints[0], rectFPoints[1], false));
    controlPointList.append(getControlPoint(rectFPoints[1], anotherFPoints[3], true));
    controlPointList.append(getControlPoint(anotherFPoints[1], rectFPoints[2], false));
    controlPointList.append(getControlPoint(rectFPoints[2], anotherFPoints[2], true));
    controlPointList.append(getControlPoint(anotherFPoints[2], rectFPoints[3], false));
    controlPointList.append(getControlPoint(rectFPoints[3], anotherFPoints[3], true));

    if (pointOnBezier(anotherFPoints[0], controlPointList[0], controlPointList[1],
        anotherFPoints[1], pos) || pointOnBezier(anotherFPoints[1], controlPointList[4],
      controlPointList[5], anotherFPoints[2], pos) || pointOnBezier(anotherFPoints[2],
      controlPointList[6], controlPointList[7], anotherFPoints[3], pos) || pointOnBezier(
      anotherFPoints[3], controlPointList[3], controlPointList[2], anotherFPoints[0], pos)) {
        return true;
    } else {
        return false;
    }
}

/* get the three points of arrow A/B/D */
QList<QPointF> pointOfArrow(QPointF startPoint, QPointF endPoint, qreal arrowLength) {
    qreal xMultiplier, yMultiplier;
    if (startPoint.x() == endPoint.x()) {
        xMultiplier = 1;
    } else {
        xMultiplier = (startPoint.x() - endPoint.x())/std::abs(startPoint.x() - endPoint.x());
    }

    if (startPoint.y() == endPoint.y()) {
        yMultiplier = 1;
    } else {
        yMultiplier = (startPoint.y() - endPoint.y())/std::abs(startPoint.y() - endPoint.y());
    }

    QPointF add = pointSplid(startPoint, endPoint, arrowLength );
    QPointF pointA = QPointF(endPoint.x() + xMultiplier*add.x(), endPoint.y() + yMultiplier*add.y());
    qreal angle = qreal(M_PI/6);
    QPointF pointB = pointRotate(endPoint, pointA, angle);
    QPointF pointD = pointRotate(endPoint, pointA,  angle*5+ M_PI);
    add = pointSplid(startPoint, endPoint, arrowLength );
    QPointF pointE = QPointF(endPoint.x() - xMultiplier*add.x(), endPoint.y() - yMultiplier*add.y());

    QList<QPointF> arrowPoints;
    arrowPoints.append(pointB);
    arrowPoints.append(pointD);
    arrowPoints.append(pointE);
    return arrowPoints;
}

/* judge whether the pos is on the points of arbitrary- curved*/
bool pointOnArLine(QList<QPointF> points, QPointF pos) {
    for(int i = 0; i < points.length(); i++) {
        if (pointClickIn(points[i], pos)) {
            return true;
        } else {
            continue;
        }
    }

    return false;
}

/* resize arbitrary curved */
QList<qreal> relativePosition(FourPoints mainPoints,  QPointF pos) {
    if (mainPoints.length() != 4) {
        return QList<qreal>();
    }
    qreal firstRelaPosit, secondRelaPosit;
    qreal distance12 = pointToLineDistance(mainPoints[0], mainPoints[1], pos);
    qreal distance34 = pointToLineDistance(mainPoints[2], mainPoints[3], pos);
    qreal distance13 = pointToLineDistance(mainPoints[0], mainPoints[2], pos);
    qreal distance24 = pointToLineDistance(mainPoints[1], mainPoints[3], pos);

    if (distance34 == 0) {
        firstRelaPosit = -2;
    } else {
        firstRelaPosit = distance12/distance34;
    }

    if (distance24 == 0) {
        secondRelaPosit = -2;
    } else {
        secondRelaPosit = distance13/distance24;
    }
    QList<qreal> relativePosit;
    relativePosit.append(0);
    relativePosit.append(0);
    relativePosit[0] = firstRelaPosit;
    relativePosit[1] = secondRelaPosit;
    return relativePosit;
}

QPointF           getNewPosition(FourPoints mainPoints, QList<qreal> re) {
    qreal changeX, changeY;

    if (re[0] == -2) {
        changeX = mainPoints[2].x();
        changeY = (mainPoints[0].y() + re[1]*mainPoints[1].y())/(1 + re[1]);
    }
    if (re[1] == -2) {
        changeX = (mainPoints[1].x() + re[0]*mainPoints[3].x())/(1 + re[0]);
        changeY = mainPoints[1].y();
    }
    if (re[0] != -2 && re[1] != -2) {
        QPointF pointi = QPointF((mainPoints[1].x() + re[0]*mainPoints[3].x())/(1 + re[0]),
                                                       (mainPoints[1].y() + re[0]*mainPoints[3].y())/(1 + re[0]));
        QPointF pointj = QPointF((mainPoints[0].x() + re[1]*mainPoints[1].x())/(1 + re[1]),
                                                       (mainPoints[0].y() + re[1]*mainPoints[1].y())/(1 + re[1]));
        if (mainPoints[0].x() == mainPoints[1].x()) {
            changeX = pointi.x();
            changeY = pointj.y();
        }
        if (mainPoints[0].x() == mainPoints[2].x()) {
            changeX = pointj.x();
            changeY = pointi.y();
        }
        if (mainPoints[0].x() != mainPoints[1].x() && mainPoints[0].x() != mainPoints[2].x()) {
            qreal k1 = (mainPoints[0].y() - mainPoints[1].y())/(mainPoints[0].x() - mainPoints[1].x());
            qreal b1 = pointi.y() - k1*pointi.x();

            qreal k2 = (mainPoints[0].y() - mainPoints[2].y())/(mainPoints[0].x() - mainPoints[2].x());
            qreal b2 = pointj.y() - k2*pointj.x();

            changeX = (b1 - b2)/(k2 - k1);
            changeY = changeX*k1 + b1;
        }
    }
    return QPointF(changeX, changeY);
}

/* init FourPoints*/
FourPoints initFourPoints(FourPoints fourPoints) {
    fourPoints.clear();
    fourPoints.append(QPointF(0, 0));
    fourPoints.append(QPointF(0, 0));
    fourPoints.append(QPointF(0, 0));
    fourPoints.append(QPointF(0, 0));
    return fourPoints;
}
/* handle resize of eight points in rectangle */
FourPoints resizePointPosition(QPointF point1, QPointF point2, QPointF point3, QPointF point4,
                          QPointF pos, int key,  bool isShift) {
    FourPoints resizeFPoints ;
    resizeFPoints = initFourPoints(resizeFPoints);
    resizeFPoints[0] = point1;
    resizeFPoints[1] = point2;
    resizeFPoints[2] = point3;
    resizeFPoints[3] = point4;

    if (point1.x() - point2.x() < 0 && point1.y() - point2.y() < 0 &&
    point1.x() - point3.x() < 0 && point1.y() - point3.y() > 0) {
        switch (key) {
        case 0: { resizeFPoints = point1Resize1(point1, point2, point3, point4, pos, isShift); return resizeFPoints;}
        case 1: { resizeFPoints = point2Resize1(point1, point2, point3, point4, pos, isShift); return resizeFPoints;}
        case 2: { resizeFPoints = point3Resize1(point1, point2, point3, point4, pos, isShift); return resizeFPoints;}
        case 3: { resizeFPoints = point4Resize1(point1, point2, point3, point4, pos, isShift); return resizeFPoints;}
        case 4: { resizeFPoints = point5Resize1(point1, point2, point3, point4, pos, isShift); return resizeFPoints;}
        case 5: { resizeFPoints = point6Resize1(point1, point2, point3, point4, pos, isShift); return resizeFPoints;}
        case 6: { resizeFPoints = point7Resize1(point1, point2, point3, point4, pos, isShift); return resizeFPoints;}
        case 7: { resizeFPoints = point8Resize1(point1, point2, point3, point4, pos, isShift); return resizeFPoints;}
        }
    }
    if (point1.x() - point2.x() < 0 && point1.y() - point2.y() > 0 &&
    point1.x() - point3.x() > 0 && point1.y() - point3.y() > 0) {
        switch(key) {
        case 0: { resizeFPoints = point1Resize2(point1, point2, point3, point4, pos, isShift); return resizeFPoints;}
        case 1: { resizeFPoints = point2Resize2(point1, point2, point3, point4, pos, isShift); return resizeFPoints;}
        case 2: { resizeFPoints = point3Resize2(point1, point2, point3, point4, pos, isShift); return resizeFPoints;}
        case 3: { resizeFPoints = point4Resize2(point1, point2, point3, point4, pos, isShift); return resizeFPoints;}
        case 4: { resizeFPoints = point5Resize2(point1, point2, point3, point4, pos, isShift); return resizeFPoints;}
        case 5: { resizeFPoints = point6Resize2(point1, point2, point3, point4, pos, isShift); return resizeFPoints;}
        case 6: { resizeFPoints = point7Resize2(point1, point2, point3, point4, pos, isShift); return resizeFPoints;}
        case 7: { resizeFPoints = point8Resize2(point1, point2, point3, point4, pos, isShift); return resizeFPoints;}
        }
    }
    if (point1.x() - point2.x() > 0 && point1.y() - point2.y() < 0 &&
    point1.x() - point3.x() < 0 && point1.y() - point3.y()) {
        switch(key) {
        case 0: { resizeFPoints = point1Resize3(point1, point2, point3, point4, pos, isShift); return resizeFPoints;}
        case 1: { resizeFPoints = point2Resize3(point1, point2, point3, point4, pos, isShift); return resizeFPoints;}
        case 2: { resizeFPoints = point3Resize3(point1, point2, point3, point4, pos, isShift); return resizeFPoints;}
        case 3: { resizeFPoints = point4Resize3(point1, point2, point3, point4, pos, isShift); return resizeFPoints;}
        case 4: { resizeFPoints = point5Resize3(point1, point2, point3, point4, pos, isShift); return resizeFPoints;}
        case 5: { resizeFPoints = point6Resize3(point1, point2, point3, point4, pos, isShift); return resizeFPoints;}
        case 6: { resizeFPoints = point7Resize3(point1, point2, point3, point4, pos, isShift); return resizeFPoints;}
        case 7: { resizeFPoints = point8Resize3(point1, point2, point3, point4, pos, isShift); return resizeFPoints;}
        }
    }
    if (point1.x() - point2.x() > 0 && point1.y() - point2.y() > 0 &&
    point1.x() - point3.x() > 0 && point1.y() - point3.y() < 0) {
        switch(key) {
        case 0: { resizeFPoints = point1Resize4(point1, point2, point3, point4, pos, isShift); return resizeFPoints;}
        case 1: { resizeFPoints = point2Resize4(point1, point2, point3, point4, pos, isShift); return resizeFPoints;}
        case 2: { resizeFPoints = point3Resize4(point1, point2, point3, point4, pos, isShift); return resizeFPoints;}
        case 3: { resizeFPoints = point4Resize4(point1, point2, point3, point4, pos, isShift); return resizeFPoints;}
        case 4: { resizeFPoints = point5Resize4(point1, point2, point3, point4, pos, isShift); return resizeFPoints;}
        case 5: { resizeFPoints = point6Resize4(point1, point2, point3, point4, pos, isShift); return resizeFPoints;}
        case 6: { resizeFPoints = point7Resize4(point1, point2, point3, point4, pos, isShift); return resizeFPoints;}
        case 7: { resizeFPoints = point8Resize4(point1, point2, point3, point4, pos, isShift); return resizeFPoints;}
        }
    }
    if (point1.x() == point2.x() && point1.y() < point2.y() &&
    point1.x() < point3.x() && point1.y() == point3.y()) {
        switch(key) {
        case 0: { resizeFPoints = point1Resize5(point1, point2, point3, point4, pos, isShift); return resizeFPoints;}
        case 1: { resizeFPoints = point2Resize5(point1, point2, point3, point4, pos, isShift); return resizeFPoints;}
        case 2: { resizeFPoints = point3Resize5(point1, point2, point3, point4, pos, isShift); return resizeFPoints;}
        case 3: { resizeFPoints = point4Resize5(point1, point2, point3, point4, pos, isShift); return resizeFPoints;}
        case 4: { resizeFPoints = point5Resize5(point1, point2, point3, point4, pos, isShift); return resizeFPoints;}
        case 5: { resizeFPoints = point6Resize5(point1, point2, point3, point4, pos, isShift); return resizeFPoints;}
        case 6: { resizeFPoints = point7Resize5(point1, point2, point3, point4, pos, isShift); return resizeFPoints;}
        case 7: { resizeFPoints = point8Resize5(point1, point2, point3, point4, pos, isShift); return resizeFPoints;}
        }
    }
    if (point1.x() < point2.x() && point1.y() == point2.y() &&
    point1.x() == point3.x() && point1.y() < point3.y()) {
        switch(key) {
        case 0: { resizeFPoints = point1Resize6(point1, point2, point3, point4, pos, isShift); return resizeFPoints;}
        case 1: { resizeFPoints = point2Resize6(point1, point2, point3, point4, pos, isShift); return resizeFPoints;}
        case 2: { resizeFPoints = point3Resize6(point1, point2, point3, point4, pos, isShift); return resizeFPoints;}
        case 3: { resizeFPoints = point4Resize6(point1, point2, point3, point4, pos, isShift); return resizeFPoints;}
        case 4: { resizeFPoints = point5Resize6(point1, point2, point3, point4, pos, isShift); return resizeFPoints;}
        case 5: { resizeFPoints = point6Resize6(point1, point2, point3, point4, pos, isShift); return resizeFPoints;}
        case 6: { resizeFPoints = point7Resize6(point1, point2, point3, point4, pos, isShift); return resizeFPoints;}
        case 7: { resizeFPoints = point8Resize6(point1, point2, point3, point4, pos, isShift); return resizeFPoints;}
        }
    }
    if (point1.x() < point2.x() && point1.y() == point2.y() &&
    point1.x() == point3.x() && point1.y() > point3.y()) {
        switch(key) {
        case 0: { resizeFPoints = point1Resize7(point1, point2, point3, point4, pos, isShift); return resizeFPoints;}
        case 1: { resizeFPoints = point2Resize7(point1, point2, point3, point4, pos, isShift); return resizeFPoints;}
        case 2: { resizeFPoints = point3Resize7(point1, point2, point3, point4, pos, isShift); return resizeFPoints;}
        case 3: { resizeFPoints = point4Resize7(point1, point2, point3, point4, pos, isShift); return resizeFPoints;}
        case 4: { resizeFPoints = point5Resize7(point1, point2, point3, point4, pos, isShift); return resizeFPoints;}
        case 5: { resizeFPoints = point6Resize7(point1, point2, point3, point4, pos, isShift); return resizeFPoints;}
        case 6: { resizeFPoints = point7Resize7(point1, point2, point3, point4, pos, isShift); return resizeFPoints;}
        case 7: { resizeFPoints = point8Resize7(point1, point2, point3, point4, pos, isShift); return resizeFPoints;}
        }
    }
    return resizeFPoints;
}

/* first point1 */
/* point1 in the first position*/
FourPoints point1Resize1(QPointF point1, QPointF point2, QPointF point3,
                         QPointF point4, QPointF pos, bool isShift) {
    FourPoints newResizeFPoints;
    newResizeFPoints = initFourPoints(newResizeFPoints);
    newResizeFPoints[0] = point1;
    newResizeFPoints[1] = point2;
    newResizeFPoints[2] = point3;
    newResizeFPoints[3] = point4;

    if (std::atan2((point2.y() - point1.y()), (point2.x() - point1.x())) >= TANT_EDGEVALUE &&
    (pos.y() + MIN_PADDING > point2.y() || pos.x() + MIN_PADDING > point3.x() ||
     pointLineDir(point3, point4, pos) == -1 || pointLineDir(point2, point4, pos) == 1)) {
        return newResizeFPoints;
    } else if (std::atan2((point2.y() - point1.y()), (point2.x() - point1.x())) < TANT_EDGEVALUE &&
      (pos.x() + MIN_PADDING > point2.x() || pos.y() - MIN_PADDING < point3.y() ||
       pointLineDir(point3, point4, pos) == -1 || pointLineDir(point2, point4, pos) == 1)) {
        return newResizeFPoints;
    }  else {
        if (pointToLineDistance(point4, point2, pos) < MIN_PADDING ||
                pointToLineDistance(point3, point4, pos) < MIN_PADDING) {
            return newResizeFPoints;
        } else {
            if (!isShift) {
                if (pointLineDir(point1, point3, pos) == -1 && pointLineDir(point1, point2, pos) == 1) {
                    qreal distance= pointToLineDistance(point1, point2, pos);
                    QPointF add = pointSplid(point2, point4, distance);
                    point2 = QPointF(point2.x() - add.x(), point2.y() + add.y());
                    distance = pointToLineDistance(point1, point3, pos);
                    add = pointSplid(point3, point4, distance);
                    point3 = QPointF(point3.x() - add.x(), point3.y() - add.y());
                    point1 = pos;
                }
                if (pointLineDir(point1, point3, pos) == -1 && pointLineDir(point1, point2, pos) == -1) {
                    qreal distance= pointToLineDistance(point1, point2, pos);
                    QPointF add = pointSplid(point2, point4, distance);
                    point2 = QPointF(point2.x() + add.x(), point2.y() - add.y());
                    distance = pointToLineDistance(point1, point3, pos);
                    add = pointSplid(point3, point4, distance);
                    point3 = QPointF(point3.x() - add.x(), point3.y() - add.y());
                    point1 = pos;
                }
                if (pointLineDir(point1, point3, pos) == 1 && pointLineDir(point1, point2, pos) == -1) {
                    qreal distance= pointToLineDistance(point1, point2, pos);
                    QPointF add = pointSplid(point2, point4, distance);
                    point2 = QPointF(point2.x() + add.x(), point2.y() - add.y());
                    distance = pointToLineDistance(point1, point3, pos);
                    add = pointSplid(point3, point4, distance);
                    point3 = QPointF(point3.x() + add.x(), point3.y() + add.y());
                    point1 = pos;
                }
                if (pointLineDir(point1, point3, pos) == 1 && pointLineDir(point1, point2, pos) == 1) {
                    qreal distance= pointToLineDistance(point1, point2, pos);
                    QPointF add = pointSplid(point2, point4, distance);
                    point2 = QPointF(point2.x() - add.x(), point2.y() + add.y());
                    distance = pointToLineDistance(point1, point3, pos);
                    add = pointSplid(point3, point4, distance);
                    point3 = QPointF(point3.x() + add.x(), point3.y() + add.y());
                    point1 = pos;
                }
                newResizeFPoints[0] = point1;
                newResizeFPoints[1] = point2;
                newResizeFPoints[2] = point3;
                newResizeFPoints[3] = point4;
                return newResizeFPoints;
            } else {
                 qreal distance1 = pointToLineDistance(point1, point2, pos);
                 qreal distance2 = pointToLineDistance(point1, point3, pos);
                 qreal distance = std::min(distance1, distance2);
                if (pointLineDir(point1, point3, pos) == 1 && pointLineDir(point1, point2, pos) == -1) {
                    QPointF add = pointSplid(point2, point4, distance);
                    point2 = QPointF(point2.x() + add.x(), point2.y() - add.y());
                    add = pointSplid(point3, point4, distance);
                    point3 = QPointF(point3.x() + add.x(), point3.y() + add.y());
                    point1 = QPointF(point2.x() + point3.x() - point4.x(), point2.y() + point3.y() - point4.y());
                } else {
                    QPointF add = pointSplid(point2, point4, distance);
                    point2 = QPointF(point2.x() - add.x(), point2.y() + add.y());
                    add = pointSplid(point3, point4, distance);
                    point3 = QPointF(point3.x() - add.x(), point3.y() - add.y());
                    point1 = QPointF(point2.x() + point3.x() - point4.x(), point2.y() + point3.y() - point4.y());
                }
                newResizeFPoints[0] = point1;
                newResizeFPoints[1] = point2;
                newResizeFPoints[2] = point3;
                newResizeFPoints[3] = point4;
                return newResizeFPoints;
            }
            return newResizeFPoints;
        }
    }
}

/* point1 in the second position */
FourPoints point1Resize2(QPointF point1, QPointF point2, QPointF point3,
                         QPointF point4, QPointF pos, bool isShift) {
    FourPoints newResizeFPoints;
    newResizeFPoints = initFourPoints(newResizeFPoints);
    newResizeFPoints[0] = point1;
    newResizeFPoints[1] = point2;
    newResizeFPoints[2] = point3;
    newResizeFPoints[3] = point4;

    if (std::atan2((point2.y() - point1.y()), (point2.x() - point1.x())) <= -TANT_EDGEVALUE
    && (pos.y() - MIN_PADDING < point2.y() || pos.x() - MIN_PADDING < point3.x() ||
        pointLineDir(point3, point4, pos) == -1 || pointLineDir(point2, point4, pos) == -1)) {
        return newResizeFPoints;
    } else if (std::atan2((point2.y() - point1.y()), (point2.x() - point1.x())) > -TANT_EDGEVALUE
    && (pos.y() - MIN_PADDING < point3.y() || pos.x() + MIN_PADDING > point2.x() ||
    pointLineDir(point3, point4, pos) == -1 || pointLineDir(point2, point4, pos) == -1))  {
        return newResizeFPoints;
    } else {
        if (!isShift) {
            if (pointLineDir(point1, point3, pos) == 1 && pointLineDir(point1, point2, pos) == 1) {
                qreal distance = pointToLineDistance(point1, point2, pos);
                QPointF add = pointSplid(point2, point4, distance);
                point2 = QPointF(point2.x() + add.x(), point2.y() + add.y());
                distance = pointToLineDistance(point1, point3, pos);
                add = pointSplid(point3, point4, distance);
                point3 = QPointF(point3.x() - add.x(), point3.y() + add.y());
                point1 = pos;
            }
            if (pointLineDir(point1, point3, pos) == 1 && pointLineDir(point1, point2, pos) == -1) {
                qreal distance = pointToLineDistance(point1, point2, pos);
                QPointF add = pointSplid(point2, point4, distance);
                point2 = QPointF(point2.x() - add.x(), point2.y() - add.y());
                distance = pointToLineDistance(point1, point3, pos);
                add = pointSplid(point3, point4, distance);
                point3 = QPointF(point3.x() - add.x(), point3.y() + add.y());
                point1 = pos;
            }
            if (pointLineDir(point1, point3, pos) == -1 && pointLineDir(point1, point2, pos) == -1) {
                qreal distance = pointToLineDistance(point1, point2, pos);
                QPointF add = pointSplid(point2, point4, distance);
                point2 = QPointF(point2.x() - add.x(), point2.y() - add.y());
                distance = pointToLineDistance(point1, point3, pos);
                add = pointSplid(point3, point4, distance);
                point3 = QPointF(point3.x() + add.x(), point3.y() - add.y());
                point1 = pos;
            }
            if (pointLineDir(point1, point3, pos) == -1 && pointLineDir(point1, point2, pos) == 1) {
                qreal distance = pointToLineDistance(point1, point2, pos);
                QPointF add = pointSplid(point2, point4, distance);
                point2 = QPointF(point2.x() + add.x(), point2.y() + add.y());
                distance = pointToLineDistance(point1, point3, pos);
                add = pointSplid(point3, point4, distance);
                point3 = QPointF(point3.x() + add.x(), point3.y() - add.y());
                point1 = pos;
            }
            newResizeFPoints[0] = point1;
            newResizeFPoints[1] = point2;
            newResizeFPoints[2] = point3;
            newResizeFPoints[3] = point4;
            return newResizeFPoints;
        } else {
            qreal distance1 = pointToLineDistance(point1, point2, pos);
            qreal distance2 = pointToLineDistance(point1, point3, pos);
            qreal distance = std::min(distance1, distance2);
            if (pointLineDir(point1, point2, pos) == -1 && pointLineDir(point1, point2, pos) == -1) {
                QPointF add = pointSplid(point2, point4, distance);
                point2 = QPointF(point2.x() - add.x(), point2.y() - add.y());
                add = pointSplid(point3, point4, distance);
                point3 = QPointF(point3.x() + add.x(), point3.y() - add.y());
                point1 = QPointF(point2.x() + point3.x() - point4.x(), point2.y() + point3.y() - point4.y());
            } else {
                QPointF add = pointSplid(point2, point4, distance);
                point2 = QPointF(point2.x() + add.x(), point2.y() + add.y());
                add = pointSplid(point3, point4, distance);
                point3 = QPointF(point3.x() - add.x(), point3.y() + add.y());
                point1 = QPointF(point2.x() + point3.x() - point4.x(), point2.y() + point3.y() - point4.y());
            }
            newResizeFPoints[0] = point1;
            newResizeFPoints[1] = point2;
            newResizeFPoints[2] = point3;
            newResizeFPoints[3] = point4;
            return newResizeFPoints;
        }
    }
    return newResizeFPoints;
}

/* point1 in the third position*/
FourPoints point1Resize3(QPointF point1, QPointF point2, QPointF point3,
                         QPointF point4, QPointF pos, bool isShift) {
    FourPoints newResizeFPoints;
    newResizeFPoints = initFourPoints(newResizeFPoints);
    newResizeFPoints[0] = point1;
    newResizeFPoints[1] = point2;
    newResizeFPoints[2] = point3;
    newResizeFPoints[3] = point4;

    if (std::atan2((point2.y() - point1.y()), (point2.x() - point1.x())) >= TANT2_EDGEVALUE
    && (pos.x() - MIN_PADDING < point2.x() || pos.y() + MIN_PADDING > point3.y() ||
        pointLineDir(point3, point4, pos) == 1 || pointLineDir(point2, point4, pos) == 1)) {
        return newResizeFPoints;
    } else if (std::atan2((point2.y() - point1.y()), (point2.x() - point1.x())) < TANT2_EDGEVALUE
    && (pos.x() + MIN_PADDING > point3.x() || pos.y() + MIN_PADDING > point2.y() ||
       pointLineDir(point3, point4, pos) == 1 || pointLineDir(point2, point4, pos) == 1)) {
        return newResizeFPoints;
    } else {
        if (pointToLineDistance(point4, point2, pos) < MIN_PADDING || pointToLineDistance(point3,
            point4, pos) < MIN_PADDING) {
            return newResizeFPoints;
        } else {
            if (!isShift) {
                if (pointLineDir(point1, point3, pos) == -1 && pointLineDir(point1, point2, pos) == -1) {
                    qreal distance = pointToLineDistance(point1, point2, pos);
                    QPointF add = pointSplid(point2, point4, distance);
                    point2 = QPointF(point2.x() - add.x(), point2.y() - add.y());
                    distance = pointToLineDistance(point1, point3, pos);
                    add = pointSplid(point3, point4, distance);
                    point3 = QPointF(point3.x() + add.x(), point3.y() - add.y());
                    point1 = pos;
                }
                if (pointLineDir(point1, point3, pos) == -1 && pointLineDir(point1, point2, pos) == 1) {
                    qreal distance = pointToLineDistance(point1, point2, pos);
                    QPointF add = pointSplid(point2, point4, distance);
                    point2 = QPointF(point2.x() + add.x(), point2.y() + add.y());
                    distance = pointToLineDistance(point1, point3, pos);
                    add = pointSplid(point3, point4, distance);
                    point3 = QPointF(point3.x() + add.x(), point3.y() - add.y());
                    point1 = pos;
                }
                if (pointLineDir(point1, point3, pos) == 1 && pointLineDir(point1, point2, pos) == 1) {
                    qreal distance = pointToLineDistance(point1, point2, pos);
                    QPointF add = pointSplid(point2, point4, distance);
                    point2 = QPointF(point2.x() + add.x(), point2.y() + add.y());
                    distance = pointToLineDistance(point1, point3, pos);
                    add = pointSplid(point3, point4, distance);
                    point3 = QPointF(point3.x() - add.x(), point3.y() + add.y());
                    point1 = pos;
                }
                if (pointLineDir(point1, point3, pos) == 1 && pointLineDir(point1, point2, pos) == -1) {
                    qreal distance = pointToLineDistance(point1, point2, pos);
                    QPointF add = pointSplid(point2, point4, distance);
                    point2 = QPointF(point2.x() - add.x(), point2.y() - add.y());
                    distance = pointToLineDistance(point1, point3, pos);
                    add = pointSplid(point3, point4, distance);
                    point3 = QPointF(point3.x() - add.x(), point3.y() + add.y());
                    point1 = pos;
                }
                newResizeFPoints[0] = point1;
                newResizeFPoints[1] = point2;
                newResizeFPoints[2] = point3;
                newResizeFPoints[3] = point4;
                return newResizeFPoints;
            } else {
                qreal distance1 = pointToLineDistance(point1, point2, pos);
                qreal distance2 = pointToLineDistance(point1, point3, pos);
                qreal distance = std::min(distance1, distance2);
                if (pointLineDir(point1, point3, pos) == 1 && pointLineDir(point1, point2, pos) == 1) {
                    QPointF add = pointSplid(point2, point4, distance);
                    point2 = QPointF(point2.x() + add.x(), point2.y() + add.y());
                    add = pointSplid(point3, point4, distance);
                    point3 = QPointF(point3.x() - add.x(), point3.y() + add.y());
                } else {
                    QPointF add = pointSplid(point2, point4, distance);
                    point2 = QPointF(point2.x() - add.x(), point2.y() - add.y());
                    add = pointSplid(point3, point4, distance);
                    point3 = QPointF(point3.x() + add.x(), point3.y() - add.y());
                }
                point1 = QPointF(point2.x() + point3.x() - point4.x(), point2.y() + point3.y() - point4.y());
                newResizeFPoints[0] = point1;
                newResizeFPoints[1] = point2;
                newResizeFPoints[2] = point3;
                newResizeFPoints[3] = point4;
                return newResizeFPoints;
            }
        }
        return newResizeFPoints;
    }
}

/* point1 in the fourth position */
FourPoints point1Resize4(QPointF point1, QPointF point2, QPointF point3,
                         QPointF point4, QPointF pos, bool isShift) {
    FourPoints newResizeFPoints;
    newResizeFPoints = initFourPoints(newResizeFPoints);
    newResizeFPoints[0] = point1;
    newResizeFPoints[1] = point2;
    newResizeFPoints[2] = point3;
    newResizeFPoints[3] = point4;

    if (std::atan2((point2.y() - point1.y()), (point2.x() - point1.x())) >= -TANT2_EDGEVALUE
    && (pos.y() - MIN_PADDING < point2.y() || pos.x() - MIN_PADDING < point3.x() ||
    pointLineDir(point3, point4, pos) == 1 || pointLineDir(point2, point4, pos) == -1)) {
        return newResizeFPoints;
    } else if (std::atan2((point2.y() - point1.y()), (point2.x() - point1.x())) < - TANT2_EDGEVALUE
    && (pos.y() + MIN_PADDING > point3.y() || pos.x() - MIN_PADDING < point2.x() ||
    pointLineDir(point3, point4, pos) == 1 || pointLineDir(point2, point4, pos) == -1)) {
        return newResizeFPoints;
    } else {
        if (pointToLineDistance(point4, point2, pos) < MIN_PADDING ||
                pointToLineDistance(point3, point4, pos) < MIN_PADDING) {
            return newResizeFPoints;
        } else {
            if (!isShift) {
                if (pointLineDir(point1, point3, pos) == 1 && pointLineDir(point1, point2, pos) == -1) {
                    qreal distance = pointToLineDistance(point1, point2, pos);
                    QPointF add  = pointSplid(point2, point4, distance);
                    point2 = QPointF(point2.x() + add.x(), point2.y() - add.y());
                    distance  = pointToLineDistance(point1, point3, pos);
                    add = pointSplid(point3, point4, distance);
                    point3 = QPointF(point3.x() + add.x(), point3.y() + add.y());
                    point1 = pos;
                }
                if (pointLineDir(point1, point3, pos) == -1 && pointLineDir(point1, point2, pos) == -1) {
                    qreal distance = pointToLineDistance(point1, point2, pos);
                    QPointF add  = pointSplid(point2, point4, distance);
                    point2 = QPointF(point2.x() + add.x(), point2.y() - add.y());
                    distance  = pointToLineDistance(point1, point3, pos);
                    add = pointSplid(point3, point4, distance);
                    point3 = QPointF(point3.x() - add.x(), point3.y() - add.y());
                    point1 = pos;
                }
                if (pointLineDir(point1, point3, pos) == -1 && pointLineDir(point1, point2, pos) == 1) {
                    qreal distance = pointToLineDistance(point1, point2, pos);
                    QPointF add  = pointSplid(point2, point4, distance);
                    point2 = QPointF(point2.x() - add.x(), point2.y() + add.y());
                    distance  = pointToLineDistance(point1, point3, pos);
                    add = pointSplid(point3, point4, distance);
                    point3 = QPointF(point3.x() - add.x(), point3.y() - add.y());
                    point1 = pos;
                }
                if (pointLineDir(point1, point3, pos) == 1 && pointLineDir(point1, point2, pos) == 1) {
                    qreal distance = pointToLineDistance(point1, point2, pos);
                    QPointF add  = pointSplid(point2, point4, distance);
                    point2 = QPointF(point2.x() - add.x(), point2.y() + add.y());
                    distance  = pointToLineDistance(point1, point3, pos);
                    add = pointSplid(point3, point4, distance);
                    point3 = QPointF(point3.x() + add.x(), point3.y() + add.y());
                    point1 = pos;
                }
                newResizeFPoints[0] = point1;
                newResizeFPoints[1] = point2;
                newResizeFPoints[2] = point3;
                newResizeFPoints[3] = point4;
                return newResizeFPoints;
            } else {
                qreal distance1 = pointToLineDistance(point1, point2, pos);
                qreal distance2 = pointToLineDistance(point1, point3, pos);
                qreal distance = std::min(distance1, distance2);
               if (pointLineDir(point1, point3, pos) == -1 &&pointLineDir(point1, point2, pos) == 1) {
                   QPointF add = pointSplid(point2, point4, distance);
                   point2 = QPointF(point2.x() - add.x(), point2.y() + add.y());
                   add = pointSplid(point3, point4, distance);
                   point3 = QPointF(point3.x() - add.x(), point3.y() - add.y());
               } else {
                   QPointF add = pointSplid(point2, point4, distance);
                   point2 = QPointF(point2.x() + add.x(), point2.y() - add.y());
                   add = pointSplid(point3, point4, distance);
                   point3 = QPointF(point3.x() + add.x(), point3.y() + add.y());
               }
               point1 = QPointF(point2.x() + point3.x() - point4.x(),
                               point2.y() + point3.y() - point4.y());
               newResizeFPoints[0] = point1;
               newResizeFPoints[1] = point2;
               newResizeFPoints[2] = point3;
               newResizeFPoints[3] = point4;
               return newResizeFPoints;
            }
        }
    }
    return newResizeFPoints;
}

/* point1 in the fifth position */
FourPoints point1Resize5(QPointF point1, QPointF point2, QPointF point3,
                         QPointF point4, QPointF pos, bool isShift) {
    FourPoints newResizeFPoints;
    newResizeFPoints = initFourPoints(newResizeFPoints);
    newResizeFPoints[0] = point1;
    newResizeFPoints[1] = point2;
    newResizeFPoints[2] = point3;
    newResizeFPoints[3] = point4;

    if (pos.y() + MIN_PADDING > point2.y() || pos.x() + MIN_PADDING > point3.x()) {
        return newResizeFPoints;
    } else {
        qreal distanceLeft = pointToLineDistance(point1, point2, pos);
        QPointF addLeft = pointSplid(point2, point4, distanceLeft);
        qreal distanceRight = pointToLineDistance(point1, point3, pos);
        QPointF addRight = pointSplid(point3, point4, distanceRight);
        if (!isShift) {
            if (pointLineDir(point1, point3, pos) == -1 && pointLineDir(point1, point2, pos) == -1) {
                point2 = QPointF(point2.x() - addLeft.x(), point2.y() + addLeft.y());
                point3 = QPointF(point3.x() - addRight.x(), point3.y() - addRight.y());
                point1 = pos;
            }
            if (pointLineDir(point1, point3, pos) == -1 && pointLineDir(point1, point2, pos) == 1) {
                point2 = QPointF(point2.x() + addLeft.x(), point2.y() - addLeft.y());
                point3 = QPointF(point3.x() - addRight.x(), point3.y() - addRight.y());
                point1 = pos;
            }
            if (pointLineDir(point1, point3, pos) == 1 && pointLineDir(point1, point2, pos) == 1) {
                point2 = QPointF(point2.x() + addLeft.x(), point2.y() - addLeft.y());
                point3 = QPointF(point3.x() + addRight.x(), point3.y() + addRight.y());
                point1 = pos;
            }
            if (pointLineDir(point1, point3, pos) == 1 && pointLineDir(point1, point2, pos) == -1) {
                point2 = QPointF(point2.x() - addLeft.x(), point2.y() + addLeft.y());
                point3 = QPointF(point3.x() + addRight.x(), point3.y() + addRight.y());
                point1 = pos;
            }
            newResizeFPoints[0] = point1;
            newResizeFPoints[1] = point2;
            newResizeFPoints[2] = point3;
            newResizeFPoints[3] = point4;
            return newResizeFPoints;
        } else {
            qreal distance = std::min(distanceLeft, distanceRight);
            QPointF addLeft = pointSplid(point2, point4, distance);
            QPointF addRight = pointSplid(point3, point4, distance);
            if (pointLineDir(point1, point3, pos) == 1 && pointLineDir(point1, point2, pos) == 1) {
                point2 = QPointF(point2.x() + addLeft.x(), point2.y() +  addLeft.y());
                point3 = QPointF(point3.x() + addRight.x(), point3.y() + addRight.y());
            } else {
                point2 = QPointF(point2.x() - addLeft.x(), point2.y() -  addLeft.y());
                point3 = QPointF(point3.x() - addRight.x(), point3.y() - addRight.y());
            }
            point1 = QPointF(point2.x() + point3.x() - point4.x(), point2.y() + point3.y() - point4.y());
            newResizeFPoints[0] = point1;
            newResizeFPoints[1] = point2;
            newResizeFPoints[2] = point3;
            newResizeFPoints[3] = point4;
            return newResizeFPoints;
        }
    }
    return newResizeFPoints;
}

/* point1 in the sixth position */
FourPoints point1Resize6(QPointF point1, QPointF point2, QPointF point3,
                         QPointF point4, QPointF pos, bool isShift) {
    Q_UNUSED(pos);
    Q_UNUSED(isShift);
    FourPoints newResizeFPoints;
    newResizeFPoints = initFourPoints(newResizeFPoints);
    newResizeFPoints[0] = point1;
    newResizeFPoints[1] = point2;
    newResizeFPoints[2] = point3;
    newResizeFPoints[3] = point4;
    return newResizeFPoints;
}

/* point1 in the seventh position */
FourPoints point1Resize7(QPointF point1, QPointF point2, QPointF point3,
                         QPointF point4, QPointF pos, bool isShift) {
    Q_UNUSED(pos);
    Q_UNUSED(isShift);
    FourPoints newResizeFPoints;
    newResizeFPoints = initFourPoints(newResizeFPoints);
    newResizeFPoints[0] = point1;
    newResizeFPoints[1] = point2;
    newResizeFPoints[2] = point3;
    newResizeFPoints[3] = point4;
    return newResizeFPoints;
}

/***************** second point2 *******************/
/* point2 in the first position */
FourPoints point2Resize1(QPointF point1, QPointF point2, QPointF point3,
                         QPointF point4, QPointF pos, bool isShift) {
    FourPoints newResizeFPoints;
    newResizeFPoints = initFourPoints(newResizeFPoints);
    newResizeFPoints[0] = point1;
    newResizeFPoints[1] = point2;
    newResizeFPoints[2] = point3;
    newResizeFPoints[3] = point4;

    if (std::atan2((point2.y() - point1.y()), (point2.x() - point1.x())) >= TANT_EDGEVALUE
    && (pos.x() + MIN_PADDING > point4.x() || pos.y() - MIN_PADDING < point1.y() ||
    pointLineDir(point1, point3, pos) == -1 || pointLineDir(point3, point4, pos) == -1)) {
        return newResizeFPoints;
    } else if (std::atan2((point2.y() - point1.y()), (point2.x() - point1.x())) < TANT_EDGEVALUE
    && (pos.x() - MIN_PADDING < point1.x() || pos.y() - MIN_PADDING < point4.y() ||
        pointLineDir(point1, point3, pos) == -1 || pointLineDir(point3, point4, pos) == -1)) {
        return newResizeFPoints;
    } else {
        if (pointToLineDistance(point1, point3, pos) < MIN_PADDING ||
                pointToLineDistance(point3, point4, pos) < MIN_PADDING) {
            return newResizeFPoints;
        } else {
            if (!isShift) {
                if (pointLineDir(point1, point2, pos) == 1 && pointLineDir(point2, point4, pos) == 1) {
                    qreal distance = pointToLineDistance(point1, point2, pos);
                    QPointF add = pointSplid(point1, point3, distance);
                    point1 = QPointF(point1.x() - add.x(), point1.y() + add.y());
                    distance = pointToLineDistance(point2, point4, pos);
                    add = pointSplid(point3, point4, distance);
                    point4 = QPointF(point4.x() + add.x(), point4.y() + add.y());
                    point2 = pos;
                }
                if (pointLineDir(point1, point2, pos) == 1 && pointLineDir(point2, point4, pos) == -1) {
                    qreal distance = pointToLineDistance(point1, point2, pos);
                    QPointF add = pointSplid(point1, point3, distance);
                    point1 = QPointF(point1.x() - add.x(), point1.y() + add.y());
                    distance = pointToLineDistance(point2, point4, pos);
                    add = pointSplid(point3, point4, distance);
                    point4 = QPointF(point4.x() - add.x(), point4.y() - add.y());
                    point2 = pos;
                }
                if (pointLineDir(point1, point2, pos) == -1 && pointLineDir(point2,point4, pos) == -1) {
                    qreal distance = pointToLineDistance(point1, point2, pos);
                    QPointF add = pointSplid(point1, point3, distance);
                    point1 = QPointF(point1.x() + add.x(), point1.y() - add.y());
                    distance = pointToLineDistance(point2, point4, pos);
                    add = pointSplid(point3, point4, distance);
                    point4 = QPointF(point4.x() - add.x(), point4.y() - add.y());
                    point2 = pos;
                }
                if (pointLineDir(point1, point2, pos) == -1 && pointLineDir(point2, point4, pos) == 1) {
                    qreal distance = pointToLineDistance(point1, point2, pos);
                    QPointF add = pointSplid(point1, point3, distance);
                    point1 = QPointF(point1.x() + add.x(), point1.y() - add.y());
                    distance = pointToLineDistance(point2, point4, pos);
                    add = pointSplid(point3, point4, distance);
                    point4 = QPointF(point4.x() + add.x(), point4.y() + add.y());
                    point2 = pos;
                }
                newResizeFPoints[0] = point1;
                newResizeFPoints[1] = point2;
                newResizeFPoints[2] = point3;
                newResizeFPoints[3] = point4;
                return newResizeFPoints;
            } else {
                qreal distance1 = pointToLineDistance(point1, point2, pos);
                qreal distance2 = pointToLineDistance(point2, point4, pos);
                qreal distance = std::min(distance1, distance2);
                if (pointLineDir(point1, point2, pos) == -1 && pointLineDir(point2, point4, pos) == -1) {
                    QPointF add = pointSplid(point1, point3, distance);
                    point1 = QPointF(point1.x() + add.x(), point1.y() - add.y());
                    add = pointSplid(point3, point4, distance);
                    point4 = QPointF(point4.x() - add.x(), point4.y() - add.y());               
                } else {
                    QPointF add = pointSplid(point1, point3, distance);
                    point1 = QPointF(point1.x() - add.x(), point1.y() + add.y());
                    add = pointSplid(point3, point4, distance);
                    point4 = QPointF(point4.x() + add.x(), point4.y() + add.y());
                }
                point2 = QPointF(point1.x() + point4.x() - point3.x(), point1.y() + point4.y() - point3.y());
                newResizeFPoints[0] = point1;
                newResizeFPoints[1] = point2;
                newResizeFPoints[2] = point3;
                newResizeFPoints[3] = point4;
                return newResizeFPoints;
            }
        }
    }
    return newResizeFPoints;
}

/* point2 in the second position */
FourPoints point2Resize2(QPointF point1, QPointF point2, QPointF point3,
                         QPointF point4, QPointF pos, bool isShift) {
    FourPoints newResizeFPoints;
    newResizeFPoints = initFourPoints(newResizeFPoints);
    newResizeFPoints[0] = point1;
    newResizeFPoints[1] = point2;
    newResizeFPoints[2] = point3;
    newResizeFPoints[3] = point4;

    if (std::atan2((point2.y() - point1.y()), (point2.x() - point1.x())) <= -TANT_EDGEVALUE
    && (pos.y() + MIN_PADDING > point1.x() || pos.x() - MIN_PADDING < point4.x() ||
    pointLineDir(point1, point3, pos) == 1 || pointLineDir(point3, point4, pos) == -1)) {
        return newResizeFPoints;
    } else if (std::atan2((point2.y() - point1.y()), (point2.x() - point1.x())) > -TANT_EDGEVALUE
    && (pos.y() - MIN_PADDING < point4.y() || pos.x() - MIN_PADDING < point1.x() ||
        pointLineDir(point1, point3, pos) == 1 || pointLineDir(point3, point4, pos) == -1)) {
        return newResizeFPoints;
    } else {
        if (pointToLineDistance(point1, point3, pos) < MIN_PADDING ||
                pointToLineDistance(point3, point4, pos) < MIN_PADDING) {
            return newResizeFPoints;
        } else {
            if (!isShift) {
                if (pointLineDir(point1, point2, pos) == 1 && pointLineDir(point2, point4, pos) == -1) {
                    qreal distance = pointToLineDistance(point1, point2, pos);
                    QPointF add= pointSplid(point1, point3, distance);
                    point1 = QPointF(point1.x() + add.x(), point1.y() + add.y());
                    distance = pointToLineDistance(point2, point4, pos);
                    add = pointSplid(point3, point4, distance);
                    point4 = QPointF(point4.x() + add.x(), point4.y() - add.y());
                    point2 = pos;
                }
                if (pointLineDir(point1, point2, pos) == 1 && pointLineDir(point2, point4, pos) == 1) {
                    qreal distance = pointToLineDistance(point1, point2, pos);
                    QPointF add= pointSplid(point1, point3, distance);
                    point1 = QPointF(point1.x() + add.x(), point1.y() + add.y());
                    distance = pointToLineDistance(point2, point4, pos);
                    add = pointSplid(point3, point4, distance);
                    point4 = QPointF(point4.x() - add.x(), point4.y() + add.y());
                    point2 = pos;
                }
                if (pointLineDir(point1, point2, pos) == -1 && pointLineDir(point2, point4, pos) == 1) {
                    qreal distance = pointToLineDistance(point1, point2, pos);
                    QPointF add= pointSplid(point1, point3, distance);
                    point1 = QPointF(point1.x() - add.x(), point1.y() - add.y());
                    distance = pointToLineDistance(point2, point4, pos);
                    add = pointSplid(point3, point4, distance);
                    point4 = QPointF(point4.x() - add.x(), point4.y() + add.y());
                    point2 = pos;
                }
                if (pointLineDir(point1, point2, pos) == -1 && pointLineDir(point2, point4, pos) == -1) {
                    qreal distance = pointToLineDistance(point1, point2, pos);
                    QPointF add= pointSplid(point1, point3, distance);
                    point1 = QPointF(point1.x() - add.x(), point1.y() - add.y());
                    distance = pointToLineDistance(point2, point4, pos);
                    add = pointSplid(point3, point4, distance);
                    point4 = QPointF(point4.x() + add.x(), point4.y() - add.y());
                    point2 = pos;
                }
                newResizeFPoints[0] = point1;
                newResizeFPoints[1] = point2;
                newResizeFPoints[2] = point3;
                newResizeFPoints[3] = point4;
                return newResizeFPoints;
            } else {
                qreal distance1 = pointToLineDistance(point1, point2, pos);
                qreal distance2 = pointToLineDistance(point2, point4, pos);
                qreal distance = std::min(distance1, distance2);
                if (pointLineDir(point1, point2, pos) == -1 && pointLineDir(point2, point4, pos) == 1) {
                    QPointF add = pointSplid(point1, point3, distance);
                    point1 = QPointF(point1.x() - add.x(), point1.y() - add.y());
                    add = pointSplid(point3, point4, distance);
                    point4 = QPointF(point4.x() - add.x(), point4.y() + add.y());
                } else {
                    QPointF add = pointSplid(point1, point3, distance);
                    point1 = QPointF(point1.x() + add.x(), point1.y() + add.y());
                    add = pointSplid(point3, point4, distance);
                    point4 = QPointF(point4.x() + add.x(), point4.y() - add.y());
                }
                point2 = QPointF(point1.x() + point4.x() - point3.x(), point1.y() + point4.y() - point3.y());
                newResizeFPoints[0] = point1;
                newResizeFPoints[1] = point2;
                newResizeFPoints[2] = point3;
                newResizeFPoints[3] = point4;
                return newResizeFPoints;
            }
        }
    }
    return newResizeFPoints;
}

/* point2 in the third position */
FourPoints point2Resize3(QPointF point1, QPointF point2, QPointF point3,
                         QPointF point4, QPointF pos, bool isShift) {
    FourPoints newResizeFPoints;
    newResizeFPoints = initFourPoints(newResizeFPoints);
    newResizeFPoints[0] = point1;
    newResizeFPoints[1] = point2;
    newResizeFPoints[2] = point3;
    newResizeFPoints[3] = point4;

    if (std::atan2((point2.y() - point1.y()), (point2.x() - point1.x())) >= TANT2_EDGEVALUE
    && (pos.y() + MIN_PADDING > point4.y() || pos.x() + MIN_PADDING > point1.x() ||
    pointLineDir(point1, point3, pos) == -1 || pointLineDir(point3, point4, pos) == 1)) {
        return newResizeFPoints;
    } else if (std::atan2((point2.y() - point1.y()), (point2.x() - point1.x())) < TANT2_EDGEVALUE
    && (pos.y() - MIN_PADDING < point1.y() || pos.x() + MIN_PADDING > point4.x() ||
        pointLineDir(point1, point3, pos) == -1 || pointLineDir(point3, point4, pos) == 1)) {
        return newResizeFPoints;
    } else {
        if (pointToLineDistance(point1, point3, pos) < MIN_PADDING ||
                pointToLineDistance(point3, point4, pos) < MIN_PADDING) {
            return newResizeFPoints;
        } else {
            if (!isShift) {
                if (pointLineDir(point1, point2, pos) == -1 && pointLineDir(point2, point4, pos) == 1) {
                    qreal distance = pointToLineDistance(point1, point2, pos);
                    QPointF add = pointSplid(point1, point3, distance);
                    point1 = QPointF(point1.x() - add.x(), point1.y() - add.y());
                    distance = pointToLineDistance(point2, point4, pos);
                    add = pointSplid(point3, point4, distance);
                    point4 = QPointF(point4.x() - add.x(), point4.y() + add.y());
                    point2 = pos;
                }
                if (pointLineDir(point1, point2, pos) == -1 && pointLineDir(point2, point4, pos) == -1) {
                    qreal distance = pointToLineDistance(point1, point2, pos);
                    QPointF add = pointSplid(point1, point3, distance);
                    point1 = QPointF(point1.x() - add.x(), point1.y() - add.y());
                    distance = pointToLineDistance(point2, point4, pos);
                    add = pointSplid(point3, point4, distance);
                    point4 = QPointF(point4.x() + add.x(), point4.y() - add.y());
                    point2 = pos;
                }
                if (pointLineDir(point1, point2, pos) == 1 && pointLineDir(point2, point4, pos) == -1) {
                    qreal distance = pointToLineDistance(point1, point2, pos);
                    QPointF add = pointSplid(point1, point3, distance);
                    point1 = QPointF(point1.x() + add.x(), point1.y() + add.y());
                    distance = pointToLineDistance(point2, point4, pos);
                    add = pointSplid(point3, point4, distance);
                    point4 = QPointF(point4.x() + add.x(), point4.y() - add.y());
                    point2 = pos;
                }
                if (pointLineDir(point1, point2, pos) == 1&& pointLineDir(point2, point4, pos) == 1) {
                    qreal distance = pointToLineDistance(point1, point2, pos);
                    QPointF add = pointSplid(point1, point3, distance);
                    point1 = QPointF(point1.x() + add.x(), point1.y() + add.y());
                    distance = pointToLineDistance(point2, point4, pos);
                    add = pointSplid(point3, point4, distance);
                    point4 = QPointF(point4.x() - add.x(), point4.y() + add.y());
                    point2 = pos;
                }
                newResizeFPoints[0] = point1;
                newResizeFPoints[1] = point2;
                newResizeFPoints[2] = point3;
                newResizeFPoints[3] = point4;
                return newResizeFPoints;
            } else {
                qreal distance1 = pointToLineDistance(point1, point2, pos);
                qreal distance2 = pointToLineDistance(point2, point4, pos);
                qreal distance = std::min(distance1, distance2);
                if (pointLineDir(point1, point2, pos) == 1 && pointLineDir(point2, point4, pos) == -1) {
                    QPointF add = pointSplid(point1, point3, distance);
                    point1 = QPointF(point1.x() + add.x(), point1.y() + add.y());
                    add = pointSplid(point3, point4, distance);
                    point4 = QPointF(point4.x() + add.x(), point4.y() - add.y());
                } else {
                    QPointF add = pointSplid(point1, point3, distance);
                    point1 = QPointF(point1.x() - add.x(), point1.y() - add.y());
                    add = pointSplid(point3, point4, distance);
                    point4 = QPointF(point4.x() - add.x(), point4.y() + add.y());
                }
                point2 = QPointF(point1.x() + point4.x() - point3.x(), point1.y() + point4.y() - point3.y());
                newResizeFPoints[0] = point1;
                newResizeFPoints[1] = point2;
                newResizeFPoints[2] = point3;
                newResizeFPoints[3] = point4;
                return newResizeFPoints;
            }
        }
    }
    return newResizeFPoints;
}

/* point2 in the fourth position */
FourPoints point2Resize4(QPointF point1, QPointF point2, QPointF point3,
                         QPointF point4, QPointF pos, bool isShift) {
    FourPoints newResizeFPoints;
    newResizeFPoints = initFourPoints(newResizeFPoints);
    newResizeFPoints[0] = point1;
    newResizeFPoints[1] = point2;
    newResizeFPoints[2] = point3;
    newResizeFPoints[3] = point4;

    if (std::atan2((point2.y() - point1.y()), (point2.x() - point1.x())) >= -TANT2_EDGEVALUE
    && (pos.y() + MIN_PADDING > point1.y() || pos.x() - MIN_PADDING < point4.x() ||
    pointLineDir(point1, point3, pos) == 1 || pointLineDir(point3, point4, pos) == 1)) {
        return newResizeFPoints;
    } else if (std::atan2((point2.y() - point1.y()), (point2.x() - point1.x())) < -TANT2_EDGEVALUE
    && (pos.y() + MIN_PADDING > point4.y() || pos.x() + MIN_PADDING > point1.x() ||
        pointLineDir(point1, point3, pos) == 1 || pointLineDir(point3, point4, pos) == 1)) {
        return newResizeFPoints;
    } else {
        if (pointToLineDistance(point1, point3, pos) < MIN_PADDING ||
                pointToLineDistance(point3, point4, pos) < MIN_PADDING) {
            return newResizeFPoints;
        } else {
            if (!isShift) {
                if (pointLineDir(point1, point2, pos) == 1 && pointLineDir(point2, point4, pos) == 1) {
                    qreal distance = pointToLineDistance(point1, point2, pos);
                    QPointF add = pointSplid(point1, point3, distance);
                    point1 = QPointF(point1.x() - add.x(), point1.y() + add.y());
                    distance = pointToLineDistance(point2, point4, pos);
                    add = pointSplid(point3, point4, distance);
                    point4 = QPointF(point4.x() + add.x(), point4.y() + add.y());
                    point2 = pos;
                }
                if (pointLineDir(point1, point2, pos) == 1 && pointLineDir(point2, point4, pos) == -1) {
                    qreal distance = pointToLineDistance(point1, point2, pos);
                    QPointF add = pointSplid(point1, point3, distance);
                    point1 = QPointF(point1.x() - add.x(), point1.y() + add.y());
                    distance = pointToLineDistance(point2, point4, pos);
                    add = pointSplid(point3, point4, distance);
                    point4 = QPointF(point4.x() - add.x(), point4.y() - add.y());
                    point2 = pos;
                }
                if (pointLineDir(point1, point2, pos) == -1 && pointLineDir(point2, point4, pos) == 1) {
                    qreal distance = pointToLineDistance(point1, point2, pos);
                    QPointF add = pointSplid(point1, point3, distance);
                    point1 = QPointF(point1.x() + add.x(), point1.y() - add.y());
                    distance = pointToLineDistance(point2, point4, pos);
                    add = pointSplid(point3, point4, distance);
                    point4 = QPointF(point4.x() + add.x(), point4.y() + add.y());
                    point2 = pos;
                }
                if (pointLineDir(point1, point2, pos) == -1 && pointLineDir(point2, point4, pos) == -1) {
                    qreal distance = pointToLineDistance(point1, point2, pos);
                    QPointF add = pointSplid(point1, point3, distance);
                    point1 = QPointF(point1.x() + add.x(), point1.y() - add.y());
                    distance = pointToLineDistance(point2, point4, pos);
                    add = pointSplid(point3, point4, distance);
                    point4 = QPointF(point4.x() - add.x(), point4.y() - add.y());
                    point2 = pos;
                }
                newResizeFPoints[0] = point1;
                newResizeFPoints[1] = point2;
                newResizeFPoints[2] = point3;
                newResizeFPoints[3] = point4;
                return newResizeFPoints;
            } else {
                qreal distance1 = pointToLineDistance(point1, point2, pos);
                qreal distance2 = pointToLineDistance(point2, point4, pos);
                qreal distance = std::min(distance1, distance2);
                if (pointLineDir(point1, point2, pos) == 1 && pointLineDir(point2, point4, pos) == 1) {
                    QPointF add = pointSplid(point1, point3, distance);
                    point1 = QPointF(point1.x() - add.x(), point1.y() + add.y());
                    add = pointSplid(point3, point4, distance);
                    point4 = QPointF(point4.x() + add.x(), point4.y() + add.y());
                } else {
                    QPointF add = pointSplid(point1, point3, distance);
                    point1 = QPointF(point1.x() + add.x(), point1.y() - add.y());
                    add = pointSplid(point3, point4, distance);
                    point4 = QPointF(point4.x() - add.x(), point4.y() - add.y());
                }
                point2 = QPointF(point1.x() + point4.x() - point3.x(),
                                point1.y() + point4.y() - point3.y());
                newResizeFPoints[0] = point1;
                newResizeFPoints[1] = point2;
                newResizeFPoints[2] = point3;
                newResizeFPoints[3] = point4;
                return newResizeFPoints;
            }
        }
    }
    return newResizeFPoints;
}

/* point2 in the fifth position*/
FourPoints point2Resize5(QPointF point1, QPointF point2, QPointF point3,
                         QPointF point4, QPointF pos, bool isShift) {
    FourPoints newResizeFPoints;
    newResizeFPoints = initFourPoints(newResizeFPoints);
    newResizeFPoints[0] = point1;
    newResizeFPoints[1] = point2;
    newResizeFPoints[2] = point3;
    newResizeFPoints[3] = point4;

    if (pos.y() - MIN_PADDING < point1.y() || pos.x() + MIN_PADDING > point4.x()) {
        return newResizeFPoints;
    } else {
        if (!isShift) {
            point1.setX(pos.x());
            point4.setY(pos.y());
            point2 = pos;
            newResizeFPoints[0] = point1;
            newResizeFPoints[1] = point2;
            newResizeFPoints[2] = point3;
            newResizeFPoints[3] = point4;
            return newResizeFPoints;
        } else {
            qreal distance1 = pointToLineDistance(point1, point2, pos);
            qreal distance2 = pointToLineDistance(point2, point4, pos);
            qreal distance = std::min(distance1, distance2);
            if (pointLineDir(point1, point2, pos) == 1 && pointLineDir(point2, point4, pos) == -1) {
                QPointF add = pointSplid(point1, point3, distance);
                point1 = QPointF(point1.x() + add.x(), point1.y() - add.y());
                add = pointSplid(point3, point4, distance);
                point4 = QPointF(point4.x() - add.x(), point4.y() - add.y());
            } else {
                QPointF add = pointSplid(point1, point3, distance);
                point1 = QPointF(point1.x() - add.x(), point1.y() + add.y());
                add = pointSplid(point3, point4, distance);
                point4 = QPointF(point4.x() + add.x(), point4.y() + add.y());
            }
            point2 = QPointF(point1.x() + point4.x() - point3.x(),
                             point1.y() + point4.y() - point3.y());
            newResizeFPoints[0] = point1;
            newResizeFPoints[1] = point2;
            newResizeFPoints[2] = point3;
            newResizeFPoints[3] = point4;
            return newResizeFPoints;
        }
    }
    return newResizeFPoints;
}

/* point2 in the sixth position */
FourPoints point2Resize6(QPointF point1, QPointF point2, QPointF point3,
                         QPointF point4, QPointF pos, bool isShift) {
    Q_UNUSED(pos);
    Q_UNUSED(isShift);
    FourPoints newResizeFPoints;
    newResizeFPoints = initFourPoints(newResizeFPoints);
    newResizeFPoints[0] = point1;
    newResizeFPoints[1] = point2;
    newResizeFPoints[2] = point3;
    newResizeFPoints[3] = point4;
    return newResizeFPoints;
}

/* point2 in the seventh position */
FourPoints point2Resize7(QPointF point1, QPointF point2, QPointF point3,
                         QPointF point4, QPointF pos, bool isShift) {
    Q_UNUSED(pos);
    Q_UNUSED(isShift);
    FourPoints newResizeFPoints;
    newResizeFPoints = initFourPoints(newResizeFPoints);
    newResizeFPoints[0] = point1;
    newResizeFPoints[1] = point2;
    newResizeFPoints[2] = point3;
    newResizeFPoints[3] = point4;
    return newResizeFPoints;
}

/***************** third point3 *******************/
/* point3 in the first position */
FourPoints point3Resize1(QPointF point1, QPointF point2, QPointF point3,
                         QPointF point4, QPointF pos, bool isShift) {
    FourPoints newResizeFPoints;
    newResizeFPoints = initFourPoints(newResizeFPoints);
    newResizeFPoints[0] = point1;
    newResizeFPoints[1] = point2;
    newResizeFPoints[2] = point3;
    newResizeFPoints[3] = point4;

    if (std::atan2((point2.y() - point1.y()), (point2.x() - point1.x())) >= TANT_EDGEVALUE &&
    (pos.x() - MIN_PADDING < point1.x() || pos.y() + MIN_PADDING > point4.y() ||
     pointLineDir(point1, point2, pos) == 1 || pointLineDir(point2, point4, pos) == 1)) {
        return newResizeFPoints;
    } else if (std::atan2((point2.y() - point1.y()), (point2.x() - point1.x())) < TANT_EDGEVALUE &&
     (pos.x() + MIN_PADDING > point4.x() || pos.y() + MIN_PADDING > point1.y() ||
      pointLineDir(point1, point2, pos) == 1 || pointLineDir(point2, point4, pos) == 1)) {
        return newResizeFPoints;
    } else {
        if (pointToLineDistance(point2, point4, pos) < MIN_PADDING ||
                pointToLineDistance(point1, point2, pos) < MIN_PADDING) {
            return newResizeFPoints;
        } else {
            if (!isShift) {
                if (pointLineDir(point1, point3, pos) == -1 && pointLineDir(point3, point4, pos) == -1) {
                    qreal distance = pointToLineDistance(point3, point4, pos);
                    QPointF add = pointSplid(point2, point4, distance);
                    point4 = QPointF(point4.x() + add.x(), point4.y() - add.y());
                    distance = pointToLineDistance(point1, point3, pos);
                    add = pointSplid(point1, point2, distance);
                    point1 = QPointF(point1.x() - add.x(), point1.y() - add.y());
                    point3 = pos;
                }
                if (pointLineDir(point1, point3, pos) == -1 && pointLineDir(point3, point4, pos) == 1) {
                    qreal distance = pointToLineDistance(point3, point4, pos);
                    QPointF add = pointSplid(point2, point4, distance);
                    point4 = QPointF(point4.x() - add.x(), point4.y() + add.y());
                    distance = pointToLineDistance(point1, point3, pos);
                    add = pointSplid(point1, point2, distance);
                    point1 = QPointF(point1.x() - add.x(), point1.y() - add.y());
                    point3 = pos;
                }
                if (pointLineDir(point1, point3, pos) == 1 && pointLineDir(point3, point4, pos) == 1) {
                    qreal distance = pointToLineDistance(point3, point4, pos);
                    QPointF add = pointSplid(point2, point4, distance);
                    point4 = QPointF(point4.x() - add.x(), point4.y() + add.y());
                    distance = pointToLineDistance(point1, point3, pos);
                    add = pointSplid(point1, point2, distance);
                    point1 = QPointF(point1.x() + add.x(), point1.y() + add.y());
                    point3 = pos;
                }
                if (pointLineDir(point1, point3, pos) == 1 && pointLineDir(point3, point4, pos) == -1) {
                    qreal distance = pointToLineDistance(point3, point4, pos);
                    QPointF add = pointSplid(point2, point4, distance);
                    point4 = QPointF(point4.x() + add.x(), point4.y() - add.y());
                    distance = pointToLineDistance(point1, point3, pos);
                    add = pointSplid(point1, point2, distance);
                    point1 = QPointF(point1.x() + add.x(), point1.y() + add.y());
                    point3 = pos;
                }
                newResizeFPoints[0] = point1;
                newResizeFPoints[1] = point2;
                newResizeFPoints[2] = point3;
                newResizeFPoints[3] = point4;
                return newResizeFPoints;
            } else {
                qreal distance1 = pointToLineDistance(point1, point3, pos);
                qreal distance2 = pointToLineDistance(point3, point4, pos);
                qreal distance = std::min(distance1, distance2);
                if (pointLineDir(point1, point3, pos) == 1 && pointLineDir(point3, point4, pos) == 1) {
                    QPointF add = pointSplid(point1, point2, distance);
                    point1 = QPointF(point1.x() + add.x(), point1.y() + add.y());
                    add = pointSplid(point2, point4, distance);
                    point4 = QPointF(point4.x() - add.x(), point4.y() + add.y());
                    point3 = QPointF(point1.x() + point4.x() - point2.x(), point1.y() + point4.y() - point2.y());
                } else {
                    QPointF add = pointSplid(point1, point2, distance);
                    point1 = QPointF(point1.x() - add.x(), point1.y() - add.y());
                    add = pointSplid(point2, point4, distance);
                    point4 = QPointF(point4.x() + add.x(), point4.y() - add.y());
                    point3 = QPointF(point1.x() + point4.x() - point2.x(), point1.y() + point4.y() - point2.y());
                    point3 = QPointF(point1.x() + point4.x() - point2.x(), point1.y() + point4.y() - point2.y());
                }
                newResizeFPoints[0] = point1;
                newResizeFPoints[1] = point2;
                newResizeFPoints[2] = point3;
                newResizeFPoints[3] = point4;
                return newResizeFPoints;
            }
        }
    }
    return newResizeFPoints;
}

/* point3 in the second position */
FourPoints point3Resize2(QPointF point1, QPointF point2, QPointF point3,
                         QPointF point4, QPointF pos, bool isShift) {
    FourPoints newResizeFPoints;
    newResizeFPoints = initFourPoints(newResizeFPoints);
    newResizeFPoints[0] = point1;
    newResizeFPoints[1] = point2;
    newResizeFPoints[2] = point3;
    newResizeFPoints[3] = point4;

    if (std::atan2((point2.y() - point1.y()), (point2.x() - point1.x())) <= -TANT_EDGEVALUE &&
    (pos.x() + MIN_PADDING > point1.x() || pos.y() - MIN_PADDING < point4.y() ||
     pointLineDir(point1, point2, pos) == 1 || pointLineDir(point2, point4, pos) == -1)) {
        return newResizeFPoints;
    } else if (std::atan2((point2.y() - point1.y()), (point2.x() - point1.x())) > -TANT_EDGEVALUE &&
     (pos.x() + MIN_PADDING > point4.x() || pos.y() + MIN_PADDING > point1.y() ||
      pointLineDir(point1, point2, pos) == 1 || pointLineDir(point2, point4, pos) == -1)) {
        return newResizeFPoints;
    } else {
        if (pointToLineDistance(point2, point4, pos) < MIN_PADDING ||
                pointToLineDistance(point1, point2, pos) < MIN_PADDING) {
            return newResizeFPoints;
        } else {
            if (!isShift) {
                if (pointLineDir(point1, point3, pos) == 1 && pointLineDir(point3, point4, pos) == -1) {
                    qreal distance = pointToLineDistance(point3, point4, pos);
                    QPointF add = pointSplid(point2, point4, distance);
                    point4 = QPointF(point4.x() - add.x(), point4.y() - add.y());
                    distance = pointToLineDistance(point1, point3, pos);
                    add = pointSplid(point1, point2, distance);
                    point1 = QPointF(point1.x() - add.x(), point1.y() + add.y());
                    point3 = pos;
                }
                if (pointLineDir(point1, point3, pos) == -1 && pointLineDir(point3, point4, pos) == -1) {
                    qreal distance = pointToLineDistance(point3, point4, pos);
                    QPointF add = pointSplid(point2, point4, distance);
                    point4 = QPointF(point4.x() - add.x(), point4.y() - add.y());
                    distance = pointToLineDistance(point1, point3, pos);
                    add = pointSplid(point1, point2, distance);
                    point1 = QPointF(point1.x() + add.x(), point1.y() - add.y());
                    point3 = pos;
                }
                if (pointLineDir(point1, point3, pos) == -1 && pointLineDir(point3, point4, pos) == 1) {
                    qreal distance = pointToLineDistance(point3, point4, pos);
                    QPointF add = pointSplid(point2, point4, distance);
                    point4 = QPointF(point4.x() + add.x(), point4.y() + add.y());
                    distance = pointToLineDistance(point1, point3, pos);
                    add = pointSplid(point1, point2, distance);
                    point1 = QPointF(point1.x() + add.x(), point1.y() - add.y());
                    point3 = pos;
                }
                if (pointLineDir(point1, point3, pos) == 1 && pointLineDir(point3, point4, pos) == 1) {
                    qreal distance = pointToLineDistance(point3, point4, pos);
                    QPointF add = pointSplid(point2, point4, distance);
                    point4 = QPointF(point4.x() + add.x(), point4.y() + add.y());
                    distance = pointToLineDistance(point1, point3, pos);
                    add = pointSplid(point1, point2, distance);
                    point1 = QPointF(point1.x() - add.x(), point1.y() + add.y());
                    point3 = pos;
                }
                newResizeFPoints[0] = point1;
                newResizeFPoints[1] = point2;
                newResizeFPoints[2] = point3;
                newResizeFPoints[3] = point4;
                return newResizeFPoints;
            } else {
                qreal distance1 = pointToLineDistance(point1, point3, pos);
                qreal distance2 = pointToLineDistance(point3, point4, pos);
                qreal distance = std::min(distance1, distance2);
                if (pointLineDir(point1, point3, pos) == -1 && pointLineDir(point3, point4, pos) == 1) {
                    QPointF add = pointSplid(point1, point2, distance);
                    point1 = QPointF(point1.x() + add.x(), point1.y() - add.y());
                    add = pointSplid(point2, point4, distance);
                    point4 = QPointF(point4.x() + add.x(), point4.y() + add.y());
                } else {
                    QPointF add = pointSplid(point1, point2, distance);
                    point1 = QPointF(point1.x() - add.x(), point1.y() + add.y());
                    add = pointSplid(point2, point4, distance);
                    point4 = QPointF(point4.x() - add.x(), point4.y() - add.y());
                }
                point3 = QPointF(point1.x() + point4.x() - point2.x(), point1.y() + point4.y() - point2.y());
                newResizeFPoints[0] = point1;
                newResizeFPoints[1] = point2;
                newResizeFPoints[2] = point3;
                newResizeFPoints[3] = point4;
                return newResizeFPoints;
            }
        }
    }
    return newResizeFPoints;
}

/* point3 in the third position */
FourPoints point3Resize3(QPointF point1, QPointF point2, QPointF point3,
                         QPointF point4, QPointF pos, bool isShift) {
    FourPoints newResizeFPoints;
    newResizeFPoints = initFourPoints(newResizeFPoints);
    newResizeFPoints[0] = point1;
    newResizeFPoints[1] = point2;
    newResizeFPoints[2] = point3;
    newResizeFPoints[3] = point4;

    if (std::atan2((point2.y() - point1.y()), (point2.x() - point1.x())) >= TANT2_EDGEVALUE &&
    (pos.x() - MIN_PADDING < point4.x() || pos.y() - MIN_PADDING < point1.y() ||
     pointLineDir(point1, point2, pos) == -1 || pointLineDir(point2, point4, pos) == 1)) {
        return newResizeFPoints;
    } else if (std::atan2((point2.y() - point1.y()), (point2.x() - point1.x())) < TANT2_EDGEVALUE &&
     (pos.x() - MIN_PADDING < point1.x() || pos.y() + MIN_PADDING > point4.y() ||
      pointLineDir(point1, point2, pos) == -1 || pointLineDir(point2, point4, pos) == 1)) {
        return newResizeFPoints;
    } else {
        if (pointToLineDistance(point2, point4, pos) < MIN_PADDING ||
                pointToLineDistance(point1, point2, pos) < MIN_PADDING) {
            return newResizeFPoints;
        } else {
            if (!isShift) {
                if (pointLineDir(point1, point3, pos) == -1 && pointLineDir(point3, point4, pos) == 1) {
                    qreal distance = pointToLineDistance(point3, point4, pos);
                    QPointF add = pointSplid(point2, point4, distance);
                    point4 = QPointF(point4.x() + add.x(), point4.y() + add.y());
                    distance = pointToLineDistance(point1, point3, pos);
                    add = pointSplid(point1, point2, distance);
                    point1 = QPointF(point1.x() + add.x(), point1.y() - add.y());
                    point3 = pos;
                }
                if (pointLineDir(point1, point3, pos) == -1 && pointLineDir(point3, point4, pos) == -1) {
                    qreal distance = pointToLineDistance(point3, point4, pos);
                    QPointF add = pointSplid(point2, point4, distance);
                    point4 = QPointF(point4.x() - add.x(), point4.y() - add.y());
                    distance = pointToLineDistance(point1, point3, pos);
                    add = pointSplid(point1, point2, distance);
                    point1 = QPointF(point1.x() + add.x(), point1.y() - add.y());
                    point3 = pos;
                }
                if (pointLineDir(point1, point3, pos) == 1 && pointLineDir(point3, point4, pos) == -1) {
                    qreal distance = pointToLineDistance(point3, point4, pos);
                    QPointF add = pointSplid(point2, point4, distance);
                    point4 = QPointF(point4.x() - add.x(), point4.y() - add.y());
                    distance = pointToLineDistance(point1, point3, pos);
                    add = pointSplid(point1, point2, distance);
                    point1 = QPointF(point1.x() - add.x(), point1.y() + add.y());
                    point3 = pos;
                }
                if (pointLineDir(point1, point3, pos) == 1 && pointLineDir(point3, point4, pos) == 1) {
                    qreal distance = pointToLineDistance(point3, point4, pos);
                    QPointF add = pointSplid(point2, point4, distance);
                    point4 = QPointF(point4.x() + add.x(), point4.y() + add.y());
                    distance = pointToLineDistance(point1, point3, pos);
                    add = pointSplid(point1, point2, distance);
                    point1 = QPointF(point1.x() - add.x(), point1.y() + add.y());
                    point3 = pos;
                }
                newResizeFPoints[0] = point1;
                newResizeFPoints[1] = point2;
                newResizeFPoints[2] = point3;
                newResizeFPoints[3] = point4;
                return newResizeFPoints;
            } else {
                qreal distance1 = pointToLineDistance(point1, point3, pos);
                qreal distance2 = pointToLineDistance(point3, point4, pos);
                qreal distance = std::min(distance1, distance2);
                if (pointLineDir(point1, point3, pos) == 1 && pointLineDir(point3, point4, pos) == -1) {
                    QPointF add = pointSplid(point1, point2, distance);
                    point1 = QPointF(point1.x() - add.x(), point1.y() + add.y());
                    add = pointSplid(point2, point4, distance);
                    point4 = QPointF(point4.x() - add.x(), point4.y() - add.y());
                } else {
                    QPointF add = pointSplid(point1, point2, distance);
                    point1 = QPointF(point1.x() + add.x(), point1.y() - add.y());
                    add = pointSplid(point2, point4, distance);
                    point4 = QPointF(point4.x() + add.x(), point4.y() + add.y());
                }
                point3 = QPointF(point1.x() + point4.x() - point2.x(), point1.y() + point4.y() - point2.y());
                newResizeFPoints[0] = point1;
                newResizeFPoints[1] = point2;
                newResizeFPoints[2] = point3;
                newResizeFPoints[3] = point4;
                return newResizeFPoints;
            }
        }
    }
    return newResizeFPoints;
}

/* point3 in the fourth position */
FourPoints point3Resize4(QPointF point1, QPointF point2, QPointF point3,
                         QPointF point4, QPointF pos, bool isShift) {
    FourPoints newResizeFPoints;
    newResizeFPoints = initFourPoints(newResizeFPoints);
    newResizeFPoints[0] = point1;
    newResizeFPoints[1] = point2;
    newResizeFPoints[2] = point3;
    newResizeFPoints[3] = point4;

    if (std::atan2((point2.y() - point1.y()), (point2.x() - point1.x())) >= -TANT2_EDGEVALUE &&
    (pos.y() - MIN_PADDING < point4.y() || pos.x() + MIN_PADDING > point1.x() ||
     pointLineDir(point1, point2, pos) == -1 || pointLineDir(point2, point4, pos) == -1)) {
        return newResizeFPoints;
    } else if (std::atan2((point2.y() - point1.y()), (point2.x() - point1.x())) < -TANT2_EDGEVALUE &&
     (pos.y() - MIN_PADDING < point1.y() || pos.x() - MIN_PADDING < point4.x() ||
      pointLineDir(point1, point2, pos) == -1 || pointLineDir(point2, point4, pos) == -1)) {
        return newResizeFPoints;
    } else {
        if (pointToLineDistance(point2, point4, pos) < MIN_PADDING ||
                pointToLineDistance(point1, point2, pos) < MIN_PADDING) {
            return newResizeFPoints;
        } else {
            if (!isShift) {
                if (pointLineDir(point1, point3, pos) == 1 && pointLineDir(point3, point4, pos) == 1) {
                    qreal distance = pointToLineDistance(point3, point4, pos);
                    QPointF add = pointSplid(point2, point4, distance);
                    point4 = QPointF(point4.x() - add.x(), point4.y() + add.y());
                    distance = pointToLineDistance(point1, point3, pos);
                    add  = pointSplid(point1, point2, distance);
                    point1 = QPointF(point1.x() + add.x(), point1.y() + add.y());
                    point3 = pos;
                }
                if (pointLineDir(point1, point3, pos) == 1 && pointLineDir(point3, point4, pos) == -1) {
                    qreal distance = pointToLineDistance(point3, point4, pos);
                    QPointF add = pointSplid(point2, point4, distance);
                    point4 = QPointF(point4.x() + add.x(), point4.y() - add.y());
                    distance = pointToLineDistance(point1, point3, pos);
                    add  = pointSplid(point1, point2, distance);
                    point1 = QPointF(point1.x() + add.x(), point1.y() + add.y());
                    point3 = pos;
                }
                if (pointLineDir(point1, point3, pos) == -1 && pointLineDir(point3, point4, pos) == -1) {
                    qreal distance = pointToLineDistance(point3, point4, pos);
                    QPointF add = pointSplid(point2, point4, distance);
                    point4 = QPointF(point4.x() + add.x(), point4.y() - add.y());
                    distance = pointToLineDistance(point1, point3, pos);
                    add  = pointSplid(point1, point2, distance);
                    point1 = QPointF(point1.x() - add.x(), point1.y() - add.y());
                    point3 = pos;
                }
                if (pointLineDir(point1, point3, pos) == -1 && pointLineDir(point3, point4, pos) == 1) {
                    qreal distance = pointToLineDistance(point3, point4, pos);
                    QPointF add = pointSplid(point2, point4, distance);
                    point4 = QPointF(point4.x() - add.x(), point4.y() + add.y());
                    distance = pointToLineDistance(point1, point3, pos);
                    add  = pointSplid(point1, point2, distance);
                    point1 = QPointF(point1.x() - add.x(), point1.y() - add.y());
                    point3 = pos;
                }
                newResizeFPoints[0] = point1;
                newResizeFPoints[1] = point2;
                newResizeFPoints[2] = point3;
                newResizeFPoints[3] = point4;
                return newResizeFPoints;
            } else {
                qreal distance1 = pointToLineDistance(point1, point3, pos);
                qreal distance2 = pointToLineDistance(point3, point4, pos);
                qreal distance = std::min(distance1, distance2);

                if (pointLineDir(point1, point3, pos) == -1 && pointLineDir(point3, point4, pos) == -1) {
                    QPointF add = pointSplid(point1, point2, distance);
                    point1 = QPointF(point1.x() - add.x(), point1.y() - add.y());
                    add = pointSplid(point2, point4, distance);
                    point4 = QPointF(point4.x() + add.x(), point4.y() - add.y());
                } else {
                    QPointF add = pointSplid(point1, point2, distance);
                    point1 = QPointF(point1.x() + add.x(), point1.y() + add.y());
                    add = pointSplid(point2, point4, distance);
                    point4 = QPointF(point4.x() - add.x(), point4.y() + add.y());
                }
                point3 = QPointF(point1.x() + point4.x() - point2.x(), point1.y() + point4.y() - point2.y());
                newResizeFPoints[0] = point1;
                newResizeFPoints[1] = point2;
                newResizeFPoints[2] = point3;
                newResizeFPoints[3] = point4;
                return newResizeFPoints;
            }
        }
    }
    return newResizeFPoints;
}

/* point3 in the fifth position */
FourPoints point3Resize5(QPointF point1, QPointF point2, QPointF point3,
                         QPointF point4, QPointF pos, bool isShift) {
    FourPoints newResizeFPoints;
    newResizeFPoints = initFourPoints(newResizeFPoints);
    newResizeFPoints[0] = point1;
    newResizeFPoints[1] = point2;
    newResizeFPoints[2] = point3;
    newResizeFPoints[3] = point4;

    if (pos.y() + MIN_PADDING > point4.y() || pos.x() - MIN_PADDING < point1.x()) {
        return newResizeFPoints;
    } else {
        if (!isShift) {
            point4.setX(pos.x());
            point1.setY(pos.y());
            point3 = pos;

            newResizeFPoints[0] = point1;
            newResizeFPoints[1] = point2;
            newResizeFPoints[2] = point3;
            newResizeFPoints[3] = point4;
            return newResizeFPoints;
        } else {
            qreal distance1 = pointToLineDistance(point1, point3,  pos);
            qreal distance2 = pointToLineDistance(point3, point4, pos);
            qreal distance = std::min(distance1, distance2);

            if (pointLineDir(point1, point3, pos) == 1 && pointLineDir(point3, point4, pos) == -1) {
                QPointF add = pointSplid(point1, point2, distance);
                point1 = QPointF(point1.x() - add.x(), point1.y() + add.y());
                add = pointSplid(point2, point4, distance);
                point4 = QPointF(point4.x() - add.x(), point4.y() - add.y());
            } else {
                QPointF add = pointSplid(point1, point2, distance);
                point1 = QPointF(point1.x() + add.x(), point1.y() - add.y());
                add = pointSplid(point2, point4, distance);
                point4 = QPointF(point4.x() + add.x(), point4.y() + add.y());
            }
            point3 = QPointF(point1.x() + point4.x() - point2.x(), point1.y() + point4.y() - point2.y());
            newResizeFPoints[0] = point1;
            newResizeFPoints[1] = point2;
            newResizeFPoints[2] = point3;
            newResizeFPoints[3] = point4;
            return newResizeFPoints;
        }
    }
    return newResizeFPoints;
}
/* point3 in the sixth position */
FourPoints point3Resize6(QPointF point1, QPointF point2, QPointF point3,
                         QPointF point4, QPointF pos, bool isShift) {
    Q_UNUSED(pos);
    Q_UNUSED(isShift);
    FourPoints newResizeFPoints;
    newResizeFPoints = initFourPoints(newResizeFPoints);
    newResizeFPoints[0] = point1;
    newResizeFPoints[1] = point2;
    newResizeFPoints[2] = point3;
    newResizeFPoints[3] = point4;

    return newResizeFPoints;
}
/* point3 in the seventh position */
FourPoints point3Resize7(QPointF point1, QPointF point2, QPointF point3,
                         QPointF point4, QPointF pos, bool isShift) {
    Q_UNUSED(pos);
    Q_UNUSED(isShift);
    FourPoints newResizeFPoints;
    newResizeFPoints = initFourPoints(newResizeFPoints);
    newResizeFPoints[0] = point1;
    newResizeFPoints[1] = point2;
    newResizeFPoints[2] = point3;
    newResizeFPoints[3] = point4;

    return newResizeFPoints;
}

/***************** fourth point4 *******************/
/* point4 in the first position */
FourPoints point4Resize1(QPointF point1, QPointF point2, QPointF point3,
                         QPointF point4, QPointF pos, bool isShift) {
    FourPoints newResizeFPoints;
    newResizeFPoints = initFourPoints(newResizeFPoints);
    newResizeFPoints[0] = point1;
    newResizeFPoints[1] = point2;
    newResizeFPoints[2] = point3;
    newResizeFPoints[3] = point4;

    if (std::atan2((point2.y() - point1.y()), (point2.x() - point1.x())) >= TANT_EDGEVALUE &&
    (pos.x() - MIN_PADDING < point2.x() || pos.y() - MIN_PADDING < point3.y() ||
     pointLineDir(point1, point2, pos) == 1 || pointLineDir(point1, point3, pos) == -1)) {
        return newResizeFPoints;
    } else if (std::atan2((point2.y() - point1.y()), (point2.x() - point1.x())) < TANT_EDGEVALUE &&
     (pos.x() - MIN_PADDING < point3.x() || pos.y() + MIN_PADDING > point2.y() ||
      pointLineDir(point1, point2, pos) == 1 || pointLineDir(point1, point3, pos) == -1)) {
        return newResizeFPoints;
    } else {
        if (pointToLineDistance(point1, point2, pos) < MIN_PADDING ||
                pointToLineDistance(point1, point3, pos) < MIN_PADDING) {
            return newResizeFPoints;
        } else {
            if (!isShift) {
                if (pointLineDir(point3, point4, pos) == -1 && pointLineDir(point2, point4, pos) == 1) {
                    qreal distance = pointToLineDistance(point2, point4, pos);
                    QPointF add = pointSplid(point1, point2, distance);
                    point2 = QPointF(point2.x() + add.x(), point2.y() + add.y());
                    distance = pointToLineDistance(point3, point4, pos);
                    add = pointSplid(point1, point3, distance);
                    point3 = QPointF(point3.x() + add.x(), point3.y() - add.y());
                    point4 = pos;
                }
                if (pointLineDir(point3, point4, pos) == -1 && pointLineDir(point2, point4, pos) == -1) {
                    qreal distance = pointToLineDistance(point2, point4, pos);
                    QPointF add = pointSplid(point1, point2, distance);
                    point2 = QPointF(point2.x() - add.x(), point2.y() - add.y());
                    distance = pointToLineDistance(point3, point4, pos);
                    add = pointSplid(point1, point3, distance);
                    point3 = QPointF(point3.x() + add.x(), point3.y() - add.y());
                    point4 = pos;
                }
                if (pointLineDir(point3, point4, pos) == 1 && pointLineDir(point2, point4, pos) == -1) {
                    qreal distance = pointToLineDistance(point2, point4, pos);
                    QPointF add = pointSplid(point1, point2, distance);
                    point2 = QPointF(point2.x() - add.x(), point2.y() - add.y());
                    distance = pointToLineDistance(point3, point4, pos);
                    add = pointSplid(point1, point3, distance);
                    point3 = QPointF(point3.x() - add.x(), point3.y() + add.y());
                    point4 = pos;
                }
                if (pointLineDir(point3, point4, pos) == 1 && pointLineDir(point2, point4, pos) == 1) {
                    qreal distance = pointToLineDistance(point2, point4, pos);
                    QPointF add = pointSplid(point1, point2, distance);
                    point2 = QPointF(point2.x() + add.x(), point2.y() + add.y());
                    distance = pointToLineDistance(point3, point4, pos);
                    add = pointSplid(point1, point3, distance);
                    point3 = QPointF(point3.x() - add.x(), point3.y() + add.y());
                    point4 = pos;
                }
                newResizeFPoints[0] = point1;
                newResizeFPoints[1] = point2;
                newResizeFPoints[2] = point3;
                newResizeFPoints[3] = point4;
                return newResizeFPoints;
            } else {
                qreal distance1 = pointToLineDistance(point2, point4, pos);
                qreal distance2 = pointToLineDistance(point3, point4, pos);
                qreal distance =  std::min(distance1, distance2);
                if (pointLineDir(point2, point4, pos) == 1 && pointLineDir(point3, point4, pos) == -1) {
                    QPointF add = pointSplid(point1, point2, distance);
                    point2 = QPointF(point2.x() + add.x(), point2.y() + add.y());
                    add = pointSplid(point1, point3, distance);
                    point3 = QPointF(point3.x() + add.x(), point3.y() - add.y());
                } else {
                    QPointF add = pointSplid(point1, point2, distance);
                    point2 = QPointF(point2.x() - add.x(), point2.y() - add.y());
                    add = pointSplid(point1, point3, distance);
                    point3 = QPointF(point3.x() - add.x(), point3.y() + add.y());
                }
                point4 = QPointF(point2.x() + point3.x() - point1.x(), point2.y() + point3.y() - point1.y());
                newResizeFPoints[0] = point1;
                newResizeFPoints[1] = point2;
                newResizeFPoints[2] = point3;
                newResizeFPoints[3] = point4;
                return newResizeFPoints;
            }
        }
    }
    return newResizeFPoints;
}

/* point4 in the second position */
FourPoints point4Resize2(QPointF point1, QPointF point2, QPointF point3,
                         QPointF point4, QPointF pos, bool isShift) {
    FourPoints newResizeFPoints;
    newResizeFPoints = initFourPoints(newResizeFPoints);
    newResizeFPoints[0] = point1;
    newResizeFPoints[1] = point2;
    newResizeFPoints[2] = point3;
    newResizeFPoints[3] = point4;

    if (std::atan2((point2.y() - point1.y()), (point2.x() - point1.x())) <= -TANT_EDGEVALUE &&
    (pos.y() + MIN_PADDING > point3.y() || pos.x() + MIN_PADDING > point2.x() ||
     pointLineDir(point1, point2, pos) == 1 || pointLineDir(point1, point3, pos) == 1)) {
        return newResizeFPoints;
    } else if (std::atan2((point2.y() - point1.y()), (point2.x() - point1.x())) > -TANT_EDGEVALUE &&
     (pos.y() + MIN_PADDING > point2.y() || pos.x() - MIN_PADDING < point3.x() ||
      pointLineDir(point1, point2, pos) == 1 || pointLineDir(point1, point3, pos) == 1)) {
        return newResizeFPoints;
    } else {
        if (pointToLineDistance(point1, point2, pos) < MIN_PADDING ||
                pointToLineDistance(point1, point3, pos) < MIN_PADDING) {
            return newResizeFPoints;
        } else {
            if (!isShift) {
                if (pointLineDir(point3, point4, pos) == 1 && pointLineDir(point2, point4, pos) == 1) {
                    qreal distance = pointToLineDistance(point2, point4, pos);
                    QPointF add = pointSplid(point1, point2, distance);
                    point2 = QPointF(point2.x() - add.x(), point2.y() + add.y());
                    distance = pointToLineDistance(point3, point4, pos);
                    add = pointSplid(point1, point3, distance);
                    point3 = QPointF(point3.x() + add.x(), point3.y() + add.y());
                    point4 = pos;
                }
                if (pointLineDir(point3, point4, pos) == -1 && pointLineDir(point2, point4, pos) == 1) {
                    qreal distance = pointToLineDistance(point2, point4, pos);
                    QPointF add = pointSplid(point1, point2, distance);
                    point2 = QPointF(point2.x() - add.x(), point2.y() + add.y());
                    distance = pointToLineDistance(point3, point4, pos);
                    add = pointSplid(point1, point3, distance);
                    point3 = QPointF(point3.x() - add.x(), point3.y() - add.y());
                    point4 = pos;
                }
                if (pointLineDir(point3, point4, pos) == -1 && pointLineDir(point2, point4, pos) == -1) {
                    qreal distance = pointToLineDistance(point2, point4, pos);
                    QPointF add = pointSplid(point1, point2, distance);
                    point2 = QPointF(point2.x() + add.x(), point2.y() - add.y());
                    distance = pointToLineDistance(point3, point4, pos);
                    add = pointSplid(point1, point3, distance);
                    point3 = QPointF(point3.x() - add.x(), point3.y() - add.y());
                    point4 = pos;
                }
                if (pointLineDir(point3, point4, pos) == 1 && pointLineDir(point2, point4, pos) == -1) {
                    qreal distance = pointToLineDistance(point2, point4, pos);
                    QPointF add = pointSplid(point1, point2, distance);
                    point2 = QPointF(point2.x() + add.x(), point2.y() - add.y());
                    distance = pointToLineDistance(point3, point4, pos);
                    add = pointSplid(point1, point3, distance);
                    point3 = QPointF(point3.x() + add.x(), point3.y() + add.y());
                    point4 = pos;
                }
                newResizeFPoints[0] = point1;
                newResizeFPoints[1] = point2;
                newResizeFPoints[2] = point3;
                newResizeFPoints[3] = point4;
                return newResizeFPoints;
            } else {
                qreal distance1 = pointToLineDistance(point2, point4, pos);
                qreal distance2 = pointToLineDistance(point3, point4, pos);
                qreal distance = std::min(distance1, distance2);
                if (pointLineDir(point2, point4, pos) == -1 && pointLineDir(point3, point4, pos) == -1) {
                    QPointF add = pointSplid(point1, point2, distance);
                    point2 = QPointF(point2.x() + add.x(), point2.y() - add.y());
                    add = pointSplid(point1, point3, distance);
                    point3 = QPointF(point3.x() - add.x(), point3.y() - add.y());
                } else {
                    QPointF add = pointSplid(point1, point2, distance);
                    point2 = QPointF(point2.x() - add.x(), point2.y() + add.y());
                    add = pointSplid(point1, point3, distance);
                    point3 = QPointF(point3.x() + add.x(), point3.y() + add.y());
                }
                point4 = QPointF(point2.x() + point3.x() - point1.x(), point2.y() + point3.y() - point1.y());
                newResizeFPoints[0] = point1;
                newResizeFPoints[1] = point2;
                newResizeFPoints[2] = point3;
                newResizeFPoints[3] = point4;
                return newResizeFPoints;
            }
        }
    }
    return newResizeFPoints;
}

/* point4 in the third position */
FourPoints point4Resize3(QPointF point1, QPointF point2, QPointF point3,
                         QPointF point4, QPointF pos, bool isShift) {
    FourPoints newResizeFPoints;
    newResizeFPoints = initFourPoints(newResizeFPoints);
    newResizeFPoints[0] = point1;
    newResizeFPoints[1] = point2;
    newResizeFPoints[2] = point3;
    newResizeFPoints[3] = point4;

    if (std::atan2((point2.y() - point1.y()), (point2.x() - point1.x())) >= TANT2_EDGEVALUE &&
    (pos.y() - MIN_PADDING < point2.y() || pos.x() + MIN_PADDING > point3.x() ||
     pointLineDir(point1, point2, pos) == -1 || pointLineDir(point1, point3, pos) == -1)) {
        return newResizeFPoints;
    } else if (std::atan2((point2.y() - point1.y()), (point2.x() - point1.x())) < TANT2_EDGEVALUE &&
     (pos.y() - MIN_PADDING < point3.y() || pos.x() - MIN_PADDING < point2.x() ||
      pointLineDir(point1, point2, pos) == -1 || pointLineDir(point1, point3, pos) == -1)) {
        return newResizeFPoints;
    } else {
        if (pointToLineDistance(point1, point2, pos) < MIN_PADDING ||
                pointToLineDistance(point1, point3, pos) < MIN_PADDING) {
            return newResizeFPoints;
        } else {
            if (!isShift) {
                if (pointLineDir(point3, point4, pos) == 1 && pointLineDir(point2, point4, pos) == 1) {
                    qreal distance = pointToLineDistance(point2, point4, pos);
                    QPointF add = pointSplid(point1, point2, distance);
                    point2 = QPointF(point2.x() - add.x(), point2.y() + add.y());
                    distance = pointToLineDistance(point3, point4, pos);
                    add = pointSplid(point1, point3, distance);
                    point3 = QPointF(point3.x() + add.x(), point3.y() + add.y());
                    point4 = pos;
                }
                if (pointLineDir(point3, point4, pos) == -1 && pointLineDir(point2, point4, pos) == 1) {
                    qreal distance = pointToLineDistance(point2, point4, pos);
                    QPointF add = pointSplid(point1, point2, distance);
                    point2 = QPointF(point2.x() - add.x(), point2.y() + add.y());
                    distance = pointToLineDistance(point3, point4, pos);
                    add = pointSplid(point1, point3, distance);
                    point3 = QPointF(point3.x() - add.x(), point3.y() - add.y());
                    point4 = pos;
                }
                if (pointLineDir(point3, point4, pos) == -1 && pointLineDir(point2, point4, pos) == -1) {
                    qreal distance = pointToLineDistance(point2, point4, pos);
                    QPointF add = pointSplid(point1, point2, distance);
                    point2 = QPointF(point2.x() + add.x(), point2.y() - add.y());
                    distance = pointToLineDistance(point3, point4, pos);
                    add = pointSplid(point1, point3, distance);
                    point3 = QPointF(point3.x() - add.x(), point3.y() - add.y());
                    point4 = pos;
                }
                if (pointLineDir(point3, point4, pos) == 1 && pointLineDir(point2, point4, pos) == -1) {
                    qreal distance = pointToLineDistance(point2, point4, pos);
                    QPointF add = pointSplid(point1, point2, distance);
                    point2 = QPointF(point2.x() + add.x(), point2.y() - add.y());
                    distance = pointToLineDistance(point3, point4, pos);
                    add = pointSplid(point1, point3, distance);
                    point3 = QPointF(point3.x() + add.x(), point3.y() + add.y());
                    point4 = pos;
                }
                newResizeFPoints[0] = point1;
                newResizeFPoints[1] = point2;
                newResizeFPoints[2] = point3;
                newResizeFPoints[3] = point4;
                return newResizeFPoints;
            } else {
                qreal distance1 = pointToLineDistance(point2, point4, pos);
                qreal distance2 = pointToLineDistance(point3, point4, pos);
                qreal distance = std::min(distance1, distance2);
                if (pointLineDir(point2, point4, pos) == 1 && pointLineDir(point3, point4, pos) == 1) {
                    QPointF add = pointSplid(point1, point2, distance);
                    point2 = QPointF(point2.x() - add.x(), point2.y() + add.y());
                    add = pointSplid(point1, point3, distance);
                    point3 = QPointF(point3.x() + add.x(), point3.y() + add.y());
                } else {
                    QPointF add = pointSplid(point1, point2, distance);
                    point2 = QPointF(point2.x() + add.x(), point2.y() - add.y());
                    add = pointSplid(point1, point3, distance);
                    point3 = QPointF(point3.x() - add.x(), point3.y() - add.y());
                }
                point4 = QPointF(point2.x() + point3.x() - point1.x(), point2.y() + point3.y() - point1.y());
                newResizeFPoints[0] = point1;
                newResizeFPoints[1] = point2;
                newResizeFPoints[2] = point3;
                newResizeFPoints[3] = point4;
                return newResizeFPoints;
            }
        }
    }
    return newResizeFPoints;
}

/* point4 in the third position */
FourPoints point4Resize4(QPointF point1, QPointF point2, QPointF point3,
                         QPointF point4, QPointF pos, bool isShift) {
    FourPoints newResizeFPoints;
    newResizeFPoints = initFourPoints(newResizeFPoints);
    newResizeFPoints[0] = point1;
    newResizeFPoints[1] = point2;
    newResizeFPoints[2] = point3;
    newResizeFPoints[3] = point4;

    if (std::atan2((point2.y() - point1.y()), (point2.x() - point1.x())) >= -TANT2_EDGEVALUE &&
    (pos.x() + MIN_PADDING > point2.x() || pos.y() + MIN_PADDING > point3.y() ||
     pointLineDir(point1, point2, pos) == -1 || pointLineDir(point1, point3, pos) == 1)) {
        return newResizeFPoints;
    } else if (std::atan2((point2.y() - point1.y()), (point2.x() - point1.x())) < -TANT2_EDGEVALUE &&
     (pos.x() + MIN_PADDING > point3.x() || pos.y() - MIN_PADDING < point2.y() ||
      pointLineDir(point1, point2, pos) == -1 || pointLineDir(point1, point3, pos) == 1)) {
        return newResizeFPoints;
    } else {
        if (pointToLineDistance(point1, point2, pos) < MIN_PADDING ||
                pointToLineDistance(point1, point3, pos) < MIN_PADDING) {
            return newResizeFPoints;
        } else {
            if (!isShift) {
                if (pointLineDir(point3, point4, pos) == 1 && pointLineDir(point2, point4, pos) == -1) {
                    qreal distance = pointToLineDistance(point2, point4, pos);
                    QPointF add = pointSplid(point1, point2, distance);
                    point2 = QPointF(point2.x() - add.x(), point2.y() - add.y());
                    distance = pointToLineDistance(point3, point4, pos);
                    add = pointSplid(point1, point3, distance);
                    point3 = QPointF(point3.x() - add.x(), point3.y() + add.y());
                    point4 = pos;
                }
                if (pointLineDir(point3, point4, pos) == -1 && pointLineDir(point2, point4, pos) == -1) {
                    qreal distance = pointToLineDistance(point2, point4, pos);
                    QPointF add = pointSplid(point1, point2, distance);
                    point2 = QPointF(point2.x() - add.x(), point2.y() - add.y());
                    distance = pointToLineDistance(point3, point4, pos);
                    add = pointSplid(point1, point3, distance);
                    point3 = QPointF(point3.x() + add.x(), point3.y() - add.y());
                    point4 = pos;
                }
                if (pointLineDir(point3, point4, pos) == -1 && pointLineDir(point2, point4, pos) == 1) {
                    qreal distance = pointToLineDistance(point2, point4, pos);
                    QPointF add = pointSplid(point1, point2, distance);
                    point2 = QPointF(point2.x() + add.x(), point2.y() + add.y());
                    distance = pointToLineDistance(point3, point4, pos);
                    add = pointSplid(point1, point3, distance);
                    point3 = QPointF(point3.x() + add.x(), point3.y() - add.y());
                    point4 = pos;
                }
                if (pointLineDir(point3, point4, pos) == 1 && pointLineDir(point2, point4, pos) == 1) {
                    qreal distance = pointToLineDistance(point2, point4, pos);
                    QPointF add = pointSplid(point1, point2, distance);
                    point2 = QPointF(point2.x() + add.x(), point2.y() + add.y());
                    distance = pointToLineDistance(point3, point4, pos);
                    add = pointSplid(point1, point3, distance);
                    point3 = QPointF(point3.x() - add.x(), point3.y() + add.y());
                    point4 = pos;
                }
                newResizeFPoints[0] = point1;
                newResizeFPoints[1] = point2;
                newResizeFPoints[2] = point3;
                newResizeFPoints[3] = point4;
                return newResizeFPoints;
            } else {
                qreal distance1 = pointToLineDistance(point2,  point4, pos);
                qreal distance2 = pointToLineDistance(point3, point4, pos);
                qreal distance = std::min(distance1, distance2);
                if (pointLineDir(point2, point4, pos) == -1 && pointLineDir(point3, point4, pos) == 1) {
                    QPointF add = pointSplid(point1, point2, distance);
                    point2 = QPointF(point2.x() - add.x(), point2.y() - add.y());
                    add = pointSplid(point1, point3, distance);
                    point3 = QPointF(point3.x() - add.x(), point3.y() + add.y());
                } else {
                    QPointF add = pointSplid(point1, point2, distance);
                    point2 = QPointF(point2.x() + add.x(), point2.y() + add.y());
                    add = pointSplid(point1, point3, distance);
                    point3 = QPointF(point3.x() + add.x(), point3.y() - add.y());
                }
                point4 = QPointF(point2.x() + point3.x() - point1.x(), point2.y() + point3.y() - point1.y());
                newResizeFPoints[0] = point1;
                newResizeFPoints[1] = point2;
                newResizeFPoints[2] = point3;
                newResizeFPoints[3] = point4;
                return newResizeFPoints;
            }
        }
    }
    return newResizeFPoints;
}

/* point4 in the fifth position */
FourPoints point4Resize5(QPointF point1, QPointF point2, QPointF point3,
                         QPointF point4, QPointF pos, bool isShift) {
    FourPoints newResizeFPoints;
    newResizeFPoints = initFourPoints(newResizeFPoints);
    newResizeFPoints[0] = point1;
    newResizeFPoints[1] = point2;
    newResizeFPoints[2] = point3;
    newResizeFPoints[3] = point4;

    if (pos.y() - MIN_PADDING < point3.y() || pos.x() - MIN_PADDING < point2.x()) {
        return newResizeFPoints;
    } else {
        if (!isShift) {
            point2.setY(pos.y());
            point3.setX(pos.x());
            point4 = pos;

            newResizeFPoints[0] = point1;
            newResizeFPoints[1] = point2;
            newResizeFPoints[2] = point3;
            newResizeFPoints[3] = point4;
            return newResizeFPoints;
        } else {
            qreal distance1 = pointToLineDistance(point2, point4,  pos);
            qreal distance2 = pointToLineDistance(point3, point4, pos);
            qreal distance = std::min(distance1, distance2);

            if (pointLineDir(point2, point4, pos) == -1 && pointLineDir(point3, point4, pos) == -1) {
                QPointF add = pointSplid(point1, point2, distance);
                point2 = QPointF(point2.x() - add.x(), point2.y() - add.y());
                add = pointSplid(point1, point3, distance);
                point3 = QPointF(point3.x() - add.x(), point3.y() + add.y());
            } else {
                QPointF add = pointSplid(point1, point2, distance);
                point2 = QPointF(point2.x() + add.x(), point2.y() + add.y());
                add = pointSplid(point1, point3, distance);
                point3 = QPointF(point3.x() + add.x(), point3.y() - add.y());
            }
            point4 = QPointF(point2.x() + point3.x() - point1.x(), point2.y() + point3.y() - point1.y());
            newResizeFPoints[0] = point1;
            newResizeFPoints[1] = point2;
            newResizeFPoints[2] = point3;
            newResizeFPoints[3] = point4;
            return newResizeFPoints;
        }
    }
    return newResizeFPoints;
}
/* point4 in the sixth position */
FourPoints point4Resize6(QPointF point1, QPointF point2, QPointF point3,
                         QPointF point4, QPointF pos, bool isShift) {
    Q_UNUSED(pos);
    Q_UNUSED(isShift);
    FourPoints newResizeFPoints;
    newResizeFPoints = initFourPoints(newResizeFPoints);
    newResizeFPoints[0] = point1;
    newResizeFPoints[1] = point2;
    newResizeFPoints[2] = point3;
    newResizeFPoints[3] = point4;

    return newResizeFPoints;
}
/* point4 in the seventh position */
FourPoints point4Resize7(QPointF point1, QPointF point2, QPointF point3,
                         QPointF point4, QPointF pos, bool isShift) {
    Q_UNUSED(pos);
    Q_UNUSED(isShift);
    FourPoints newResizeFPoints;
    newResizeFPoints = initFourPoints(newResizeFPoints);
    newResizeFPoints[0] = point1;
    newResizeFPoints[1] = point2;
    newResizeFPoints[2] = point3;
    newResizeFPoints[3] = point4;

    return newResizeFPoints;
}

/********************** fifth point5 ************************/
/* point5 in the first position */
FourPoints point5Resize1(QPointF point1, QPointF point2, QPointF point3,
                         QPointF point4, QPointF pos, bool isShift) {
    FourPoints newResizeFPoints;
    newResizeFPoints = initFourPoints(newResizeFPoints);
    newResizeFPoints[0] = point1;
    newResizeFPoints[1] = point2;
    newResizeFPoints[2] = point3;
    newResizeFPoints[3] = point4;

    QPointF point7 = QPointF((point3.x() + point4.x())/2, (point3.y() + point4.y())/2);

    if (std::atan2((point2.y() - point1.y()), (point2.x() - point1.x())) >= TANT_EDGEVALUE &&
            (pos.x() + MIN_PADDING > point7.x()  || pointLineDir(point3, point4, pos) == -1 ||
             pointLineDir(point2, point4, pos) == 1)) {
        return newResizeFPoints;
    } else if (std::atan2((point2.y() - point1.y()), (point2.x() - point1.x())) < TANT_EDGEVALUE &&
               (pos.y() - MIN_PADDING < point7.y() ||pointLineDir(point3, point4, pos) == -1 ||
                pointLineDir(point2, point4, pos) == 1)) {
        return newResizeFPoints;
    } else {
        if (pointToLineDistance(point3, point4, pos) < MIN_PADDING) {
            return newResizeFPoints;
        } else {
            if (!isShift) {
                if (pointLineDir(point1, point2, pos) == 1) {
                    qreal distance = pointToLineDistance(point1, point2, pos);
                    QPointF add = pointSplid(point1, point3, distance);
                    point1 = QPointF(point1.x() - add.x(), point1.y() + add.y());
                    add = pointSplid(point2, point4, distance);
                    point2 = QPointF(point2.x() - add.x(), point2.y() + add.y());
                } else {
                    qreal distance = pointToLineDistance(point1, point2, pos);
                    QPointF add = pointSplid(point1, point3, distance);
                    point1 = QPointF(point1.x() + add.x(), point1.y() - add.y());
                    add = pointSplid(point2, point4, distance);
                    point2 = QPointF(point2.x() + add.x(), point2.y() - add.y());
                }
                newResizeFPoints[0] = point1;
                newResizeFPoints[1] = point2;
                newResizeFPoints[2] = point3;
                newResizeFPoints[3] = point4;
                return newResizeFPoints;
            } else {
                qreal distance = pointToLineDistance(point1,  point2, pos);
                if (pointLineDir(point1, point2, pos) == -1) {
                    QPointF add = pointSplid(point2, point4, distance);
                    point2 = QPointF(point2.x() + add.x(), point2.y() - add.y());
                    add = pointSplid(point3, point4, distance);
                    point3 = QPointF(point3.x() + add.x(), point3.y() + add.y());
                } else {
                    QPointF add = pointSplid(point2, point4, distance);
                    point2 = QPointF(point2.x() - add.x(), point2.y() + add.y());
                    add = pointSplid(point3, point4, distance);
                    point3 = QPointF(point3.x() - add.x(), point3.y() - add.y());
                }
                point1 = QPointF(point2.x() + point3.x() - point4.x(), point2.y() + point3.y() - point4.y());
                newResizeFPoints[0] = point1;
                newResizeFPoints[1] = point2;
                newResizeFPoints[2] = point3;
                newResizeFPoints[3] = point4;
                return newResizeFPoints;
            }
        }
    }
    return newResizeFPoints;
}

/* point5 in the second position */
FourPoints point5Resize2(QPointF point1, QPointF point2, QPointF point3,
                         QPointF point4, QPointF pos, bool isShift) {
    FourPoints newResizeFPoints;
    newResizeFPoints = initFourPoints(newResizeFPoints);
    newResizeFPoints[0] = point1;
    newResizeFPoints[1] = point2;
    newResizeFPoints[2] = point3;
    newResizeFPoints[3] = point4;

    QPointF point7 = QPointF((point3.x() + point4.x())/2, (point3.y() + point4.y())/2);

    if (std::atan2((point2.y() - point1.y()), (point2.x() - point1.x())) <= -TANT_EDGEVALUE &&
            (pos.x() - MIN_PADDING < point7.x()  || pointLineDir(point3, point4, pos) == -1 ||
             pointLineDir(point2, point4, pos) == -1)) {
        return newResizeFPoints;
    } else if (std::atan2((point2.y() - point1.y()), (point2.x() - point1.x())) > -TANT_EDGEVALUE &&
               (pos.y() - MIN_PADDING < point7.y() ||pointLineDir(point3, point4, pos) == -1 ||
                pointLineDir(point2, point4, pos) == -1)) {
        return newResizeFPoints;
    } else {
        if (pointToLineDistance(point3, point4, pos) < MIN_PADDING) {
            return newResizeFPoints;
        } else {
            if (!isShift) {
                if (pointLineDir(point1, point2, pos) == 1) {
                    qreal distance = pointToLineDistance(point1, point2, pos);
                    QPointF add = pointSplid(point1, point3, distance);
                    point1 = QPointF(point1.x() + add.x(), point1.y() + add.y());
                    add = pointSplid(point2, point4, distance);
                    point2 = QPointF(point2.x() + add.x(), point2.y() + add.y());
                } else {
                    qreal distance = pointToLineDistance(point1, point2, pos);
                    QPointF add = pointSplid(point1, point3, distance);
                    point1 = QPointF(point1.x() - add.x(), point1.y() - add.y());
                    add = pointSplid(point2, point4, distance);
                    point2 = QPointF(point2.x() - add.x(), point2.y() - add.y());
                }
                newResizeFPoints[0] = point1;
                newResizeFPoints[1] = point2;
                newResizeFPoints[2] = point3;
                newResizeFPoints[3] = point4;
                    return newResizeFPoints;
                } else {
                    qreal distance = pointToLineDistance(point1,  point2, pos);
                    if (pointLineDir(point1, point2, pos) == -1) {
                        QPointF add = pointSplid(point2, point4, distance);
                        point2 = QPointF(point2.x() - add.x(), point2.y() - add.y());
                        add = pointSplid(point3, point4, distance);
                        point3 = QPointF(point3.x() + add.x(), point3.y() - add.y());
                    } else {
                        QPointF add = pointSplid(point2, point4, distance);
                        point2 = QPointF(point2.x() + add.x(), point2.y() + add.y());
                        add = pointSplid(point3, point4, distance);
                        point3 = QPointF(point3.x() - add.x(), point3.y() + add.y());
                    }
                    point1 = QPointF(point2.x() + point3.x() - point4.x(), point2.y() + point3.y() - point4.y());
                    newResizeFPoints[0] = point1;
                    newResizeFPoints[1] = point2;
                    newResizeFPoints[2] = point3;
                    newResizeFPoints[3] = point4;
                    return newResizeFPoints;
                }
            }
    }
    return newResizeFPoints;
}

/* point5 in the  third position */
FourPoints point5Resize3(QPointF point1, QPointF point2, QPointF point3,
                         QPointF point4, QPointF pos, bool isShift) {
    FourPoints newResizeFPoints;
    newResizeFPoints = initFourPoints(newResizeFPoints);
    newResizeFPoints[0] = point1;
    newResizeFPoints[1] = point2;
    newResizeFPoints[2] = point3;
    newResizeFPoints[3] = point4;

    QPointF point7 = QPointF((point3.x() + point4.x())/2, (point3.y() + point4.y())/2);

    if (std::atan2((point2.y() - point1.y()), (point2.x() - point1.x())) >= TANT2_EDGEVALUE &&
            (pos.y() + MIN_PADDING > point7.y()  || pointLineDir(point3, point4, pos) == 1 ||
             pointLineDir(point2, point4, pos) == 1)) {
        return newResizeFPoints;
    } else if (std::atan2((point2.y() - point1.y()), (point2.x() - point1.x()))  < TANT2_EDGEVALUE &&
               (pos.x() + MIN_PADDING > point7.x() ||pointLineDir(point3, point4, pos) == 1 ||
                pointLineDir(point2, point4, pos) == 1)) {
        return newResizeFPoints;
    } else {
        if (pointToLineDistance(point3, point4, pos) < MIN_PADDING) {
            return newResizeFPoints;
        } else {
            if (!isShift) {
                if (pointLineDir(point1, point2, pos) == 1) {
                    qreal distance = pointToLineDistance(point1, point2, pos);
                    QPointF add = pointSplid(point1, point3, distance);
                    point1 = QPointF(point1.x() + add.x(), point1.y() + add.y());
                    add = pointSplid(point2, point4, distance);
                    point2 = QPointF(point2.x() + add.x(), point2.y() + add.y());
                } else {
                    qreal distance = pointToLineDistance(point1, point2, pos);
                    QPointF add = pointSplid(point1, point3, distance);
                    point1 = QPointF(point1.x() - add.x(), point1.y() - add.y());
                    add = pointSplid(point2, point4, distance);
                    point2 = QPointF(point2.x() - add.x(), point2.y() - add.y());
                }
                newResizeFPoints[0] = point1;
                newResizeFPoints[1] = point2;
                newResizeFPoints[2] = point3;
                newResizeFPoints[3] = point4;
                    return newResizeFPoints;
                } else {
                    qreal distance = pointToLineDistance(point1,  point2, pos);
                    if (pointLineDir(point1, point2, pos) == 1) {
                        QPointF add = pointSplid(point2, point4, distance);
                        point2 = QPointF(point2.x() + add.x(), point2.y() + add.y());
                        add = pointSplid(point3, point4, distance);
                        point3 = QPointF(point3.x() - add.x(), point3.y() + add.y());
                    } else {
                        QPointF add = pointSplid(point2, point4, distance);
                        point2 = QPointF(point2.x() - add.x(), point2.y() - add.y());
                        add = pointSplid(point3, point4, distance);
                        point3 = QPointF(point3.x() + add.x(), point3.y() - add.y());
                    }
                    point1 = QPointF(point2.x() + point3.x() - point4.x(), point2.y() + point3.y() - point4.y());
                    newResizeFPoints[0] = point1;
                    newResizeFPoints[1] = point2;
                    newResizeFPoints[2] = point3;
                    newResizeFPoints[3] = point4;
                    return newResizeFPoints;
                }
            }
    }
    return newResizeFPoints;
}

/* point5 in the  fourth position */
FourPoints point5Resize4(QPointF point1, QPointF point2, QPointF point3,
                         QPointF point4, QPointF pos, bool isShift) {
    FourPoints newResizeFPoints;
    newResizeFPoints = initFourPoints(newResizeFPoints);
    newResizeFPoints[0] = point1;
    newResizeFPoints[1] = point2;
    newResizeFPoints[2] = point3;
    newResizeFPoints[3] = point4;

    QPointF point7 = QPointF((point3.x() + point4.x())/2, (point3.y() + point4.y())/2);

    if (std::atan2((point2.y() - point1.y()), (point2.x() - point1.x())) >= -TANT2_EDGEVALUE &&
            (pos.x() - MIN_PADDING< point7.x()  || pointLineDir(point3, point4, pos) == 1 ||
             pointLineDir(point2, point4, pos) == -1)) {
        return newResizeFPoints;
    } else if (std::atan2((point2.y() - point1.y()), (point2.x() - point1.x()))  < -TANT2_EDGEVALUE &&
               (pos.y() + MIN_PADDING > point7.y() ||pointLineDir(point3, point4, pos) == 1 ||
                pointLineDir(point2, point4, pos) == -1)) {
        return newResizeFPoints;
    } else {
        if (pointToLineDistance(point3, point4, pos) < MIN_PADDING) {
            return newResizeFPoints;
        } else {
            if (!isShift) {
                if (pointLineDir(point1, point2, pos) == -1) {
                    qreal distance = pointToLineDistance(point1, point2, pos);
                    QPointF add = pointSplid(point1, point3, distance);
                    point1 = QPointF(point1.x() + add.x(), point1.y() - add.y());
                    add = pointSplid(point2, point4, distance);
                    point2 = QPointF(point2.x() + add.x(), point2.y() - add.y());
                } else {
                    qreal distance = pointToLineDistance(point1, point2, pos);
                    QPointF add = pointSplid(point1, point3, distance);
                    point1 = QPointF(point1.x() - add.x(), point1.y() + add.y());
                    add = pointSplid(point2, point4, distance);
                    point2 = QPointF(point2.x() - add.x(), point2.y() + add.y());
                }
                newResizeFPoints[0] = point1;
                newResizeFPoints[1] = point2;
                newResizeFPoints[2] = point3;
                newResizeFPoints[3] = point4;
                    return newResizeFPoints;
                } else {
                    qreal distance = pointToLineDistance(point1,  point2, pos);
                    if (pointLineDir(point1, point2, pos) == 1) {
                        QPointF add = pointSplid(point2, point4, distance);
                        point2 = QPointF(point2.x() - add.x(), point2.y() + add.y());
                        add = pointSplid(point3, point4, distance);
                        point3 = QPointF(point3.x() - add.x(), point3.y() - add.y());
                    } else {
                        QPointF add = pointSplid(point2, point4, distance);
                        point2 = QPointF(point2.x() + add.x(), point2.y() - add.y());
                        add = pointSplid(point3, point4, distance);
                        point3 = QPointF(point3.x() + add.x(), point3.y() + add.y());
                    }
                    point1 = QPointF(point2.x() + point3.x() - point4.x(), point2.y() + point3.y() - point4.y());
                    newResizeFPoints[0] = point1;
                    newResizeFPoints[1] = point2;
                    newResizeFPoints[2] = point3;
                    newResizeFPoints[3] = point4;
                    return newResizeFPoints;
                }
            }
        }

    return newResizeFPoints;
}

/* point5 in the fifth position */
FourPoints point5Resize5(QPointF point1, QPointF point2, QPointF point3,
                         QPointF point4, QPointF pos, bool isShift) {
    FourPoints newResizeFPoints;
    newResizeFPoints = initFourPoints(newResizeFPoints);
    newResizeFPoints[0] = point1;
    newResizeFPoints[1] = point2;
    newResizeFPoints[2] = point3;
    newResizeFPoints[3] = point4;

    QPointF point7 = QPointF((point3.x() + point4.x())/2, (point3.y() + point4.y())/2);

    if (pos.x() + MIN_PADDING > point7.x()) {
        return newResizeFPoints;
    } else {
        if (!isShift) {
            if (pointLineDir(point1, point2, pos) == -1) {
                qreal distance = pointToLineDistance(point1, point2, pos);
                QPointF add = pointSplid(point1, point3, distance);
                point1 = QPointF(point1.x() - add.x(), point1.y() + add.y());
                add = pointSplid(point2, point4, distance);
                point2 = QPointF(point2.x() - add.x(), point2.y() + add.y());
            } else {
                qreal distance = pointToLineDistance(point1, point2, pos);
                QPointF add = pointSplid(point1, point3, distance);
                point1 = QPointF(point1.x() + add.x(), point1.y() - add.y());
                add = pointSplid(point2, point4, distance);
                point2 = QPointF(point2.x() + add.x(), point2.y() - add.y());
            }
            newResizeFPoints[0] = point1;
            newResizeFPoints[1] = point2;
            newResizeFPoints[2] = point3;
            newResizeFPoints[3] = point4;
            return newResizeFPoints;
        } else {
            qreal distance = pointToLineDistance(point1,  point2, pos);
            if (pointLineDir(point1, point2, pos) == 1) {
                QPointF add = pointSplid(point2, point4, distance);
                point2 = QPointF(point2.x() + add.x(), point2.y() - add.y());
                add = pointSplid(point3, point4, distance);
                point3 = QPointF(point3.x() + add.x(), point3.y() + add.y());
            } else {
                QPointF add = pointSplid(point2, point4, distance);
                point2 = QPointF(point2.x() - add.x(), point2.y() + add.y());
                add = pointSplid(point3, point4, distance);
                point3 = QPointF(point3.x() - add.x(), point3.y() - add.y());
            }
            point1 = QPointF(point2.x() + point3.x() - point4.x(), point2.y() + point3.y() - point4.y());
            newResizeFPoints[0] = point1;
            newResizeFPoints[1] = point2;
            newResizeFPoints[2] = point3;
            newResizeFPoints[3] = point4;
            return newResizeFPoints;
        }
    }
    return newResizeFPoints;
}

/* point5 in the sixth position */
FourPoints point5Resize6(QPointF point1, QPointF point2, QPointF point3,
                         QPointF point4, QPointF pos, bool isShift) {
    Q_UNUSED(pos);
    Q_UNUSED(isShift);
    FourPoints newResizeFPoints;
    newResizeFPoints = initFourPoints(newResizeFPoints);
    newResizeFPoints[0] = point1;
    newResizeFPoints[1] = point2;
    newResizeFPoints[2] = point3;
    newResizeFPoints[3] = point4;

    return newResizeFPoints;
}

/* point5 in the seventh position */
FourPoints point5Resize7(QPointF point1, QPointF point2, QPointF point3,
                         QPointF point4, QPointF pos, bool isShift) {
    Q_UNUSED(pos);
    Q_UNUSED(isShift);
    FourPoints newResizeFPoints;
    newResizeFPoints = initFourPoints(newResizeFPoints);
    newResizeFPoints[0] = point1;
    newResizeFPoints[1] = point2;
    newResizeFPoints[2] = point3;
    newResizeFPoints[3] = point4;

    return newResizeFPoints;
}

/********************** sixth point6 ************************/
/* point6 in the first position */
FourPoints point6Resize1(QPointF point1, QPointF point2, QPointF point3,
                         QPointF point4, QPointF pos, bool isShift) {
    FourPoints newResizeFPoints;
    newResizeFPoints = initFourPoints(newResizeFPoints);
    newResizeFPoints[0] = point1;
    newResizeFPoints[1] = point2;
    newResizeFPoints[2] = point3;
    newResizeFPoints[3] = point4;

    QPointF point8 = QPointF((point2.x() + point4.x())/2, (point2.y() + point4.y())/2);

    if (std::atan2((point2.y() - point1.y()), (point2.x() - point1.x())) >= TANT_EDGEVALUE &&
            (pos.y() + MIN_PADDING > point8.x()  || pointLineDir(point3, point4, pos) == -1 ||
             pointLineDir(point2, point4, pos) == 1)) {
        return newResizeFPoints;
    } else if (std::atan2((point2.y() - point1.y()), (point2.x() - point1.x())) < TANT_EDGEVALUE &&
               (pos.x() + MIN_PADDING > point8.x() ||pointLineDir(point3, point4, pos) == -1 ||
                pointLineDir(point2, point4, pos) == 1)) {
        return newResizeFPoints;
    } else {
        if (pointToLineDistance(point2, point4, pos) < MIN_PADDING) {
            return newResizeFPoints;
        } else {
            if (!isShift) {
                if (pos.x()  >= (point2.x() + point4.x())/2 || pos.y() >= (point2.y() + point4.y())/2) {
                    return newResizeFPoints;
                } else {
                    if (pointLineDir(point1, point3, pos) == 1) {
                        qreal distance = pointToLineDistance(point1, point3, pos);
                        QPointF add = pointSplid(point1, point2, distance);
                        point1 = QPointF(point1.x() + add.x(), point1.y() + add.y());
                        add = pointSplid(point3, point4, distance);
                        point3 = QPointF(point3.x() + add.x(), point3.y() + add.y());
                    } else {
                        qreal distance = pointToLineDistance(point1, point3, pos);
                        QPointF add = pointSplid(point1, point2, distance);
                        point1 = QPointF(point1.x() - add.x(), point1.y() - add.y());
                        add = pointSplid(point3, point4, distance);
                        point3 = QPointF(point3.x() - add.x(), point3.y() - add.y());
                    }
                }
                newResizeFPoints[0] = point1;
                newResizeFPoints[1] = point2;
                newResizeFPoints[2] = point3;
                newResizeFPoints[3] = point4;
                return newResizeFPoints;
            } else {
                qreal distance = pointToLineDistance(point1,  point3, pos);
                if (pointLineDir(point1, point3, pos) == 1) {
                    QPointF add = pointSplid(point1, point2, distance);
                    point1 = QPointF(point1.x() + add.x(), point1.y() + add.y());
                    add = pointSplid(point2, point4, distance);
                    point4 = QPointF(point4.x() - add.x(), point4.y() + add.y());
                } else {
                    QPointF add = pointSplid(point1, point2, distance);
                    point1 = QPointF(point1.x() - add.x(), point1.y() - add.y());
                    add = pointSplid(point2, point4, distance);
                    point4 = QPointF(point4.x() + add.x(), point4.y() - add.y());
                }
                point3 = QPointF(point1.x() + point4.x() - point2.x(), point1.y() + point4.y() - point2.y());
                newResizeFPoints[0] = point1;
                newResizeFPoints[1] = point2;
                newResizeFPoints[2] = point3;
                newResizeFPoints[3] = point4;
                return newResizeFPoints;
            }
        }
    }
    return newResizeFPoints;
}
/* point6 in the second position */
FourPoints point6Resize2(QPointF point1, QPointF point2, QPointF point3,
                         QPointF point4, QPointF pos, bool isShift) {
    FourPoints newResizeFPoints;
    newResizeFPoints = initFourPoints(newResizeFPoints);
    newResizeFPoints[0] = point1;
    newResizeFPoints[1] = point2;
    newResizeFPoints[2] = point3;
    newResizeFPoints[3] = point4;

    QPointF point8 = QPointF((point2.x() + point4.x())/2, (point2.y() + point4.y())/2);

    if (std::atan2((point2.y() - point1.y()), (point2.x() - point1.x())) <= -TANT_EDGEVALUE &&
            (pos.y() - MIN_PADDING < point8.y()  || pointLineDir(point3, point4, pos) == -1 ||
             pointLineDir(point2, point4, pos) == -1)) {
        return newResizeFPoints;
    } else if (std::atan2((point2.y() - point1.y()), (point2.x() - point1.x())) > -TANT_EDGEVALUE &&
               (pos.x() + MIN_PADDING > point8.x() ||pointLineDir(point3, point4, pos) == -1 ||
                pointLineDir(point2, point4, pos) == -1)) {
        return newResizeFPoints;
    } else {
        if (pointToLineDistance(point2, point4, pos) < MIN_PADDING) {
            return newResizeFPoints;
        } else {
            if (!isShift) {
                if (pointLineDir(point1, point3, pos) == 1) {
                    qreal distance = pointToLineDistance(point1, point3, pos);
                    QPointF add = pointSplid(point1, point2, distance);
                    point1 = QPointF(point1.x() - add.x(), point1.y() + add.y());
                    add = pointSplid(point3, point4, distance);
                    point3 = QPointF(point3.x() - add.x(), point3.y() + add.y());
                } else {
                    qreal distance = pointToLineDistance(point1, point3, pos);
                    QPointF add = pointSplid(point1, point2, distance);
                    point1 = QPointF(point1.x() + add.x(), point1.y() - add.y());
                    add = pointSplid(point3, point4, distance);
                    point3 = QPointF(point3.x() + add.x(), point3.y() - add.y());
                }
                newResizeFPoints[0] = point1;
                newResizeFPoints[1] = point2;
                newResizeFPoints[2] = point3;
                newResizeFPoints[3] = point4;
                return newResizeFPoints;
            } else {
                qreal distance = pointToLineDistance(point1,  point3, pos);
                if (pointLineDir(point1, point3, pos) == -1) {
                    QPointF add = pointSplid(point1, point2, distance);
                    point1 = QPointF(point1.x() + add.x(), point1.y() - add.y());
                    add = pointSplid(point2, point4, distance);
                    point4 = QPointF(point4.x() + add.x(), point4.y() + add.y());
                } else {
                    QPointF add = pointSplid(point1, point2, distance);
                    point1 = QPointF(point1.x() - add.x(), point1.y() + add.y());
                    add = pointSplid(point2, point4, distance);
                    point4 = QPointF(point4.x() - add.x(), point4.y() - add.y());
                }
                point3 = QPointF(point1.x() + point4.x() - point2.x(), point1.y() + point4.y() - point2.y());
                newResizeFPoints[0] = point1;
                newResizeFPoints[1] = point2;
                newResizeFPoints[2] = point3;
                newResizeFPoints[3] = point4;
                return newResizeFPoints;
            }
        }
    }
    return newResizeFPoints;
}
/* point6 in the third position */
FourPoints point6Resize3(QPointF point1, QPointF point2, QPointF point3,
                         QPointF point4, QPointF pos, bool isShift) {
    FourPoints newResizeFPoints;
    newResizeFPoints = initFourPoints(newResizeFPoints);
    newResizeFPoints[0] = point1;
    newResizeFPoints[1] = point2;
    newResizeFPoints[2] = point3;
    newResizeFPoints[3] = point4;

    QPointF point8 = QPointF((point2.x() + point4.x())/2, (point2.y() + point4.y())/2);

    if (std::atan2((point2.y() - point1.y()), (point2.x() - point1.x())) >= TANT2_EDGEVALUE &&
            (pos.x() - MIN_PADDING < point8.x()  || pointLineDir(point3, point4, pos) == 1 ||
             pointLineDir(point2, point4, pos) == 1)) {
        return newResizeFPoints;
    } else if (std::atan2((point2.y() - point1.y()), (point2.x() - point1.x())) < TANT2_EDGEVALUE &&
               (pos.y() + MIN_PADDING > point8.y() ||pointLineDir(point3, point4, pos) == 1 ||
                pointLineDir(point2, point4, pos) == 1)) {
        return newResizeFPoints;
    } else {
        if (pointToLineDistance(point2, point4, pos) < MIN_PADDING) {
            return newResizeFPoints;
        } else {
            if (!isShift) {
                if (pointLineDir(point1, point3, pos) == -1) {
                    qreal distance = pointToLineDistance(point1, point3, pos);
                    QPointF add = pointSplid(point1, point2, distance);
                    point1 = QPointF(point1.x() + add.x(), point1.y() - add.y());
                    add = pointSplid(point3, point4, distance);
                    point3 = QPointF(point3.x() + add.x(), point3.y() - add.y());
                } else {
                    qreal distance = pointToLineDistance(point1, point3, pos);
                    QPointF add = pointSplid(point1, point2, distance);
                    point1 = QPointF(point1.x() - add.x(), point1.y() + add.y());
                    add = pointSplid(point3, point4, distance);
                    point3 = QPointF(point3.x() - add.x(), point3.y() + add.y());
                }
                newResizeFPoints[0] = point1;
                newResizeFPoints[1] = point2;
                newResizeFPoints[2] = point3;
                newResizeFPoints[3] = point4;
                return newResizeFPoints;
            } else {
                qreal distance = pointToLineDistance(point1,  point3, pos);
                if (pointLineDir(point1, point3, pos) == 1) {
                    QPointF add = pointSplid(point1, point2, distance);
                    point1 = QPointF(point1.x() - add.x(), point1.y() + add.y());
                    add = pointSplid(point2, point4, distance);
                    point4 = QPointF(point4.x() - add.x(), point4.y() - add.y());
                } else {
                    QPointF add = pointSplid(point1, point2, distance);
                    point1 = QPointF(point1.x() + add.x(), point1.y() - add.y());
                    add = pointSplid(point2, point4, distance);
                    point4 = QPointF(point4.x() + add.x(), point4.y() + add.y());
                }
                point3 = QPointF(point1.x() + point4.x() - point2.x(), point1.y() + point4.y() - point2.y());
                newResizeFPoints[0] = point1;
                newResizeFPoints[1] = point2;
                newResizeFPoints[2] = point3;
                newResizeFPoints[3] = point4;
                return newResizeFPoints;
            }
        }
    }
    return newResizeFPoints;
}
/* point6 in the fourth position */
FourPoints point6Resize4(QPointF point1, QPointF point2, QPointF point3,
                         QPointF point4, QPointF pos, bool isShift) {
    FourPoints newResizeFPoints;
    newResizeFPoints = initFourPoints(newResizeFPoints);
    newResizeFPoints[0] = point1;
    newResizeFPoints[1] = point2;
    newResizeFPoints[2] = point3;
    newResizeFPoints[3] = point4;

    QPointF point8 = QPointF((point2.x() + point4.x())/2, (point2.y() + point4.y())/2);

    if (std::atan2((point2.y() - point1.y()), (point2.x() - point1.x())) >= -TANT2_EDGEVALUE &&
            (pos.y() - MIN_PADDING < point8.y()  || pointLineDir(point3, point4, pos) == 1 ||
             pointLineDir(point2, point4, pos) == -1)) {
        return newResizeFPoints;
    } else if (std::atan2((point2.y() - point1.y()), (point2.x() - point1.x())) < -TANT2_EDGEVALUE &&
               (pos.x() - MIN_PADDING < point8.x() ||pointLineDir(point3, point4, pos) == 1 ||
                pointLineDir(point2, point4, pos) == -1)) {
        return newResizeFPoints;
    } else {
        if (pointToLineDistance(point2, point4, pos) < MIN_PADDING) {
            return newResizeFPoints;
        } else {
            if (!isShift) {
                if (pointLineDir(point1, point3, pos) == -1) {
                    qreal distance = pointToLineDistance(point1, point3, pos);
                    QPointF add = pointSplid(point1, point2, distance);
                    point1 = QPointF(point1.x() - add.x(), point1.y() - add.y());
                    add = pointSplid(point3, point4, distance);
                    point3 = QPointF(point3.x() - add.x(), point3.y() - add.y());
                } else {
                    qreal distance = pointToLineDistance(point1, point3, pos);
                    QPointF add = pointSplid(point1, point2, distance);
                    point1 = QPointF(point1.x() + add.x(), point1.y() + add.y());
                    add = pointSplid(point3, point4, distance);
                    point3 = QPointF(point3.x() + add.x(), point3.y() + add.y());
                }
                newResizeFPoints[0] = point1;
                newResizeFPoints[1] = point2;
                newResizeFPoints[2] = point3;
                newResizeFPoints[3] = point4;
                return newResizeFPoints;
            } else {
                qreal distance = pointToLineDistance(point1,  point3, pos);
                if (pointLineDir(point1, point3, pos) == -1) {
                    QPointF add = pointSplid(point1, point2, distance);
                    point1 = QPointF(point1.x() - add.x(), point1.y() - add.y());
                    add = pointSplid(point2, point4, distance);
                    point4 = QPointF(point4.x() + add.x(), point4.y() - add.y());
                } else {
                    QPointF add = pointSplid(point1, point2, distance);
                    point1 = QPointF(point1.x() + add.x(), point1.y() + add.y());
                    add = pointSplid(point2, point4, distance);
                    point4 = QPointF(point4.x() - add.x(), point4.y() + add.y());
                }
                point3 = QPointF(point1.x() + point4.x() - point2.x(), point1.y() + point4.y() - point2.y());
                newResizeFPoints[0] = point1;
                newResizeFPoints[1] = point2;
                newResizeFPoints[2] = point3;
                newResizeFPoints[3] = point4;
                return newResizeFPoints;
            }
        }
    }
    return newResizeFPoints;
}
/* point6 in the fifth position */
FourPoints point6Resize5(QPointF point1, QPointF point2, QPointF point3,
                         QPointF point4, QPointF pos, bool isShift) {
    FourPoints newResizeFPoints;
    newResizeFPoints = initFourPoints(newResizeFPoints);
    newResizeFPoints[0] = point1;
    newResizeFPoints[1] = point2;
    newResizeFPoints[2] = point3;
    newResizeFPoints[3] = point4;

    QPointF point8 = QPointF((point2.x() + point4.x())/2, (point2.y() + point4.y())/2);

    if (pos.y() + MIN_PADDING > point8.y()) {
        return newResizeFPoints;
    } else {
        if (!isShift) {
            if (pointLineDir(point1, point3, pos) == -1) {
                qreal distance = pointToLineDistance(point1, point3, pos);
                QPointF add = pointSplid(point1, point2, distance);
                point1 = QPointF(point1.x() - add.x(), point1.y() - add.y());
                add = pointSplid(point3, point4, distance);
                point3 = QPointF(point3.x() - add.x(), point3.y() - add.y());
            } else {
                qreal distance = pointToLineDistance(point1, point3, pos);
                QPointF add = pointSplid(point1, point2, distance);
                point1 = QPointF(point1.x() + add.x(), point1.y() + add.y());
                add = pointSplid(point3, point4, distance);
                point3 = QPointF(point3.x() + add.x(), point3.y() + add.y());
            }
            newResizeFPoints[0] = point1;
            newResizeFPoints[1] = point2;
            newResizeFPoints[2] = point3;
            newResizeFPoints[3] = point4;
            return newResizeFPoints;
        } else {
            qreal distance = pointToLineDistance(point1,  point3, pos);
            if (pointLineDir(point1, point3, pos) == 1) {
                QPointF add = pointSplid(point1, point2, distance);
                point1 = QPointF(point1.x() + add.x(), point1.y() + add.y());
                add = pointSplid(point2, point4, distance);
                point4 = QPointF(point4.x() - add.x(), point4.y() + add.y());
            } else {
                QPointF add = pointSplid(point1, point2, distance);
                point1 = QPointF(point1.x() - add.x(), point1.y() - add.y());
                add = pointSplid(point2, point4, distance);
                point4 = QPointF(point4.x() + add.x(), point4.y() - add.y());
            }
            point3 = QPointF(point1.x() + point4.x() - point2.x(), point1.y() + point4.y() - point2.y());
            newResizeFPoints[0] = point1;
            newResizeFPoints[1] = point2;
            newResizeFPoints[2] = point3;
            newResizeFPoints[3] = point4;
            return newResizeFPoints;
        }
    }
    return newResizeFPoints;
}
/* point6 in the sixth position */
FourPoints point6Resize6(QPointF point1, QPointF point2, QPointF point3,
                         QPointF point4, QPointF pos, bool isShift) {
    Q_UNUSED(pos);
    Q_UNUSED(isShift);
    FourPoints newResizeFPoints;
    newResizeFPoints = initFourPoints(newResizeFPoints);
    newResizeFPoints[0] = point1;
    newResizeFPoints[1] = point2;
    newResizeFPoints[2] = point3;
    newResizeFPoints[3] = point4;

    return newResizeFPoints;
}
/* point6 in the seventh position */
FourPoints point6Resize7(QPointF point1, QPointF point2, QPointF point3,
                         QPointF point4, QPointF pos, bool isShift) {
    Q_UNUSED(pos);
    Q_UNUSED(isShift);
    FourPoints newResizeFPoints;
    newResizeFPoints = initFourPoints(newResizeFPoints);
    newResizeFPoints[0] = point1;
    newResizeFPoints[1] = point2;
    newResizeFPoints[2] = point3;
    newResizeFPoints[3] = point4;

    return newResizeFPoints;
}

/********************** seventh point7 ************************/
/* point7 in the first position */
FourPoints point7Resize1(QPointF point1, QPointF point2, QPointF point3,
                         QPointF point4, QPointF pos, bool isShift) {
    FourPoints newResizeFPoints;
    newResizeFPoints = initFourPoints(newResizeFPoints);
    newResizeFPoints[0] = point1;
    newResizeFPoints[1] = point2;
    newResizeFPoints[2] = point3;
    newResizeFPoints[3] = point4;

    QPointF point5 = QPointF((point2.x() + point1.x())/2, (point2.y() + point1.y())/2);

    if (std::atan2((point2.y() - point1.y()), (point2.x() - point1.x())) >= TANT_EDGEVALUE &&
            (pos.x() - MIN_PADDING < point5.x()  || pointLineDir(point1, point2, pos) == 1 ||
             pointLineDir(point2, point4, pos) == 1)) {
        return newResizeFPoints;
    } else if (std::atan2((point2.y() - point1.y()), (point2.x() - point1.x())) < TANT_EDGEVALUE &&
               (pos.y() + MIN_PADDING > point5.y() ||pointLineDir(point1, point2, pos) == 1 ||
                pointLineDir(point2, point4, pos) == 1)) {
        return newResizeFPoints;
    } else {
        if (pointToLineDistance(point2, point1, pos) < MIN_PADDING) {
            return newResizeFPoints;
        } else {
            if (!isShift) {
                if (pos.x()  < (point1.x() + point2.x())/2 || pos.y() > (point1.y() + point2.y())/2) {
                    return newResizeFPoints;
                } else {
                    if (pointLineDir(point3, point4, pos) == -1) {
                        qreal distance = pointToLineDistance(point3, point4, pos);
                        QPointF add = pointSplid(point1, point3, distance);
                        point3 = QPointF(point3.x() + add.x(), point3.y() - add.y());
                        add = pointSplid(point2, point4, distance);
                        point4 = QPointF(point4.x() + add.x(), point4.y() - add.y());
                    } else {
                        qreal distance = pointToLineDistance(point3, point4, pos);
                        QPointF add = pointSplid(point1, point3, distance);
                        point3 = QPointF(point3.x() - add.x(), point3.y() + add.y());
                        add = pointSplid(point2, point4, distance);
                        point4 = QPointF(point4.x() - add.x(), point4.y() + add.y());
                    }
                }
                newResizeFPoints[0] = point1;
                newResizeFPoints[1] = point2;
                newResizeFPoints[2] = point3;
                newResizeFPoints[3] = point4;
                return newResizeFPoints;
            } else {
                qreal distance = pointToLineDistance(point3,  point4, pos);
                if (pointLineDir(point3, point4, pos) == 1) {
                    QPointF add = pointSplid(point1, point2, distance);
                    point2 = QPointF(point2.x() - add.x(), point2.y() - add.y());
                    add = pointSplid(point1, point3, distance);
                    point3 = QPointF(point3.x() - add.x(), point3.y() + add.y());
                } else {
                    QPointF add = pointSplid(point1, point2, distance);
                    point2 = QPointF(point2.x() + add.x(), point2.y() + add.y());
                    add = pointSplid(point1, point3, distance);
                    point3 = QPointF(point3.x() + add.x(), point3.y() - add.y());
                }
                point4 = QPointF(point2.x() + point3.x() - point1.x(), point2.y() + point3.y() - point1.y());
                newResizeFPoints[0] = point1;
                newResizeFPoints[1] = point2;
                newResizeFPoints[2] = point3;
                newResizeFPoints[3] = point4;
                return newResizeFPoints;
            }
        }
    }
    return newResizeFPoints;
}
/* point7 in the second position */
FourPoints point7Resize2(QPointF point1, QPointF point2, QPointF point3,
                         QPointF point4, QPointF pos, bool isShift) {
    FourPoints newResizeFPoints;
    newResizeFPoints = initFourPoints(newResizeFPoints);
    newResizeFPoints[0] = point1;
    newResizeFPoints[1] = point2;
    newResizeFPoints[2] = point3;
    newResizeFPoints[3] = point4;

    QPointF point5 = QPointF((point2.x() + point1.x())/2, (point2.y() + point1.y())/2);

    if (std::atan2((point2.y() - point1.y()), (point2.x() - point1.x())) <= -TANT_EDGEVALUE &&
            (pos.x() + MIN_PADDING > point5.x()  || pointLineDir(point1, point2, pos) == 1 ||
             pointLineDir(point2, point4, pos) == -1)) {
        return newResizeFPoints;
    } else if (std::atan2((point2.y() - point1.y()), (point2.x() - point1.x())) > -TANT_EDGEVALUE &&
               (pos.y() + MIN_PADDING > point5.y() ||pointLineDir(point1, point2, pos) == 1 ||
                pointLineDir(point2, point4, pos) == -1)) {
        return newResizeFPoints;
    } else {
        if (pointToLineDistance(point2, point1, pos) < MIN_PADDING) {
            return newResizeFPoints;
        } else {
            if (!isShift) {
                if (pointLineDir(point3, point4, pos) == -1) {
                    qreal distance = pointToLineDistance(point3, point4, pos);
                    QPointF add = pointSplid(point1, point3, distance);
                    point3 = QPointF(point3.x() - add.x(), point3.y() - add.y());
                    add = pointSplid(point2, point4, distance);
                    point4 = QPointF(point4.x() - add.x(), point4.y() - add.y());
                } else {
                    qreal distance = pointToLineDistance(point3, point4, pos);
                    QPointF add = pointSplid(point1, point3, distance);
                    point3 = QPointF(point3.x() + add.x(), point3.y() + add.y());
                    add = pointSplid(point2, point4, distance);
                    point4 = QPointF(point4.x() + add.x(), point4.y() + add.y());
                }
                newResizeFPoints[0] = point1;
                newResizeFPoints[1] = point2;
                newResizeFPoints[2] = point3;
                newResizeFPoints[3] = point4;
                return newResizeFPoints;
            } else {
                qreal distance = pointToLineDistance(point3,  point4, pos);
                if (pointLineDir(point3, point4, pos) == 1) {
                    QPointF add = pointSplid(point1, point2, distance);
                    point2 = QPointF(point2.x() - add.x(), point2.y() + add.y());
                    add = pointSplid(point1, point3, distance);
                    point3 = QPointF(point3.x() + add.x(), point3.y() + add.y());
                } else {
                    QPointF add = pointSplid(point1, point2, distance);
                    point2 = QPointF(point2.x() + add.x(), point2.y() - add.y());
                    add = pointSplid(point1, point3, distance);
                    point3 = QPointF(point3.x() - add.x(), point3.y() - add.y());
                }
                point4 = QPointF(point2.x() + point3.x() - point1.x(), point2.y() + point3.y() - point1.y());
                newResizeFPoints[0] = point1;
                newResizeFPoints[1] = point2;
                newResizeFPoints[2] = point3;
                newResizeFPoints[3] = point4;
                return newResizeFPoints;
            }
        }
    }
    return newResizeFPoints;
}
/* point7 in the third position */
FourPoints point7Resize3(QPointF point1, QPointF point2, QPointF point3,
                         QPointF point4, QPointF pos, bool isShift) {
    FourPoints newResizeFPoints;
    newResizeFPoints = initFourPoints(newResizeFPoints);
    newResizeFPoints[0] = point1;
    newResizeFPoints[1] = point2;
    newResizeFPoints[2] = point3;
    newResizeFPoints[3] = point4;

    QPointF point5 = QPointF((point2.x() + point1.x())/2, (point2.y() + point1.y())/2);

    if (std::atan2((point2.y() - point1.y()), (point2.x() - point1.x())) >= TANT2_EDGEVALUE &&
            (pos.y() - MIN_PADDING < point5.y()|| pointLineDir(point1, point2, pos) == -1 ||
             pointLineDir(point2, point4, pos) == 1)) {
        return newResizeFPoints;
    } else if (std::atan2((point2.y() - point1.y()), (point2.x() - point1.x())) < TANT2_EDGEVALUE &&
               (pos.x() - MIN_PADDING < point5.x() ||pointLineDir(point1, point2, pos) == -1 ||
                pointLineDir(point2, point4, pos) == 1)) {
        return newResizeFPoints;
    } else {
        if (pointToLineDistance(point2, point1, pos) < MIN_PADDING) {
            return newResizeFPoints;
        } else {
            if (!isShift) {
                if (pointLineDir(point3, point4, pos) == 1) {
                    qreal distance = pointToLineDistance(point3, point4, pos);
                    QPointF add = pointSplid(point1, point3, distance);
                    point3 = QPointF(point3.x() + add.x(), point3.y() + add.y());
                    add = pointSplid(point2, point4, distance);
                    point4 = QPointF(point4.x() + add.x(), point4.y() + add.y());
                } else {
                    qreal distance = pointToLineDistance(point3, point4, pos);
                    QPointF add = pointSplid(point1, point3, distance);
                    point3 = QPointF(point3.x() - add.x(), point3.y() - add.y());
                    add = pointSplid(point2, point4, distance);
                    point4 = QPointF(point4.x() - add.x(), point4.y() - add.y());
                }
                newResizeFPoints[0] = point1;
                newResizeFPoints[1] = point2;
                newResizeFPoints[2] = point3;
                newResizeFPoints[3] = point4;
                return newResizeFPoints;
            } else {
                qreal distance = pointToLineDistance(point3,  point4, pos);
                if (pointLineDir(point3, point4, pos) == -1) {
                    QPointF add = pointSplid(point1, point2, distance);
                    point2 = QPointF(point2.x() + add.x(), point2.y() - add.y());
                    add = pointSplid(point1, point3, distance);
                    point3 = QPointF(point3.x() - add.x(), point3.y() - add.y());
                } else {
                    QPointF add = pointSplid(point1, point2, distance);
                    point2 = QPointF(point2.x() - add.x(), point2.y() + add.y());
                    add = pointSplid(point1, point3, distance);
                    point3 = QPointF(point3.x() + add.x(), point3.y() + add.y());
                }
                point4 = QPointF(point2.x() + point3.x() - point1.x(), point2.y() + point3.y() - point1.y());
                newResizeFPoints[0] = point1;
                newResizeFPoints[1] = point2;
                newResizeFPoints[2] = point3;
                newResizeFPoints[3] = point4;
                return newResizeFPoints;
            }
        }
    }
    return newResizeFPoints;
}
/* point7 in the fourth position */
FourPoints point7Resize4(QPointF point1, QPointF point2, QPointF point3,
                         QPointF point4, QPointF pos, bool isShift) {
    FourPoints newResizeFPoints;
    newResizeFPoints = initFourPoints(newResizeFPoints);
    newResizeFPoints[0] = point1;
    newResizeFPoints[1] = point2;
    newResizeFPoints[2] = point3;
    newResizeFPoints[3] = point4;

    QPointF point5 = QPointF((point2.x() + point4.x())/2, (point2.y() + point4.y())/2);

    if (std::atan2((point2.y() - point1.y()), (point2.x() - point1.x())) >= -TANT2_EDGEVALUE &&
            (pos.x() + MIN_PADDING > point5.x()  || pointLineDir(point1, point2, pos) == -1 ||
             pointLineDir(point2, point4, pos) == -1)) {
        return newResizeFPoints;
    } else if (std::atan2((point2.y() - point1.y()), (point2.x() - point1.x())) < -TANT2_EDGEVALUE &&
               (pos.y() - MIN_PADDING < point5.y() ||pointLineDir(point1, point2, pos) == -1 ||
                pointLineDir(point2, point4, pos) == -1)) {
        return newResizeFPoints;
    } else {
        if (pointToLineDistance(point2, point1, pos) < MIN_PADDING) {
            return newResizeFPoints;
        } else {
            if (!isShift) {
                if (pointLineDir(point3, point4, pos) == -1) {
                    qreal distance = pointToLineDistance(point3, point4, pos);
                    QPointF add = pointSplid(point1, point3, distance);
                    point3 = QPointF(point3.x() + add.x(), point3.y() - add.y());
                    add = pointSplid(point2, point4, distance);
                    point4 = QPointF(point4.x() + add.x(), point4.y() - add.y());
                } else {
                    qreal distance = pointToLineDistance(point3, point4, pos);
                    QPointF add = pointSplid(point1, point3, distance);
                    point3 = QPointF(point3.x() - add.x(), point3.y() + add.y());
                    add = pointSplid(point2, point4, distance);
                    point4 = QPointF(point4.x() - add.x(), point4.y() + add.y());
                }
                newResizeFPoints[0] = point1;
                newResizeFPoints[1] = point2;
                newResizeFPoints[2] = point3;
                newResizeFPoints[3] = point4;
                return newResizeFPoints;
            } else {
                qreal distance = pointToLineDistance(point3,  point4, pos);
                if (pointLineDir(point3, point4, pos) == -1) {
                    QPointF add = pointSplid(point1, point2, distance);
                    point2 = QPointF(point2.x() + add.x(), point2.y() + add.y());
                    add = pointSplid(point1, point3, distance);
                    point3 = QPointF(point3.x() + add.x(), point3.y() - add.y());
                } else {
                    QPointF add = pointSplid(point1, point2, distance);
                    point2 = QPointF(point2.x() - add.x(), point2.y() - add.y());
                    add = pointSplid(point1, point3, distance);
                    point3 = QPointF(point3.x() - add.x(), point3.y() + add.y());
                }
                point4 = QPointF(point2.x() + point3.x() - point1.x(), point2.y() + point3.y() - point1.y());
                newResizeFPoints[0] = point1;
                newResizeFPoints[1] = point2;
                newResizeFPoints[2] = point3;
                newResizeFPoints[3] = point4;
                return newResizeFPoints;
            }
        }
    }
    return newResizeFPoints;
}
/* point7 in the fifth position */
FourPoints point7Resize5(QPointF point1, QPointF point2, QPointF point3,
                         QPointF point4, QPointF pos, bool isShift) {
    FourPoints newResizeFPoints;
    newResizeFPoints = initFourPoints(newResizeFPoints);
    newResizeFPoints[0] = point1;
    newResizeFPoints[1] = point2;
    newResizeFPoints[2] = point3;
    newResizeFPoints[3] = point4;

    QPointF point5 = QPointF((point2.x() + point1.x())/2, (point2.y() + point1.y())/2);

    if (pos.x() - MIN_PADDING < point5.x()) {
        return newResizeFPoints;
    } else {
        if (!isShift) {
            if (pointLineDir(point3, point4, pos) == 1) {
                qreal distance = pointToLineDistance(point3, point4, pos);
                QPointF add = pointSplid(point1, point3, distance);
                point3 = QPointF(point3.x() + add.x(), point3.y() - add.y());
                add = pointSplid(point2, point4, distance);
                point4 = QPointF(point4.x() + add.x(), point4.y() - add.y());
            } else {
                qreal distance = pointToLineDistance(point3, point4, pos);
                QPointF add = pointSplid(point1, point3, distance);
                point3 = QPointF(point3.x() - add.x(), point3.y() + add.y());
                add = pointSplid(point2, point4, distance);
                point4 = QPointF(point4.x() - add.x(), point4.y() + add.y());
            }
            newResizeFPoints[0] = point1;
            newResizeFPoints[1] = point2;
            newResizeFPoints[2] = point3;
            newResizeFPoints[3] = point4;
            return newResizeFPoints;
        } else {
            qreal distance = pointToLineDistance(point3,  point4, pos);
            if (pointLineDir(point3, point4, pos) == -1) {
                QPointF add = pointSplid(point1, point2, distance);
                point2 = QPointF(point2.x() - add.x(), point2.y() - add.y());
                add = pointSplid(point1, point3, distance);
                point3 = QPointF(point3.x() - add.x(), point3.y() + add.y());
            } else {
                QPointF add = pointSplid(point1, point2, distance);
                point2 = QPointF(point2.x() + add.x(), point2.y() + add.y());
                add = pointSplid(point1, point3, distance);
                point3 = QPointF(point3.x() + add.x(), point3.y() - add.y());
            }
            point4 = QPointF(point2.x() + point3.x() - point1.x(), point2.y() + point3.y() - point1.y());
            newResizeFPoints[0] = point1;
            newResizeFPoints[1] = point2;
            newResizeFPoints[2] = point3;
            newResizeFPoints[3] = point4;
            return newResizeFPoints;
        }
    }
    return newResizeFPoints;
}
/* point7 in the sixth position */
FourPoints point7Resize6(QPointF point1, QPointF point2, QPointF point3,
                         QPointF point4, QPointF pos, bool isShift) {
    Q_UNUSED(pos);
    Q_UNUSED(isShift);
    FourPoints newResizeFPoints;
    newResizeFPoints = initFourPoints(newResizeFPoints);
    newResizeFPoints[0] = point1;
    newResizeFPoints[1] = point2;
    newResizeFPoints[2] = point3;
    newResizeFPoints[3] = point4;

    return newResizeFPoints;
}
/* point6 in the seventh position */
FourPoints point7Resize7(QPointF point1, QPointF point2, QPointF point3,
                         QPointF point4, QPointF pos, bool isShift) {
    Q_UNUSED(pos);
    Q_UNUSED(isShift);
    FourPoints newResizeFPoints;
    newResizeFPoints = initFourPoints(newResizeFPoints);
    newResizeFPoints[0] = point1;
    newResizeFPoints[1] = point2;
    newResizeFPoints[2] = point3;
    newResizeFPoints[3] = point4;

    return newResizeFPoints;
}

/********************** eighth point8 ************************/
/* point8 in the first position */
FourPoints point8Resize1(QPointF point1, QPointF point2, QPointF point3,
                         QPointF point4, QPointF pos, bool isShift) {
    FourPoints newResizeFPoints;
    newResizeFPoints = initFourPoints(newResizeFPoints);
    newResizeFPoints[0] = point1;
    newResizeFPoints[1] = point2;
    newResizeFPoints[2] = point3;
    newResizeFPoints[3] = point4;

    QPointF point6 = QPointF((point3.x() + point1.x())/2, (point3.y() + point1.y())/2);

    if (std::atan2((point2.y() - point1.y()), (point2.x() - point1.x())) >= TANT_EDGEVALUE &&
            (pos.y() - MIN_PADDING < point6.y()  || pointLineDir(point1, point3, pos) == -1 ||
             pointLineDir(point3, point4, pos) == -1)) {
        return newResizeFPoints;
    } else if (std::atan2((point2.y() - point1.y()), (point2.x() - point1.x())) < TANT_EDGEVALUE &&
               (pos.x() - MIN_PADDING < point6.x() ||pointLineDir(point1, point3, pos) == -1 ||
                pointLineDir(point3, point4, pos) == -1)) {
        return newResizeFPoints;
    } else {
        if (pointToLineDistance(point1, point3, pos) < MIN_PADDING) {
            return newResizeFPoints;
        } else {
            if (pointToLineDistance(point1, point3, pos) < MIN_PADDING) {
                return newResizeFPoints;
            } else {
                if (!isShift) {
                    if (pos.y()  <= (point1.y() + point3.y())/2) {
                        return newResizeFPoints;
                    } else {
                        if (pointLineDir(point2, point4, pos) == 1) {
                            qreal distance = pointToLineDistance(point2, point4, pos);
                            QPointF add = pointSplid(point1, point2, distance);
                            point2 = QPointF(point2.x() + add.x(), point2.y() + add.y());
                            add = pointSplid(point3, point4, distance);
                            point4 = QPointF(point4.x() + add.x(), point4.y() + add.y());
                        } else {
                            qreal distance = pointToLineDistance(point2, point4, pos);
                            QPointF add = pointSplid(point1, point2, distance);
                            point2 = QPointF(point2.x() - add.x(), point2.y() - add.y());
                            add = pointSplid(point3, point4, distance);
                            point4 = QPointF(point4.x() - add.x(), point4.y() - add.y());
                        }
                    }
                    newResizeFPoints[0] = point1;
                    newResizeFPoints[1] = point2;
                    newResizeFPoints[2] = point3;
                    newResizeFPoints[3] = point4;
                    return newResizeFPoints;
                } else {
                    qreal distance = pointToLineDistance(point2,  point4, pos);
                    if (pointLineDir(point2, point4, pos) == -1) {
                        QPointF add = pointSplid(point1, point3, distance);
                        point1 = QPointF(point1.x() + add.x(), point1.y() - add.y());
                        add = pointSplid(point3, point4, distance);
                        point4 = QPointF(point4.x() - add.x(), point4.y() - add.y());
                    } else {
                        QPointF add = pointSplid(point1, point3, distance);
                        point1 = QPointF(point1.x() - add.x(), point1.y() + add.y());
                        add = pointSplid(point3, point4, distance);
                        point4 = QPointF(point4.x() + add.x(), point4.y() + add.y());
                    }
                    point2 = QPointF(point1.x() + point4.x() - point3.x(), point1.y() + point4.y() - point3.y());
                    newResizeFPoints[0] = point1;
                    newResizeFPoints[1] = point2;
                    newResizeFPoints[2] = point3;
                    newResizeFPoints[3] = point4;
                    return newResizeFPoints;
                }
            }
        }
    }
    return newResizeFPoints;
}
/* point8 in the second position */
FourPoints point8Resize2(QPointF point1, QPointF point2, QPointF point3,
                         QPointF point4, QPointF pos, bool isShift) {
    FourPoints newResizeFPoints;
    newResizeFPoints = initFourPoints(newResizeFPoints);
    newResizeFPoints[0] = point1;
    newResizeFPoints[1] = point2;
    newResizeFPoints[2] = point3;
    newResizeFPoints[3] = point4;

    QPointF point6 = QPointF((point3.x() + point1.x())/2, (point3.y() + point1.y())/2);

    if (std::atan2((point2.y() - point1.y()), (point2.x() - point1.x())) <= -TANT_EDGEVALUE &&
            (pos.y() + MIN_PADDING > point6.y()  || pointLineDir(point1, point3, pos) == 1 ||
             pointLineDir(point3, point4, pos) == -1)) {
        return newResizeFPoints;
    } else if (std::atan2((point2.y() - point1.y()), (point2.x() - point1.x())) > -TANT_EDGEVALUE &&
               (pos.x() - MIN_PADDING < point6.x() ||pointLineDir(point1, point3, pos) == 1 ||
                pointLineDir(point3, point4, pos) == -1)) {
        return newResizeFPoints;
    } else {
        if (pointToLineDistance(point1, point3, pos) < MIN_PADDING) {
            return newResizeFPoints;
        } else {
            if (!isShift) {
                if (pointLineDir(point2, point4, pos) == -1) {
                    qreal distance = pointToLineDistance(point2, point4, pos);
                    QPointF add = pointSplid(point1, point2, distance);
                    point2 = QPointF(point2.x() + add.x(), point2.y() - add.y());
                    add = pointSplid(point3, point4, distance);
                    point4 = QPointF(point4.x() + add.x(), point4.y() - add.y());
                } else {
                    qreal distance = pointToLineDistance(point2, point4, pos);
                    QPointF add = pointSplid(point1, point2, distance);
                    point2 = QPointF(point2.x() - add.x(), point2.y() + add.y());
                    add = pointSplid(point3, point4, distance);
                    point4 = QPointF(point4.x() - add.x(), point4.y() + add.y());
                }
                newResizeFPoints[0] = point1;
                newResizeFPoints[1] = point2;
                newResizeFPoints[2] = point3;
                newResizeFPoints[3] = point4;
                return newResizeFPoints;
            } else {
                qreal distance = pointToLineDistance(point2,  point4, pos);
                if (pointLineDir(point2, point4, pos) == 1) {
                    QPointF add = pointSplid(point1, point3, distance);
                    point1 = QPointF(point1.x() - add.x(), point1.y() - add.y());
                    add = pointSplid(point3, point4, distance);
                    point4 = QPointF(point4.x() - add.x(), point4.y() + add.y());
                } else {
                    QPointF add = pointSplid(point1, point3, distance);
                    point1 = QPointF(point1.x() + add.x(), point1.y() + add.y());
                    add = pointSplid(point3, point4, distance);
                    point4 = QPointF(point4.x() + add.x(), point4.y() - add.y());
                }
                point2 = QPointF(point1.x() + point4.x() - point3.x(), point1.y() + point4.y() - point3.y());
                newResizeFPoints[0] = point1;
                newResizeFPoints[1] = point2;
                newResizeFPoints[2] = point3;
                newResizeFPoints[3] = point4;
                return newResizeFPoints;
            }
        }
    }
    return newResizeFPoints;
}
/* point8 in the third position */
FourPoints point8Resize3(QPointF point1, QPointF point2, QPointF point3,
                         QPointF point4, QPointF pos, bool isShift) {
    FourPoints newResizeFPoints;
    newResizeFPoints = initFourPoints(newResizeFPoints);
    newResizeFPoints[0] = point1;
    newResizeFPoints[1] = point2;
    newResizeFPoints[2] = point3;
    newResizeFPoints[3] = point4;

    QPointF point6 = QPointF((point3.x() + point1.x())/2, (point3.y() + point1.y())/2);

    if (std::atan2((point2.y() - point1.y()), (point2.x() - point1.x())) >= TANT2_EDGEVALUE &&
            (pos.x() + MIN_PADDING > point6.x()  || pointLineDir(point1, point3, pos) == -1 ||
             pointLineDir(point3, point4, pos) == 1)) {
        return newResizeFPoints;
    } else if (std::atan2((point2.y() - point1.y()), (point2.x() - point1.x())) < TANT2_EDGEVALUE &&
               (pos.y() - MIN_PADDING < point6.y() ||pointLineDir(point1, point3, pos) == -1 ||
                pointLineDir(point3, point4, pos) == 1)) {
        return newResizeFPoints;
    } else {
        if (pointToLineDistance(point1, point3, pos) < MIN_PADDING) {
            return newResizeFPoints;
        } else {
            if (!isShift) {
                if (pointLineDir(point2, point4, pos) == -1) {
                    qreal distance = pointToLineDistance(point2, point4, pos);
                    QPointF add = pointSplid(point1, point2, distance);
                    point2 = QPointF(point2.x() + add.x(), point2.y() - add.y());
                    add = pointSplid(point3, point4, distance);
                    point4 = QPointF(point4.x() + add.x(), point4.y() - add.y());
                } else {
                    qreal distance = pointToLineDistance(point2, point4, pos);
                    QPointF add = pointSplid(point1, point2, distance);
                    point2 = QPointF(point2.x() - add.x(), point2.y() + add.y());
                    add = pointSplid(point3, point4, distance);
                    point4 = QPointF(point4.x() - add.x(), point4.y() + add.y());
                }
                newResizeFPoints[0] = point1;
                newResizeFPoints[1] = point2;
                newResizeFPoints[2] = point3;
                newResizeFPoints[3] = point4;
                return newResizeFPoints;
            } else {
                qreal distance = pointToLineDistance(point2,  point4, pos);
                if (pointLineDir(point2, point4, pos) == 1) {
                    QPointF add = pointSplid(point1, point3, distance);
                    point1 = QPointF(point1.x() - add.x(), point1.y() - add.y());
                    add = pointSplid(point3, point4, distance);
                    point4 = QPointF(point4.x() - add.x(), point4.y() + add.y());
                } else {
                    QPointF add = pointSplid(point1, point3, distance);
                    point1 = QPointF(point1.x() + add.x(), point1.y() + add.y());
                    add = pointSplid(point3, point4, distance);
                    point4 = QPointF(point4.x() + add.x(), point4.y() - add.y());
                }
                point2 = QPointF(point1.x() + point4.x() - point3.x(), point1.y() + point4.y() - point3.y());
                newResizeFPoints[0] = point1;
                newResizeFPoints[1] = point2;
                newResizeFPoints[2] = point3;
                newResizeFPoints[3] = point4;
                return newResizeFPoints;
            }
        }
    }
    return newResizeFPoints;
}
/* point8 in the fourth position */
FourPoints point8Resize4(QPointF point1, QPointF point2, QPointF point3,
                         QPointF point4, QPointF pos, bool isShift) {
    FourPoints newResizeFPoints;
    newResizeFPoints = initFourPoints(newResizeFPoints);
    newResizeFPoints[0] = point1;
    newResizeFPoints[1] = point2;
    newResizeFPoints[2] = point3;
    newResizeFPoints[3] = point4;

    QPointF point6 = QPointF((point3.x() + point1.x())/2, (point3.y() + point1.y())/2);

    if (std::atan2((point2.y() - point1.y()), (point2.x() - point1.x())) >= -TANT2_EDGEVALUE &&
            (pos.y() + MIN_PADDING > point6.y()  || pointLineDir(point1, point3, pos) == 1 ||
             pointLineDir(point3, point4, pos) == 1)) {
        return newResizeFPoints;
    } else if (std::atan2((point2.y() - point1.y()), (point2.x() - point1.x())) < -TANT2_EDGEVALUE &&
               (pos.x() + MIN_PADDING > point6.x() ||pointLineDir(point1, point3, pos) == 1 ||
                pointLineDir(point3, point4, pos) == 1)) {
        return newResizeFPoints;
    } else {
        if (pointToLineDistance(point3, point1, pos) < MIN_PADDING) {
            return newResizeFPoints;
        } else {
            if (!isShift) {
                if (pointLineDir(point2, point4, pos) == -1) {
                    qreal distance = pointToLineDistance(point2, point4, pos);
                    QPointF add = pointSplid(point1, point2, distance);
                    point2 = QPointF(point2.x() - add.x(), point2.y() - add.y());
                    add = pointSplid(point3, point4, distance);
                    point4 = QPointF(point4.x() - add.x(), point4.y() - add.y());
                } else {
                    qreal distance = pointToLineDistance(point2, point4, pos);
                    QPointF add = pointSplid(point1, point2, distance);
                    point2 = QPointF(point2.x() + add.x(), point2.y() + add.y());
                    add = pointSplid(point3, point4, distance);
                    point4 = QPointF(point4.x() + add.x(), point4.y() + add.y());
                }
                newResizeFPoints[0] = point1;
                newResizeFPoints[1] = point2;
                newResizeFPoints[2] = point3;
                newResizeFPoints[3] = point4;
                return newResizeFPoints;
            } else {
                qreal distance = pointToLineDistance(point2,  point4, pos);
                if (pointLineDir(point2, point4, pos) == 1) {
                    QPointF add = pointSplid(point1, point3, distance);
                    point1 = QPointF(point1.x() - add.x(), point1.y() + add.y());
                    add = pointSplid(point3, point4, distance);
                    point4 = QPointF(point4.x() + add.x(), point4.y() + add.y());
                } else {
                    QPointF add = pointSplid(point1, point3, distance);
                    point1 = QPointF(point1.x() + add.x(), point1.y() - add.y());
                    add = pointSplid(point3, point4, distance);
                    point4 = QPointF(point4.x() - add.x(), point4.y() - add.y());
                }
                point2 = QPointF(point1.x() + point4.x() - point3.x(), point1.y() + point4.y() - point3.y());
                newResizeFPoints[0] = point1;
                newResizeFPoints[1] = point2;
                newResizeFPoints[2] = point3;
                newResizeFPoints[3] = point4;
                return newResizeFPoints;
            }
        }
    }
    return newResizeFPoints;
}
/* point8 in the fifth position */
FourPoints point8Resize5(QPointF point1, QPointF point2, QPointF point3,
                         QPointF point4, QPointF pos, bool isShift) {
    FourPoints newResizeFPoints;
    newResizeFPoints = initFourPoints(newResizeFPoints);
    newResizeFPoints[0] = point1;
    newResizeFPoints[1] = point2;
    newResizeFPoints[2] = point3;
    newResizeFPoints[3] = point4;

    QPointF point6 = QPointF((point3.x() + point1.x())/2, (point3.y() + point1.y())/2);

    if (pos.y() - MIN_PADDING < point6.y()) {
        return newResizeFPoints;
    } else {
        if (!isShift) {
            if (pointLineDir(point2, point4, pos) == 1) {
                qreal distance = pointToLineDistance(point2, point4, pos);
                QPointF add = pointSplid(point1, point2, distance);
                point2 = QPointF(point2.x() + add.x(), point2.y() + add.y());
                add = pointSplid(point3, point4, distance);
                point4 = QPointF(point4.x() + add.x(), point4.y() + add.y());
            } else {
                qreal distance = pointToLineDistance(point2, point4, pos);
                QPointF add = pointSplid(point1, point2, distance);
                point2 = QPointF(point2.x() - add.x(), point2.y() - add.y());
                add = pointSplid(point3, point4, distance);
                point4 = QPointF(point4.x() - add.x(), point4.y() - add.y());
            }
            newResizeFPoints[0] = point1;
            newResizeFPoints[1] = point2;
            newResizeFPoints[2] = point3;
            newResizeFPoints[3] = point4;
            return newResizeFPoints;
        } else {
            qreal distance = pointToLineDistance(point2,  point4, pos);
            if (pointLineDir(point2, point4, pos) == -1) {
                QPointF add = pointSplid(point1, point3, distance);
                point1 = QPointF(point1.x() + add.x(), point1.y() - add.y());
                add = pointSplid(point3, point4, distance);
                point4 = QPointF(point4.x() - add.x(), point4.y() - add.y());
            } else {
                QPointF add = pointSplid(point1, point3, distance);
                point1 = QPointF(point1.x() - add.x(), point1.y() + add.y());
                add = pointSplid(point3, point4, distance);
                point4 = QPointF(point4.x() + add.x(), point4.y() + add.y());
            }
            point2 = QPointF(point1.x() + point4.x() - point3.x(), point1.y() + point4.y() - point3.y());
            newResizeFPoints[0] = point1;
            newResizeFPoints[1] = point2;
            newResizeFPoints[2] = point3;
            newResizeFPoints[3] = point4;
            return newResizeFPoints;
        }
    }
    return newResizeFPoints;
}
/* point8 in the sixth position */
FourPoints point8Resize6(QPointF point1, QPointF point2, QPointF point3,
                         QPointF point4, QPointF pos, bool isShift) {
    Q_UNUSED(pos);
    Q_UNUSED(isShift);
    FourPoints newResizeFPoints;
    newResizeFPoints = initFourPoints(newResizeFPoints);
    newResizeFPoints[0] = point1;
    newResizeFPoints[1] = point2;
    newResizeFPoints[2] = point3;
    newResizeFPoints[3] = point4;

    return newResizeFPoints;
}
/* point8 in the seventh position */
FourPoints point8Resize7(QPointF point1, QPointF point2, QPointF point3,
                         QPointF point4, QPointF pos, bool isShift) {
    Q_UNUSED(pos);
    Q_UNUSED(isShift);
    FourPoints newResizeFPoints;
    newResizeFPoints = initFourPoints(newResizeFPoints);
    newResizeFPoints[0] = point1;
    newResizeFPoints[1] = point2;
    newResizeFPoints[2] = point3;
    newResizeFPoints[3] = point4;

    return newResizeFPoints;
}

/************************ micro-adjust  **************************/
FourPoints pointMoveMicro(FourPoints fourPoints, QString dir) {
    QPointF point1 = fourPoints[0];
    QPointF point2 = fourPoints[1];
    QPointF point3 = fourPoints[2];
    QPointF point4 = fourPoints[3];
    if (dir == "Left") {
        point1 = QPoint(point1.x() - 1, point1.y());
        point2 = QPoint(point2.x() - 1, point2.y());
        point3 = QPoint(point3.x() - 1, point3.y());
        point4 = QPoint(point4.x() - 1, point4.y());
    }
    if (dir == "Right") {
        point1 = QPoint(point1.x() + 1, point1.y());
        point2 = QPoint(point2.x() + 1, point2.y());
        point3 = QPoint(point3.x() + 1, point3.y());
        point4 = QPoint(point4.x() + 1, point4.y());
    }
    if (dir == "Up") {
        point1 = QPoint(point1.x() , point1.y() - 1);
        point2 = QPoint(point2.x(), point2.y() - 1);
        point3 = QPoint(point3.x(), point3.y() - 1);
        point4 = QPoint(point4.x(), point4.y() - 1);
    }
    if (dir == "Down") {
        point1 = QPoint(point1.x() , point1.y() + 1);
        point2 = QPoint(point2.x(), point2.y() + 1);
        point3 = QPoint(point3.x(), point3.y() + 1);
        point4 = QPoint(point4.x(), point4.y() + 1);
    }
    fourPoints[0] = point1;
    fourPoints[1] = point2;
    fourPoints[2] = point3;
    fourPoints[3] = point4;
    return fourPoints;
}

FourPoints pointResizeMicro(FourPoints fourPoints, QString dir, bool isBig) {
    Q_UNUSED(isBig);
    if (dir == "Ctrl+Left" || dir == "Ctrl+Shift+Left") {
        fourPoints = point5ResizeMicro(fourPoints, isBig);
    }
    if (dir == "Ctrl+Right" || dir == "Ctrl+Shift+Right") {
        fourPoints = point7ResizeMicro(fourPoints, isBig);
    }
    if (dir == "Ctrl+Up" || dir == "Ctrl+Shift+Up") {
        fourPoints = point6ResizeMicro(fourPoints, isBig);
    }
    if (dir == "Ctrl+Down" || dir == "Ctrl+Shift+Down") {
        fourPoints = point8ResizeMicro(fourPoints, isBig);
    }
    return fourPoints;
}
FourPoints point5ResizeMicro(FourPoints fourPoints, bool isBig) {
    QPointF point1 = fourPoints[0];
    QPointF point2 = fourPoints[1];
    QPointF point3 = fourPoints[2];
//    QPointF point4 = fourPoints[3];
    if (getDistance(point1, point3) < MIN_PADDING && !isBig) {
        return fourPoints;
    } else {
        qreal distance = 1;
        qreal weight = 1;
        if (isBig) {
            weight = 1;
        } else {
            weight = -1;
        }

        if (point1.x() - point2.x() <= 0 && point1.y() - point2.y() <= 0 &&
        point1.x() - point3.x() <= 0 && point1.y() - point3.y() >= 0) {
            QPointF add = pointSplid(point1, point3, distance);
            point1 = QPointF(point1.x() - weight*add.x(), point1.y() + weight*add.y());
            point2 = QPointF(point2.x() - weight*add.x(), point2.y() + weight*add.y());
            fourPoints[0] = point1;
            fourPoints[1] = point2;
            return fourPoints;
        }
        if (point1.x() - point2.x() < 0 && point1.y() - point2.y() > 0 &&
        point1.x() - point3.x() > 0 && point1.y() - point3.y() > 0) {
            QPointF add = pointSplid(point1, point3, distance);
            point1 = QPointF(point1.x() + weight*add.x(), point1.y() + weight*add.y());
            point2 = QPointF(point2.x() + weight*add.x(), point2.y() + weight*add.y());
            fourPoints[0] = point1;
            fourPoints[1] = point2;
            return fourPoints;
        }
        if (point1.x() - point2.x() > 0 && point1.y() - point2.y() < 0 &&
        point1.x() - point3.x() < 0 && point1.y() - point3.y() < 0) {
            QPointF add = pointSplid(point1, point3, distance);
            point1 = QPointF(point1.x() - weight*add.x(), point1.y() - weight*add.y());
            point2 = QPointF(point2.x() - weight*add.x(), point2.y() - weight*add.y());
            fourPoints[0] = point1;
            fourPoints[1] = point2;
            return fourPoints;
        }
        if (point1.x() - point2.x() > 0 && point1.y() - point2.y() > 0 &&
        point1.x() - point3.x() > 0 && point1.y() - point3.y() < 0) {
            QPointF add = pointSplid(point1, point3, distance);
            point1 = QPointF(point1.x() + weight*add.x(), point1.y() - weight*add.y());
            point2 = QPointF(point2.x() + weight*add.x(), point2.y() - weight*add.y());
            fourPoints[0] = point1;
            fourPoints[1] = point2;
            return fourPoints;
        }
    }
    return fourPoints;
}
FourPoints point6ResizeMicro(FourPoints fourPoints,  bool isBig) {
    QPointF point1 = fourPoints[0];
    QPointF point2 = fourPoints[1];
    QPointF point3 = fourPoints[2];
//    QPointF point4 = fourPoints[3];
    if (getDistance(point1, point2) < MIN_PADDING && !isBig) {
        return fourPoints;
    } else {
        qreal distance = 1;
        qreal weight = 1;
        if (isBig) {
            weight = 1;
        } else {
            weight = -1;
        }

        if (point1.x() - point2.x() <= 0 && point1.y() - point2.y() <= 0 &&
        point1.x() - point3.x() <= 0 && point1.y() - point3.y() >= 0) {
            QPointF add = pointSplid(point1, point2, distance);
            point1 = QPointF(point1.x() - weight*add.x(), point1.y() - weight*add.y());
            point3= QPointF(point3.x() - weight*add.x(), point3.y() - weight*add.y());
            fourPoints[0] = point1;
            fourPoints[2] = point3;
            return fourPoints;
        }
        if (point1.x() - point2.x() < 0 && point1.y() - point2.y() > 0 &&
        point1.x() - point3.x() > 0 && point1.y() - point3.y() > 0) {
            QPointF add = pointSplid(point1, point2, distance);
            point1 = QPointF(point1.x() - weight*add.x(), point1.y() + weight*add.y());
            point3 = QPointF(point3.x() - weight*add.x(), point3.y() + weight*add.y());
            fourPoints[0] = point1;
            fourPoints[2] = point3;
            return fourPoints;
        }
        if (point1.x() - point2.x() > 0 && point1.y() - point2.y() < 0 &&
        point1.x() - point3.x() < 0 && point1.y() - point3.y() < 0) {
            QPointF add = pointSplid(point1, point2, distance);
            point1 = QPointF(point1.x() + weight*add.x(), point1.y() - weight*add.y());
            point3 = QPointF(point3.x() + weight*add.x(), point3.y() - weight*add.y());
            fourPoints[0] = point1;
            fourPoints[2] = point3;
            return fourPoints;
        }
        if (point1.x() - point2.x() > 0 && point1.y() - point2.y() > 0 &&
        point1.x() - point3.x() > 0 && point1.y() - point3.y() < 0) {
            QPointF add = pointSplid(point1, point2, distance);
            point1 = QPointF(point1.x() + weight*add.x(), point1.y() + weight*add.y());
            point3 = QPointF(point3.x() + weight*add.x(), point3.y() + weight*add.y());
            fourPoints[0] = point1;
            fourPoints[2] = point3;
            return fourPoints;
        }
    }
    return fourPoints;
}
FourPoints point7ResizeMicro(FourPoints fourPoints,  bool isBig) {
    QPointF point1 = fourPoints[0];
    QPointF point2 = fourPoints[1];
    QPointF point3 = fourPoints[2];
    QPointF point4 = fourPoints[3];
    if (getDistance(point1, point3) < MIN_PADDING && !isBig) {
        return fourPoints;
    } else {
        qreal distance = 1;
        qreal weight = 1;
        if (isBig) {
            weight = 1;
        } else {
            weight = -1;
        }

        if (point1.x() - point2.x() <= 0 && point1.y() - point2.y() <= 0 &&
        point1.x() - point3.x() <= 0 && point1.y() - point3.y() >= 0) {
            QPointF add = pointSplid(point1, point3, distance);
            point3 = QPointF(point3.x() + weight*add.x(), point3.y() - weight*add.y());
            point4 = QPointF(point4.x() + weight*add.x(), point4.y() - weight*add.y());
            fourPoints[2] = point3;
            fourPoints[3] = point4;
            return fourPoints;
        }
        if (point1.x() - point2.x() < 0 && point1.y() - point2.y() > 0 &&
        point1.x() - point3.x() > 0 && point1.y() - point3.y() > 0) {
            QPointF add = pointSplid(point1, point3, distance);
            point3 = QPointF(point3.x() - weight*add.x(), point3.y() - weight*add.y());
            point4 = QPointF(point4.x() - weight*add.x(), point4.y() - weight*add.y());
            fourPoints[2] = point3;
            fourPoints[3] = point4;
            return fourPoints;
        }
        if (point1.x() - point2.x() > 0 && point1.y() - point2.y() < 0 &&
        point1.x() - point3.x() < 0 && point1.y() - point3.y() < 0) {
            QPointF add = pointSplid(point1, point3, distance);
            point3 = QPointF(point3.x() + weight*add.x(), point3.y() + weight*add.y());
            point4 = QPointF(point4.x() + weight*add.x(), point4.y() + weight*add.y());
            fourPoints[2] = point3;
            fourPoints[3] = point4;
            return fourPoints;
        }
        if (point1.x() - point2.x() > 0 && point1.y() - point2.y() > 0 &&
        point1.x() - point3.x() > 0 && point1.y() - point3.y() < 0) {
            QPointF add = pointSplid(point1, point3, distance);
            point3 = QPointF(point3.x() - weight*add.x(), point3.y() + weight*add.y());
            point4 = QPointF(point4.x() - weight*add.x(), point4.y() + weight*add.y());
            fourPoints[2] = point3;
            fourPoints[3] = point4;
            return fourPoints;
        }
    }
    return fourPoints;
}

FourPoints point8ResizeMicro(FourPoints fourPoints,  bool isBig) {
    QPointF point1 = fourPoints[0];
    QPointF point2 = fourPoints[1];
    QPointF point3 = fourPoints[2];
    QPointF point4 = fourPoints[3];
    if (getDistance(point1, point2) < MIN_PADDING && !isBig) {
        return fourPoints;
    } else {
        qreal distance = 1;
        qreal weight = 1;
        if (isBig) {
            weight = 1;
        } else {
            weight = -1;
        }

        if (point1.x() - point2.x() <= 0 && point1.y() - point2.y() <= 0 &&
        point1.x() - point3.x() <= 0 && point1.y() - point3.y() >= 0) {
            QPointF add = pointSplid(point1, point2, distance);
            point2 = QPointF(point2.x() + weight*add.x(), point2.y() + weight*add.y());
            point4 = QPointF(point4.x() + weight*add.x(), point4.y() + weight*add.y());
            fourPoints[1] = point2;
            fourPoints[3] = point4;
            return fourPoints;
        }
        if (point1.x() - point2.x() < 0 && point1.y() - point2.y() > 0 &&
        point1.x() - point3.x() > 0 && point1.y() - point3.y() > 0) {
            QPointF add = pointSplid(point1, point2, distance);
            point2 = QPointF(point2.x() + weight*add.x(), point2.y() - weight*add.y());
            point4 = QPointF(point4.x() + weight*add.x(), point4.y() - weight*add.y());
            fourPoints[1] = point2;
            fourPoints[3] = point4;
            return fourPoints;
        }
        if (point1.x() - point2.x() > 0 && point1.y() - point2.y() < 0 &&
        point1.x() - point3.x() < 0 && point1.y() - point3.y() < 0) {
            QPointF add = pointSplid(point1, point2, distance);
            point2 = QPointF(point2.x() - weight*add.x(), point2.y() + weight*add.y());
            point4 = QPointF(point4.x() - weight*add.x(), point4.y() + weight*add.y());
            fourPoints[1] = point2;
            fourPoints[3] = point4;
            return fourPoints;
        }
        if (point1.x() - point2.x() > 0 && point1.y() - point2.y() > 0 &&
        point1.x() - point3.x() > 0 && point1.y() - point3.y() < 0) {
            QPointF add = pointSplid(point1, point2, distance);
            point2 = QPointF(point2.x() - weight*add.x(), point2.y() - weight*add.y());
            point4 = QPointF(point4.x() - weight*add.x(), point4.y() - weight*add.y());
            fourPoints[1] = point2;
            fourPoints[3] = point4;
            return fourPoints;
        }
    }
    return fourPoints;
}

/***********************  special process   ***************************/
bool pointInRect(FourPoints fourPoints, QPointF pos) {
    QPointF point1 = fourPoints[0];
    QPointF point2 = fourPoints[1];
    QPointF point3 = fourPoints[2];
    QPointF point4 = fourPoints[3];

    qreal sumArea = std::sqrt(std::pow(point1.x() - point2.x(), 2) + std::pow(point1.y() - point2.y(), 2))*std::sqrt(
                std::pow(point4.x() - point2.x(), 2) + std::pow(point4.y() - point2.y(), 2));

    qreal sumArea_1 = pointToLineDistance(point1, point2, pos)*std::sqrt(std::pow(point1.x() - point2.x(), 2) +
                std::pow(point1.y() - point2.y(), 2))/2;
    qreal sumArea_2 = pointToLineDistance(point4, point2, pos)*std::sqrt(std::pow(point4.x() - point2.x(), 2) +
                std::pow(point4.y() - point2.y(), 2))/2;
    qreal sumArea_3 = pointToLineDistance(point4, point3, pos)*std::sqrt(std::pow(point4.x() - point3.x(), 2) +
                std::pow(point4.y() - point3.y(), 2))/2;
    qreal sumArea_4 = pointToLineDistance(point1, point3, pos)*std::sqrt(std::pow(point1.x() - point3.x(), 2) +
                std::pow(point1.y() - point3.y(), 2))/2;

    if (sumArea_1 >= sumArea) {
        return false;
    }
    if (sumArea_2 >= sumArea || sumArea_2 + sumArea_1 > sumArea) {
        return false;
    }
    if (sumArea_3 >= sumArea || sumArea_3 + sumArea_2 + sumArea_1 > sumArea) {
        return false;
    }
    if (sumArea_4 >= sumArea || sumArea_4 + sumArea_3 + sumArea_2 + sumArea_1 > sumArea) {
        return false;
    }

    return true;
}

FourPoints getMainPoints(QPointF point1, QPointF point2, bool isShift) {
    FourPoints fourPoints;
    fourPoints = initFourPoints(fourPoints);
    qreal padding = 4;

    qreal leftX = std::min(point1.x(), point2.x());
    qreal leftY = std::min(point1.y(), point2.y());

    qreal pWidth = std::max(std::abs(point1.x() - point2.x()), padding);
    qreal pHeight = std::max(std::abs(point1.y() - point2.y()), padding);

    if (isShift) {
        qreal shiftWidth = std::min(pWidth, pHeight);

        if (point2.x() >= point1.x()) {
            if (point2.y() >= point1.y()) {
                fourPoints[0] = point1;
                fourPoints[1] = QPointF(point1.x(), point1.y() + shiftWidth);
                fourPoints[2] = QPointF(point1.x() + shiftWidth, point1.y());
                fourPoints[3] = QPointF(point1.x() + shiftWidth, point1.y() + shiftWidth);
            } else {
                fourPoints[0] = QPointF(point1.x(), point1.y() - shiftWidth);
                fourPoints[1] = point1;
                fourPoints[2] = QPointF(point1.x() + shiftWidth, point1.y() - shiftWidth);
                fourPoints[3] = QPointF(point1.x() + shiftWidth, point1.y());
            }
        } else {
            if (point2.y() >= point1.y()) {
                fourPoints[0] = QPointF(point1.x() - shiftWidth, point1.y());
                fourPoints[1] = QPointF(point1.x() - shiftWidth, point1.y() + shiftWidth);
                fourPoints[2] = point1;
                fourPoints[3] = QPointF(point1.x(), point1.y() + shiftWidth);
            } else {
                fourPoints[0] = QPointF(point1.x() - shiftWidth, point1.y() - shiftWidth);
                fourPoints[1] = QPointF(point1.x() - shiftWidth, point1.y());
                fourPoints[2] = QPointF(point1.x(), point1.y() - shiftWidth);
                fourPoints[3] = point1;
            }
        }
    } else {
        fourPoints[0] = QPointF(leftX, leftY);
        fourPoints[1] = QPointF(leftX, leftY + pHeight);
        fourPoints[2] = QPointF(leftX + pWidth,  leftY);
        fourPoints[3] = QPointF(leftX + pWidth, leftY + pHeight);
    }

    return fourPoints;
}
