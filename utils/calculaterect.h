#ifndef CALCULATERECT_H
#define CALCULATERECT_H

#include <QPoint>
#include <QtMath>
#include "shapesutils.h"

QRect   diagPointsRect(DiagPoints diagPoints);
bool    pointOnLine(QPoint point1, QPoint point2, QPoint point3);
bool    pointOnRect(DiagPoints diagPoints, QPoint pos);

QPoint        pointSplid(QPoint point1, QPoint point2, int padding);
QPoint        getRotatePoint(QPoint point1, QPoint point2,
                             QPoint point3, QPoint point4);
QList<QPoint> fourPointsOnRect(DiagPoints diagPoints);


#endif // CALCULATERECT_H
