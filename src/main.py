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

from PyQt5.QtQuick import QQuickView
from PyQt5.QtGui import (QSurfaceFormat, QColor, QImage,
    QPixmap, QCursor, QKeySequence, qRed, qGreen, qBlue)
from PyQt5.QtWidgets import QApplication, qApp, QFileDialog
from PyQt5.QtCore import (pyqtSlot, QStandardPaths, QUrl,
    QCommandLineParser, QCommandLineOption, QTimer, Qt)
from PyQt5.QtDBus import QDBusConnection, QDBusInterface
from PyQt5.QtMultimedia import QSoundEffect
app = QApplication(sys.argv)
app.setOrganizationName("Deepin")
app.setApplicationName("Deepin Screenshot")
app.setApplicationVersion("3.0")
app.setQuitOnLastWindowClosed(False)

from i18n import _
from window_info import WindowInfo
from menu_controller import MenuController
from settings import ScreenShotSettings
from dbus_services import is_service_exist, unregister_service
from dbus_interfaces import notificationsInterface, socialSharingInterface
from constants import MAIN_QML, SOUND_FILE, MAIN_DIR, TMP_IMAGE_FILE

def init_cursor_shape_dict():
    global cursor_shape_dict

    file_name_except_extension = lambda x: os.path.basename(x).split(".")[0]

    mouse_style_dir = os.path.join(MAIN_DIR, "image/mouse_style")
    shape_dir = os.path.join(mouse_style_dir, "shape")
    color_pen_dir = os.path.join(mouse_style_dir, "color_pen")

    for _file in os.listdir(shape_dir):
        key = CURSOR_SHAPE_SHAPE_PREFIX + file_name_except_extension(_file)
        cursor_shape_dict[key] = os.path.join(shape_dir, _file)

    for _file in os.listdir(color_pen_dir):
        key = CURSOR_SHAPE_COLOR_PEN_PREFIX + file_name_except_extension(_file)
        cursor_shape_dict[key] = os.path.join(color_pen_dir, _file)

CURSOR_SHAPE_SHAPE_PREFIX = "shape_"
CURSOR_SHAPE_COLOR_PEN_PREFIX = "color_pen_"
SAVE_DEST_TEMP = os.path.join(tempfile.gettempdir() or "/tmp",
                              "DeepinScreenshot-save-tmp.png")
ACTION_ID_OPEN = "id_open"
cursor_shape_dict = {}
init_cursor_shape_dict()

soundEffect = QSoundEffect()
soundEffect.setSource(QUrl(SOUND_FILE))
settings = ScreenShotSettings()

_notificationId = None
_fileSaveLocation = None

class Window(QQuickView):
    def __init__(self, settings, windowInfo):
        QQuickView.__init__(self)
        self._settings = settings

        surface_format = QSurfaceFormat()
        surface_format.setAlphaBufferSize(8)

        self.set_cursor_shape("shape_start_cursor")
        self.setColor(QColor(0, 0, 0, 0))
        self.setFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setResizeMode(QQuickView.SizeRootObjectToView)
        self.setFormat(surface_format)
        self.setTitle(_("Deepin screenshot"))

        self.qimage = QImage(self._settings.tmpImageFile)
        self.qpixmap = QPixmap()
        self.qpixmap.convertFromImage(self.qimage)

        self.window_info = windowInfo

        self._grabPointerStatus = False
        self._grabKeyboardStatus = False
        self._grabFocusTimer = self._getGrabFocusTimer()

    @pyqtSlot(int, int, result="QVariant")
    def get_color_at_point(self, x, y):
        rgb = self.qimage.pixel(x, y)
        return [qRed(rgb), qGreen(rgb), qBlue(rgb)]

    @pyqtSlot(result="QVariant")
    def get_window_info_at_pointer(self):
        return self.window_info.get_window_info_at_pointer()

    @pyqtSlot(result="QVariant")
    def get_cursor_pos(self):
        return QCursor.pos()

    @pyqtSlot(str)
    def set_cursor_shape(self, shape):
        '''
        Set the shape of cursor, the param shape should be one of the keys
        of the global variable cursor_shape_dict.
        '''
        if cursor_shape_dict.get(shape):
            pix = QPixmap(cursor_shape_dict[shape])
            if shape.startswith(CURSOR_SHAPE_COLOR_PEN_PREFIX):
                cur = QCursor(pix, hotX=0, hotY=pix.height())
            else:
                cur = QCursor(pix, hotX=5, hotY=5)
            self.setCursor(cur)

    @pyqtSlot(str,int,int,int,int)
    def save_overload(self, style, x,y,width,height):
        p = QPixmap.fromImage(self.grabWindow())
        p = p.copy(x,y,width,height)
        image_dir = "/tmp/deepin-screenshot-%s.png" %style
        p.save(os.path.join(image_dir))

    def _getGrabFocusTimer(self):
        timer = QTimer()
        timer.setSingleShot(True)
        timer.setInterval(100)
        timer.timeout.connect(self._grabFocusInternal)
        return timer

    def _grabFocusInternal(self):
        if not self._grabPointerStatus:
            self._grabPointerStatus = self.setMouseGrabEnabled(True)
        if not self._grabKeyboardStatus:
            self._grabKeyboardStatus = self.setKeyboardGrabEnabled(True)

        if not (self._grabPointerStatus and self._grabKeyboardStatus):
            self._grabFocusTimer.start()


    def grabFocus(self):
        self._grabFocusTimer.start()

    def ungrabFocus(self):
        self._grabPointerStatus = False
        self._grabKeyboardStatus = False
        self.setMouseGrabEnabled(False)
        self.setKeyboardGrabEnabled(False)

    @pyqtSlot(str,str,result="QVariant")
    def get_save_config(self, group_name,op_name):
        return self._settings.getOption(group_name, op_name)

    @pyqtSlot(str,str,str)
    def set_save_config(self,group_name,op_name,op_index):
        self._settings.setOption(group_name, op_name, op_index)

    @pyqtSlot(int,int,int,int)
    def save_screenshot(self, x, y, width, height):
        pixmap = QPixmap.fromImage(self.grabWindow())
        pixmap = pixmap.copy(x, y, width, height)
        pixmap.save(SAVE_DEST_TEMP)

        self.hide()
        saveScreenshot(pixmap)

    @pyqtSlot()
    def enable_zone(self):
        try:
            iface = QDBusInterface("com.deepin.daemon.Zone", "/com/deepin/daemon/Zone", '', QDBusConnection.sessionBus())
            iface.asyncCall("EnableZoneDetected", True)
        except:
            pass

    @pyqtSlot()
    def disable_zone(self):
        try:
            iface = QDBusInterface("com.deepin.daemon.Zone", "/com/deepin/daemon/Zone", '', QDBusConnection.sessionBus())
            iface.asyncCall("EnableZoneDetected", False)
        except:
            pass

    @pyqtSlot()
    def share(self):
        socialSharingInterface.share("", SAVE_DEST_TEMP)

    @pyqtSlot(int, int, str, result=bool)
    def checkKeySequenceEqual(self, modifier, key, targetKeySequence):
        keySequence = QKeySequence(modifier + key).toString()
        return keySequence == targetKeySequence

    @pyqtSlot(int, int, result=str)
    def keyEventToQKeySequenceString(self, modifier, key):
        keySequence = QKeySequence(modifier + key).toString()
        return keySequence

    def showHotKeyOSD(self):
        self.rootObject().showHotKeyOSD()

    def showWindow(self):
        self.showFullScreen()
        self.grabFocus()

    @pyqtSlot()
    def closeWindow(self):
        self.enable_zone()
        unregister_service()
        self.close()
        if self._settings.showOSD:
            self.showHotKeyOSD()
        else:
            qApp.quit()


def _actionInvoked(notificationId, actionId):
    global _fileSaveLocation

    if _notificationId == notificationId:
        if actionId == ACTION_ID_OPEN:
            subprocess.call(["xdg-open", os.path.dirname(_fileSaveLocation)])

def _notificationClosed( notificationId, reason):
    if _notificationId == notificationId:
        qApp.quit()

def copyPixmap(pixmap):
    global _notificationId
    clipboard = QApplication.clipboard()
    clipboard.clear()
    clipboard.setPixmap(pixmap)

    _notificationId = notificationsInterface.notify("Deepin Screenshot", "Screenshot has been copied to clipboard")

def savePixmap(pixmap, fileName):
    global _notificationId
    global _fileSaveLocation
    pixmap.save(fileName)

    _fileSaveLocation = fileName
    _notificationId = notificationsInterface.notify("Deepin Screenshot", _fileSaveLocation, [ACTION_ID_OPEN, "Open"])

def saveScreenshot(pixmap):
    global settings
    global soundEffect
    global savePathValue

    soundEffect.play()

    fileName = "%s%s.png" % (_("DeepinScreenshot"),
                             time.strftime("%Y%m%d%H%M%S", time.localtime()))
    save_op = settings.getOption("save", "save_op")
    save_op_index = int(save_op)

    absSavePath = os.path.abspath(savePathValue)
    if savePathValue and os.path.exists(os.path.dirname(absSavePath)):
        savePixmap(pixmap, absSavePath)
    else:
        saveDir = ""
        copy = False
        if save_op_index == 0: #saveId == "save_to_desktop":
            saveDir = QStandardPaths.writableLocation(QStandardPaths.DesktopLocation)
        elif save_op_index == 1: #saveId == "auto_save" :
            saveDir = QStandardPaths.writableLocation(QStandardPaths.PicturesLocation)
        elif save_op_index == 2: #saveId == "save_to_dir":
            saveDir = QFileDialog.getExistingDirectory()
        elif save_op_index == 4: #saveId == "auto_save_ClipBoard":
            copy = True
            saveDir = QStandardPaths.writableLocation(QStandardPaths.PicturesLocation)
        else: copy = True

        if copy: copyPixmap(pixmap)
        if saveDir: savePixmap(pixmap, os.path.join(saveDir, fileName))

def main():
    global view
    global settings
    global windoInfo
    global menu_controller

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
        view = Window(settings, windoInfo)
        view.setX(screen_geo.x())
        view.setY(screen_geo.y())
        view.setWidth(screen_geo.width())
        view.setHeight(screen_geo.height())

        qml_context = view.rootContext()
        qml_context.setContextProperty("windowView", view)
        qml_context.setContextProperty("qApp", qApp)
        qml_context.setContextProperty("screenWidth", view.window_info.screen_width)
        qml_context.setContextProperty("screenHeight", view.window_info.screen_height)
        qml_context.setContextProperty("_menu_controller", menu_controller)

        view.setSource(QUrl.fromLocalFile(MAIN_QML))
        view.disable_zone()
        view.showWindow()

        menu_controller.preMenuShow.connect(view.ungrabFocus)
        menu_controller.postMenuHide.connect(view.grabFocus)

if __name__ == "__main__":
    parser = QCommandLineParser()
    parser.addHelpOption()
    parser.addVersionOption()

    delayOption = QCommandLineOption(["d", "delay"],
                                     _("Take a screenshot after NUM seconds"),
                                     "NUM")
    fullscreenOption = QCommandLineOption(["f", "fullscreen"],
                                     _("Take a screenshot of the whole screen"))
    topWindowOption = QCommandLineOption(["w", "top-window"],
                                     _("Take a screenshot of the most top \
                                        window"))
    savePathOption = QCommandLineOption(["s", "save-path"],
                                     _("Specify a path to save the screenshot"),
                                     "PATH")
    startFromDesktopOption = QCommandLineOption(["i", "icon"],
                                     _("Indicate that this program's started \
                                        by clicking desktop file."))
    parser.addOption(delayOption)
    parser.addOption(fullscreenOption)
    parser.addOption(topWindowOption)
    parser.addOption(savePathOption)
    parser.addOption(startFromDesktopOption)
    parser.process(app)

    delayValue = int(parser.value(delayOption) or 0)
    fullscreenValue = bool(parser.isSet(fullscreenOption) or False)
    topWindowValue = bool(parser.isSet(topWindowOption) or False)
    savePathValue = str(parser.value(savePathOption) or "")
    startFromDesktopValue = bool(parser.isSet(startFromDesktopOption) or False)

    if is_service_exist():
        notificationsInterface.notify("Deepin Screenshot",
            "Deepin Screenshot is running!")
    else:
        QTimer.singleShot(max(0, delayValue * 1000), main)

        signal.signal(signal.SIGINT, signal.SIG_DFL)
        sys.exit(app.exec_())
