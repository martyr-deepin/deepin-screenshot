
# -*- coding: utf-8 -*-
#! /usr/bin/env python

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

from math import *
from draw import *
from constant import *
import pango
import pangocairo

class Action:
    '''Action'''
    def __init__(self, aType, size, color):
        '''Init action.'''
        self.type = aType
        self.size = size
        self.color = color
        self.start_x = self.end_x = self.start_y = self.end_y = None
        self.track = []
        
    def start_draw(self, (sx, sy)):
        '''Start draw.'''
        self.end_x = self.start_x = sx
        self.end_y = self.start_y = sy
        
    def end_draw(self, (ex, ey), (rx, ry, rw, rh)):
        '''End draw.'''
        self.end_x = min((max(ex, rx)), rx + rw)
        self.end_y = min((max(ey, ry)), ry + rh)

    def get_action_type(self):
        ''' get action type.'''
        return self.type
    
class RectangleAction(Action):
    '''Rectangle action.'''
    def __init__(self, aType, size, color):
        '''Rectangle action.'''
        Action.__init__(self, aType, size, color)
        if size == ACTION_SIZE_RECTANGLE_ELLIPSE_FILL: self.fill_flag = True
        else: self.fill_flag = False
        
    def drawing(self, (ex, ey), (rx, ry, rw, rh)):
        '''Drawing.'''
        self.end_x = min((max(ex, rx)), rx + rw)
        self.end_y = min((max(ey, ry)), ry + rh)
        
    def expose(self, cr):
        '''Expose.'''
        cr.set_source_rgb(*colorHexToCairo(self.color))
        cr.set_line_width(self.size)
        cr.rectangle(self.start_x, self.start_y, (self.end_x - self.start_x), (self.end_y - self.start_y))
        if self.fill_flag: cr.fill()
        else: cr.stroke()

class EllipseAction(Action):
    '''Ellipse action.'''
    def __init__(self, aType, size, color):
        '''Ellipse action.'''
        Action.__init__(self, aType, size, color)
        if size == ACTION_SIZE_RECTANGLE_ELLIPSE_FILL: self.fill_flag = True
        else: self.fill_flag = False
        
    def drawing(self, (ex, ey), (rx, ry, rw, rh)):
        '''Drawing.'''
        self.end_x = min((max(ex, rx)), rx + rw)
        self.end_y = min((max(ey, ry)), ry + rh)
        
    def expose(self, cr):
        '''Expose.'''
        ew = self.end_x - self.start_x
        eh = self.end_y - self.start_y
        if ew != 0 and eh != 0:
            draw_ellipse(cr, self.start_x + ew / 2, self.start_y + eh / 2,
                fabs(ew), fabs(eh), self.color, self.size, self.fill_flag)

class ArrowAction(Action):
    '''Arrow action.'''
    def __init__(self, aType, size, color):
        '''Arrow action.'''
        Action.__init__(self, aType, size, color)
        
    def drawing(self, (ex, ey), (rx, ry, rw, rh)):
        '''Drawing.'''
        self.end_x = min((max(ex, rx)), rx + rw)
        self.end_y = min((max(ey, ry)), ry + rh)
        
    def expose(self, cr):
        '''Expose.'''
        #print self.end_x, self.end_y
        draw_arrow(cr, (self.start_x, self.start_y), (self.end_x, self.end_y),
            self.color, self.size)

class LineAction(Action):
    '''Line action.'''
    def __init__(self, aType, size, color):
        '''Line action.'''
        Action.__init__(self, aType, size, color)
        
    def drawing(self, (ex, ey), (rx, ry, rw, rh)):
        '''Drawing.'''
        newX = min((max(ex, rx)), rx + rw)
        newY = min((max(ey, ry)), ry + rh)
        self.end_x = newX
        self.end_y = newY
        if self.track == []:        
            self.track.append([newX, newY])
        elif self.track[-1] != [newX, newY]:
            self.track.append([newX, newY])
        
    def expose(self, cr):
        '''Expose.'''
        if len(self.track) > 0:
            cr.set_line_width(self.size)
            cr.move_to(*self.track[0])
            for (px, py) in self.track[1:]:
                cr.line_to(px, py)

            cr.set_source_rgb(*colorHexToCairo(self.color))
            cr.stroke()
            
class TextAction(Action):
    '''Text action.'''
    def __init__(self, aType, size, color, layout):
        '''Text action.'''
        Action.__init__(self, aType, size, color)
        self.layout = layout
        #self.content = self.layout.get_text()
        #self.fontname = fontname
        
    def expose(self, cr):
        '''Expose.'''
        cr.move_to(self.start_x, self.start_y)
        context = pangocairo.CairoContext(cr)

        #self.layout = context.create_layout()
        #self.layout.set_font_description(pango.FontDescription(self.fontname))
        #self.layout.set_text(self.content)

        cr.set_source_rgb(*colorHexToCairo(self.color))
        context.update_layout(self.layout)
        context.show_layout(self.layout)
 
    def update_coord(self, x, y):
        "update arguments"
        self.start_x = x
        self.start_y = y
    
    def set_color(self, color):
        '''set color'''
        self.color = color

    #def set_fontname(self, fontname):
        #'''set fontname'''
        #self.fontname = fontname

    def set_content(self, content):
        '''set content'''
        #self.content = content
        self.layout.set_text(content)
    
    def update(self, color, layout):
        self.set_color(color)
        self.layout = layout

    def get_layout_info(self):
        ''' get layout (x, y, width, height) '''
        return (self.start_x, self.start_y, 
                self.layout.get_size()[0] / pango.SCALE,
                self.layout.get_size()[1] / pango.SCALE)

    def get_content(self):
        '''get Content '''
        return self.layout.get_text()

    def get_color(self):
        ''' get color '''
        return self.color

    def get_font_size(self):
        '''get font size'''
        return self.layout.get_font_description().get_size() / pango.SCALE

    #def get_fontname(self):
        #return self.fontname
    
