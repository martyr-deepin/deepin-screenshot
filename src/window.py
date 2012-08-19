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
from constant import *
import pygtk
pygtk.require("2.0")
import gtk
import wnck

DISPLAY_NUM = len(gtk.gdk.display_manager_get().list_displays())
DISPLAY = gtk.gdk.display_get_default()
SCREEN_NUM = DISPLAY.get_n_screens()
GDK_SCREEN = DISPLAY.get_default_screen()

WNCK_SCREEN = wnck.screen_get_default()
WNCK_SCREEN.force_update()
WNCK_WORKSPACE = WNCK_SCREEN.get_active_workspace()
SCREEN_WIDTH = WNCK_SCREEN.get_width()
SCREEN_HEIGHT = WNCK_SCREEN.get_height()

def convert_coord(x, y, width, height):
    ''' cut out overlop the screen'''
    end_x = x + width
    end_y = y + height
    if x < 0:
        width += x
        x = 0
    if y < 0:
        height += y
        y = 0
    if end_x > SCREEN_WIDTH: width = SCREEN_WIDTH - x
    if end_y > SCREEN_HEIGHT: height = SCREEN_HEIGHT - y
    return (x, y, width, height)

def get_screenshot_window_info():
    ''' return (x, y, width, height) '''
    coordInfo = namedtuple('coord', 'x y width height')
    screenshot_window_info = []
    screenshot_window_info.insert(0, coordInfo(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
    win_list = WNCK_SCREEN.get_windows_stacked()
    for w in win_list:
        if not w.is_on_workspace(WNCK_WORKSPACE):
            continue
        if w.get_state() & wnck.WINDOW_STATE_MINIMIZED:
            continue
        if w.is_shaded():
            w.unshade()
            (x, y, width, height) = w.get_geometry()                # with frame
            w.shade()
        else:
            (x, y, width, height) = w.get_geometry()                # with frame
        #(x, y, width, height) = w.get_client_window_geometry()  # without frame
        screenshot_window_info.insert(0, coordInfo(*convert_coord(x, y, width, height)))
    return screenshot_window_info

SCREENSHOT_WINDOW_INFO = get_screenshot_window_info()

def get_window_info_at_pointer():
    ''' get the window at pointer '''
    (x, y) = DISPLAY.get_pointer()[1:3]
    for info in SCREENSHOT_WINDOW_INFO:
        if info.x <= x <= info.x + info.width and info.y <= y <= info.y + info.height:
            return info

def get_screenshot_pixbuf(fullscreen=True):
    ''' save snapshot to file with filetype. '''
    #root_window = gtk.gdk.get_default_root_window() 
    root_window = GDK_SCREEN.get_root_window()
    if not fullscreen:
        info = get_window_info_at_pointer()
        (x, y, width, height) = (info.x, info.y, info.width, info.height)
    else:
        (x, y, width, height, depth) = root_window.get_geometry() 
    
    pixbuf = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, False, 8, width, height)
    pixbuf.get_from_drawable(root_window, root_window.get_colormap(), x, y, 0, 0, width, height)
    return pixbuf

# 多屏幕
def get_display(index):
    ''' get the index display '''
    if index >= DISPLAY_NUM:
        return
    global DISPLAY
    global SCREEN_NUM
    DISPLAY = gtk.gdk.display_manager_get().list_displays()[index]
    SCREEN_NUM = DISPLAY.get_n_screens()

def get_wnck_screen(index):
    '''get the index screen'''
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

#def find_window_by_property(xlibWindow, atom=WM_STATE):
    #''' find Window by property '''
    #result = xlibWindow.query_tree().children
    #if not result:
        #return None
    #else:
        #for children in result:
            #status = children.get_property(atom, WM_HINTS, 0, 0)
            #if status:
                #child = children
            #else:
                #child = find_window_by_property(children, atom)
        #return child

#def get_client_window(target):
    #''' Enumerate clientWindow '''
    ## 枚举所有窗口
    #status = target.get_property(WM_STATE, WM_HINTS, 0, 0)
    #if status:
        #return target
    #client = find_window_by_property(target)
    #if client:
        #return client
    #return target

#def filter_window():
    #''' without other window'''
    #windowList = []
    #for xlibWindow in enum_xlib_window():
        #if xlibWindow.get_property(WM_DESKTOP, WM_HINTS, 0, 0):
            #windowList.append(xlibWindow)
        #else:
            #if find_window_by_property(xlibWindow, WM_DESKTOP):
                #windowList.append(xlibWindow)
    #return windowList

#def get_xlib_pointer_window():
    #''' grab pointer window '''
    ## 获取鼠标指针当前的窗口
    #return ROOT_WINDOW.query_pointer().child

#def get_xlib_focus_window():
    #''' grab focus window'''
    #return disp.get_input_focus().focus

#def get_window_coord(xlibWindow):
    #''' covert xlibWindow's coord'''
    ## 获取窗口坐标
    #clientWindow = get_client_window(xlibWindow)
    #if xlibWindow != clientWindow:
        ##print "xwindow:", xlibWindow.get_geometry()
        ##print "client window:", clientWindow.get_geometry()
        ##print ""
        #x = xlibWindow.get_geometry().x + clientWindow.get_geometry().x
        #y = xlibWindow.get_geometry().y + clientWindow.get_geometry().y - 30
        #width = clientWindow.get_geometry().width
        #height = clientWindow.get_geometry().height + 30
    #else:
        #x = xlibWindow.get_geometry().x
        #y = xlibWindow.get_geometry().y
        #width = xlibWindow.get_geometry().width
        #height = xlibWindow.get_geometry().height
    #return (x, y, width, height)

#def get_pointer_window_coord():
    #''' get current Focus Window's Coord '''
    #return get_window_coord(get_xlib_pointer_window())

#def get_focus_window_coord():
    #focusWindow = get_xlib_focus_window()
    ##(x, y, width, height) = get_window_coord(focusWindow)
    #return get_window_coord(focusWindow)

#def enum_xlib_window():
    #''' enumerate child window of ROOT_WINDOW'''
    #return ROOT_WINDOW.query_tree().children

#def xwindow_to_gwindow(xlibWindow):
    #''' convert Xlib's window to Gtk's window '''
    #return gtk.gdk.window_foreign_new(xlibWindow.id)

#def get_usertime_window():
    #'''Usertime Window  '''
    #usertimeWindow = {}
    #for eachWindow in enum_xlib_window():
        #sequence_number = eachWindow.get_geometry().sequence_number
        #usertimeWindow[sequence_number] = eachWindow
    #return sorted(usertimeWindow.iteritems(), key=lambda k: k[0], reverse=True)

#def enum_gtk_window():
    #'''  enumerate gtkWindow from xlibWindow '''
    #gtkWindowList = []
    #for eachWindow in enum_xlib_window():
        #gtkWindowList.append(xwindow_to_gwindow(eachWindow))
    #return gtkWindowList

#def get_window_title(xlibWindow):
    #''' get window title'''
    #clientWindow = get_client_window(xlibWindow)
    #if clientWindow != xlibWindeow:
        #return clientWindow.get_wm_name()
    #return xlibWindow.get_wm_name()

