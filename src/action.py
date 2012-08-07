
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
        self.startX = self.endX = self.startY = self.endY = None
        self.track = []
        
    def startDraw(self, (sx, sy)):
        '''Start draw.'''
        self.startX = sx
        self.startY = sy
        
    def endDraw(self, (ex, ey), (rx, ry, rw, rh)):
        '''End draw.'''
        self.endX = min((max(ex, rx)), rx + rw)
        self.endY = min((max(ey, ry)), ry + rh)
    
class RectangleAction(Action):
    '''Rectangle action.'''
	
    def __init__(self, aType, size, color):
        '''Rectangle action.'''
        Action.__init__(self, aType, size, color)
        
    def drawing(self, (ex, ey), (rx, ry, rw, rh)):
        '''Drawing.'''
        self.endX = min((max(ex, rx)), rx + rw)
        self.endY = min((max(ey, ry)), ry + rh)
        
    def expose(self, cr):
        '''Expose.'''
        cr.set_source_rgb(*colorHexToCairo(self.color))
        cr.set_line_width(self.size)
        cr.rectangle(self.startX, self.startY, (self.endX - self.startX), (self.endY - self.startY))
        cr.stroke()
   
    def getActionType(self):
        ''' get action type.'''
        return ACTION_RECTANGLE

class EllipseAction(Action):
    '''Ellipse action.'''
	
    def __init__(self, aType, size, color):
        '''Ellipse action.'''
        Action.__init__(self, aType, size, color)
        
    def drawing(self, (ex, ey), (rx, ry, rw, rh)):
        '''Drawing.'''
        self.endX = min((max(ex, rx)), rx + rw)
        self.endY = min((max(ey, ry)), ry + rh)
        
    def expose(self, cr):
        '''Expose.'''
        ew = self.endX - self.startX
        eh = self.endY - self.startY
        if ew != 0 and eh != 0:
            drawEllipse(cr, self.startX + ew / 2, self.startY + eh / 2, fabs(ew), fabs(eh), 
                        self.color, self.size)

    def getActionType(self):
        ''' get action type.'''
        return ACTION_ELLIPSE            
   
class ArrowAction(Action):
    '''Arrow action.'''
	
    def __init__(self, aType, size, color):
        '''Arrow action.'''
        Action.__init__(self, aType, size, color)
        
    def drawing(self, (ex, ey), (rx, ry, rw, rh)):
        '''Drawing.'''
        self.endX = min((max(ex, rx)), rx + rw)
        self.endY = min((max(ey, ry)), ry + rh)
        
    def expose(self, cr):
        '''Expose.'''
        #print self.endX, self.endY
        drawArrow(cr, (self.startX, self.startY), (self.endX, self.endY),
                  self.color, self.size)
    def getActionType(self):
        ''' get action type.'''
        return ACTION_ARROW

class LineAction(Action):
    '''Line action.'''
	
    def __init__(self, aType, size, color):
        '''Line action.'''
        Action.__init__(self, aType, size, color)
        
    def drawing(self, (ex, ey), (rx, ry, rw, rh)):
        '''Drawing.'''
        newX = min((max(ex, rx)), rx + rw)
        newY = min((max(ey, ry)), ry + rh)
        self.endX = newX
        self.endY = newY
        if self.track == []:        
            self.track.append((newX, newY))
        elif self.track[-1] != (newX, newY):
            self.track.append((newX, newY))
        
    def expose(self, cr):
        '''Expose.'''
        if len(self.track) > 0:
            cr.set_line_width(self.size)
            cr.move_to(*self.track[0])
            for (px, py) in self.track[1:]:
                cr.line_to(px, py)

            cr.set_source_rgb(*colorHexToCairo(self.color))
            cr.stroke()
            
    def getActionType(self):
        ''' get action type.'''
        return ACTION_LINE            

class TextAction(Action):
    '''Text action.'''
	
    def __init__(self, aType, size, color, fontname, content):
        '''Text action.'''
        Action.__init__(self, aType, size, color)
        self.content = content
        self.fontname = fontname
        
    def expose(self, cr):
        '''Expose.'''

        cr.move_to(self.startX, self.startY)
        context = pangocairo.CairoContext(cr)
        self.layout = context.create_layout()
        self.layout.set_font_description(pango.FontDescription(self.fontname))
        self.layout.set_text(self.content)
        cr.set_source_rgb(*colorHexToCairo(self.color))
        context.update_layout(self.layout)
        context.show_layout(self.layout)
 
        
    def updateCoord(self, x, y):
        "update arguments"
        self.startX = x
        self.startY = y
        
        
    def update(self, color, fontname, content):
        self.color = color
        self.fontname = fontname 
        self.content = content

    def getLayoutInfo(self):
        ''' get layout (x, y, width, height) '''
        return (self.startX, self.startY, 
                self.layout.get_size()[0] / pango.SCALE,
                self.layout.get_size()[1] / pango.SCALE)

    def getContent(self):
        '''get Content '''
        return self.content

    def getColor(self):
        ''' get color '''
        return self.color

    def getFontname(self):
        return self.fontname
    
    def getActionType(self):
        ''' get action type.'''
        return ACTION_TEXT    
