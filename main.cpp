/*
 * Copyright (C) 2017 ~ 2017 Deepin Technology Co., Ltd.
 *
 * Maintainer: Peng Hui<penghui@deepin.com>
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

#include <DApplication>
#include <DLog>
#include <DWidgetUtil>

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
     a.setAttribute(Qt::AA_UseHighDpiPixmaps);

     using namespace Dtk::Core;
     Dtk::Core::DLogManager::registerConsoleAppender();
     Dtk::Core::DLogManager::registerFileAppender();

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
    QCommandLineOption dbusOption(QStringList() << "u" << "dbus",
                                                                            "Start  from dbus.");
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
     cmdParser.addOption(dbusOption);
     cmdParser.process(a);

     Screenshot w;
     w.hide();

     DBusScreenshotService dbusService (&w);
     Q_UNUSED(dbusService);
     //Register Screenshot's dbus service.
     QDBusConnection conn = QDBusConnection::sessionBus();
     if (!conn.registerService("com.deepin.Screenshot") ||
             !conn.registerObject("/com/deepin/Screenshot", &w)) {
         qDebug() << "deepin-screenshot is running!";

         qApp->quit();
         return 0;
     }

     if (cmdParser.isSet(dbusOption))
     {
         qDebug() << "dbus register wating!";
         return a.exec();
     } else {
         if (cmdParser.isSet(delayOption)) {
             qDebug() << "cmd delay screenshot";
             w.delayScreenshot(cmdParser.value(delayOption).toInt());
         } else if (cmdParser.isSet(fullscreenOption)) {
             w.fullscreenScreenshot();
         } else if (cmdParser.isSet(topWindowOption)) {
             w.topWindowScreenshot();
         } else if (cmdParser.isSet(savePathOption)) {
             qDebug() << "cmd savepath screenshot";
             w.savePathScreenshot(cmdParser.value(savePathOption));
         } else if (cmdParser.isSet(prohibitNotifyOption)) {
             qDebug() << "screenshot no notify!";
             w.noNotifyScreenshot();
         } else if (cmdParser.isSet(iconOption)) {
             w.delayScreenshot(0.2);
         }  else {
             w.startScreenshot();
         }
     }

     return a.exec();
}
