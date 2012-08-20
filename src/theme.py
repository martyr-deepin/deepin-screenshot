#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2011 Deepin, Inc.
#               2011 Wang Yong
# 
# Author:     Wang Yong <lazycat.manatee@gmail.com>
# Maintainer: Wang Yong <lazycat.manatee@gmail.com>
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

from dtk.ui.init_skin import init_skin
from dtk.ui.utils import get_parent_dir
from constant import *
import os
import gtk

app_theme = init_skin(
    "deepin-screenshot",
    "2.1",
    "01",
    os.path.join(get_parent_dir(__file__, 2), "skin"),
    os.path.join(get_parent_dir(__file__, 2), "theme"))

theme_cursor = {
    DRAG_INSIDE: gtk.gdk.Cursor(gtk.gdk.FLEUR),
    DRAG_OUTSIDE: None,
    DRAG_TOP_LEFT_CORNER: gtk.gdk.Cursor(gtk.gdk.TOP_LEFT_CORNER),
    DRAG_TOP_RIGHT_CORNER: gtk.gdk.Cursor(gtk.gdk.TOP_RIGHT_CORNER),
    DRAG_BOTTOM_LEFT_CORNER: gtk.gdk.Cursor(gtk.gdk.BOTTOM_LEFT_CORNER),
    DRAG_BOTTOM_RIGHT_CORNER: gtk.gdk.Cursor(gtk.gdk.BOTTOM_RIGHT_CORNER),
    DRAG_TOP_SIDE: gtk.gdk.Cursor(gtk.gdk.TOP_SIDE),
    DRAG_BOTTOM_SIDE: gtk.gdk.Cursor(gtk.gdk.BOTTOM_SIDE),
    DRAG_LEFT_SIDE: gtk.gdk.Cursor(gtk.gdk.LEFT_SIDE),
    DRAG_RIGHT_SIDE: gtk.gdk.Cursor(gtk.gdk.RIGHT_SIDE),
    ACTION_INIT: None,
    ACTION_RECTANGLE: gtk.gdk.Cursor(gtk.gdk.TCROSS),
    ACTION_ELLIPSE: gtk.gdk.Cursor(gtk.gdk.TCROSS),
    ACTION_ARROW: None,
    ACTION_LINE: gtk.gdk.Cursor(gtk.gdk.PENCIL),
    ACTION_TEXT: gtk.gdk.Cursor(gtk.gdk.XTERM),
    ACTION_WINDOW: gtk.gdk.Cursor(gtk.gdk.display_get_default(), app_theme.get_pixbuf("start_cursor.png").get_pixbuf(), 0, 0),
    None: None}
theme_cursor['drag'] = theme_cursor[DRAG_INSIDE]

def app_theme_get_pixbuf(filename):
    ''' from file get theme pixbuf '''
    return app_theme.get_pixbuf(filename).get_pixbuf()
