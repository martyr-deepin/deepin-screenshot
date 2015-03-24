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
import tempfile

from PyQt5.QtQuick import QQuickView
from PyQt5.QtWidgets import qApp
from PyQt5.QtCore import Qt, QTimer, pyqtSlot
from PyQt5.QtGui import QSurfaceFormat, QColor, QImage, QPixmap, QCursor
from PyQt5.QtGui import QKeySequence, qRed, qGreen, qBlue

from i18n import _
from constants import MAIN_DIR
from dbus_interfaces import socialSharingInterface, hotZoneInterface

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
cursor_shape_dict = {}
init_cursor_shape_dict()

class Window(QQuickView):
    def __init__(self, settings, windowInfo, saveScreenshot):
        QQuickView.__init__(self)
        self._settings = settings
        self._saveScreenshotFunc = saveScreenshot

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

        self._osdShowed = False
        self._osdShowing = False
        self._quitOnOsdTimeout = False

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
        self._saveScreenshotFunc(pixmap)
        self._settings.showOSD and self.showHotKeyOSD()

    @pyqtSlot()
    def enable_zone(self):
        hotZoneInterface.enableZone()

    @pyqtSlot()
    def disable_zone(self):
        hotZoneInterface.disableZone()

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
        self.close()

        self._quitOnOsdTimeout = True
        if self._settings.showOSD:
            if not self._osdShowed:
                self.showHotKeyOSD()
            elif not self._osdShowing:
                qApp.quit()
        else:
            qApp.quit()