#include "mainwindow.h"
#include <DApplication>

#include <dutility.h>
#include <QObject>
#include <QTranslator>

DWIDGET_USE_NAMESPACE

int main(int argc, char *argv[])
{
#if defined(STATIC_LIB)
    DWIDGET_INIT_RESOURCE();
#endif

    DApplication::loadDXcbPlugin();

     DApplication a(argc, argv);
     a.loadTranslator(QList<QLocale>() << QLocale::system());
     a.setOrganizationName("deepin");
     a.setApplicationName(QObject::tr("Deepin Screenshot"));
     a.setApplicationVersion("4.0");
     a.setQuitOnLastWindowClosed(false);

    MainWindow w;
    w.showFullScreen();

    return a.exec();
}
