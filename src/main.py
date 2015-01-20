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
import time
from PyQt5 import QtCore
from PyQt5.QtCore import QCoreApplication
if os.name == 'posix':
    QCoreApplication.setAttribute(QtCore.Qt.AA_X11InitThreads, True)

from PyQt5.QtQuick import QQuickView
from PyQt5.QtGui import (QSurfaceFormat, QColor, QGuiApplication,
    QPixmap, QCursor, qRed, qGreen, qBlue)
from PyQt5.QtWidgets import QApplication, qApp, QFileDialog
from PyQt5.QtCore import pyqtSlot, QStandardPaths, QUrl
from PyQt5.QtDBus import QDBusConnection, QDBusInterface

import sys
import signal
from window_info import WindowInfo
from dbus_interfaces import screenShotInterface

import tempfile
from shutil import copyfile

from share_service.config import OperateConfig

def init_cursor_shape_dict():
    global cursor_shape_dict

    dirname = os.path.dirname
    abspath = os.path.abspath
    file_name_except_extension = lambda x: os.path.basename(x).split(".")[0]

    mouse_style_dir = os.path.join(dirname(dirname(abspath(__file__))),
                                   "image/mouse_style")
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
cursor_shape_dict = {}
init_cursor_shape_dict()

def saveToClipboard(pixmap):
    clipboard = QApplication.clipboard()
    clipboard.clear()
    clipboard.setPixmap(pixmap)

class Window(QQuickView):
    def __init__(self):
        QQuickView.__init__(self)

        surface_format = QSurfaceFormat()
        surface_format.setAlphaBufferSize(8)

        self.set_cursor_shape("shape_start_cursor")
        self.setColor(QColor(0, 0, 0, 0))
        self.setFlags(QtCore.Qt.FramelessWindowHint)
        self.setResizeMode(QQuickView.SizeRootObjectToView)
        self.setFormat(surface_format)

        self.qml_context = self.rootContext()
        self.qpixmap = QGuiApplication.primaryScreen().grabWindow(0)
        self.qpixmap.save("/tmp/deepin-screenshot.png")
        self.qimage = self.qpixmap.toImage()
        self.window_info = WindowInfo()

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

    @pyqtSlot(str)
    def save_config(self, save_op_index):
        self.__config = OperateConfig()
        self.__config.set("save", save_op=str(save_op_index))

    @pyqtSlot(result="QVariant")
    def get_save_config(self):
        self.__config = OperateConfig()
        save_op = self.__config.get("save", "save_op")
        return int(save_op)

    @pyqtSlot(int,int,int,int)
    def save_screenshot(self,x,y,width,height):
        self.__config =  OperateConfig()
        save_op = self.__config.get("save", "save_op")
        save_op_index = int(save_op)
        pixmap = QPixmap.fromImage(self.grabWindow())
        pixmap = pixmap.copy(x, y, width, height)
        name = "%s%s" % (self.title(), time.strftime("%Y%m%d%H%M%S", time.localtime()))
        tmpFile = SAVE_DEST_TEMP
        pixmap.save(tmpFile)

        if save_op_index == 0: #saveId == "save_to_desktop":
            saveDir = QStandardPaths.writableLocation(QStandardPaths.DesktopLocation)
        elif save_op_index == 1: #saveId == "auto_save" :
            saveDir = QStandardPaths.writableLocation(QStandardPaths.PicturesLocation)
        elif save_op_index == 2: #saveId == "save_to_dir":
            saveDir = QFileDialog.getExistingDirectory()
        elif save_op_index == 4: #saveId == "auto_save_ClipBoard":
            saveToClipboard(pixmap)
            saveDir = QStandardPaths.writableLocation(QStandardPaths.PicturesLocation)
        else :
            saveToClipboard(pixmap)
            saveDir = ""

        if saveDir: copyfile(tmpFile, os.path.join(saveDir, name))

        screenShotInterface.notify("深度截图", saveDir + "DeepinScreenshot%s.png" %name)

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
        import subprocess
        exec_file = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                 "share_service/share.py")
        subprocess.call(["python", exec_file, SAVE_DEST_TEMP])
        self.close()

    def exit_app(self):
        self.enable_zone()
        qApp.quit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    view = Window()

    qApp.lastWindowClosed.connect(view.exit_app)

    qml_context = view.rootContext()
    qml_context.setContextProperty("windowView", view)
    qml_context.setContextProperty("qApp", qApp)
    qml_context.setContextProperty("screenWidth", view.window_info.screen_width)
    qml_context.setContextProperty("screenHeight", view.window_info.screen_height)

    view.setSource(QUrl.fromLocalFile(os.path.join(os.path.dirname(__file__), 'Main.qml')))

    view.disable_zone()
    view.showFullScreen()

    signal.signal(signal.SIGINT, signal.SIG_DFL)
    sys.exit(app.exec_())
