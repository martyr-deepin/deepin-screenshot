#include "shapesutils.h"

#include <QDebug>

DiagPoints::DiagPoints() {
}

DiagPoints::~DiagPoints() {
}

void DiagPoints::registerMetaType() {
    qRegisterMetaType<DiagPoints>();
}

QDebug &operator<<(QDebug &argument, const DiagPoints &obj) {
    argument.nospace()
            << obj.deputyPoint << ","
            << obj.masterPoint;

    return argument.space();
}

QDataStream &operator>>(QDataStream &in, DiagPoints &obj) {
    in >> obj.deputyPoint;
    in >> obj.masterPoint;
    return in;
}

DiagPoints DiagPoints::operator=(DiagPoints obj){
     masterPoint = obj.masterPoint;
     deputyPoint = obj.deputyPoint;

    return (*this);
}
