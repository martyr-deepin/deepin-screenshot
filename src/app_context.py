#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2011 ~ 2015 Deepin, Inc.
#               2011 ~ 2015 Wang YaoHua
#
# Author:     Wang YaoHua <mr.asianwang@gmail.com>
# Maintainer: Wang YaoHua <mr.asianwang@gmail.com>
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
import time
import tempfile
import subprocess
from weakref import ref
from functools import partial

from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import qApp, QFileDialog
from PyQt5.QtCore import QStandardPaths, QUrl, QObject
from PyQt5.QtCore import QRect, QPoint, QSize, QTimer, pyqtSignal

from i18n import _
from app_window import Window
from window_info import WindowInfo
from menu_controller import MenuController
from dbus_interfaces import controlCenterInterface
from dbus_interfaces import notificationsInterface
from constants import MAIN_QML, GTK_CLIP

ACTION_ID_OPEN = "id_open"

class AppContext(QObject):
    """Every AppContext instance keeps an environment which is different
       from other instances, acting like a container.
    """

    needSound = pyqtSignal()
    needOSD = pyqtSignal(QRect)
    finished = pyqtSignal()

    def __init__(self, argValues):
        super(AppContext, self).__init__()
        self.argValues = argValues
        self.settings = None
        self.windowInfo = None
        self.window = None

        self._notificationId = None
        self._fileSaveLocation = None

        self._waitNotificationTimer = QTimer()
        self._waitNotificationTimer.setInterval(10 * 1000)
        self._waitNotificationTimer.setSingleShot(True)
        self._waitNotificationTimer.timeout.connect(self.finished)

    def _notify(self, *args, **kwargs):
        self._waitNotificationTimer.start()
        notify = partial(notificationsInterface.notify, _("Deepin Screenshot"))
        return notify(*args, **kwargs)

    def _actionInvoked(self, notificationId, actionId):
        self._waitNotificationTimer.stop()

        if self._notificationId == notificationId:
            if actionId == ACTION_ID_OPEN:
                subprocess.call(["xdg-open",
                    os.path.dirname(self._fileSaveLocation)])
            self.finished.emit()

    def _notificationClosed(self, notificationId, reason):
        self._waitNotificationTimer.stop()

        if self._notificationId == notificationId:
            self.finished.emit()

    def _windowVisibleChanged(self, visible):
        if visible:
            self.sender().disable_zone()
            self.sender().grabFocus()

            controlCenterInterface.hideImmediately()
        else:
            self.sender().enable_zone()
            self.sender().ungrabFocus()

            if self.settings.showOSD:
                area = QRect(QPoint(self.window.x(), self.window.y()),
                             QSize(self.window.width(), self.window.height()))
                self.needOSD.emit(area)

    # this function just handles the situation that this context's
    # finished by the user interaction.
    def _windowClosing(self):
        if self.settings.showOSD:
            area = QRect(QPoint(self.window.x(), self.window.y()),
                         QSize(self.window.width(), self.window.height()))
            self.needOSD.emit(area)
        self.finished.emit()

    def copyPixmap(self, pixmap):
        _temp = "%s.png" % tempfile.mktemp()
        pixmap.save(_temp)
        subprocess.call([GTK_CLIP, _temp])

        self._notificationId = self._notify(
            _("Picture has been saved to clipboard"))

    def savePixmap(self, pixmap, fileName):
        pixmap.save(fileName)

        self._fileSaveLocation = fileName
        self._notificationId = self._notify(
            _("Picture has been saved to") + fileName,
            [ACTION_ID_OPEN, _("View")])

    def saveScreenshot(self, pixmap):
        self.needSound.emit()

        savePathValue = self.argValues["savePath"]
        timeStamp = time.strftime("%Y%m%d%H%M%S", time.localtime())
        fileName = "%s%s.png" % (_("DeepinScreenshot"), timeStamp)

        save_op = self.settings.getOption("save", "save_op")
        save_op_index = int(save_op)

        absSavePath = ""
        copyToClipborad = False
        if savePathValue and os.path.exists(os.path.dirname(absSavePath)):
            absSavePath = os.path.abspath(savePathValue)
        else:
            if save_op_index == 0: #saveId == "save_to_desktop":
                saveDir = QStandardPaths.writableLocation(
                    QStandardPaths.DesktopLocation)
                absSavePath = os.path.join(saveDir, fileName)
            elif save_op_index == 1: #saveId == "auto_save" :
                saveDir = QStandardPaths.writableLocation(
                    QStandardPaths.PicturesLocation)
                absSavePath = os.path.join(saveDir, fileName)
            elif save_op_index == 2: #saveId == "save_to_dir":
                lastSavePath = self.settings.getOption("save", "folder")
                absSavePath = QFileDialog.getSaveFileName(None, _("Save"),
                    os.path.join(lastSavePath, fileName))[0]
                self.settings.setOption("save", "folder",
                    os.path.dirname(absSavePath) or lastSavePath)
            elif save_op_index == 4: #saveId == "auto_save_ClipBoard":
                copyToClipborad = True
                saveDir = QStandardPaths.writableLocation(
                    QStandardPaths.PicturesLocation)
                absSavePath = os.path.join(saveDir, fileName)
            else: copyToClipborad = True

        if absSavePath or copyToClipborad:
            if copyToClipborad: self.copyPixmap(pixmap)
            if absSavePath: self.savePixmap(pixmap, absSavePath)
        else:
            self.finished.emit()

    def main(self):
        fullscreenValue = self.argValues["fullscreen"]
        topWindowValue = self.argValues["topWindow"]
        startFromDesktopValue = self.argValues["startFromDesktop"]

        cursor_pos = QCursor.pos()
        desktop = qApp.desktop()
        screen_num = desktop.screenNumber(cursor_pos)
        screen_geo = desktop.screenGeometry(screen_num)
        pixmap = qApp.primaryScreen().grabWindow(0)
        pixmap = pixmap.copy(screen_geo.x(), screen_geo.y(),
                             screen_geo.width(), screen_geo.height())
        pixmap.save(self.settings.tmpImageFile)

        self.settings.showOSD = startFromDesktopValue
        menu_controller = MenuController()
        self.windowInfo = WindowInfo(screen_num)

        notificationsInterface.ActionInvoked.connect(
            self._actionInvoked)
        notificationsInterface.NotificationClosed.connect(
            self._notificationClosed)

        if fullscreenValue:
            self.saveScreenshot(pixmap)
        elif topWindowValue:
            wInfos = self.windoInfo.get_windows_info()
            if len(wInfos) > 0:
                wInfo = wInfos[0]
                pix = pixmap.copy(wInfo[0] - screen_geo.x(),
                                  wInfo[1] - screen_geo.y(),
                                  wInfo[2], wInfo[3])
                self.saveScreenshot(pix)
        else:
            self.window = Window(ref(self)())
            self.window.setX(screen_geo.x())
            self.window.setY(screen_geo.y())
            self.window.setWidth(screen_geo.width())
            self.window.setHeight(screen_geo.height())
            self.window.windowClosing.connect(self._windowClosing)
            self.window.visibleChanged.connect(self._windowVisibleChanged)

            qml_context = self.window.rootContext()
            qml_context.setContextProperty("windowView", self.window)
            qml_context.setContextProperty("qApp", qApp)
            qml_context.setContextProperty("screenWidth",
                self.window.window_info.screen_width)
            qml_context.setContextProperty("screenHeight",
                self.window.window_info.screen_height)
            qml_context.setContextProperty("tmpImageFile",
                self.settings.tmpImageFile)
            qml_context.setContextProperty("blurImageFile",
                self.settings.tmpBlurFile)
            qml_context.setContextProperty("mosaicImageFile",
                self.settings.tmpMosaiceFile)
            qml_context.setContextProperty("_menu_controller", menu_controller)

            self.window.setSource(QUrl.fromLocalFile(MAIN_QML))
            self.window.showWindow()

            menu_controller.preMenuShow.connect(self.window.ungrabFocus)
            menu_controller.postMenuHide.connect(self.window.grabFocus)
