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

Toolshape::Toolshape() {
    mainPoints.append(QPointF(0, 0));
    mainPoints.append(QPointF(0, 0));
    mainPoints.append(QPointF(0, 0));
    mainPoints.append(QPointF(0, 0));
    portion.clear();
}

Toolshape::~Toolshape() {
}

void Toolshape::registerMetaType() {
    qRegisterMetaType<Toolshape>();
}

QDebug &operator<<(QDebug &argument, const Toolshape &obj) {
    argument.nospace()
            << obj.type << ","
            << "[" << obj.mainPoints << "]" << ","
            << obj.lineWidth << ","
            << obj.colorIndex <<","
            << obj.isBlur << ","
            << obj.isMosaic << ","
            << obj.isStraight << ","
            << obj.fontSize << ","
            << obj.points;
    return argument.space();
}

QDataStream &operator>>(QDataStream &in, Toolshape &obj) {
    in >> obj.points;
    in >> obj.fontSize;
    in >> obj.isBlur;
    in >> obj.isMosaic;
    in >> obj.isStraight;
    in >> obj.colorIndex;
    in >> obj.lineWidth;
    in >> obj.mainPoints;
    in >> obj.type;

    return in;
}

Toolshape Toolshape::operator=(Toolshape obj) {
    type = obj.type;
    mainPoints = obj.mainPoints;
    lineWidth = obj.lineWidth;
    colorIndex = obj.colorIndex;
    isBlur = obj.isBlur;
    isMosaic = obj.isMosaic;
    isStraight = obj.isStraight;
    fontSize = obj.fontSize;
    points = obj.points;

    return (*this);
}

bool Toolshape::operator==(const Toolshape &other) const {
    if (this->mainPoints == other.mainPoints && this->colorIndex == other.colorIndex &&
            this->fontSize == other.fontSize && this->isBlur == other.isBlur && this->isMosaic
            == other.isMosaic && this->isStraight == other.isStraight && this->points == other.points) {
        return true;
    } else {
        return false;
    }
}
