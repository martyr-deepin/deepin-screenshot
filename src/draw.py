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

from math import *
from theme import *
from utils import *
import sys
from constant import DEFAULT_FONT
import cairo
import gtk
import pygtk
import glib
from window import screenWidth, screenHeight

pygtk.require('2.0')

def drawPixbuf(cr, pixbuf, x=0, y=0):
    '''Draw pixbuf.'''
    if pixbuf != None:
        cr.set_source_pixbuf(pixbuf, x, y)
        cr.paint()
        
def colorHexToCairo(color):
    """ 
    Convert a html (hex) RGB value to cairo color. 
     
    @type color: html color string 
    @param color: The color to convert. 
    @return: A color in cairo format. 
    """ 
    if color[0] == '#': 
        color = color[1:] 
    (r, g, b) = (int(color[:2], 16), 
                    int(color[2:4], 16),  
                    int(color[4:], 16)) 
    return colorRGBToCairo((r, g, b)) 

def colorRGBToCairo(color): 
    """ 
    Convert a 8 bit RGB value to cairo color. 
     
    @type color: a triple of integers between 0 and 255 
    @param color: The color to convert. 
    @return: A color in cairo format. 
    """ 
    return (color[0] / 255.0, color[1] / 255.0, color[2] / 255.0) 

def drawSimpleButton(widget, img, helpText = None):
    '''Draw simple button.'''
    pixbuf = appTheme.getDynamicPixbuf(img + "_normal.png").getPixbuf()
    widget.set_size_request(pixbuf.get_width(), pixbuf.get_height())
    widget.connect("expose-event", lambda w, e: simpleButtonOnExpose(w, e, img))
    
    # simpleButtonSetBackground(widget, img)
    if helpText != None:
        setHelpTooltip(widget, helpText)

def simpleButtonOnExpose(widget, event, img):
    '''Expose function to replace event box's image.'''
    if widget.state == gtk.STATE_NORMAL:
        pixbuf = appTheme.getDynamicPixbuf(img + "_normal.png").getPixbuf()
    elif widget.state == gtk.STATE_PRELIGHT:
        pixbuf = appTheme.getDynamicPixbuf(img + "_hover.png").getPixbuf()
    elif widget.state == gtk.STATE_ACTIVE:
        pixbuf = appTheme.getDynamicPixbuf(img + "_press.png").getPixbuf()
    
    cr = widget.window.cairo_create()
    drawPixbuf(cr, pixbuf, 
               widget.allocation.x,
               widget.allocation.y)

    if widget.get_child() != None:
        widget.propagate_expose(widget.get_child(), event)

    return True

def drawSizeButton(widget, img, index, getIndex):
    '''Draw sizeButton'''
    pixbuf = appTheme.getDynamicPixbuf(img + ".png").getPixbuf()
    widget.set_size_request(pixbuf.get_width(), pixbuf.get_height())
    
    widget.connect("expose-event", lambda w, e: SizeButtonOnExpose(w, e, img, index, getIndex))

def SizeButtonOnExpose(widget, event, img, index, getIndex):
    '''Expose function to replace event box's image.'''
    if widget.state == gtk.STATE_NORMAL:
        if getIndex() == index:
            pixbuf = appTheme.getDynamicPixbuf(img + "_press.png").getPixbuf()
        else:
            pixbuf = appTheme.getDynamicPixbuf(img + ".png").getPixbuf()
    elif widget.state == gtk.STATE_PRELIGHT:
        pixbuf = appTheme.getDynamicPixbuf(img + "_hover.png").getPixbuf()
    elif widget.state == gtk.STATE_ACTIVE:
        pixbuf = appTheme.getDynamicPixbuf(img + "_press.png").getPixbuf()
        
    
    cr = widget.window.cairo_create()
    drawPixbuf(cr, pixbuf, 
               widget.allocation.x,
               widget.allocation.y)

    if widget.get_child() != None:
        widget.propagate_expose(widget.get_child(), event)

    return True

def drawColorButton(widget, img, helpText = None):
    '''Draw simple button.'''
    pixbuf = appTheme.getDynamicPixbuf(img + ".png").getPixbuf()
    widget.set_size_request(pixbuf.get_width(), pixbuf.get_height())
    
    # simpleButtonSetBackground(widget, img)
    widget.connect("expose-event", lambda w, e: simpleColorOnExpose(w, e, img))
    if helpText != None:
        setHelpTooltip(widget, helpText)

def simpleColorOnExpose(widget, event, img):
    '''Expose function to replace event box's image.'''
    if widget.state == gtk.STATE_NORMAL:
        pixbuf = appTheme.getDynamicPixbuf(img + ".png").getPixbuf()
    elif widget.state == gtk.STATE_PRELIGHT:
        pixbuf = appTheme.getDynamicPixbuf(img + "_hover.png").getPixbuf()
    elif widget.state == gtk.STATE_ACTIVE:
        pixbuf = appTheme.getDynamicPixbuf(img + "_hover.png").getPixbuf()
    
    cr = widget.window.cairo_create()
    drawPixbuf(cr, pixbuf, 
               widget.allocation.x,
               widget.allocation.y)

    if widget.get_child() != None:
        widget.propagate_expose(widget.get_child(), event)

    return True

def drawSeparator(widget, img):
    '''draw separator'''
    pixbuf = appTheme.getDynamicPixbuf(img + ".png").getPixbuf()
    widget.set_size_request(pixbuf.get_width(), pixbuf.get_height())
    
    # simpleButtonSetBackground(widget, img)
    widget.connect("expose-event", lambda w, e: SeparatorOnExpose(w, e, img))

def SeparatorOnExpose(widget, event, img):
    '''Expose function to replace event box's image.'''
    pixbuf = appTheme.getDynamicPixbuf(img + ".png").getPixbuf()

    
    cr = widget.window.cairo_create()
    drawPixbuf(cr, pixbuf, 
               widget.allocation.x,
               widget.allocation.y)

    return True

def drawEllipse(cr, ex, ey, ew, eh, color, size):
    '''Draw ellipse'''
    cr.new_path()
    cr.save()
    cr.translate(ex, ey)
    cr.scale(ew / 2.0, eh / 2.0)
    cr.arc(0.0, 0.0, 1.0, 0.0, 2 * pi)
    cr.restore()
    cr.set_source_rgb(*colorHexToCairo(color))
    cr.set_line_width(size)
    cr.stroke()
    

def drawArrow(cr, (sx, sy), (ex, ey), color, size):
    '''Draw arrow.'''
    # Init.
    arrowSize = 10              # in pixel
    arrowAngle = 10             # in degree
    
    # Draw arrow body.
    lineWidth = fabs(sx - ex)
    lineHeight = fabs(sy - ey)
    lineSide = sqrt(pow(lineWidth, 2) + pow(lineHeight, 2))
    offsetSide = arrowSize * sin(arrowAngle)
    if lineSide == 0:
        offsetX = offsetY = 0
    else:
        offsetX = offsetSide / lineSide * lineWidth
        offsetY = offsetSide / lineSide * lineHeight
    
    if ex >= sx:
        offsetX = -offsetX
    if ey >= sy:
        offsetY = -offsetY
        
    cr.move_to(sx, sy)
    cr.line_to(ex - offsetX, ey - offsetY)
    cr.set_source_rgb(*colorHexToCairo(color))
    cr.set_line_width(size)
    cr.stroke()
    
    # Draw arrow head.
    angle = atan2(ey - sy, ex - sx) + pi
    x2 = ex - arrowSize * cos(angle - arrowAngle)
    y2 = ey - arrowSize * sin(angle - arrowAngle)

    x1 = ex - arrowSize * cos(angle + arrowAngle)
    y1 = ey - arrowSize * sin(angle + arrowAngle)
    
    cr.move_to(ex, ey)
    cr.line_to(x1, y1)
    cr.line_to(x2, y2)
    cr.fill()

def updateShape(widget, allocation, radius):
    '''Update shape.'''
    if allocation.width > 0 and allocation.height > 0:
        # Init.
        w, h = allocation.width, allocation.height
        bitmap = gtk.gdk.Pixmap(None, w, h, 1)
        cr = bitmap.cairo_create()
        
        # Clear the bitmap
        cr.set_source_rgb(0.0, 0.0, 0.0)
        cr.set_operator(cairo.OPERATOR_CLEAR)
        cr.paint()
        
        # Draw our shape into the bitmap using cairo
        cr.set_source_rgb(1.0, 1.0, 1.0)
        cr.set_operator(cairo.OPERATOR_SOURCE)
        drawRoundRectangle(cr, 0, 0, w, h, radius)
        cr.fill()
        
        widget.shape_combine_mask(bitmap, 0, 0)

def drawRoundRectangle(cr, x, y, width, height, r):
    '''Draw round rectangle.'''
    cr.move_to(x + r, y)
    cr.line_to(x + width - r, y)

    cr.move_to(x + width, y + r)
    cr.line_to(x + width, y + height - r)

    cr.move_to(x + width - r, y + height)
    cr.line_to(x + r, y + height)

    cr.move_to(x, y + height - r)
    cr.line_to(x, y + r)

    cr.arc(x + r, y + r, r, pi, 3 * pi / 2.0)
    cr.arc(x + width - r, y + r, r, 3 * pi / 2, 2 * pi)
    cr.arc(x + width - r, y + height - r, r, 0, pi / 2)
    cr.arc(x + r, y + height - r, r, pi / 2, pi)

def exposeBackground(widget, event, dPixbuf):
    '''Expose background.'''
    cr = widget.window.cairo_create()
    rect = widget.allocation

    drawPixbuf(cr, dPixbuf.getPixbuf().scale_simple(rect.width, rect.height, gtk.gdk.INTERP_BILINEAR), rect.x, rect.y)
    
    if widget.get_child() != None:
        widget.propagate_expose(widget.get_child(), event)

    return True

def drawRoundTextRectangle(cr, x, y, width, height, r, Text, alpha=0.8):
    ''' draw Round Text Rectangle''' 
    cr.set_source_rgba(0.14, 0.13, 0.15, alpha)
    cr.move_to(x+r, y)
    cr.line_to(x+width-r,y)
        
    cr.move_to(x+width, y+r)
    cr.line_to(x+width, y+height - r)
        
    cr.move_to(x+width-r,y+height)
    cr.line_to(x+r, y+height)
        
    cr.move_to(x, y+height-r)
    cr.line_to(x, y+r)
    cr.arc(x+r, y+r, r, pi, 3*pi / 2)
    cr.arc(x+width-r,y+r,r, 3*pi / 2, 2*pi)
    cr.arc(x+width-r, y+height-r, r, 2*pi, pi / 2)
    cr.arc(x+r, y+height-r, r, pi / 2, pi)    
    cr.fill()
        
    drawFont(cr, Text, 14.0, "#FFFFFF", x + width / 12.0, y + height / 1.5)

    

def drawFont(cr, content, fontSize, fontColor, x, y):
    '''Draw font.'''
    if DEFAULT_FONT in getFontFamilies():
        cr.select_font_face(DEFAULT_FONT,
                            cairo.FONT_SLANT_NORMAL, 
                            cairo.FONT_WEIGHT_NORMAL)
    cr.set_source_rgb(*colorHexToCairo(fontColor))
    cr.set_font_size(fontSize)
    cr.move_to(x, y)
    cr.show_text(content)


def setPixbufCursor(widget, cursorName):
    pixbuf = appTheme.getDynamicPixbuf(cursorName).getPixbuf()
    display = widget.window.get_display()
    widget.window.set_cursor(gtk.gdk.Cursor(display, pixbuf, 0, 0))


def drawMagnifier(cr, widget, x, y, sizeContent, tipContent = "", rgbContent = "RGB:(255,255,255)"):
    ''' draw Magnifier'''
    
    pixbufWidth = 30
    pixbufHeight = 20
    
    if screenHeight - y < 168:
        offsetY = -34
    else:
        offsetY = 8
    if screenWidth - x < 142:
        offsetX = -33
    else:
        offsetX = 3

    pixbuf = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, False, 8, pixbufWidth, pixbufHeight)
    pixbuf.get_from_drawable(widget.get_window(), widget.get_window().get_colormap(),
            int(fabs(x - pixbufWidth / 2)), int(fabs(y - pixbufHeight / 2)),
            0, 0,
            pixbufWidth, pixbufHeight)
    
    
    #set zoom scale and translate
    cr.save()
    cr.translate(0 - 3 * x, 0 - 3 * y)
    cr.scale(4.0, 4.0)
    
    cr.set_source_rgba(0.0, 0.0, 0.0, 0.8)
    cr.rectangle(x + offsetX - 1, y + offsetY - 1, pixbufWidth + 2, pixbufHeight + 14)
    cr.fill()
    
    #draw magnifier
    cr.set_line_width(1)
    cr.set_source_rgb(1, 1, 1)
    #cr.transform(matrix)
    cr.rectangle(x + offsetX, y + offsetY, pixbufWidth, pixbufHeight)
    cr.stroke_preserve()
    cr.set_source_pixbuf(pixbuf, x + offsetX, y + offsetY)
    cr.fill()
    
    #draw Hline
    cr.set_line_width(1.2)
    cr.set_source_rgba(0, 0.7, 1.0, 0.5)
    cr.move_to(x + offsetX , y + offsetY + pixbufHeight / 2)
    cr.line_to(x + offsetX + pixbufWidth, y + offsetY + pixbufHeight / 2)
    cr.stroke()
    
    #draw Vline
    cr.move_to(x + offsetX + pixbufWidth / 2, y + offsetY)
    cr.line_to(x + offsetX + pixbufWidth / 2, y + pixbufHeight + offsetY)
    cr.stroke()
    
    
    drawFont(cr, sizeContent, 3.0, "#FFFFFF", x + offsetX, y + offsetY + pixbufHeight + 4)
    drawFont(cr, rgbContent, 3.0, "#FFFFFF", x + offsetX, y + offsetY + pixbufHeight + 7.5)
    drawFont(cr, tipContent, 3.0, "#FFFFFF", x + offsetX, y + offsetY + pixbufHeight + 11)
    cr.restore()

def drawAlphaRectangle(cr, x, y, width, height):
    ''' draw alpha Rectangle '''
    cr.set_source_rgba(0.18, 0.62, 0.18, 0.6)
    cr.rectangle(x, y, width, height)
    cr.stroke_preserve()
    #cr.stroke()
    cr.set_source_rgba(0, 0.7, 1.0, 0.4)
    cr.fill()
    
def drawTitlebar(widget, name):
    ''' draw title bar '''
    widget.set_size_request(-1,
                             appTheme.getDynamicPixbuf('%s_bg_middle.png' % name).getPixbuf().get_height())
    widget.connect('expose-event', 
                   lambda w, e: drawTitlebarOnExpose(
                       w, e,
                       appTheme.getDynamicPixbuf('%s_bg_left.png' % name),
                       appTheme.getDynamicPixbuf('%s_bg_middle.png' % name),
                       appTheme.getDynamicPixbuf('%s_bg_right.png' % name)))

def drawTitlebarOnExpose(widget, event, bgLeftDPixbuf,
                         bgMiddleDPixbuf, bgRightDPixbuf):
    ''' draw titlebar'''
    bgLeftPixbuf = bgLeftDPixbuf.getPixbuf()
    bgMiddlePixbuf = bgMiddleDPixbuf.getPixbuf()
    bgRightPixbuf = bgRightDPixbuf.getPixbuf()
    
    rect = widget.allocation
    
    # Get cairo object
    cr = widget.window.cairo_create()
    
    # Draw background
    mOffsetX = rect.x + bgLeftPixbuf.get_width()
    mWidth =  rect.width - bgLeftPixbuf.get_width() - bgRightPixbuf.get_width()
    rOffsetX = mOffsetX + mWidth
    bgLeftPixbuf = bgLeftPixbuf.scale_simple(bgLeftPixbuf.get_width(), rect.height, gtk.gdk.INTERP_BILINEAR)
    bgRightPixbuf = bgRightPixbuf.scale_simple(bgRightPixbuf.get_width(), rect.height, gtk.gdk.INTERP_BILINEAR)
    drawPixbuf(cr, bgLeftPixbuf, rect.x, rect.y)
    bmPixbuf = bgMiddlePixbuf.scale_simple(mWidth, rect.height, gtk.gdk.INTERP_BILINEAR)
    drawPixbuf(cr, bmPixbuf, mOffsetX, rect.y)
    drawPixbuf(cr, bgRightPixbuf, rOffsetX, rect.y)

    if widget.get_child() != None:
        widget.propagate_expose(widget.get_child(), event)
    
    return True


def drawButton(widget, iconPrefix, scaleX=False):
    '''draw button '''
    buttonSetBackground(widget, scaleX, False,
                        appTheme.getDynamicPixbuf("%s_normal.png" % iconPrefix),
                        appTheme.getDynamicPixbuf("%s_hover.png" % iconPrefix),
                        appTheme.getDynamicPixbuf("%s_press.png" % iconPrefix)
                        )

def buttonSetBackground(widget, scaleX, scaleY, normalDPixbuf, hoverDPixbuf, pressDPixbuf):
    ''' set event box's background. '''
    if scaleX:
        Width = -1
    else:
        Width = normalDPixbuf.getPixbuf().get_width()
    
    if scaleY:
        Height = -1
    else:
        Height = normalDPixbuf.getPixbuf().get_width()
        
    
    widget.set_size_request(Width, Height)
    widget.connect('expose-event', lambda w, e: buttonOnExpose(
            w, e,
            scaleX, scaleY,
            normalDPixbuf, hoverDPixbuf, pressDPixbuf))

def buttonOnExpose(widget, event, scaleX, scaleY, normalDPixbuf, hoverDPixbuf, pressDPixbuf):
    ''' Expose function to replace event box's image. '''
    if widget.state == gtk.STATE_NORMAL:
        image = normalDPixbuf.getPixbuf()
    elif widget.state == gtk.STATE_PRELIGHT:
        image = hoverDPixbuf.getPixbuf()
    elif widget.state == gtk.STATE_ACTIVE:
        image = pressDPixbuf.getPixbuf()
        
    if scaleX:
        imageWidth = widget.allocation.width
    else:
        imageWidth = image.get_width()
    
    if scaleY:
        imageHeight = widget.allocation.height
    else:
        imageHeight = image.get_height()
        
    
    pixbuf = image.scale_simple(imageWidth, imageHeight, gtk.gdk.INTERP_BILINEAR)
    
    cr = widget.window.cairo_create()
    drawPixbuf(cr, pixbuf, widget.allocation.x, widget.allocation.y)
    
    if widget.get_child() != None:
        widget.propagate_expose(widget.get_child(), event)
    
    return True 

    
    
