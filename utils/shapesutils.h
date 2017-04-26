#ifndef SHAPESUTILS_H
#define SHAPESUTILS_H

#include <QtCore>
#include <QColor>

//Dialognal Points on a line
class DiagPoints {
public:
    QPointF masterPoint;
    QPointF deputyPoint;

    DiagPoints();
    ~DiagPoints();

    friend QDebug &operator<<(QDebug &argument, const DiagPoints &obj);
    friend QDataStream &operator>>(QDataStream &in, DiagPoints &obj);
    DiagPoints operator=(DiagPoints obj);

    static void registerMetaType();
};

typedef QList<DiagPoints> DiagPointsList;

Q_DECLARE_METATYPE(DiagPoints)
Q_DECLARE_METATYPE(DiagPointsList)

typedef QList<QPointF> FourPoints;
Q_DECLARE_METATYPE(FourPoints)

/* shape*/
class Toolshape {
public:
     QString type;
     FourPoints mainPoints;
     int lineWidth;
     int colorIndex;
     bool isBlur = false;
     bool isMosaic = false;
     int fontSize = 1;
    QList<QPointF> points;
    QList<QList<qreal>> portion;
    Toolshape();
    ~Toolshape();

    friend QDebug &operator<<(QDebug &argument, const Toolshape &obj);
    friend QDataStream &operator>>(QDataStream &in, Toolshape &obj);
    Toolshape operator=(Toolshape obj);

    static void registerMetaType();
};

//typedef QList<QPointF> FourPoints;
typedef QList <Toolshape> Toolshapes;
Q_DECLARE_METATYPE(Toolshape)
Q_DECLARE_METATYPE(Toolshapes)

#endif // SHAPESUTILS_H
