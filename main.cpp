#include "mainwindow.h"
#include "dbusinterface/dbusscreenshot.h"
#include "dbusservice/dbusscreenshotservice.h"

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



     QCommandLineOption  delayOption(QStringList() << "d" << "delay <NUM>",
                                                                             "Take a screenshot after NUM seconds.");
     QCommandLineOption fullscreenOption(QStringList() << "f" << "fullscreen",
                                                                                "Take a screenshot the whole screen.");
     QCommandLineOption topWindowOption(QStringList() << "w" << "top-window",
                                                                             "Take a screenshot of the most top window");
     QCommandLineOption savePathOption(QStringList() << "s" << "save-path <PATH>",
                                                                             "Specifiy a path to save the screenshot.");
     QCommandLineOption prohibitNotifyOption(QStringList() << "n" << "no-notification",
                                                                              "Don't send notifications.");
//     QCommandLineOption iconOption(QStringList() << "i" << "icon",
//                                                                           "Indicate that this program's started by clicking.");

     QCommandLineParser cmdParser;
     cmdParser.setApplicationDescription("deepin-screenshot");
     cmdParser.addHelpOption();
     cmdParser.addVersionOption();
     cmdParser.addOption(delayOption);
     cmdParser.addOption(fullscreenOption);
     cmdParser.addOption(topWindowOption);
     cmdParser.addOption(savePathOption);
     cmdParser.addOption(prohibitNotifyOption);
//     cmdParser.addOption(iconOption);
     cmdParser.process(a);

     MainWindow w;
     DBusScreenshotService dbusService (&w);
     Q_UNUSED(dbusService);
    QDBusConnection conn = QDBusConnection::sessionBus();
    if (!conn.registerService("com.deepin.DeepinScreenshot") ||
            !conn.registerObject("/com/deepin/DeepinScreenshot", &w)) {
        qDebug() << "deepin-screenshot is running!";

        a.exit(0);
    } else {
        const QStringList cmdNames = cmdParser.optionNames();
        const QStringList args = cmdParser.positionalArguments();
        QString cmdName,  argument;
        qDebug() << "cmd" << cmdNames << args;
        if (cmdNames.length() >= 1)
            cmdName = cmdNames[0];
        if (args.length() >= 1)
            argument = args[0];
        if (cmdName == "d" || cmdName == "delay") {
               w.delayScreenshot(argument.toInt());
        } else if (cmdName == "f" || cmdName == "fullscreen") {
            w.fullScreenshot();
        } else if (cmdName == "w" || cmdName == "top-window") {
            qDebug() << "screenshot topWindow";
            w.topWindow();
        } else if (cmdName == "s" || cmdName == "save-path") {
            w.savePath(argument);
        } else if (cmdName == "n" || cmdName == "no-notification") {
            qDebug() << "screenshot no notify!";
            w.noNotify();
        } else {
            w.startScreenshot();
        }
    }

    return a.exec();
}
