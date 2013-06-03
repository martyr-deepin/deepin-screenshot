#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2011 Deepin, Inc.
#               2011 Wang Yong
#
# Author:     Wang Yong <lazycat.manatee@gmail.com>
# Maintainer: Wang Yong <lazycat.manatee@gmail.com>
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

import gtk
import pygtk
import pangocairo
import os
import sys
import time
from subprocess import Popen,PIPE

pygtk.require('2.0')

def is_collide_rect((cx, cy), (x, y, w, h)):
    '''
    Whether coordinate collide with rectangle.
    @param (cx, cy): the coordinate which will to judge
    @param (x, y, w, h): the rectangle geometry
    @return: True if the coordinate inside the rectangle, otherwise False
    '''
    return (x <= cx <= x + w and y <= cy <= y + h)

def is_in_rect((cx, cy), (x, y, w, h)):
    '''
    Whether coordinate in rectangle.
    @param (cx, cy): the coordinate which will to judge
    @param (x, y, w, h): the rectangle geometry
    @return: True if the coordinate inside the rectangle, otherwise False
    '''
    return (x < cx < x + w and y < cy < y + h)

def set_default_cursor(widget):
    '''
    Set default cursor.
    @param widget: a gtk.Widget
    '''
    widget.window.set_cursor(None)
    return False

def set_cursor(widget, cursor):
    '''
    Set cursor.
    @param widget: a gtk.Widget
    @param cursor: a gtk.gdk.Cursor 
    '''
    widget.window.set_cursor(cursor)
    return False

def get_screen_size():
    '''
    Get screen size.
    @return: a tuple containing width and height
    '''
    return gtk.gdk.get_default_root_window().get_size()

def get_font_families():
    '''Get all font families in system.'''
    fontmap = pangocairo.cairo_font_map_get_default()
    return map(lambda f: f.get_name(), fontmap.list_families())

def modifyBackground(widget, color):
    ''' modify widget background'''
    widget.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse(color))

def gdkColorToString(gdkcolor):
    '''gdkColor to string '''
    return "#%0.2x%0.2x%0.2x" % (gdkcolor.red / 256, gdkcolor.green / 256, gdkcolor.blue / 256)
     
def encode(text):
    return unicode(text, sys.getfilesystemencoding())

def get_coord_rgb(screenshot, x, y):
    '''
    get coordinate's pixel.
    @param screenshot: a Screenshot object
    @param x: the X coordinate of point
    @param y: the Y coordinate of point
    @return: a list containing the point pixel's rgb info
    '''
    rowstride = screenshot.desktop_background_rowstride
    n_channels = screenshot.desktop_background_n_channels
    pixels = screenshot.desktop_background_pixels
    pos = int(y * rowstride + x * n_channels)
    i = 0
    pix_color = []
    while i < n_channels:
        pix_color.append(ord(pixels[pos+i]))
        i += 1
    pix_color = map(ord, (pixels[pos], pixels[pos+1], pixels[pos+2]))
    #img = screenshot.desktop_background_img
    #pix_color = img.getpixel((x, y))
    return pix_color[0:3]

def make_menu_item(name, callback, data=None):
    item = gtk.MenuItem(name)
    item.connect("activate", callback, data)
    item.show()
    return item

def get_format_time():
    '''
    @return: current time for format
    '''
    #return time.strftime("%M%S", time.localtime())
    return time.strftime("%Y%m%d%H%M%S", time.localtime())

def moveWindow(widget, event, window):
    ''' Move Window.'''
    window.begin_move_drag(
        event.button,
        int(event.x_root),
        int(event.y_root),
        event.time)

def get_pictures_dir():
    '''
    get user pictures dir.
    @return: current user's own pictures dir, a string type
    '''
    picturesDir = os.path.expanduser("~/Pictures")
    try:
        p = Popen(["xdg-user-dir", "PICTURES"], stdout=PIPE)
    except OSError:    
        if not os.path.exists(picturesDir):
            os.mkdir(picturesDir)
        return picturesDir
    else:
        picturesPath = p.communicate()[0].strip()
        if p.returncode == 0 and picturesPath and picturesPath != os.path.expanduser("~"):
            if not os.path.exists(picturesPath):
                os.mkdir(picturesPath)
            return picturesPath
                
        else:
            if not os.path.exists(picturesDir):
                os.mkdir(picturesDir)
            return picturesDir

def parser_path(filepath):
    '''
    parser filepath
    @param filepath: the file being parser
    @return: a tuple containing filename and filetype
    '''
    filename, ext = os.path.splitext(filepath)
    if ext == ".bmp":
        return (filename + ".bmp", "bmp")
    elif ext in [".jpeg", ".jpg"]:
        return (filename + ".jpeg", "jpeg")
    else:
        return (filename + ".png", "png")
