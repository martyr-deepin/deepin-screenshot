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

FourPoints::FourPoints() {
}

FourPoints::~FourPoints() {
}

void FourPoints::registerMetaType() {
    qRegisterMetaType<FourPoints>();
}

QDebug &operator<<(QDebug &argument, const FourPoints &obj) {
    argument.nospace()
            << obj.point1 << ","
            << obj.point2 << ","
            << obj.point3 << ","
            << obj.point4  << ","
            << obj.shapeType << ","
            << obj.points;
    return argument.space();
}

QDataStream &operator>>(QDataStream &in, FourPoints &obj) {
    in >> obj.points;
    in >> obj.shapeType;
    in >> obj.point4;
    in >> obj.point3;
    in >> obj.point2;
    in >> obj.point1;
    return in;
}

FourPoints FourPoints::operator=(FourPoints obj) {
    point1 = obj.point1;
    point2 = obj.point2;
    point3 = obj.point3;
    point4 = obj.point4;
    shapeType = obj.shapeType;
    obj.points = obj.points;
    return (*this);
}

/* define ToolShape     */
Toolshape::Toolshape() {
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
            << obj.penColor <<","
            << obj.isBlur << ","
            << obj.isMosaic << ","
            << obj.fontSize << ","
            << obj.points;
    return argument.space();
}

QDataStream &operator>>(QDataStream &in, Toolshape &obj) {
    in >> obj.points;
    in >> obj.fontSize;
    in >> obj.isBlur;
    in >> obj.isMosaic;
    in >> obj.penColor;
    in >> obj.lineWidth;
    in >> obj.mainPoints;
    in >> obj.type;

    return in;
}

Toolshape Toolshape::operator=(Toolshape obj) {
    type = obj.type;
    mainPoints = obj.mainPoints;
    lineWidth = obj.lineWidth;
    penColor = obj.penColor;
    isBlur = obj.isBlur;
    isMosaic = obj.isMosaic;
    fontSize = obj.fontSize;
    points = obj.points;

    return (*this);
}
