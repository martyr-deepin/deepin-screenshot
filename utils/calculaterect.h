#ifndef CALCULATERECT_H
#define CALCULATERECT_H

#include <QPointF>
#include <QtMath>
#include "shapesutils.h"

QRect   diagPointsRect(DiagPoints diagPoints);
bool    pointClickIn(QPointF point2, QPointF point1, int padding = 4);
bool    pointOnLine(QPointF point1, QPointF point2, QPointF point3);
bool    pointOnRect(DiagPoints diagPoints, QPointF pos);

QPointF        pointSplid(QPointF point1, QPointF point2, int padding);
QPointF        getRotatePoint(QPointF point1, QPointF point2,
                             QPointF point3, QPointF point4);
FourPoints    fourPointsOnRect(DiagPoints diagPoints);
qreal         calculateAngle(QPointF point1, QPointF point2, QPointF point3);
QPointF        pointRotate(QPointF point1, QPointF point2, qreal angle);
//QRect         fPointsRect(FourPoints fourPoints);
#endif // CALCULATERECT_H
