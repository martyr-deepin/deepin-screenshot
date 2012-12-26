#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2011 Deepin, Inc.
#               2011 Hou Shaohui
#
# Author:     Hou Shaohui <houshao55@gmail.com>
#             Long Changjin <admin@longchangjin.cn>
# Maintainer: Hou ShaoHui <houshao55@gmail.com>
#             Long Changjin <admin@longchangjin.cn>
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

from collections import namedtuple
import pygtk
pygtk.require("2.0")
import gtk
import wnck
from Xlib import display

DISPLAY_NUM = len(gtk.gdk.display_manager_get().list_displays())    # gtk.gdk.Display num
DISPLAY = gtk.gdk.display_get_default()         # gtk.gdk.Display
SCREEN_NUM = DISPLAY.get_n_screens()            # gtk.gdk.Screen num
GDK_SCREEN = DISPLAY.get_default_screen()       # gtk.gdk.Screen
MONITOR_NUM = GDK_SCREEN.get_n_monitors()       # the monitors number

CURRENT_MONITOR = 0                             # index of current monitor
CURRENT_MONITOR_INFO = GDK_SCREEN.get_monitor_geometry(CURRENT_MONITOR) # current monitor info
SCREEN_WIDTH = CURRENT_MONITOR_INFO.width       # current monitor width
SCREEN_HEIGHT = CURRENT_MONITOR_INFO.height     # current monitor height
SCREEN_X = CURRENT_MONITOR_INFO.x               # current monitor x coordinate
SCREEN_Y = CURRENT_MONITOR_INFO.y               # current monitor y coordinate

WNCK_SCREEN = wnck.screen_get_default()         # wnck.Screen
WNCK_SCREEN.force_update()                      # update wnc.Screen
WNCK_WORKSPACE = WNCK_SCREEN.get_active_workspace() # current workspace

# for multi monitor, get current monitor
def get_current_monitor():
    '''
    get current monitor
    @return: the index of current monitor
    '''
    global CURRENT_MONITOR
    CURRENT_MONITOR = GDK_SCREEN.get_monitor_at_point(*DISPLAY.get_pointer()[1:3])
    return CURRENT_MONITOR

def get_current_monitor_info():
    '''
    get current monitor geometry
    @return: a tuple containing the X and Y coordinate and width and height of current monitor
    '''
    global CURRENT_MONITOR_INFO
    global SCREEN_X, SCREEN_Y, SCREEN_WIDTH, SCREEN_HEIGHT
    CURRENT_MONITOR_INFO = GDK_SCREEN.get_monitor_geometry(get_current_monitor())
    SCREEN_WIDTH = CURRENT_MONITOR_INFO.width
    SCREEN_HEIGHT = CURRENT_MONITOR_INFO.height
    SCREEN_X = CURRENT_MONITOR_INFO.x
    SCREEN_Y = CURRENT_MONITOR_INFO.y
    return CURRENT_MONITOR_INFO

def convert_coord(x, y, width, height):
    '''
    cut out overstep the monitor
    @param x: X coordinate of the source point
    @param y: Y coordinate of the source point
    @param width: the area's width
    @param height: the area's height
    @return: a tuple containing new x and y and width and height that in this monitor
    '''
    end_x = x + width - SCREEN_X
    end_y = y + height - SCREEN_Y
    # overstep left of monitor
    if x < SCREEN_X:
        width += x - SCREEN_X
        x = SCREEN_X
    # overstep top of monitor
    if y < SCREEN_Y:
        height += y - SCREEN_Y
        y = SCREEN_Y
    # overstep right of monitor
    if end_x > SCREEN_WIDTH:
        width = SCREEN_WIDTH - x
    # overstep bottom of monitor
    if end_y > SCREEN_HEIGHT:
        height = SCREEN_HEIGHT - y
    return (x, y, width, height)

def get_screenshot_window_info():
    '''
    get current monitor windows info
    @return: all windows' coordinate in this workspace
    @rtype: a list, each in the list is a tuple which containing x and y and width and height
    '''
    get_current_monitor_info()
    return get_windows_info()

def get_windows_info():
    '''
    @return: all windows' coordinate in this workspace
    @rtype: a list, each in the list is a tuple which containing x and y and width and height
    '''
    coord= namedtuple('coord', 'x y width height')
    screenshot_window_info = []
    screenshot_window_info.insert(0, coord(SCREEN_X, SCREEN_Y, SCREEN_WIDTH, SCREEN_HEIGHT))
    WNCK_SCREEN.force_update()
    win_list = WNCK_SCREEN.get_windows_stacked()
    WNCK_WORKSPACE = WNCK_SCREEN.get_active_workspace()
    for w in win_list:
        if not w.is_on_workspace(WNCK_WORKSPACE):
            continue
        try:    # some environment has not WINDOW_STATE_MINIMIZED property
            if w.get_state() & wnck.WINDOW_STATE_MINIMIZED or\
                    w.get_state() & wnck.WINDOW_STATE_HIDDEN or\
                    w.get_window_type() == wnck.WINDOW_DESKTOP:
                continue
        except:
            pass
        (x, y, width, height) = w.get_geometry()                # with frame
        #(x, y, width, height) = w.get_client_window_geometry()  # without frame
        if w.get_window_type() == wnck.WINDOW_DOCK and\
                width >= SCREEN_WIDTH and height >= SCREEN_HEIGHT:
            continue
        screenshot_window_info.insert(0, coord(*convert_coord(x, y, width, height)))
    return screenshot_window_info

def get_window_info_at_pointer():
    '''
    get the window's coordinate at pointer
    return: a tuple containing x and y and width and height of the window at pointer
    '''
    (x, y) = DISPLAY.get_pointer()[1:3]
    win_info = get_screenshot_window_info()
    for info in win_info:
        if info.x <= x <= info.x + info.width and info.y <= y <= info.y + info.height:
            return info

def get_screenshot_pixbuf(fullscreen=True):
    '''
    get the screenshot pixbuf
    @param fullscreen: if get fullscreen snapshot.
    @return: a gtk.gdk.Pixbuf of screenshot
    '''
    xroot = display.Display().screen().root
    root_window = gtk.gdk.window_foreign_new(xroot.id)
    if not fullscreen:
        info = get_window_info_at_pointer()
        (x, y, width, height) = (info.x, info.y, info.width, info.height)
    else:
        (x, y, width, height) = get_current_monitor_info()
    
    pixbuf = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, False, 8, width, height)
    pixbuf.get_from_drawable(root_window, root_window.get_colormap(), x, y, 0, 0, width, height)
    return pixbuf


# 
def get_display(index):
    '''
    get the index display
    @param index: the index of display
    '''
    if index >= DISPLAY_NUM:
        return
    global DISPLAY
    global SCREEN_NUM
    DISPLAY = gtk.gdk.display_manager_get().list_displays()[index]
    SCREEN_NUM = DISPLAY.get_n_screens()

def get_wnck_screen(index):
    '''
    get the index screen
    @param index: the index of screen
    '''
    global WNCK_SCREEN
    screen = wnck.screen_get(index)
    if screen:
        WNCK_SCREEN = screen
        WNCK_SCREEN.force_update()
        
        global WNCK_WORKSPACE
        global SCREEN_WIDTH
        global SCREEN_HEIGHT
        WNCK_WORKSPACE = WNCK_SCREEN.get_active_workspace()
        SCREEN_WIDTH = WNCK_SCREEN.get_width()
        SCREEN_HEIGHT = WNCK_SCREEN.get_height()
    if index >= SCREEN_NUM:
        return
    global GDK_SCREEN
    GDK_SCREEN = DISPLAY.get_screen(index)
