#ifndef CALCULATERECT_H
#define CALCULATERECT_H

#include <QPoint>
#include <QtMath>
#include "shapesutils.h"

QRect   diagPointsRect(DiagPoints diagPoints);
bool    pointClickIn(QPoint point2, QPoint point1, int padding = 4);
bool    pointOnLine(QPoint point1, QPoint point2, QPoint point3);
bool    pointOnRect(DiagPoints diagPoints, QPoint pos);

QPoint        pointSplid(QPoint point1, QPoint point2, int padding);
QPoint        getRotatePoint(QPoint point1, QPoint point2,
                             QPoint point3, QPoint point4);
FourPoints    fourPointsOnRect(DiagPoints diagPoints);
qreal         calculateAngle(QPoint point1, QPoint point2, QPoint point3);
QPoint        pointRotate(QPoint point1, QPoint point2, qreal angle);
//QRect         fPointsRect(FourPoints fourPoints);
#endif // CALCULATERECT_H
