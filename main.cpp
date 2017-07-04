#include <DApplication>
#include <DLog>
#include <dutility.h>

#include <QObject>
#include <QTranslator>

#include "screenshot.h"
#include "dbusservice/dbusscreenshotservice.h"
#include "dbusinterface/dbusscreenshot.h"

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
     a.setApplicationName("deepin-screenshot");
     a.setApplicationVersion("4.0");
     a.setTheme("light");
     a.setQuitOnLastWindowClosed(false);

     using namespace Dtk::Util;
     Dtk::Util::DLogManager::registerConsoleAppender();
     Dtk::Util::DLogManager::registerFileAppender();

     QCommandLineOption  delayOption(QStringList() << "d" << "delay",
                                                                             "Take a screenshot after NUM seconds.", "NUM");
     QCommandLineOption fullscreenOption(QStringList() << "f" << "fullscreen",
                                                                                "Take a screenshot the whole screen.");
     QCommandLineOption topWindowOption(QStringList() << "w" << "top-window",
                                                                             "Take a screenshot of the most top window.");
     QCommandLineOption savePathOption(QStringList() << "s" << "save-path",
                                                                             "Specifiy a path to save the screenshot.", "PATH");
     QCommandLineOption prohibitNotifyOption(QStringList() << "n" << "no-notification",
                                                                              "Don't send notifications.");
     QCommandLineOption iconOption(QStringList() << "i" << "icon",
                                                                           "Indicate that this program's started by clicking.");

     QCommandLineParser cmdParser;
     cmdParser.setApplicationDescription("deepin-screenshot");
     cmdParser.addHelpOption();
     cmdParser.addVersionOption();
     cmdParser.addOption(delayOption);
     cmdParser.addOption(fullscreenOption);
     cmdParser.addOption(topWindowOption);
     cmdParser.addOption(savePathOption);
     cmdParser.addOption(prohibitNotifyOption);
     cmdParser.addOption(iconOption);
     cmdParser.process(a);

     Screenshot w;
     w.hide();

     //Register Screenshot's dbus service.
     DBusScreenshotService dbusService (&w);
     Q_UNUSED(dbusService);

    QDBusConnection conn = QDBusConnection::sessionBus();
    if (!conn.registerService("com.deepin.DeepinScreenshot") ||
            !conn.registerObject("/com/deepin/DeepinScreenshot", &w)) {
        qDebug() << "deepin-screenshot is running!";

        qApp->quit();
        return 0;
    } else {
        qDebug() << "deepin-screenshot first started!";

        if (cmdParser.isSet(delayOption)) {
            qDebug() << "cmd delay screenshot";
            w.delayScreenshot(cmdParser.value(delayOption).toInt());
        } else if (cmdParser.isSet(fullscreenOption)) {
            w.fullscreenScreenshot();
        } else if (cmdParser.isSet(topWindowOption)) {
            qDebug() << "cmd topWindow";
            w.topWindowScreenshot();
        } else if (cmdParser.isSet(savePathOption)) {
            qDebug() << "cmd savepath screenshot";
            w.savePathScreenshot(cmdParser.value(savePathOption));
        } else if (cmdParser.isSet(prohibitNotifyOption)) {
            qDebug() << "screenshot no notify!";
            w.noNotifyScreenshot();
        } else if (cmdParser.isSet(iconOption)) {
            w.startScreenshot();
        }  else {
            w.startScreenshot();
        }

        return a.exec();
    }
}
