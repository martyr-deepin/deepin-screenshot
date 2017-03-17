#-------------------------------------------------
#
# Project created by QtCreator 2017-03-15T09:11:16
#
#-------------------------------------------------

QT       += core gui  network x11extras dbus

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = deepin-screenshot
TEMPLATE = app

CONFIG += c++11 link_pkgconfig
PKGCONFIG += xcb xcb-util dtkwidget dtkbase

LIBS += -lX11 -lXext -lXtst
QMAKE_CXXFLAGS += -g

SOURCES += main.cpp\
        mainwindow.cpp \
    windowmanager.cpp \
    eventmonitor.cpp \
    utils.cpp

HEADERS  += mainwindow.h \
    windowmanager.h \
    eventmonitor.h \
    utils.h

RESOURCES += \
    resources.qrc
