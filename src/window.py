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

from Xlib import X, display, Xutil, Xcursorfont
import gtk
from  collections import namedtuple

(screenWidth, screenHeight) = gtk.gdk.get_default_root_window().get_size()
disp = display.Display()
rootWindow = disp.screen().root
WM_HINTS = disp.intern_atom("WM_HINTS", True)
WM_STATE = disp.intern_atom("WM_STATE", True)
WM_DESKTOP  = disp.intern_atom("_NET_WM_DESKTOP", True)
 
def findWindowByProperty(xlibWindow, atom=WM_STATE):
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
                child = findWindowByProperty(children, atom)
        return child

def getClientWindow(target):
    ''' Enumerate clientWindow '''
    status = target.get_property(WM_STATE, WM_HINTS, 0, 0)
    if status:
        return target
    client = findWindowByProperty(target)
    if client:
        return client
    return target

def filterWindow():
    ''' without other window'''
    windowList = []
    for xlibWindow in enumXlibWindow():
        if xlibWindow.get_property(WM_DESKTOP, WM_HINTS, 0, 0):
            windowList.append(xlibWindow)
        else:
             if findWindowByProperty(xlibWindow, WM_DESKTOP):
                 windowList.append(xlibWindow)
    return windowList

def getXlibPointerWindow():
    ''' grab pointer window '''
    return rootWindow.query_pointer().child

def getXlibFocusWindow():
    ''' grab focus window'''
    return disp.get_input_focus().focus

def getWindowCoord(xlibWindow):
    ''' covert xlibWindow's coord'''
    clientWindow = getClientWindow(xlibWindow)
    if xlibWindow != clientWindow:
        x = xlibWindow.get_geometry().x + clientWindow.get_geometry().x
        y = xlibWindow.get_geometry().y + clientWindow.get_geometry().y - 26
        width =  clientWindow.get_geometry().width
        height = clientWindow.get_geometry().height + 26
    else:
        x = xlibWindow.get_geometry().x
        y = xlibWindow.get_geometry().y
        width = xlibWindow.get_geometry().width
        height = xlibWindow.get_geometry().height
    return (x, y, width, height)

def getPointerWindowCoord():
    ''' get current Focus Window's Coord '''
    return getWindowCoord(getXlibPointerWindow())

def getFocusWindowCoord():
    focusWindow = getXlibFocusWindow()
    #(x, y, width, height) = getWindowCoord(focusWindow)
    return getWindowCoord(focusWindow)

def enumXlibWindow():
    ''' enumerate child window of rootWindow'''
    return rootWindow.query_tree().children

def xlibWindowToGtkWindow(xlibWindow):
    ''' convert Xlib's window to Gtk's window '''
    return gtk.gdk.window_foreign_new(xlibWindow.id)

def getUsertimeWindow():
    '''Usertime Window  '''
    usertimeWindow = {}
    for eachWindow in enumXlibWindow():
       sequence_number = eachWindow.get_geometry().sequence_number
       usertimeWindow[sequence_number] = eachWindow
    return sorted(usertimeWindow.iteritems(), key=lambda k: k[0], reverse=True)

def enumGtkWindow():
    '''  enumerate gtkWindow from xlibWindow '''
    gtkWindowList = []
    for eachWindow in enumXlibWindow():
        gtkWindowList.append(xlibWindowToGtkWindow(eachWindow))
    return gtkWindowList

def getWindowTitle(xlibWindow):
    ''' get window title'''
    clientWindow = getClientWindow(xlibWindow)
    if clientWindow != xlibWindeow:
        return clientWindow.get_wm_name()
    return xlibWindow.get_wm_name()

def convertCoord(x, y, width, height):
    ''' cut out overlop the screen'''
    xWidth = x + width
    yHeight = y + height
       
    if x < 0 and y > 0 and  y < yHeight < screenHeight:
        return (0, y, width+x, height)
    
    if x < 0 and yHeight > screenHeight:
        return (0, y, width+x, height - (yHeight - screenHeight))
    
    if xWidth > screenWidth and yHeight > screenHeight:
        return (x, y, width - (xWidth - screenWidth), height - (yHeight - screenHeight))
    
    if  x > 0 and x < xWidth < screenWidth and yHeight > screenHeight:
        return (x, y, width, height - (yHeight - screenHeight))
    
    if xWidth > screenWidth and y > 0 and y < yHeight < screenHeight:
        return (x, y, width - (xWidth - screenWidth), height)
    
    if x < 0 and y < 0:
        return (0, 0, xWidth, yHeight)
    
    if x > 0 and x < xWidth < screenWidth and y < 0:
        return (x, 0, width, yHeight)
    
    if x > 0 and xWidth > screenWidth and y < 0:
        return (x, 0, width - (xWidth - screenWidth), yHeight) 
    return (x, y, width, height)

def getScrotWindowInfo():
    ''' return (x, y, width, height) '''
    coordInfo = namedtuple('coord', 'x y width height')
    scrotWindowInfo = []
    scrotWindowInfo.append(coordInfo(0, 0, screenWidth, screenHeight))
    for eachWindow in filterWindow():
        (x, y, width, height) = getWindowCoord(eachWindow)
        scrotWindowInfo.append(coordInfo(*convertCoord(x, y, width, height)))
    return scrotWindowInfo

def getScrotPixbuf(fullscreen=True):
    ''' save snapshot to file with filetype. '''
    rootWindow = gtk.gdk.get_default_root_window() 
    if not fullscreen:
        (x, y, width, height) = convertCoord(*getWindowCoord(getXlibPointerWindow()))
    else:
        (x, y, width, height, depth) = rootWindow.get_geometry() 
    
    pixbuf = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, False, 8, width, height)
    pixbuf.get_from_drawable(rootWindow, rootWindow.get_colormap(), x, y, 0, 0, width, height)
    return pixbuf
