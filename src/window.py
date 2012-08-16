#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2011 Deepin, Inc.
#               2011 Hou Shaohui
#
# Author:     Hou Shaohui <houshao55@gmail.com>
# Maintainer: Hou ShaoHui <houshao55@gmail.com>
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
from Xlib import display

from constant import *
import pygtk
pygtk.require("2.0")
import gtk
import ewmh

DISPLAY = display.Display()
SCREEN = DISPLAY.screen()
ROOT_WINDOW = SCREEN.root
SCREEN_WIDTH = SCREEN.width_in_pixels
SCREEN_HEIGHT = SCREEN.height_in_pixels
WM_HINTS = DISPLAY.intern_atom("WM_HINTS", True)
WM_STATE = DISPLAY.intern_atom("WM_STATE", True)
WM_DESKTOP = DISPLAY.intern_atom("_NET_WM_DESKTOP", True)
EWMH = ewmh.EWMH(DISPLAY, ROOT_WINDOW)

def find_window_by_property(xlibWindow, atom=WM_STATE):
    ''' find Window by property '''
    result = xlibWindow.query_tree().children
    if not result:
        return None
    else:
        for children in result:
            status = children.get_property(atom, WM_HINTS, 0, 0)
            if status:
                child = children
            else:
                child = find_window_by_property(children, atom)
        return child

def get_client_window(target):
    ''' Enumerate clientWindow '''
    # 枚举所有窗口
    status = target.get_property(WM_STATE, WM_HINTS, 0, 0)
    if status:
        return target
    client = find_window_by_property(target)
    if client:
        return client
    return target

def filter_window():
    ''' without other window'''
    windowList = []
    for xlibWindow in enum_xlib_window():
        if xlibWindow.get_property(WM_DESKTOP, WM_HINTS, 0, 0):
            windowList.append(xlibWindow)
        else:
            if find_window_by_property(xlibWindow, WM_DESKTOP):
                windowList.append(xlibWindow)
    return windowList

def get_xlib_pointer_window():
    ''' grab pointer window '''
    # 获取鼠标指针当前的窗口
    return ROOT_WINDOW.query_pointer().child

def get_xlib_focus_window():
    ''' grab focus window'''
    return disp.get_input_focus().focus

def get_window_coord(xlibWindow):
    ''' covert xlibWindow's coord'''
    # 获取窗口坐标
    clientWindow = get_client_window(xlibWindow)
    if xlibWindow != clientWindow:
        #print "xwindow:", xlibWindow.get_geometry()
        #print "client window:", clientWindow.get_geometry()
        #print ""
        x = xlibWindow.get_geometry().x + clientWindow.get_geometry().x
        y = xlibWindow.get_geometry().y + clientWindow.get_geometry().y - 30
        width = clientWindow.get_geometry().width
        height = clientWindow.get_geometry().height + 30
    else:
        x = xlibWindow.get_geometry().x
        y = xlibWindow.get_geometry().y
        width = xlibWindow.get_geometry().width
        height = xlibWindow.get_geometry().height
    return (x, y, width, height)

def get_pointer_window_coord():
    ''' get current Focus Window's Coord '''
    return get_window_coord(get_xlib_pointer_window())

def get_focus_window_coord():
    focusWindow = get_xlib_focus_window()
    #(x, y, width, height) = get_window_coord(focusWindow)
    return get_window_coord(focusWindow)

def enum_xlib_window():
    ''' enumerate child window of ROOT_WINDOW'''
    return ROOT_WINDOW.query_tree().children

def xwindow_to_gwindow(xlibWindow):
    ''' convert Xlib's window to Gtk's window '''
    return gtk.gdk.window_foreign_new(xlibWindow.id)

def get_usertime_window():
    '''Usertime Window  '''
    usertimeWindow = {}
    for eachWindow in enum_xlib_window():
        sequence_number = eachWindow.get_geometry().sequence_number
        usertimeWindow[sequence_number] = eachWindow
    return sorted(usertimeWindow.iteritems(), key=lambda k: k[0], reverse=True)

def enum_gtk_window():
    '''  enumerate gtkWindow from xlibWindow '''
    gtkWindowList = []
    for eachWindow in enum_xlib_window():
        gtkWindowList.append(xwindow_to_gwindow(eachWindow))
    return gtkWindowList

def get_window_title(xlibWindow):
    ''' get window title'''
    clientWindow = get_client_window(xlibWindow)
    if clientWindow != xlibWindeow:
        return clientWindow.get_wm_name()
    return xlibWindow.get_wm_name()

def convert_coord(x, y, width, height):
    ''' cut out overlop the screen'''
    # 获取在屏幕内的部分
    xWidth = x + width
    yHeight = y + height
       
    if x < 0 and y > 0 and y < yHeight < SCREEN_HEIGHT:
        return (0, y, width+x, height)
    
    if x < 0 and yHeight > SCREEN_HEIGHT:
        return (0, y, width+x, height - (yHeight - SCREEN_HEIGHT))
    
    if xWidth > SCREEN_WIDTH and yHeight > SCREEN_HEIGHT:
        return (x, y, width - (xWidth - SCREEN_WIDTH), height - (yHeight - SCREEN_HEIGHT))
    
    if x > 0 and x < xWidth < SCREEN_WIDTH and yHeight > SCREEN_HEIGHT:
        return (x, y, width, height - (yHeight - SCREEN_HEIGHT))
    
    if xWidth > SCREEN_WIDTH and y > 0 and y < yHeight < SCREEN_HEIGHT:
        return (x, y, width - (xWidth - SCREEN_WIDTH), height)
    
    if x < 0 and y < 0:
        return (0, 0, xWidth, yHeight)
    
    if x > 0 and x < xWidth < SCREEN_WIDTH and y < 0:
        return (x, 0, width, yHeight)
    
    if x > 0 and xWidth > SCREEN_WIDTH and y < 0:
        return (x, 0, width - (xWidth - SCREEN_WIDTH), yHeight) 
    return (x, y, width, height)

def get_screenshot_window_info():
    ''' return (x, y, width, height) '''
    # 获取窗口的x,y 长，宽
    coordInfo = namedtuple('coord', 'x y width height')
    screenshotWindowInfo = []
    screenshotWindowInfo.append(coordInfo(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
    for eachWindow in filter_window():
        (x, y, width, height) = get_window_coord(eachWindow)
        screenshotWindowInfo.append(coordInfo(*convert_coord(x, y, width, height)))
    return screenshotWindowInfo

def get_screenshot_pixbuf(fullscreen=True):
    ''' save snapshot to file with filetype. '''
    rootWindow = gtk.gdk.get_default_root_window() 
    if not fullscreen:
        (x, y, width, height) = convert_coord(*get_window_coord(get_xlib_pointer_window()))
    else:
        (x, y, width, height, depth) = rootWindow.get_geometry() 
    
    pixbuf = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, False, 8, width, height)
    pixbuf.get_from_drawable(rootWindow, rootWindow.get_colormap(), x, y, 0, 0, width, height)
    return pixbuf
