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

from utils import no_error_output
with no_error_output():
    import wnck

from PyQt5 import QtGui
from PyQt5.QtWidgets import qApp
from PyQt5.QtCore import pyqtSlot
from xpybutil.util import get_property, get_property_value

class WindowInfo(object):

    def __init__(self, screenNumber):
        self.wnck_screen = wnck.screen_get_default()         # wnck.Screen
        self.wnck_screen.force_update()                      # update wnc.Screen
        self.wnck_workspace = self.wnck_screen.get_active_workspace() # current workspace

        self.screen_rect = qApp.desktop().screenGeometry(screenNumber)
        self.screen_x = self.screen_rect.x()
        self.screen_y = self.screen_rect.y()
        self.screen_width = self.screen_rect.width()
        self.screen_height = self.screen_rect.height()

        self.windows_info = self.get_windows_info()

    @pyqtSlot(result="QVariant")
    def get_window_info_at_pointer(self):
        cursor_pos = QtGui.QCursor.pos()
        for (x, y, w, h) in self.windows_info:
            if x <= cursor_pos.x() <= x + w and y <= cursor_pos.y() <= y + h:
                return [x, y, w, h]

        return [self.screen_x, self.screen_y, self.screen_width, self.screen_height]

    def get_windows_info(self):
        '''
        @return: all windows' coordinate in this workspace
        @rtype: a list, each in the list is a tuple which containing x and y and width and height
        '''
        screenshot_window_info = []
        self.wnck_screen.force_update()
        win_list = self.wnck_screen.get_windows_stacked()
        self.wnck_workspace = self.wnck_screen.get_active_workspace()
        if not self.wnck_workspace:      # there is no active workspace in some wm.
            self.wnck_workspace = self.wnck_screen.get_workspaces()[0]
        for w in win_list:
            if not w.is_on_workspace(self.wnck_workspace):
                continue
            try:    # some environment has not WINDOW_STATE_MINIMIZED property
                if w.get_state() & wnck.WINDOW_STATE_MINIMIZED or\
                        w.get_state() & wnck.WINDOW_STATE_HIDDEN or\
                        w.get_window_type() == wnck.WINDOW_DESKTOP:
                    continue
            except:
                pass
            (x, y, width, height) = w.get_geometry()                # with frame

            # Get shadow value for deepin-ui window.
            cookie = get_property(w.get_xid(), "DEEPIN_WINDOW_SHADOW")
            deepin_window_shadow_value = get_property_value(cookie.reply())
            if deepin_window_shadow_value:
                deepin_window_shadow_size = int(deepin_window_shadow_value)
            else:
                deepin_window_shadow_size = 0

            if w.get_window_type() == wnck.WINDOW_DOCK and\
                    width >= self.screen_width and height >= self.screen_height:
                continue

            (wx, wy, ww, wh) = self.convert_coord(
                x + deepin_window_shadow_size,
                y + deepin_window_shadow_size,
                width - deepin_window_shadow_size * 2,
                height - deepin_window_shadow_size * 2)

            if ww != 0 and wh != 0:
              screenshot_window_info.insert(0, (wx, wy, ww, wh))
        return screenshot_window_info

    def convert_coord(self, x, y, width, height):
        '''
        cut out overstep the monitor
        @param x: X coordinate of the source point
        @param y: Y coordinate of the source point
        @param width: the area's width
        @param height: the area's height
        @return: a tuple containing new x and y and width and height that in this monitor
        '''
        end_x = x + width - self.screen_x
        end_y = y + height - self.screen_y
        # overstep left of monitor
        if x < self.screen_x:
            width += x - self.screen_x
            x = self.screen_x
        # overstep top of monitor
        if y < self.screen_y:
            height += y - self.screen_y
            y = self.screen_y
        # overstep right of monitor
        if end_x > self.screen_width:
            width = self.screen_width - x
        # overstep bottom of monitor
        if end_y > self.screen_height:
            height = self.screen_height - y
        return (x, y, width, height)

