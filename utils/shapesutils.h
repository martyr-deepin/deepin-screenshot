#ifndef SHAPESUTILS_H
#define SHAPESUTILS_H

#include <QtCore>

//Dialognal Points on a line
class DiagPoints {
public:
    QPoint masterPoint;
    QPoint deputyPoint;

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

class FourPoints {
public:
    QPoint point1;
    QPoint point2;
    QPoint point3;
    QPoint point4;

    FourPoints();
    ~FourPoints();

    friend QDebug &operator<<(QDebug &argument, const FourPoints &obj);
    friend QDataStream &operator>>(QDataStream &in, FourPoints &obj);
    FourPoints operator=(FourPoints obj);

    static void registerMetaType();
};

typedef QList<FourPoints> MPointsList;

Q_DECLARE_METATYPE(FourPoints)
Q_DECLARE_METATYPE(MPointsList)
#endif // SHAPESUTILS_H
