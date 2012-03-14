#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2011 Deepin, Inc.
#               2011 Wang Yong
#
# Author:     Wang Yong <lazycat.manatee@gmail.com>
#             hou  shaohui <houshaohui@linuxdeepin.com>
#
# Maintainer: hou shaohui <houshaohui@linuxdeepin.com>
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
from draw import *
import sys

class tipWindow():
    ''' tip window'''
    def __init__(self, content):
        ''' Init tip Window'''
        screenWidth, screenHeight = gtk.gdk.get_default_root_window().get_size()
        self.delta = 0.01
        self.alpha = 1
        self.paddingX = 10
        self.content = content
        
        self.tipWindow = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.tipWindow.set_keep_above(True)
        self.tipWindow.set_size_request(-1, -1)
        self.tipWindow.set_decorated(False)
        self.tipWindow.set_accept_focus(False)
        self.tipWindow.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse("black"))
        self.tipWindow.set_icon_from_file("../theme/logo/deepin-scrot.ico")
        self.tipWindow.set_opacity(1)
        self.tipWindow.set_skip_taskbar_hint(True)
        self.tipWindow.set_skip_pager_hint(True)
        self.tipWindow.move(screenWidth - 250 , 34)
        self.tipWindow.connect('expose-event', self.tipExpose)
        self.tipWindow.connect("size-allocate", lambda w, a: updateShape(w, a, 4))
        
        # Create tooltips label.
        self.label = gtk.Label()
        self.label.set_markup("<span foreground='#00AEFF' size='12000'>%s</span>" % (content))
        self.label.set_single_line_mode(True) # just one line
        self.align = gtk.Alignment()
        self.align.set(0.5, 0.5, 0, 0)
        self.align.set_padding(5, 5, self.paddingX, self.paddingX)
        self.align.add(self.label)
        self.tipWindow.add(self.align)
        glib.timeout_add(50, lambda : self.timeoutHandler(self.tipWindow))
        self.tipWindow.show_all()
        
        gtk.main()
    
    def tipExpose(self, widget, event, data=None):
        self.alpha -= self.delta
        widget.set_opacity(self.alpha)
        cr = widget.window.cairo_create()
        width, height = widget.window.get_size()
        cr.set_source_rgb(0.14, 0.13, 0.15)
        drawRoundRectangle(cr, 0, 0, width, height, 4)
        cr.fill_preserve()
        cr.stroke()

        if widget.get_child() != None:
            widget.propagate_expose(widget.get_child(), event)
            
        return True
    
    def getAlpha(self):
        return self.alpha
        
    def timeoutHandler(self, widget):
        if self.getAlpha() <= 0:
            gtk.main_quit()
            return False
        widget.queue_draw()
        return True


class countdownWindow():
    '''  show a countdown before taking the shot'''
    def __init__(self, count):
        ''' Init tip Window'''
        screenWidth, screenHeight = gtk.gdk.get_default_root_window().get_size()
        self.count = count
        self.paddingX = 10
        
        self.tipWindow = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.tipWindow.set_skip_taskbar_hint(True)
        self.tipWindow.set_skip_pager_hint(True)
        self.tipWindow.set_keep_above(True)
        self.tipWindow.set_size_request(100, 100)
        self.tipWindow.set_decorated(False)
        self.tipWindow.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse("black"))
        self.tipWindow.set_accept_focus(False)
        self.tipWindow.set_icon_from_file("../theme/logo/deepin-scrot.ico")
        self.tipWindow.set_opacity(0.8)
        self.tipWindow.move(screenWidth - 200 , 34)
        self.tipWindow.connect('expose-event', self.tipExpose)
        self.tipWindow.connect("size-allocate", lambda w, a: updateShape(w, a, 4))
        
        # Create tooltips label.
        self.label = gtk.Label()
        self.label.set_markup("<span foreground='#00AEFF' size='36000'>%d</span>" % (self.count))
        self.label.set_single_line_mode(True) # just one line
        self.align = gtk.Alignment()
        self.align.set(0.5, 0.5, 1.0, 1.0)
        self.align.set_padding(0, 28, self.paddingX, self.paddingX)
        self.align.add(self.label)
        self.tipWindow.add(self.align)
        glib.timeout_add(1000, lambda : self.timeoutHandler(self.tipWindow))
        self.tipWindow.show_all()
        
        gtk.main()
    
    def tipExpose(self, widget, event, data=None):
        self.label.set_markup("<span foreground='#00AEFF' size='36000'>%d</span>" % (self.count))
        cr = widget.window.cairo_create()
        width, height = widget.window.get_size()
        cr.set_source_rgb(0.14, 0.13, 0.15)
        drawRoundRectangle(cr, 0, 0, width, height, 4)
        cr.fill_preserve()
        cr.stroke()

        if widget.get_child() != None:
            widget.propagate_expose(widget.get_child(), event)
            
        return True
        
    def timeoutHandler(self, widget):
        if self.count == 1:
            self.tipWindow.hide_all()
        elif self.count <= 0:
            gtk.main_quit()
            return False   
        else:
            pass
        self.count -= 1
        widget.queue_draw()
        return True
        
if __name__ == '__main__':
    ''' '''
    if len(sys.argv) >= 2:
        tipWindow(sys.argv[1])
    

    
