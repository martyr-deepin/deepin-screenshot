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
PKGCONFIG += xcb xcb-util dtkwidget dtkwm

LIBS += -lX11 -lXext -lXtst
QMAKE_CXXFLAGS += -g

SOURCES += main.cpp\
        mainwindow.cpp \
    dbusservice/dbusscreenshotservice.cpp \
    eventcontainer.cpp \
    screenshot.cpp

HEADERS  += mainwindow.h \
    dbusservice/dbusscreenshotservice.h \
    eventcontainer.h \
    screenshot.h

RESOURCES += \
    res.qrc

isEmpty(PREFIX){
    PREFIX = /usr
}

include (widgets/widgets.pri)
include (utils/utils.pri)
include (controller/controller.pri)
include (dbusinterface/dbusinterface.pri)

BINDIR = $$PREFIX/bin
APPSHAREDIR = $$PREFIX/share/deepin-screenshot
MANDIR = $$PREFIX/share/dman/deepin-screenshot
MANICONDIR = $$PREFIX/share/icons/hicolor/scalable/apps
APPICONDIR = $$PREFIX/share/icons/deepin/apps/scalable

DEFINES += APPSHAREDIR=\\\"$$APPSHAREDIR\\\"

target.path = $$BINDIR

desktop.path = $${PREFIX}/share/applications/
desktop.files =  deepin-screenshot.desktop

icons.path = $$APPSHAREDIR/icons
icons.files = resources/images/*

manual.path = $$MANDIR
manual.files = doc/*
manual_icon.path = $$MANICONDIR
manual_icon.files = doc/common/deepin-screenshot.svg
app_icon.path = $$APPICONDIR
app_icon.files = doc/common/deepin-screenshot.svg

# Automating generation .qm files from .ts files
CONFIG(release, debug|release) {
    system($$PWD/generate_translations.sh)
}

translations.path = $$APPSHAREDIR/translations
translations.files = translations/*.qm

service.path = $${PREFIX}/share/dbus-1/services/
service.files = $$PWD/dbusservice/com.deepin.Screenshot.service

INSTALLS = target desktop icons manual manual_icon app_icon translations service
