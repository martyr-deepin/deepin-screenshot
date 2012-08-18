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
from Xlib import X

pygtk.require('2.0')

def is_collide_rect((cx, cy), (x, y, w, h)):
    '''Whether coordinate collide with rectangle.'''
    return (x <= cx <= x + w and y <= cy <= y + h)

def is_in_rect((cx, cy), (x, y, w, h)):
    '''Whether coordinate in rectangle.'''
    return (x < cx < x + w and y < cy < y + h)

def set_default_cursor(widget):
    '''Set default cursor.'''
    widget.window.set_cursor(None)
    return False

def set_cursor(widget, cursor):
    '''Set cursor.'''
    widget.window.set_cursor(cursor)
    return False

def get_screen_size():
    '''Get screen size.'''
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

def get_coord_rgb(widget, x, y):
#def get_coord_rgb(pixbuf, width, x, y):
    '''get coordinate's pixel. '''
    #width, height = widget.get_size()
    #colormap = widget.get_window().get_colormap()
    #image = gtk.gdk.Image(gtk.gdk.IMAGE_NORMAL, widget.window.get_visual(), width, height)
    #image.set_colormap(colormap)
    #gdkcolor = colormap.query_color(image.get_pixel(x, y))
    #return (gdkcolor.red / 256, gdkcolor.green / 256, gdkcolor.blue / 256)
    #pix = pixbuf.get_pixels()
    #pos = x * width + y
    #pix_color = (ord(pix[pos]), ord(pix[pos+1]), ord(pix[pos+2]))
    #return pix_color
    img = widget.get_image(x, y, 1, 1, X.ZPixmap, 0xffffffff)
    data = []
    data.append(img.data[2])
    data.append(img.data[1])
    data.append(img.data[0])
    return (tuple(map(ord, data[0:3])))

def make_menu_item(name, callback, data=None):
    item = gtk.MenuItem(name)
    item.connect("activate", callback, data)
    item.show()
    return item

def get_format_time():
    return time.strftime("%M%S", time.localtime())

def moveWindow(widget, event, window):
    ''' Move Window.'''
    window.begin_move_drag(
        event.button,
        int(event.x_root),
        int(event.y_root),
        event.time)

def get_pictures_dir():
    ''' get user pictures dir. '''
    picturesDir = os.path.expanduser("~/Pictures")
    try:
        p = Popen(["xdg-user-dir", "PICTURES"], stdout=PIPE)
    except OSError:    
        return picturesDir
    else:
        picturesPath = p.communicate()[0].strip()
        if p.returncode == 0 and picturesPath and picturesPath != os.path.expanduser("~"):
            return picturesPath
                
        else:
            return picturesDir

def parser_path(filepath):
    filename, ext = os.path.splitext(filepath)
    if ext == ".bmp":
        return (filename + ".bmp", "bmp")
    elif ext in [".jpeg", ".jpg"]:
        return (filename + ".jpeg", "jpeg")
    else:
        return (filename + ".png", "png")
