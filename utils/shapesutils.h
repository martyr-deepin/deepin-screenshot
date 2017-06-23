#ifndef SHAPESUTILS_H
#define SHAPESUTILS_H

#include <QtCore>
#include <QColor>

typedef QList<QPointF> FourPoints;
Q_DECLARE_METATYPE(FourPoints)

/* shape*/
class Toolshape {
public:
     QString type;
     FourPoints mainPoints;
     int index = -1;
     int lineWidth;
     int colorIndex;
     bool isBlur = false;
     bool isMosaic = false;
     bool isStraight = false;
     bool isShiftPressed = false;
     int fontSize = 1;

    QList<QPointF> points;
    QList<QList<qreal>> portion;
    Toolshape();
    ~Toolshape();

    friend QDebug &operator<<(QDebug &argument, const Toolshape &obj);
    friend QDataStream &operator>>(QDataStream &in, Toolshape &obj);
    Toolshape operator=(Toolshape obj);
    bool operator==(const Toolshape &other) const;
    static void registerMetaType();
};

//typedef QList<QPointF> FourPoints;
typedef QList <Toolshape> Toolshapes;
Q_DECLARE_METATYPE(Toolshape)
Q_DECLARE_METATYPE(Toolshapes)

#endif // SHAPESUTILS_H
