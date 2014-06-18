#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2011 Deepin, Inc.
#               2011 Wang Yong
#
# Author:     Wang Yong <lazycat.manatee@gmail.com>
#             Zhang Cheng <zhangcheng@linuxdeepin.com>
#             Hou ShaoHui <houshaohui@linuxdeepin.com>
#             Long Changjin <admin@longchangjin.cn>

# Maintainer: Wang Yong <lazycat.manatee@gmail.com>
#             Zhang Cheng <zhangcheng@linuxdeepin.com>
#             Hou Shaohui <houshaohui@linuxdeepin.com>
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

from bus import SCROT_BUS
from action import *
from draw import *
from constant import *
from window import *
from nls import _
from widget import RootWindow, RightMenu 
from toolbar import Colorbar, Toolbar
from deepin_utils.file import get_parent_dir
from notify_dbus import notify
import dss

import pygtk
import subprocess
import config

pygtk.require('2.0')
import gtk


class DeepinScreenshot(object):
    ''' Main Screenshot. '''
    def __init__(self):
        '''Init Main screenshot.'''
        # Init.
        self.action = ACTION_WINDOW         # current action status
        # the windows in this workspace coordinate info
        self.screenshot_window_info = get_screenshot_window_info()
        #print "window info:", self.screenshot_window_info
        self.monitor_x, self.monitor_y, self.width, self.height = get_current_monitor_info()
        #self.width = SCREEN_WIDTH           # this monitor width
        #self.height = SCREEN_HEIGHT         # this monitor height
        #self.monitor_x = SCREEN_X           # this monitor source point's x coordinate
        #self.monitor_y = SCREEN_Y           # this monitor source point's y coordinate
        # the screenshot area's x, y, width, height
        self.x = self.y = self.rect_width = self.rect_height = 0

        self.save_op_index = SAVE_OP_AUTO   # current operation when the save button clicked

        #self.buttonToggle = None
        self.drag_position = None
        self.last_drag_position = None
        self.dragStartX = self.dragStartY = self.dragStartOffsetX = self.dragStartOffsetY = 0
        self.textDragOffsetX = self.textDragOffsetY = 0
        
        self.drag_flag = False              # a flag if the selected area can be dragged
        self.show_toolbar_flag = False      # a flag if the toolbar has shown
        self.show_colorbar_flag = False     # a flag if the colorbar has shown
        self.show_text_window_flag = False  # a flag if the text_window has shown
        self.text_drag_flag = False         # a flag if the text_window can be dragged
        self.text_modify_flag = False       # a flag if the text has been modified
        self.draw_text_layout_flag = False  # a flag if the text layout will be drawn
        self.share_to_flag = False          # a flag if the screenshot will be shared
        self.window_flag = True             # a flag if has not selected area or window

        self.is_subprocess = config.OPTION_SUB
        self.saveFiletype = 'png'
        self.saveFilename = config.OPTION_FILE
        
        # make sure the toolbar in this monitor
        self.toolbarOffsetX = self.monitor_x + 10
        self.toolbarOffsetY = self.monitor_y + 10
        #self.toolbarOffsetX = 10
        #self.toolbarOffsetY = 10
        #self.toolbar_height = 50
        
        self.action_size = ACTION_SIZE_SMALL    # the draw action's line width
        self.action_color = "#FF0000"           # the draw action's color
        self.font_name = "Sans"                 # the fontname of text to draw
        self.font_size = 12                     # the fontsize of text to draw
        
        # Init action list.
        self.current_action = None          # current drawing action
        self.action_list = []               # a list of actions have created
        self.current_text_action = None     # current drawing text action
        self.text_action_list = []          # a list of text actions have created
        self.text_action_info = {}          # the created text actions' info

        # Get desktop background.
        # a gtk.gdk.Pixbuf of the desktop_background
        self.desktop_background = self.get_desktop_snapshot()
        # a string containing the pixel data of the pixbuf
        self.desktop_background_pixels= self.desktop_background.get_pixels()
        # the number of the pixbuf channels.
        self.desktop_background_n_channels = self.desktop_background.get_n_channels()
        # the number of bytes between rows.
        self.desktop_background_rowstride = self.desktop_background.get_rowstride()
        
        # Init window.
        self.window = RootWindow(self)
        
        # Init toolbar window.
        self.toolbar = Toolbar(self.window.window, self)
        
        # Init color window.
        self.colorbar = Colorbar(self.window.window, self)

        # right button press menu
        self.right_menu = RightMenu(self)
        # Show.
        self.window.show()
        self.window.set_cursor(ACTION_WINDOW)
        dss.hide()

    def set_action_type(self, action_type):
        '''
        Set action type
        @param action_type: one of ACTION Type Constants 
        '''
        self.action = action_type    
        self.current_action = None
    
    def save_snapshot(self, filename=None, filetype='png', clip_flag=False):
        '''
        Save snapshot.
        @param filename: the filename to save, a string type
        @param filetype: the filetype to save, a string type. Default is 'png'
        @param clip_flag: a flag if copy the snapshot to clipboard. Default is False
        '''
        failed_flag = False
        tipContent = ""
        parent_dir = get_parent_dir(__file__, 1)
        # Save snapshot.
        if self.rect_width == 0 or self.rect_height == 0:
            tipContent = _("The width or height of selected area cannot be 0")
            failed_flag = True
        else:
            self.window.finish_flag = True
            surface = self.make_pic_file(
                self.desktop_background.subpixbuf(*self.get_rectangel_in_monitor()))
            # Save to file
            if filename:
                tipContent = "%s '%s'" % (_("Picture has been saved to file"), filename)
                try:
                    surface.write_to_png(filename)
                    SCROT_BUS.emit_finish(1, filename)
                    # copy to clipboard
                    if clip_flag:
                        pixbuf = gtk.gdk.pixbuf_new_from_file(filename)
                        clipboard = gtk.Clipboard(selection="CLIPBOARD")
                        clipboard.set_image(pixbuf)
                        clipboard.store()
                        #tipContent +=  _("Picture has been saved to clipboard")
                        #try:
                            #cmd = ('python2', '%s/%s' % (parent_dir, 'tipswindow.py'), _("Picture has been saved to clipboard"), '1')
                            #subprocess.Popen(cmd)
                        #except OSError:    
                            #cmd = ('python', '%s/%s' % (parent_dir, 'tipswindow.py'), _("Picture has been saved to clipboard"), '1')
                            #subprocess.Popen(cmd)
                        #notify("Deepin Screenshot", 0, summary=_("DSnapshot"), body=tipContent)
                        
                except Exception, e:
                    tipContent = "%s:%s" % (_("Failed to save the picture"), str(e))
            # Save snapshot to clipboard
            else:
                import StringIO
                fp = StringIO.StringIO()
                surface.write_to_png(fp)
                contents = fp.getvalue()
                fp.close()
                loader = gtk.gdk.PixbufLoader("png")
                loader.write(contents, len(contents))
                pixbuf = loader.get_pixbuf()
                loader.close()

                clipboard = gtk.Clipboard(selection="CLIPBOARD")
                if pixbuf:
                    clipboard.set_image(pixbuf)
                clipboard.store()
                tipContent += _("Picture has been saved to clipboard")

        # Exit
        self.window.destroy_all()
        if self.share_to_flag and not failed_flag:
            # share window
            win_x = self.monitor_x + (self.width / 2) - 300
            win_y = self.monitor_y + (self.height/ 2) - 200
            try:
                cmd = ('python2', '%s/%s' % (parent_dir, 'share.py'), filename, str(win_x), str(win_y))
                subprocess.Popen(cmd)
            except OSError:    
                cmd = ('python', '%s/%s' % (parent_dir, 'share.py'), filename, str(win_x), str(win_y))
                subprocess.Popen(cmd)
        
        # tipWindow
        #try:
            #cmd = ('python2', '%s/%s' % (parent_dir, 'tipswindow.py'), tipContent)
            #subprocess.Popen(cmd)
        #except OSError:    
            #cmd = ('python', '%s/%s' % (parent_dir, 'tipswindow.py'), tipContent)
            #subprocess.Popen(cmd)
        notify("Deepin Screenshot", 0, summary=_("DScreenshot"), body=tipContent)
        if config.OPTION_ICON:
            notify("Deepin Screenshot", 0, summary=_("DScreenshot"),
                   body=_("Next time you can just press Ctrl+Alt+A to start."))

    def make_pic_file(self, pixbuf):
        '''
        use cairo to make a picture file
        @param pixbuf: gtk.gdk.Pixbuf
        @return: a cairo.ImageSurface object
        '''
        surface = cairo.ImageSurface(cairo.FORMAT_RGB24, pixbuf.get_width(), pixbuf.get_height())
        cr = cairo.Context(surface)
        gdkcr = gtk.gdk.CairoContext(cr)
        gdkcr.set_source_pixbuf(pixbuf, 0, 0)
        gdkcr.paint()

        for action in self.action_list:
            if action is not None:
                action.start_x -= self.x - self.monitor_x
                action.start_y -= self.y - self.monitor_y
                if not isinstance(action, (TextAction)):
                    action.end_x -= self.x - self.monitor_x
                    action.end_y -= self.y - self.monitor_y
                if isinstance(action, (LineAction)):
                    for track in action.track:
                        track[0] -= self.x - self.monitor_x
                        track[1] -= self.y - self.monitor_y
                action.expose(cr)
        
        # Draw Text Action list.
        for each in self.text_action_list:
            if each is not None:
                each.expose(cr)
        return surface
    
    def save_to_tmp_file(self):
        if self.rect_width > 0 and self.rect_height > 0:
            from tempfile import mkstemp
            import os
            tmp = mkstemp(".tmp", "deepin-screenshot")
            os.close(tmp[0])
            filename = tmp[1]
            self.window.finish_flag = True
            surface = self.make_pic_file(
                self.desktop_background.subpixbuf(*self.get_rectangel_in_monitor()))
            surface.write_to_png(filename)
            SCROT_BUS.emit_finish(1, filename)
        gtk.main_quit()
        return filename

    def parse_barcode(self):
        filename = self.save_to_tmp_file()
        import os
        from debarcode import debarcode
        print filename
        print debarcode(filename)
        os.remove(filename)

    def get_desktop_snapshot(self):
        '''
        Get desktop snapshot.
        @return: a gtk.gdk.Pixbuf object
        '''
        return get_screenshot_pixbuf()
        
    def undo(self, widget=None):
        '''
        Undo the last action.
        '''
        if self.show_text_window_flag:
            self.window.hide_text_window()
        if self.current_text_action:
            self.current_text_action = None

        if self.action_list:        # undo the previous action
            tempAction = self.action_list.pop()
            if tempAction.get_action_type() == ACTION_TEXT:
                self.text_action_list.pop()
                if tempAction in self.text_action_info:
                    del self.text_action_info[tempAction]
        else:       # back to select area
            self.window.set_cursor(ACTION_WINDOW)
            self.window.magnifier = None
            self.action = ACTION_WINDOW
            self.x = self.y = self.rect_width = self.rect_height = 0
            self.window_flag = True
            self.drag_flag = False
            if self.show_colorbar_flag:
                self.toolbar.set_all_inactive()
            self.window.hide_toolbar()
            self.window.hide_colorbar()
        self.window.refresh()
        
    def get_rectangel(self):
        '''
        get select rectangle
        @return: a tuple contain the selected area coordinate.
        '''
        return (int(self.x), int(self.y), int(self.rect_width), int(self.rect_height))
    
    def get_rectangel_in_monitor(self):
        '''
        get select rectangle in the monitor
        @return: a tuple contain the selected area coordinate in this monitor.
        '''
        return (int(self.x-self.monitor_x), int(self.y-self.monitor_y),
                int(self.rect_width), int(self.rect_height))
    
    def get_monitor_info(self):
        '''
        get monitor info
        @return: a tuple contain this monitor coordinate.
        '''
        return (self.monitor_x, self.monitor_y, self.width, self.height)


def main():
    ''' main function '''
    gtk.gdk.threads_init()
    DeepinScreenshot()
    gtk.main()

if __name__ == '__main__':
    main()
