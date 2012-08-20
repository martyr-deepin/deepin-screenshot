#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2011 Deepin, Inc.
#               2011 Wang Yong
#
# Author:     Wang Yong <lazycat.manatee@gmail.com>
#             Zhang Cheng <zhangcheng@linuxdeepin.com>
#             Hou ShaoHui <houshaohui@linuxdeepin.com>

# Maintainer: Wang Yong <lazycat.manatee@gmail.com>
#             Zhang Cheng <zhangcheng@linuxdeepin.com>
#             Hou Shaohui <houshaohui@linuxdeepin.com>
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

from action import *
#from utils import *
#from math import *
from draw import *
from constant import *
#from keymap import *
from window import *
from lang import __
#from Xlib import X
from widget import RootWindow, TextWindow
from toolbar import Colorbar, Toolbar

import time
import pygtk
import subprocess
#import Image

pygtk.require('2.0')
import gtk


class DeepinScreenshot():
    '''Main screenshot.'''
    def __init__(self, save_file=""):
        '''Init Main screenshot.'''
        # Init.
        self.dis = DISPLAY

        self.action = ACTION_WINDOW
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT
        self.x = self.y = self.rect_width = self.rect_height = 0
        self.buttonToggle = None
        
        self.drag_position = None
        self.last_drag_position = None
        self.dragStartX = self.dragStartY = self.dragStartOffsetX = self.dragStartOffsetY = 0
        
        self.drag_flag = False
        self.show_toolbar_flag = False
        self.show_colorbar_flag = False 
        self.show_text_window_flag = False
        self.text_drag_flag = False
        self.text_modify_flag = False
        self.draw_text_layout_flag = False
        self.textDragOffsetX = self.textDragOffsetY = 0
        self.saveFiletype = 'png'
        self.saveFilename = save_file
        
        self.toolbarOffsetX = 10
        self.toolbarOffsetY = 10
        #self.toolbar_height = 50
        
        self.action_size = 2
        self.action_color = "#FF0000"
        self.font_name = "Sans 10"
        
        # default window 
        #self.screenshot_window_info = get_screenshot_window_info()
        self.screenshot_window_info = SCREENSHOT_WINDOW_INFO
        #print self.screenshot_window_info
        self.window_flag = True
        
        # Init action list.
        self.current_action = None
        self.action_list = []
        self.current_text_action = None
        self.text_action_list = []
        self.text_action_info = {}

        # Get desktop background.
        self.desktop_background = self.get_desktop_snapshot()
        self.desktop_background_pixels= self.desktop_background.get_pixels()
        self.desktop_background_n_channels = self.desktop_background.get_n_channels()
        self.desktop_background_rowstride = self.desktop_background.get_rowstride()
        #self.desktop_background_img = Image.fromstring("RGB", (self.width, self.height),
            #self.desktop_background_pixels, "raw", "RGB")
        
        # Init window.
        self.window = RootWindow(self)
        
        # Init toolbar window.
        self.toolbar = Toolbar(self.window.window, self)
        
        # Init text window.
        self.text_window = TextWindow(self.window.window, self)
        
        # Init color window.
        self.colorbar = Colorbar(self.window.window, self)

        # Init text window
        self.text_window = TextWindow(self.window.window, self)
        # Show.
        self.window.show()
        self.window.set_cursor(ACTION_WINDOW)

    def set_action_type(self, aType):         # 设置操作类型
        '''Set action. type'''
        self.action = aType    
        self.current_action = None
    
    def save_snapshot(self, widget=None, filename=None, filetype='png'):
        '''Save snapshot.'''
        # Save snapshot.
        if self.rect_width == 0 or self.rect_height == 0:
            tipContent = __("Tip area width or heigth cannot be 0")
        else:
            self.window.finish_flag = True
            #self.window.refresh()
            #pixmap = self.window.draw_area.get_snapshot(gtk.gdk.Rectangle(int(self.x), int(self.y), int(self.rect_width), int(self.rect_height)))
            #print self.x, self.y, self.rect_width, self.rect_height, pixmap.get_size()
            #pixbuf = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, False, 8, int(self.rect_width), int(self.rect_height))
            #pixbuf.get_from_drawable(pixmap, pixmap.get_colormap(), 0, 0, 0, 0, int(self.rect_width), int(self.rect_height))

            surface = self.make_pic_file(self.desktop_background.subpixbuf(int(self.x), int(self.y), int(self.rect_width), int(self.rect_height)), filename)
            if filename == None:
                # Save snapshot to clipboard if filename is None.
                import StringIO
                fp = StringIO.StringIO()
                surface.write_to_png(fp)
                contents = fp.getvalue()
                fp.close()
                loader = gtk.gdk.PixbufLoader()
                loader.write(contents, len(contents))
                pixbuf = loader.get_pixbuf()
                loader.close()

                #pixbuf = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, False, 8, int(self.rect_width), int(self.rect_height))
                #pixbuf.get_from_drawable(self.window.draw_area.get_window(), self.window.draw_area.get_window().get_colormap(),
                    #int(self.x), int(self.y), 0, 0, int(self.rect_width), int(self.rect_height))
                clipboard = gtk.clipboard_get()
                clipboard.clear()
                clipboard.set_image(pixbuf)
                tipContent = __("Tip save to clipboard")
            else:
                # Otherwise save to local file.
                tipContent = __("Tip save to file")
                #self.make_pic_file(self.desktop_background.subpixbuf(int(self.x), int(self.y), int(self.rect_width), int(self.rect_height)), filename)
                surface.write_to_png(filename)
                #pixbuf.save(filename, 'png')
            
        # Exit
        self.window.quit()
        
        # tipWindow
        cmd = ('python', 'tipswindow.py', tipContent)
        subprocess.Popen(cmd)

    def make_pic_file(self, pixbuf, filename):
        ''' use cairo make a picture file '''
        surface = cairo.ImageSurface(cairo.FORMAT_RGB24, pixbuf.get_width(), pixbuf.get_height())
        cr = cairo.Context(surface)
        gdkcr = gtk.gdk.CairoContext(cr)
        gdkcr.set_source_pixbuf(pixbuf, 0, 0)
        gdkcr.paint()

        for action in self.action_list:
            if action is not None:
                action.start_x -= self.x
                action.start_y -= self.y
                if not isinstance(action, (TextAction)):
                    action.end_x -= self.x
                    action.end_y -= self.y
                if isinstance(action, (LineAction)):
                    for track in action.track:
                        track[0] -= self.x
                        track[1] -= self.y
                action.expose(cr)
        
        # Draw Text Action list.
        for each in self.text_action_list:
            if each is not None:
                each.expose(cr)
        return surface
        #surface.write_to_png(filename)

        
    def get_desktop_snapshot(self):
        '''Get desktop snapshot.'''
        return get_screenshot_pixbuf()
        
    def setCursor(self, position):
        '''Set cursor.'''
        #print "in cusor position:", position
        if position == DRAG_INSIDE:         # TODO 
            setCursor(self.window, gtk.gdk.FLEUR)
        elif position == DRAG_OUTSIDE:
            setCursor(self.window, gtk.gdk.TOP_LEFT_ARROW)
        elif position == DRAG_TOP_LEFT_CORNER:
            self.window.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.TOP_LEFT_CORNER))
        elif position == DRAG_TOP_RIGHT_CORNER:
            setCursor(self.window, gtk.gdk.TOP_RIGHT_CORNER)
        elif position == DRAG_BOTTOM_LEFT_CORNER:
            setCursor(self.window, gtk.gdk.BOTTOM_LEFT_CORNER)
        elif position == DRAG_BOTTOM_RIGHT_CORNER:
            setCursor(self.window, gtk.gdk.BOTTOM_RIGHT_CORNER)
        elif position == DRAG_TOP_SIDE:
            setCursor(self.window, gtk.gdk.TOP_SIDE)
        elif position == DRAG_BOTTOM_SIDE:
            setCursor(self.window, gtk.gdk.BOTTOM_SIDE)
        elif position == DRAG_LEFT_SIDE:
            setCursor(self.window, gtk.gdk.LEFT_SIDE)
        elif position == DRAG_RIGHT_SIDE:
            setCursor(self.window, gtk.gdk.RIGHT_SIDE)
        
    def undo(self, widget=None):
        '''Undo'''
        if self.show_text_window_flag:
           self.window.hide_text_window()
        if self.current_text_action:
            self.current_text_action = None

        if self.action_list:        # undo the last action
            tempAction = self.action_list.pop()
            if tempAction.get_action_type() == ACTION_TEXT:
                self.text_action_list.pop()
                del self.text_action_info[tempAction]
        else:       # back to select area
            self.window.set_cursor(ACTION_WINDOW)
            self.action = ACTION_WINDOW
            self.x = self.y = self.rect_width = self.rect_height = 0
            self.window_flag = True
            self.drag_flag = False
            if self.show_colorbar_flag:
                self.toolbar.set_all_inactive()
            self.window.hide_toolbar()
            self.window.hide_colorbar()
        self.window.refresh()
        
    def getCurrentCoord(self, widget):
        '''get Current Coord '''
        (self.currentX, self.currentY) = widget.window.get_pointer()[:2] 
    
def main(name=""):
    ''' main function '''
    gtk.gdk.threads_init()
    DeepinScreenshot(name)
    gtk.main()

if __name__ == '__main__':
    main()
