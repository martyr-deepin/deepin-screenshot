#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2011 ~ 2014 Deepin, Inc.
#               2011 ~ 2014 Andy Stewart
#
# Author:     Andy Stewart <lazycat.manatee@gmail.com>
# Maintainer: Andy Stewart <lazycat.manatee@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import sys
import time
import signal
import tempfile
import subprocess

from PyQt5 import QtCore
from PyQt5.QtCore import QCoreApplication
if os.name == 'posix':
    QCoreApplication.setAttribute(QtCore.Qt.AA_X11InitThreads, True)

from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QApplication, qApp, QFileDialog
from PyQt5.QtCore import QStandardPaths, QUrl, QTimer
from PyQt5.QtMultimedia import QSoundEffect
app = QApplication(sys.argv)
app.setOrganizationName("Deepin")
app.setApplicationName("Deepin Screenshot")
app.setApplicationVersion("3.0")
app.setQuitOnLastWindowClosed(False)

from app_controller import AppController
from app_window import Window
from i18n import _
from window_info import WindowInfo
from menu_controller import MenuController
from settings import ScreenShotSettings
from dbus_services import is_service_exist, register_object
from dbus_interfaces import controlCenterInterface
from dbus_interfaces import notificationsInterface
from constants import MAIN_QML, SOUND_FILE, TMP_IMAGE_FILE, GTK_CLIP

ACTION_ID_OPEN = "id_open"

view = None
settings = ScreenShotSettings()
_notificationId = None
_fileSaveLocation = None
_quitTimer = QTimer()
_quitTimer.setInterval(10 * 1000)
_quitTimer.setSingleShot(True)
_quitTimer.timeout.connect(qApp.quit)

def _actionInvoked(notificationId, actionId):
    global view
    global _fileSaveLocation

    if _notificationId == notificationId:
        if actionId == ACTION_ID_OPEN:
            subprocess.call(["xdg-open", os.path.dirname(_fileSaveLocation)])
        view.closeWindow() if view else qApp.quit()

def _notificationClosed( notificationId, reason):
    global view
    if _notificationId == notificationId:
        view.closeWindow() if view else qApp.quit()


def _windowVisibleChanged(visible):
    if visible:
        controlCenterInterface.hideImmediately()

def copyPixmap(pixmap):
    global _notificationId

    _temp = "%s.png" % tempfile.mktemp()
    pixmap.save(_temp)
    subprocess.call([GTK_CLIP, _temp])

    _notificationId = notificationsInterface.notify(_("Deepin Screenshot"),
        _("Picture has been saved to clipboard"))
    _quitTimer.start()

def savePixmap(pixmap, fileName):
    global _notificationId
    global _fileSaveLocation
    pixmap.save(fileName)

    _fileSaveLocation = fileName
    _notificationId = notificationsInterface.notify(_("Deepin Screenshot"),
        _("Picture has been saved to") + _fileSaveLocation, [ACTION_ID_OPEN, _("View")])
    _quitTimer.start()

def saveScreenshot(pixmap):
    global settings
    global soundEffect
    global savePathValue

    soundEffect.play()
    fileName = "%s%s.png" % (_("DeepinScreenshot"),
                             time.strftime("%Y%m%d%H%M%S", time.localtime()))
    save_op = settings.getOption("save", "save_op")
    save_op_index = int(save_op)

    absSavePath = ""
    copyToClipborad = False
    if savePathValue and os.path.exists(os.path.dirname(absSavePath)):
        absSavePath = os.path.abspath(savePathValue)
    else:
        if save_op_index == 0: #saveId == "save_to_desktop":
            saveDir = QStandardPaths.writableLocation(QStandardPaths.DesktopLocation)
            absSavePath = os.path.join(saveDir, fileName)
        elif save_op_index == 1: #saveId == "auto_save" :
            saveDir = QStandardPaths.writableLocation(QStandardPaths.PicturesLocation)
            absSavePath = os.path.join(saveDir, fileName)
        elif save_op_index == 2: #saveId == "save_to_dir":
            lastSavePath = settings.getOption("save", "folder")
            absSavePath = QFileDialog.getSaveFileName(None, _("Save"),
                os.path.join(lastSavePath, fileName))[0]
            settings.setOption("save", "folder", os.path.dirname(absSavePath)
                                                 or lastSavePath)
        elif save_op_index == 4: #saveId == "auto_save_ClipBoard":
            copyToClipborad = True
            saveDir = QStandardPaths.writableLocation(QStandardPaths.PicturesLocation)
            absSavePath = os.path.join(saveDir, fileName)
        else: copyToClipborad = True

    if absSavePath or copyToClipborad:
        if copyToClipborad: copyPixmap(pixmap)
        if absSavePath: savePixmap(pixmap, absSavePath)
    else:
        qApp.quit()

delayValue = None
fullscreenValue = None
topWindowValue = None
savePathValue = None
startFromDesktop = None
def main(delay, fullscreen, topWindow, savePath, startFromDesktop):
    global view, settings, windoInfo, menu_controller
    global delayValue, fullscreenValue, topWindowValue
    global savePathValue, startFromDesktopValue

    delayValue = delay
    fullscreenValue = fullscreen
    topWindowValue = topWindow
    savePathValue = savePath
    startFromDesktopValue = startFromDesktop

    cursor_pos = QCursor.pos()
    desktop = qApp.desktop()
    screen_num = desktop.screenNumber(cursor_pos)
    screen_geo = desktop.screenGeometry(screen_num)
    pixmap = qApp.primaryScreen().grabWindow(0)
    pixmap = pixmap.copy(screen_geo.x(), screen_geo.y(), screen_geo.width(), screen_geo.height())
    pixmap.save(TMP_IMAGE_FILE)

    settings.showOSD = startFromDesktopValue
    settings.tmpImageFile = TMP_IMAGE_FILE
    menu_controller = MenuController()
    windoInfo = WindowInfo(screen_num)

    notificationsInterface.ActionInvoked.connect(_actionInvoked)
    notificationsInterface.NotificationClosed.connect(_notificationClosed)

    if fullscreenValue:
        saveScreenshot(pixmap)
    elif topWindowValue:
        wInfos = windoInfo.get_windows_info()
        if len(wInfos) > 0:
            wInfo = wInfos[0]
            pix = pixmap.copy(wInfo[0] - screen_geo.x(), wInfo[1] - screen_geo.y(), wInfo[2], wInfo[3])
            saveScreenshot(pix)
    else:
        view = Window(settings, windoInfo, saveScreenshot)
        view.setX(screen_geo.x())
        view.setY(screen_geo.y())
        view.setWidth(screen_geo.width())
        view.setHeight(screen_geo.height())
        view.visibleChanged.connect(_windowVisibleChanged)

        qml_context = view.rootContext()
        qml_context.setContextProperty("windowView", view)
        qml_context.setContextProperty("qApp", qApp)
        qml_context.setContextProperty("screenWidth", view.window_info.screen_width)
        qml_context.setContextProperty("screenHeight", view.window_info.screen_height)
        qml_context.setContextProperty("_menu_controller", menu_controller)

        view.setSource(QUrl.fromLocalFile(MAIN_QML))
        view.showWindow()

        menu_controller.preMenuShow.connect(view.ungrabFocus)
        menu_controller.postMenuHide.connect(view.grabFocus)

if __name__ == "__main__":
    global soundEffect

    if is_service_exist():
        screenshotInterface.runWithArguments(app.arguments())
        notificationsInterface.notify(_("Deepin Screenshot"),
            _("Deepin Screenshot has been started!"))
    else:
        controller = AppController(main)
        controller.runWithArguments(app.arguments())
        register_object(controller)

        soundEffect = QSoundEffect()
        soundEffect.setSource(QUrl(SOUND_FILE))

        signal.signal(signal.SIGINT, signal.SIG_DFL)
        sys.exit(app.exec_())