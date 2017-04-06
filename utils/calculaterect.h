#ifndef CALCULATERECT_H
#define CALCULATERECT_H

#include <QPointF>
#include <QtMath>
#include "shapesutils.h"

/* get a rect by diagPoints */
QRect   diagPointsRect(DiagPoints diagPoints);

/* judge whether the point1 is on the point2 or not */
bool    pointClickIn(QPointF point2, QPointF point1, int padding = 4);

/* judge whether the point3 is on the segment*/
bool    pointOnLine(QPointF point1, QPointF point2, QPointF point3);

/* To determine whether a point on the rectangle*/
bool    pointOnRect(DiagPoints diagPoints, QPointF pos);

/* get the point who splid a distance on a line */
QPointF  pointSplid(QPointF point1, QPointF point2, int padding);

/* get the rotate point by four points in a rectangle*/
QPointF  getRotatePoint(QPointF point1, QPointF point2,
                             QPointF point3, QPointF point4);

/* get the four points from a rectangle which isn't rotated!*/
FourPoints  fourPointsOnRect(DiagPoints diagPoints);

/* get the rotate angle by three points*/
qreal  calculateAngle(QPointF point1, QPointF point2, QPointF point3);

/* get the new points after rotate with angle*/
QPointF  pointRotate(QPointF point1, QPointF point2, qreal angle);

/* the distance from a point(point3) to a line(point1, point2) */
qreal   pointToLineDistance(QPoint point1, QPoint point2, QPoint point3);

#endif // CALCULATERECT_H
