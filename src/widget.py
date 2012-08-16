#!/usr/bin/python
#-*- coding:utf-8 -*-

# Copyright (C) 2011 ~ 2012 Deepin, Inc.
#               2011 ~ 2012 Long Changjin
# 
# Author:     Long Changjin <admin@longchangjin.cn>
# Maintainer: Long Changjin <admin@longchangjin.cn>
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

from theme import app_theme
from dtk.ui.window import Window
from dtk.ui.entry import Entry 
from dtk.ui.scrolled_window import ScrolledWindow 
from dtk.ui.keymap import get_keyevent_name
from collections import namedtuple
from draw import *
from constant import *
from lang import __
import gtk
import cairo
import utils


Magnifier = namedtuple('Magnifier', 'x y size_content tip rgb')

class RootWindow():
    ''' background window'''
    def __init__(self, screenshot=None):
        self.screenshot = screenshot
        self.__frame_border = 2
        self.__drag_point_radius = 4
        self.__frame_color = (0.0, 0.68, 1.0)

        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_size_request(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.window.fullscreen()
        self.window.set_icon_from_file("../theme/logo/deepin-screenshot.ico")
        self.window.set_keep_above(True)
        #self.window.set_app_paintable(True)

        self.window.add_events(gtk.gdk.KEY_RELEASE_MASK)
        self.window.add_events(gtk.gdk.POINTER_MOTION_MASK)
        self.window.add_events(gtk.gdk.BUTTON_PRESS_MASK)
        self.window.add_events(gtk.gdk.BUTTON_RELEASE_MASK)
        self.window.connect("destroy", self._destroy)
        #self.window.connect("expose-event", lambda w, e: self.getCurrentCoord(w))   # 获取当前坐标
        #self.window.connect("expose-event", self._expose_event)
        self.window.connect("button-press-event", self._button_press_event)
        
        self.window.connect("button-press-event", self._button_double_clicked)
        self.window.connect("button-release-event", self._button_release_event)
        self.window.connect("motion-notify-event", self._motion_notify_event)
        self.window.connect("key-press-event", self._key_press_event)
        #self.window.connect("event", self._window_event)
        
        self.draw_area = gtk.DrawingArea()
        self.draw_area.connect("expose-event", self._draw_expose)
        self.window.add(self.draw_area)
        self.magnifier = None

        # key binding.
        self.hotkey_map = { "Escape": self.window.destroy}
        if self.screenshot:
            self.hotkey_map["Ctrl + s"] = self.screenshot.saveSnapshotToFile
            self.hotkey_map["Return"] = self.screenshot.saveSnapshot
            self.hotkey_map["KP_Enter"] = self.screenshot.saveSnapshot
            self.hotkey_map["Ctrl + z"] = self.screenshot.undo

    def _window_event(self, widget, event):
        ''' window event '''
        print event

    def _draw_expose(self, widget, event):
        ''' draw area expose'''
        cr = widget.window.cairo_create()
        # draw background
        if self.screenshot:
            cr.set_source_pixbuf(self.screenshot.desktop_background, 0, 0)
            cr.paint()
        # draw magnifier
        if self.magnifier:
            self._draw_magnifier(cr)
        # draw mask
        self._draw_mask(cr)
        # draw frame
        if self.screenshot.rect_width:
            self._draw_frame(cr)
            self._draw_drag_point(cr)

    def _expose_event(self, widget, event):
        ''' expose '''
        print "expose"
        if self.screenshot is None:
            return False
    
    def _button_press_event(self, widget, event):
        ''' button press '''
        if self.screenshot is None:
            return
        screen = self.screenshot
        screen.dragFlag = True
        if screen.action == ACTION_WINDOW:
            screen.window_flag = False
        elif screen.action == ACTION_INIT:
            (screen.x, screen.y) = self.get_event_coord(event)
        elif screen.action == ACTION_SELECT:
            # Init drag position.
            screen.dragPosition = screen.getPosition(event)
            
            # Set cursor.
            #screen.setCursor(screen.dragPosition)
            
            # Get drag coord and offset.
            (screen.dragStartX, screen.dragStartY) = self.get_event_coord(event)
            screen.dragStartOffsetX = screen.dragStartX - screen.x
            screen.dragStartOffsetY = screen.dragStartY - screen.y
        elif screen.action == ACTION_RECTANGLE:
            # Just create new action when drag position at inside of select area.
            if screen.getPosition(event) == DRAG_INSIDE:
                screen.currentAction = RectangleAction(ACTION_RECTANGLE, screen.actionSize, screen.actionColor)
                screen.currentAction.start_draw(screen.get_event_coord(event))
        elif screen.action == ACTION_ELLIPSE:
            # Just create new action when drag position at inside of select area.
            if screen.getPosition(event) == DRAG_INSIDE:
                screen.currentAction = EllipseAction(ACTION_ELLIPSE, screen.actionSize, screen.actionColor)
                screen.currentAction.start_draw(self.get_event_coord(event))
        elif screen.action == ACTION_ARROW:
            # Just create new action when drag position at inside of select area.
            if screen.getPosition(event) == DRAG_INSIDE:
                screen.currentAction = ArrowAction(ACTION_ARROW, screen.actionSize, screen.actionColor)
                screen.currentAction.start_draw(self.get_event_coord(event))
        elif screen.action == ACTION_LINE:
            # Just create new action when drag position at inside of select area.
            if screen.getPosition(event) == DRAG_INSIDE:
                screen.currentAction = LineAction(ACTION_LINE, screen.actionSize, screen.actionColor)
                screen.currentAction.start_draw(self.get_event_coord(event))
        elif screen.action == ACTION_TEXT:
            
            if screen.textWindow.get_visible():
                content = screen.getInputText()
                if content != "":
                    if screen.textModifyFlag:
                        screen.currentTextAction.update(screen.actionColor, screen.fontName, content)
                        screen.textModifyFlag = False
                    else:
                        textAction = TextAction(ACTION_TEXT, 15, screen.actionColor, screen.fontName, content)
                        textAction.start_draw(screen.textWindow.get_window().get_origin())
                        screen.textActionList.append(textAction)
                        screen.actionList.append(textAction)
                    screen.hideTextWindow()
                    screen.setAllInactive()
                    
                    self.window.queue_draw()
                else:
                    screen.hideTextWindow()
                    screen.setAllInactive()
            else:
                screen.showTextWindow(self.get_event_coord(event))
        if screen.action in [ACTION_RECTANGLE, ACTION_ELLIPSE, ACTION_ARROW, ACTION_LINE] and screen.showToolbarFlag and screen.y < screen.toolbarY < screen.y + screen.rect_height:
            screen.hideToolbar()
            screen.hideColorbar()

        if screen.currentTextAction and screen.action == None:
            currentX, currentY = screen.get_event_coord(event)
            drawTextX,drawTextY = screen.currentTextAction.get_layout_info()[:2]
            screen.textDragOffsetX = currentX - drawTextX
            screen.textDragOffsetY = currentY - drawTextY
            screen.textDragFlag = True 
    
    def _button_double_clicked(self, widget, event):
        ''' double clicked '''
        if self.screenshot is None:
            return
        pass
    
    def _button_release_event(self, widget, event):
        ''' button release '''
        if self.screenshot is None:
            return
        screen = self.screenshot
        screen.textDragFlag = False
        screen.dragFlag = False
        # print "buttonRelease: %s" % (str(event.get_root_coords()))
        if screen.action == ACTION_WINDOW:
            if screen.rect_width > 5 and screen.rect_height > 5:
                #screen.showToolbar()
                screen.action = ACTION_SELECT
                self.window.queue_draw()
            else:
                screen.window_flag = True
            
        elif screen.action == ACTION_INIT:
            screen.action = ACTION_SELECT
            (ex, ey) = self.get_event_coord(event)
            
            # Adjust value when button release.
            if ex > screen.x:
                screen.rect_width = ex - screen.x
            else:
                screen.rect_width = fabs(ex - screen.x)
                screen.x = ex
                
            if ey > screen.y:
                screen.rect_height = ey - screen.y
            else:
                screen.rect_height = fabs(ey - screen.y)
                screen.y = ey
                
            self.window.queue_draw()
            
            #self.showToolbar()
        elif screen.action == ACTION_SELECT:
            pass
        elif screen.action == ACTION_RECTANGLE:
            if screen.currentAction:
                screen.currentAction.end_draw(screen.getEventCoord(event), (screen.x, screen.y, screen.rect_width, screen.rect_height))
                screen.actionList.append(screen.currentAction)
                screen.currentAction = None
                
                self.window.queue_draw()
        elif screen.action == ACTION_ELLIPSE:
            if screen.currentAction:
                screen.currentAction.end_draw(screen.getEventCoord(event), (screen.x, screen.y, screen.rect_width, screen.rect_height))
                screen.actionList.append(screen.currentAction)
                screen.currentAction = None
                
                self.window.queue_draw()
        elif screen.action == ACTION_ARROW:
            if screen.currentAction:
                screen.currentAction.end_draw(screen.getEventCoord(event), (screen.x, screen.y, screen.rect_width, screen.rect_height))
                screen.actionList.append(screen.currentAction)
                screen.currentAction = None
                
                self.window.queue_draw()
        elif screen.action == ACTION_LINE:
            if screen.currentAction:
                screen.currentAction.end_draw(screen.getEventCoord(event), (screen.x, screen.y, screen.rect_width, screen.rect_height))
                screen.actionList.append(screen.currentAction)
                screen.currentAction = None
                self.window.queue_draw()
        
        if screen.action in [ACTION_RECTANGLE, ACTION_ELLIPSE, ACTION_ARROW, ACTION_LINE, ACTION_TEXT] and not screen.showToolbarFlag and screen.y < screen.toolbarY < screen.y + screen.rect_height:
            screen.adjustToolbar()
            screen.showToolbar()
            screen.adjustColorbar()
            #self.showColorbar()
    
    def _motion_notify_event(self, widget, event):
        ''' motion notify '''
        #self.update_magnifier(event.x, event.y)
        if self.screenshot is None:
            return
        # update magnifier
        screen = self.screenshot
        size = "%d x %d " % (screen.rect_width, screen.rect_height)
        rgb = utils.get_coord_rgb(screen.root, event.x, event.y)
        self.update_magnifier(event.x, event.y, size=size, rgb=str(rgb))

        if screen.dragFlag:   # 能拖动
            # print "motionNotify: %s" % (str(event.get_root_coords()))
            (ex, ey) = self.get_event_coord(event)
            
            if screen.action == ACTION_WINDOW and not screen.window_flag: 
                
                screen.action = ACTION_INIT
                (screen.x, screen.y) = self.get_event_coord(event)
                self.window.queue_draw()
                
            elif screen.action == ACTION_INIT:
                (screen.rect_width, screen.rect_height) = (ex - screen.x, ey - screen.y)
                self.window.queue_draw()
            elif screen.action == ACTION_SELECT:
                if screen.dragPosition == DRAG_INSIDE:
                    screen.x = min(max(ex - screen.dragStartOffsetX, 0), screen.width - screen.rect_width)
                    screen.y = min(max(ey - screen.dragStartOffsetY, 0), screen.height - screen.rect_height)
                elif screen.dragPosition == DRAG_TOP_SIDE:
                    screen.dragFrameTop(ex, ey)
                elif screen.dragPosition == DRAG_BOTTOM_SIDE:
                    screen.dragFrameBottom(ex, ey)
                elif screen.dragPosition == DRAG_LEFT_SIDE:
                    screen.dragFrameLeft(ex, ey)
                elif screen.dragPosition == DRAG_RIGHT_SIDE:
                    screen.dragFrameRight(ex, ey)
                elif screen.dragPosition == DRAG_TOP_LEFT_CORNER:
                    screen.dragFrameTop(ex, ey)
                    screen.dragFrameLeft(ex, ey)
                elif screen.dragPosition == DRAG_TOP_RIGHT_CORNER:
                    screen.dragFrameTop(ex, ey)
                    screen.dragFrameRight(ex, ey)
                elif screen.dragPosition == DRAG_BOTTOM_LEFT_CORNER:
                    screen.dragFrameBottom(ex, ey)
                    screen.dragFrameLeft(ex, ey)
                elif screen.dragPosition == DRAG_BOTTOM_RIGHT_CORNER:
                    screen.dragFrameBottom(ex, ey)
                    screen.dragFrameRight(ex, ey)                      
                self.window.queue_draw()
                
            elif screen.action == ACTION_RECTANGLE and screen.currentAction:
                screen.currentAction.drawing((ex, ey), (screen.x, screen.y, screen.rect_width, screen.rect_height))
                
                self.window.queue_draw()
            elif screen.action == ACTION_ELLIPSE and screen.currentAction:
                screen.currentAction.drawing((ex, ey), (screen.x, screen.y, screen.rect_width, screen.rect_height))
                
                self.window.queue_draw()
            elif screen.action == ACTION_ARROW and screen.currentAction:
                screen.currentAction.drawing((ex, ey), (screen.x, screen.y, screen.rect_width, screen.rect_height))
                
                self.window.queue_draw()
            elif screen.action == ACTION_LINE and screen.currentAction:
                screen.currentAction.drawing((ex, ey), (screen.x, screen.y, screen.rect_width, screen.rect_height))
                
                self.window.queue_draw()
        else:               # 不能拖动
            #if screen.action == ACTION_SELECT:
                #screen.setCursor(screen.getPosition(event))
           
            #elif screen.action == ACTION_WINDOW:
                #setPixbufCursor(screen.window, "start_cursor.png")
            
            #elif screen.action in (ACTION_RECTANGLE, ACTION_ELLIPSE):
                #setCursor(screen.window, gtk.gdk.TCROSS)
            
            #elif screen.action == ACTION_LINE:
                #setCursor(screen.window, gtk.gdk.PENCIL)
            #elif screen.action == ACTION_TEXT:
                #setCursor(screen.window, gtk.gdk.XTERM)
            #else:
                #screen.window.window.set_cursor(None)
                
            if screen.window_flag:
                #screen.hideToolbar()
                (wx, wy) = self.get_event_coord(event)
                #print screen.screenshot_window_info, wx, wy
                for eachCoord in screen.screenshot_window_info:
                    if eachCoord.x < wx < (eachCoord.x + eachCoord.width) and eachCoord.y < wy < (eachCoord.y + eachCoord.height):
                        #print eachCoord
                        screen.x = eachCoord.x
                        screen.y = eachCoord.y
                        screen.rect_width = eachCoord.width
                        screen.rect_height = eachCoord.height
                #print "-"*20
                self.window.queue_draw()
                
        if screen.action == None:
            (tx, ty) = self.get_event_coord(event)       
            if screen.textDragFlag:
                screen.currentTextAction.update_coord(tx - screen.textDragOffsetX, ty - screen.textDragOffsetY)
                screen.drawTextLayoutFlag = True
                self.window.queue_draw()
            else:
                for eachAction, info in screen.textActionInfo.items():
                    if info[0] < tx < info[0]+info[2] and info[1] < ty < info[1]+info[3]:
                        screen.currentTextAction = eachAction
                        
            if screen.currentTextAction:
                drawTextX, drawTextY, drawTextWidth, drawTextHeight = screen.currentTextAction.get_layout_info()
                if drawTextX <= tx <= drawTextX + drawTextWidth and drawTextY <= ty <= drawTextY + drawTextHeight:
                    screen.drawTextLayoutFlag = True
                    #setCursor(self.window, gtk.gdk.FLEUR)
                    self.window.queue_draw()
                else:
                    screen.drawTextLayoutFlag = False    
                    screen.currentTextAction = None
                    self.window.window.set_cursor(None)
                    self.window.queue_draw()
    
    def _key_press_event(self, widget, event):
        ''' key press '''
        if event.is_modifier:
            return
        key = get_keyevent_name(event)
        if key in self.hotkey_map:
            self.hotkey_map[key]()
    
    def _destroy(self, widget):
        ''' window destroy'''
        gtk.main_quit()
        pass
    
    def update_magnifier(self, x, y, size='', tip=__("Tip Drag"), rgb="RGB:(255,255,255)"):
        ''' update magnifier '''
        self.magnifier = Magnifier(x, y, size, tip, rgb)

    def _draw_magnifier(self, cr):
        ''' draw the magnifier'''
        #cr = self._cr
        pixbuf_width = 30
        pixbuf_heigth = 20
        x = self.magnifier.x
        y = self.magnifier.y

        if SCREEN_HEIGHT - y < 168:
            offset_y = -34
        else:
            offset_y = 8
        if SCREEN_WIDTH - x < 142:
            offset_x = -33
        else:
            offset_x = 3

        pixbuf = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, False, 8, pixbuf_width, pixbuf_heigth)
        pixbuf.get_from_drawable(self.window.window, self.window.window.get_colormap(),
            int(fabs(x - pixbuf_width / 2)), int(fabs(y - pixbuf_heigth / 2)),
            0, 0, pixbuf_width, pixbuf_heigth)
        
        #set zoom scale and translate
        cr.save()
        cr.translate(0 - 3 * x, 0 - 3 * y)
        cr.scale(4.0, 4.0)
        
        cr.set_source_rgba(0.0, 0.0, 0.0, 0.8)
        cr.rectangle(x + offset_x - 1, y + offset_y - 1, pixbuf_width + 2, pixbuf_heigth + 14)
        cr.fill()
        
        #draw magnifier
        cr.set_line_width(1)
        cr.set_source_rgb(1, 1, 1)
        #cr.transform(matrix)
        cr.rectangle(x + offset_x, y + offset_y, pixbuf_width, pixbuf_heigth)
        cr.stroke_preserve()
        cr.set_source_pixbuf(pixbuf, x + offset_x, y + offset_y)
        cr.fill()
        
        #draw Hline
        cr.set_line_width(1.2)
        cr.set_source_rgba(0, 0.7, 1.0, 0.5)
        cr.move_to(x + offset_x, y + offset_y + pixbuf_heigth / 2)
        cr.line_to(x + offset_x + pixbuf_width, y + offset_y + pixbuf_heigth / 2)
        cr.stroke()
        
        #draw Vline
        cr.move_to(x + offset_x + pixbuf_width / 2, y + offset_y)
        cr.line_to(x + offset_x + pixbuf_width / 2, y + pixbuf_heigth + offset_y)
        cr.stroke()
        
        drawFont(cr, self.magnifier.size_content, 3.0, "#FFFFFF", x + offset_x, y + offset_y + pixbuf_heigth + 4)
        drawFont(cr, self.magnifier.rgb, 3.0, "#FFFFFF", x + offset_x, y + offset_y + pixbuf_heigth + 7.5)
        drawFont(cr, self.magnifier.tip, 3.0, "#FFFFFF", x + offset_x, y + offset_y + pixbuf_heigth + 11)
        cr.restore()
    
    def refresh(self):
        ''' refresh this window'''
        self.window.queue_draw()

    def _draw_background(self, cr):
        ''' draw background '''
        cr.set_source_pixbuf(self.pix, 0, 0)
        cr.paint()

    def _draw_mask(self, cr):
        '''draw mask'''
        if self.screenshot is None:
            return
        screen = self.screenshot
        #cr = self._cr
        # Adjust value when create selection area.
        if screen.rect_width > 0:
            x = screen.x
            rect_width = screen.rect_width
        else:
            x = screen.x + screen.rect_width
            rect_width = fabs(screen.rect_width)

        if screen.rect_height > 0:
            y = screen.y
            rect_height = screen.rect_height
        else:
            y = screen.y + screen.rect_height
            rect_height = fabs(screen.rect_height)
        
        # Draw top.
        cr.set_source_rgba(0, 0, 0, 0.5)
        cr.rectangle(0, 0, screen.width, y)
        cr.fill()

        # Draw bottom.
        cr.set_source_rgba(0, 0, 0, 0.5)
        cr.rectangle(0, y + rect_height, screen.width, screen.height - y - rect_height)
        cr.fill()

        # Draw left.
        cr.set_source_rgba(0, 0, 0, 0.5)
        cr.rectangle(0, y, x, rect_height)
        cr.fill()

        # Draw right.
        cr.set_source_rgba(0, 0, 0, 0.5)
        cr.rectangle(x + rect_width, y, screen.width - x - rect_width, rect_height)
        cr.fill()

    def _draw_drag_point(self, cr):
        '''Draw drag point.'''
        screen = self.screenshot
        cr.set_source_rgb(*self.__frame_color)
        # Draw left top corner.
        cr.arc(screen.x, screen.y, self.__drag_point_radius, 0, 2 * pi)
        cr.fill()
        # Draw right top corner.
        cr.arc(screen.x + screen.rect_width, screen.y, self.__drag_point_radius, 0, 2 * pi)
        cr.fill()
        # Draw left bottom corner.
        cr.arc(screen.x, screen.y + screen.rect_height, self.__drag_point_radius, 0, 2 * pi)
        cr.fill()
        # Draw right bottom corner.
        cr.arc(screen.x + screen.rect_width, screen.y + screen.rect_height, self.__drag_point_radius, 0, 2 * pi)
        cr.fill()
        # Draw top side.
        cr.arc(screen.x + screen.rect_width / 2, screen.y, self.__drag_point_radius, 0, 2 * pi)
        cr.fill()
        # Draw bottom side.
        cr.arc(screen.x + screen.rect_width / 2, screen.y + screen.rect_height, self.__drag_point_radius, 0, 2 * pi)
        cr.fill()
        # Draw left side.
        cr.arc(screen.x, screen.y + screen.rect_height / 2, self.__drag_point_radius, 0, 2 * pi)
        cr.fill()
        # Draw right side.
        cr.arc(screen.x + screen.rect_width, screen.y + screen.rect_height / 2, self.__drag_point_radius, 0, 2 * pi)
        cr.fill()

    def _draw_frame(self, cr):
        '''Draw frame.'''
        screen = self.screenshot
        cr.set_source_rgb(*self.__frame_color)
        cr.set_line_width(self.__frame_border)
        cr.rectangle(screen.x, screen.y, screen.rect_width, screen.rect_height)
        cr.stroke()

    def get_event_coord(self, event):     # 获取事件的坐标
        '''Get event coord.'''
        (rx, ry) = event.get_root_coords()
        return (int(rx), int(ry))
        
    def show(self):
        '''show'''
        self.window.show_all()
        #self._cr = self.window.window.cairo_create()
        self._cr = self.draw_area.window.cairo_create()
        time.sleep(0.01)

class TextWindow():
    ''' Text Window '''
    def __init__(self, parent=None, screenshot=None):
        self.screenshot = screenshot
        
        self.window = Window(window_type=gtk.WINDOW_TOPLEVEL)
        self.window.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_DIALOG)
        #self.window.connect("size-allocate", lambda w, a: updateShape(w, a, 3))
        self.window.set_decorated(False)
        #self.window.connect("expose-event", lambda w, e: exposeBackground(w, e, appTheme.getDynamicPixbuf("bg.png")))
        self.window.set_keep_above(True)
        self.window.set_resizable(False)
        self.window.set_transient_for(parent)
        self.window.set_size_request(300, 60)
        
        self.window.window_shadow.set(0.5, 0.5, 0, 0)
        self.window.window_shadow.set_padding(10, 10, 10, 10)

        scroll_window = ScrolledWindow()
        #entry = Entry()
        entry= gtk.TextView()           # TODO 输入框控件
        scroll_window.add_with_viewport(entry)
        #scroll_window.add(entry)
        #scroll_window.add_child(entry)
        #scrollWindow.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        #scrollWindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC) 
        entry.set_size_request(300, 60)

        self.window.window_frame.add(scroll_window)
    
    def show(self):
        ''' show window '''
        self.window.show_all()
    
    def hide(self):
        '''hide window'''
        self.window.hide_all()


if __name__ == '__main__':
    RootWindow().show()
    #TextWindow().show()
    gtk.main()
