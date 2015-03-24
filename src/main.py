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
from dbus_interfaces import controlCenterInterface, hotZoneInterface
from dbus_interfaces import notificationsInterface, socialSharingInterface
from constants import MAIN_QML, SOUND_FILE, MAIN_DIR, TMP_IMAGE_FILE, GTK_CLIP

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

view = None
settings = ScreenShotSettings()
_notificationId = None
_fileSaveLocation = None
_quitTimer = QTimer()
_quitTimer.setInterval(10 * 1000)
_quitTimer.setSingleShot(True)
_quitTimer.timeout.connect(qApp.quit)

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
        self.setTitle(_("Deepin Screenshot"))

        self.qimage = QImage(self._settings.tmpImageFile)
        self.qpixmap = QPixmap()
        self.qpixmap.convertFromImage(self.qimage)

        self.window_info = windowInfo

        self._grabPointerStatus = False
        self._grabKeyboardStatus = False
        self._grabFocusTimer = self._getGrabFocusTimer()

        self._osdShowed = False
        self._osdShowing = False
        self._quitOnOsdTimeout = False

        self._share = False

    @pyqtSlot(int, int, result="QVariant")
    def get_color_at_point(self, x, y):
        if x >= 0 and y >= 0:
            rgb = self.qimage.pixel(x, y)
            return [qRed(rgb), qGreen(rgb), qBlue(rgb)]
        else:
            return [0, 0, 0]

    @pyqtSlot(result="QVariant")
    def get_window_info_at_pointer(self):
        wInfo = self.window_info.get_window_info_at_pointer()
        wInfo[0] -= self.x()
        wInfo[1] -= self.y()
        return wInfo

    @pyqtSlot(result="QVariant")
    def get_cursor_pos(self):
        '''
        get the cursor position relative to the top-left corner of this window
        '''
        pos = QCursor.pos()
        pos.setX(pos.x() - self.x())
        pos.setY(pos.y() - self.y())
        return pos

    @pyqtSlot(str)
    def set_cursor_shape(self, shape):
        '''
        Set the shape of cursor, the param shape should be one of the keys
        of the global variable cursor_shape_dict.
        '''
        if cursor_shape_dict.get(shape):
            pix = QPixmap(cursor_shape_dict[shape])
            if shape == "shape_start_cursor":
                cur = QCursor(pix, hotX=8, hotY=8)
            elif shape.startswith(CURSOR_SHAPE_COLOR_PEN_PREFIX):
                cur = QCursor(pix, hotX=0, hotY=pix.height())
            else:
                cur = QCursor(pix, hotX=5, hotY=5)
        else:
            cur = QCursor(Qt.ArrowCursor)
        self.setCursor(cur)

    @pyqtSlot(str,int,int,int,int)
    def save_overload(self, style, x, y, width, height):
        mosaic_radius = 10
        blur_radius = 10

        p = QPixmap.fromImage(self.grabWindow())
        p = p.copy(x,y,width,height)

        if style == "mosaic":
            p = p.scaled(width / mosaic_radius, height / mosaic_radius,
                         Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
            p = p.scaled(width, height)
        elif style == "blur":
            p = p.scaled(width / blur_radius, height / blur_radius,
                         Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
            p = p.scaled(width, height,
                         Qt.IgnoreAspectRatio, Qt.SmoothTransformation)

        image_dir = "/tmp/deepin-screenshot-%s.png" % style
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
        self._settings.showOSD and self.showHotKeyOSD()

    @pyqtSlot()
    def enable_zone(self):
        hotZoneInterface.enableZone()

    @pyqtSlot()
    def disable_zone(self):
        hotZoneInterface.disableZone()

    @pyqtSlot()
    def share(self): self._share = True

    @pyqtSlot(int, int, str, result=bool)
    def checkKeySequenceEqual(self, modifier, key, targetKeySequence):
        keySequence = QKeySequence(modifier + key).toString()
        return keySequence == targetKeySequence

    @pyqtSlot(int, int, result=str)
    def keyEventToQKeySequenceString(self, modifier, key):
        keySequence = QKeySequence(modifier + key).toString()
        return keySequence

    def _handleOSDTimeout(self):
        self._osdShowing = False
        if self._quitOnOsdTimeout:
            qApp.quit()

    def showHotKeyOSD(self):
        self._osdShowing = True
        self._osdShowed = True
        self.rootObject().showHotKeyOSD()
        self.rootObject().osdTimeout.connect(self._handleOSDTimeout)

    def showWindow(self):
        self.disable_zone()
        self.showFullScreen()
        self.grabFocus()

    @pyqtSlot()
    def closeWindow(self):
        self.enable_zone()
        unregister_service()
        self.close()

        if self._share: socialSharingInterface.share("", SAVE_DEST_TEMP)

        self._quitOnOsdTimeout = True
        if self._settings.showOSD:
            if not self._osdShowed:
                self.showHotKeyOSD()
            elif not self._osdShowing:
                qApp.quit()
        else:
            qApp.quit()


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
        view.closeWindow() if view else qApp.quit()

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
    parser = QCommandLineParser()
    parser.addHelpOption()
    parser.addVersionOption()

    delayOption = QCommandLineOption(["d", "delay"],
        "Take a screenshot after NUM seconds", "NUM")
    fullscreenOption = QCommandLineOption(["f", "fullscreen"],
        "Take a screenshot of the whole screen")
    topWindowOption = QCommandLineOption(["w", "top-window"],
        "Take a screenshot of the most top window")
    savePathOption = QCommandLineOption(["s", "save-path"],
        "Specify a path to save the screenshot", "PATH")
    startFromDesktopOption = QCommandLineOption(["i", "icon"],
        "Indicate that this program's started by clicking desktop file.")

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
        notificationsInterface.notify(_("Deepin Screenshot"),
            _("Deepin Screenshot has been started."))
    else:
        if delayValue > 0:
            notificationsInterface.notify(_("Deepin Screenshot"),
            _("Deepin Screenshot will start after %s seconds.") % delayValue)

        QTimer.singleShot(max(0, delayValue * 1000), main)
        soundEffect = QSoundEffect()
        soundEffect.setSource(QUrl(SOUND_FILE))

        signal.signal(signal.SIGINT, signal.SIG_DFL)
        sys.exit(app.exec_())
