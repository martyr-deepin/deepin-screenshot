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
#endif // SHAPESUTILS_H
