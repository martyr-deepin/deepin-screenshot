#include "mainwindow.h"
#include <QApplication>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
     a.setOrganizationName("Deepin");
     a.setApplicationName("Deepin Screenshot");
     a.setApplicationVersion("4.0");
     a.setQuitOnLastWindowClosed(false);

    MainWindow w;
    w.showFullScreen();

    return a.exec();
}
