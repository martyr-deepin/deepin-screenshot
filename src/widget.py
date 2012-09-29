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

from theme import theme_cursor, app_theme_get_dynamic_pixbuf
from dtk.ui.keymap import get_keyevent_name
from dtk.ui.menu import Menu
from dtk.ui.button import ToggleButton
from collections import namedtuple
from draw import *
from constant import *
from action import TextAction
from nls import _
#from dtk.ui.entry import Entry
from text_view import TextView
import dtk.ui.constant as dtk_constant
import status
import gtk
import pango
import gobject
import threading
import subprocess
import time

DEFAULT_FONT = dtk_constant.DEFAULT_FONT            # default font to draw
DEFAULT_FONT_SIZE = dtk_constant.DEFAULT_FONT_SIZE  # default fontsize to draw

Magnifier = namedtuple('Magnifier', 'x y size_content tip rgb')

class RootWindow():
    ''' root window of the screenshot '''
    def __init__(self, screenshot):
        self.screenshot = screenshot            # a DeepinScreenshot object
        self.frame_border = 2                   # frame border width to draw
        self.drag_point_radius = 4              # the eight drag points' radius
        self.__frame_color = (0.0, 0.68, 1.0)   # frame border color to draw

        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        # move window to current monitor
        self.window.move(self.screenshot.monitor_x, self.screenshot.monitor_y)
        self.window.fullscreen()
        self.window.set_keep_above(True)
        #self.window.set_app_paintable(True)

        self.window.add_events(gtk.gdk.KEY_RELEASE_MASK)
        self.window.add_events(gtk.gdk.POINTER_MOTION_MASK)
        self.window.add_events(gtk.gdk.BUTTON_PRESS_MASK)
        self.window.add_events(gtk.gdk.BUTTON_RELEASE_MASK)
        self.window.connect("destroy", self.quit)
        #self.window.connect("destroy", self.destroy_all)
        self.window.connect("button-press-event", self._button_press_event)
        
        self.window.connect("button-press-event", self._button_double_clicked)
        self.window.connect("button-release-event", self._button_release_event)
        self.window.connect("motion-notify-event", self._motion_notify_event)
        self.window.connect("key-press-event", self._key_press_event)
        
        #self.draw_area = gtk.DrawingArea()
        self.draw_area = gtk.Fixed()
        self.draw_area.connect("expose-event", self._draw_expose)
        self.window.add(self.draw_area)
        self.magnifier = None
        self.finish_flag = False
        
        self._button_pressed_process = status.ButtonPressProcess(screenshot, self)
        self._button_released_process = status.ButtonReleaseProcess(screenshot, self)
        self._button_motion_process = status.MotionProcess(screenshot, self)

        # key binding.
        self.hotkey_map = { "Escape": self.quit}
        if self.screenshot:
            self.hotkey_map["Ctrl + s"] = self._save_to_file
            self.hotkey_map["Return"] = self._key_enter_press
            self.hotkey_map["KP_Enter"] = self._key_enter_press
            self.hotkey_map["Ctrl + z"] = self.screenshot.undo

    def _draw_expose(self, widget, event):
        ''' draw area expose-event callback, drawing background and action'''
        cr = self._cr = widget.window.cairo_create()
        # draw background
        if self.screenshot:
            cr.set_source_pixbuf(self.screenshot.desktop_background, 0, 0)
            cr.paint()
        # Draw action list.
        for action in self.screenshot.action_list:
            if action is not None:
                action.expose(cr)
        # Draw current action.
        if self.screenshot.current_action is not None:
            self.screenshot.current_action.expose(cr)
        if self.finish_flag:
            return True
        # draw mask
        self._draw_mask(cr)
        # toolbar
        if self.screenshot.show_toolbar_flag:
            self.adjust_toolbar()
            self.adjust_colorbar()

        # ACTION_WINDOW draw magnifier and window frame
        if self.magnifier and self.screenshot.action == ACTION_WINDOW:
            self._draw_magnifier(cr)
            self._draw_window_rectangle(cr)
        # action is not ACTION_WINDOW draw frame
        if self.screenshot.action != ACTION_WINDOW:
            self._draw_frame(cr)
            self._draw_drag_point(cr)
            # draw size tip
            if self.screenshot.y - 35 > self.screenshot.monitor_y:  # convert coord
                size_tip_x = self.screenshot.x - self.screenshot.monitor_x + 5
                if size_tip_x + 90 > self.screenshot.width:
                    size_tip_x = self.screenshot.width - 90
                size_tip_y = self.screenshot.y - self.screenshot.monitor_y - 35
                draw_round_text_rectangle(cr, size_tip_x, size_tip_y, 90, 30, 7,
                    '%d x %d' % (fabs(self.screenshot.rect_width), fabs(self.screenshot.rect_height)), 0.7)
            elif self.screenshot.action in [None, ACTION_SELECT, ACTION_WINDOW, ACTION_INIT]:
                size_tip_x = self.screenshot.x - self.screenshot.monitor_x + 5
                if size_tip_x + 90 > self.screenshot.width:
                    size_tip_x = self.screenshot.width - 90
                size_tip_y = self.screenshot.y - self.screenshot.monitor_y + 5
                draw_round_text_rectangle(cr, size_tip_x, size_tip_y, 90, 30, 7,
                    '%d x %d' % (fabs(self.screenshot.rect_width), fabs(self.screenshot.rect_height)), 0.7)
        # update text action info
        for each_text_action in self.screenshot.text_action_list:
            self.screenshot.text_action_info[each_text_action] = each_text_action.get_layout_info()
        # draw current text layout
        if self.screenshot.draw_text_layout_flag and self.screenshot.current_text_action:
            draw_alpha_rectangle(cr, *self.screenshot.current_text_action.get_layout_info())

    def _button_press_event(self, widget, event):
        ''' button press event callback '''
        if self.screenshot is None:
            return
        self._button_pressed_process.update(event)
        self._button_pressed_process.process()
    
    def _button_double_clicked(self, widget, event):
        ''' double clicked '''
        if self.screenshot is None:
            return
        # double click
        (ex, ey) = self.get_event_coord(event)
        if event.button == 1 and event.type == gtk.gdk._2BUTTON_PRESS:
            # edit text, create a new TextWindow
            if self.screenshot.text_drag_flag:
                current_action = self.screenshot.current_text_action
                # don't draw this  text action
                if current_action in self.screenshot.text_action_list:
                    self.screenshot.text_action_list.remove(current_action)
                if current_action in self.screenshot.action_list:
                    self.screenshot.action_list.remove(current_action)
                del self.screenshot.text_action_info[current_action]
                self.screenshot.draw_text_layout_flag = False   # don't draw text layout
                # set action_color as current_action color
                for color_name in self.screenshot.colorbar.color_map:
                    if self.screenshot.colorbar.color_map[color_name] == current_action.get_color():
                        self.screenshot.colorbar._color_button_pressed(color_name)
                        break
                self.show_text_window((current_action.start_x, current_action.start_y))
                self.screenshot.text_window.set_text(current_action.get_content())
                self.screenshot.text_window.set_font_size(current_action.get_font_size())
                self.screenshot.text_window.set_layout(current_action.get_layout())
                self.screenshot.text_window.adjust_size()
                self.screenshot.colorbar.font_spin.set_value(self.screenshot.text_window.get_font_size())
                # set action ACTION_TEXT
                self.screenshot.toolbar.set_button_active("text", True)
                self.screenshot.text_modify_flag = True
                self.refresh()
                self.screenshot.text_window.queue_draw()
            # save snapshot
            if self.screenshot.action == ACTION_SELECT \
               or self.screenshot.action == None \
               and self.screenshot.x < ex < self.screenshot.x + self.screenshot.rect_width \
               and self.screenshot.y < ey < self.screenshot.y + self.screenshot.rect_height:
                #self.screenshot.save_snapshot()
                release_event = gtk.gdk.Event(gtk.gdk.BUTTON_RELEASE)
                release_event.send_event = True
                release_event.button = event.button
                release_event.x = event.x
                release_event.y = event.y
                release_event.x_root = event.x_root
                release_event.y_root = event.y_root
                widget.event(release_event)
                self.screenshot.toolbar.save_operate()
    
    def _button_release_event(self, widget, event):
        ''' button release event callback '''
        if self.screenshot is None:
            return
        self._button_released_process.update(event)
        self._button_released_process.process()
    
    def _motion_notify_event(self, widget, event):
        ''' motion notify event callback '''
        #self.update_magnifier(event.x, event.y)
        if self.screenshot is None:
            return
        self._button_motion_process.update(event)
        self._button_motion_process.process()
    
    def _key_enter_press(self):
        '''enter key press'''
        if self.screenshot.action != ACTION_WINDOW:
            self.screenshot.toolbar.save_operate()
    
    def _key_press_event(self, widget, event):
        ''' key press event callback'''
        if event.is_modifier or self.screenshot.show_text_window_flag:
            return
        key = get_keyevent_name(event)
        if key in self.hotkey_map:
            self.hotkey_map[key]()
    
    def quit(self, widget=None):
        ''' window destroy callback, exit'''
        gtk.main_quit()

    def destroy_all(self, widget=None):
        ''' after save snapshot, destroy all window  '''
        self.window.hide()
        self.screenshot.toolbar.window.destroy()
        self.screenshot.colorbar.window.destroy()
        threading.Thread(target=self.exit_thread).start()

    def exit_thread(self):
        '''wait a little, and exit  '''
        time.sleep(0.5)
        gtk.gdk.threads_enter()
        self.window.destroy()
        gtk.gdk.threads_leave()

    
    def update_magnifier(self, x, y, size='', tip=_("Drag to select area"), rgb="RGB:(255,255,255)"):
        '''
        update magnifier
        @param x: the X coordinate of cursor point
        @param y: the Y coordinate of cursor point
        @param size: the window info at point, a string type
        @param tip: the tips shown, a string type
        @param rgb: the pixel's rgb at point, a string type
        '''
        self.magnifier = Magnifier(x, y, size, tip, rgb)

    def _draw_magnifier(self, cr):
        '''
        draw the magnifier
        @param cr: a gtk.gdk.CairoContext
        '''
        screen_width = self.screenshot.width
        screen_height = self.screenshot.height
        #cr = self._cr
        mag_width = pixbuf_width = 30
        mag_height = pixbuf_height = 20
        x = self.magnifier.x
        y = self.magnifier.y
        position = 0

        # the magnifier offset pos for pointor
        if screen_height - y < 168:
            offset_y = -34
        else:
            offset_y = 8
        if screen_width - x < 142:
            offset_x = -33
        else:
            offset_x = 3

        src_x = x - mag_width / 2
        src_y = y - mag_height / 2
        if src_x < 0:                               # position LEFT
            position |= MAGNIFIER_POS_LEFT
            pixbuf_width += src_x
            src_x = 0
        elif src_x > screen_width - pixbuf_width:   # position RIGHT
            position |= MAGNIFIER_POS_RIGHT
            pixbuf_width = screen_width - src_x
        else:
            src_x = fabs(src_x)                     # position middle
        if src_y < 0:                               # position TOP
            position |= MAGNIFIER_POS_TOP
            pixbuf_height += src_y
            src_y = 0
        elif src_y > screen_height - pixbuf_height:  # position BOTTOM
            position |= MAGNIFIER_POS_BOTTOM
            pixbuf_height = screen_height - src_y
        else:
            src_y = fabs(src_y)                     # position middle
        pixbuf = self.screenshot.desktop_background.subpixbuf(
            int(src_x), int(src_y), int(pixbuf_width), int(pixbuf_height))
        
        origin_x = offset_x + x
        origin_y = offset_y + y
        if position & MAGNIFIER_POS_LEFT:
            origin_x += (mag_width - pixbuf_width)
        if position & MAGNIFIER_POS_TOP:
            origin_y += (mag_height - pixbuf_height)
        #set zoom scale and translate
        cr.save()
        cr.translate(0 - 3 * x, 0 - 3 * y)
        cr.scale(4.0, 4.0)
        
        cr.set_source_rgba(0.0, 0.0, 0.0, 0.8)
        cr.rectangle(x + offset_x - 1, y + offset_y - 1, mag_width + 2, mag_height + 14)
        cr.fill()
        
        #draw magnifier
        cr.set_line_width(1)
        cr.set_source_rgb(1, 1, 1)
        #cr.transform(matrix)
        cr.rectangle(x + offset_x, y + offset_y, mag_width, mag_height)
        cr.stroke_preserve()
        #cr.set_source_pixbuf(pixbuf, x + offset_x, y + offset_y)
        cr.set_source_pixbuf(pixbuf, origin_x, origin_y)
        #cr.set_source_pixbuf(pixbuf.scale_simple(int(pixbuf_width)*4,
            #int(pixbuf_height)*4, gtk.gdk.INTERP_BILINEAR), origin_x, origin_y)
        cr.fill()
        
        #draw Hline
        cr.set_line_width(1.2)
        cr.set_source_rgba(0, 0.7, 1.0, 0.5)
        cr.move_to(x + offset_x, y + offset_y + mag_height / 2)
        cr.line_to(x + offset_x + mag_width, y + offset_y + mag_height / 2)
        cr.stroke()
        
        #draw Vline
        cr.move_to(x + offset_x + mag_width / 2, y + offset_y)
        cr.line_to(x + offset_x + mag_width / 2, y + mag_height + offset_y)
        cr.stroke()
        
        draw_font(cr, self.magnifier.size_content, 3.0, "#FFFFFF", x + offset_x, y + offset_y + mag_height + 4)
        draw_font(cr, self.magnifier.rgb, 3.0, "#FFFFFF", x + offset_x, y + offset_y + mag_height + 7.5)
        draw_font(cr, self.magnifier.tip, 3.0, "#FFFFFF", x + offset_x, y + offset_y + mag_height + 11)
        cr.restore()
    
    def refresh(self):
        ''' refresh this window'''
        if self.screenshot.action_list:
            self.draw_area.queue_draw_area(*self.screenshot.get_rectangel_in_monitor())
        else:
            self.draw_area.queue_draw()

    def _draw_mask(self, cr):
        '''
        draw mask
        @param cr: a gtk.gdk.CairoContext
        '''
        if self.screenshot is None:
            return
        screenshot = self.screenshot
        #cr = self._cr
        # Adjust value when create selection area.
        # convert value in the monitor
        if screenshot.rect_width > 0:
            x = screenshot.x - screenshot.monitor_x
            rect_width = screenshot.rect_width
        else:
            x = screenshot.x - screenshot.monitor_x + screenshot.rect_width
            rect_width = abs(screenshot.rect_width)

        if screenshot.rect_height > 0:
            y = screenshot.y - screenshot.monitor_y
            rect_height = screenshot.rect_height
        else:
            y = screenshot.y - screenshot.monitor_y + screenshot.rect_height
            rect_height = abs(screenshot.rect_height)
        
        # Draw top.
        cr.set_source_rgba(0, 0, 0, 0.5)
        cr.rectangle(0, 0, screenshot.width, y)
        cr.fill()

        # Draw bottom.
        cr.set_source_rgba(0, 0, 0, 0.5)
        cr.rectangle(0, y + rect_height, screenshot.width, screenshot.height - y - rect_height)
        cr.fill()

        # Draw left.
        cr.set_source_rgba(0, 0, 0, 0.5)
        cr.rectangle(0, y, x, rect_height)
        cr.fill()

        # Draw right.
        cr.set_source_rgba(0, 0, 0, 0.5)
        cr.rectangle(x + rect_width, y, screenshot.width - x - rect_width, rect_height)
        cr.fill()

    def _draw_drag_point(self, cr):
        '''
        Draw drag point.
        @param cr: a gtk.gdk.CairoContext
        '''
        screenshot = self.screenshot
        cr.set_source_rgb(*self.__frame_color)
        # convert to coord in this monitor
        (x, y, width, height) = screenshot.get_rectangel_in_monitor()
        # Draw left top corner.
        cr.arc(x, y, self.drag_point_radius, 0, 2 * pi)
        cr.fill()
        # Draw right top corner.
        cr.arc(x + width, y, self.drag_point_radius, 0, 2 * pi)
        cr.fill()
        # Draw left bottom corner.
        cr.arc(x, y + height, self.drag_point_radius, 0, 2 * pi)
        cr.fill()
        # Draw right bottom corner.
        cr.arc(x + width, y + height, self.drag_point_radius, 0, 2 * pi)
        cr.fill()
        # Draw top side.
        cr.arc(x + width / 2, y, self.drag_point_radius, 0, 2 * pi)
        cr.fill()
        # Draw bottom side.
        cr.arc(x + width / 2, y + height, self.drag_point_radius, 0, 2 * pi)
        cr.fill()
        # Draw left side.
        cr.arc(x, y + height / 2, self.drag_point_radius, 0, 2 * pi)
        cr.fill()
        # Draw right side.
        cr.arc(x + width, y + height / 2, self.drag_point_radius, 0, 2 * pi)
        cr.fill()

    def _draw_frame(self, cr):
        '''
        Draw frame.
        @param cr: a gtk.gdk.CairoContext
        '''
        screenshot = self.screenshot
        cr.set_source_rgb(*self.__frame_color)
        cr.set_line_width(self.frame_border)
        #cr.rectangle(screenshot.x, screenshot.y, screenshot.rect_width, screenshot.rect_height)
        cr.rectangle(*screenshot.get_rectangel_in_monitor())
        cr.stroke()

    def _draw_window_rectangle(self, cr):
        '''
        Draw window frame.
        @param cr: a gtk.gdk.CairoContext
        '''
        screenshot = self.screenshot
        cr.set_line_width(4.5)
        cr.set_source_rgb(*(self.__frame_color))
        rect = screenshot.get_rectangel_in_monitor()
        cr.rectangle(rect[0] + 1, rect[1] + 1, rect[2] - 2, rect[3] - 2)
        cr.stroke()
    
    def get_event_coord(self, event):
        '''
        Get event coord.
        @param event: a gtk.gdk.Event
        @return: a tuple containing the event x_root and y_root
        '''
        (rx, ry) = event.get_root_coords()
        return (int(rx), int(ry))
    
    def get_event_coord_in_monitor(self, event):
        '''
        Get event coord in current monitor
        @param event: a gtk.gdk.Event
        @return: a tuple containing the event x_root and y_root in this monitor
        '''
        (ex, ey) = self.get_event_coord(event)
        return (ex-self.screenshot.monitor_x, ey-self.screenshot.monitor_y)
        
    def drag_frame_top(self, ex, ey):
        '''
        Drag frame top.
        @param ex: the X coordinate of the drag event
        @param ey: the Y coordinate of the drag event
        '''
        screenshot = self.screenshot
        maxY = screenshot.y + screenshot.rect_height
        screenshot.rect_height = screenshot.rect_height - min(screenshot.rect_height, (ey - screenshot.y))
        screenshot.y = min(ey, maxY) 
    
    def drag_frame_bottom(self, ex, ey):
        '''
        Drag frame bottom.
        @param ex: the X coordinate of the drag event
        @param ey: the Y coordinate of the drag event
        '''
        screenshot = self.screenshot
        screenshot.rect_height = max(0, ey - screenshot.y)
    
    def drag_frame_left(self, ex, ey):
        '''
        Drag frame left.
        @param ex: the X coordinate of the drag event
        @param ey: the Y coordinate of the drag event
        '''
        screenshot = self.screenshot
        maxX = screenshot.x + screenshot.rect_width
        screenshot.rect_width = screenshot.rect_width - min(screenshot.rect_width, (ex - screenshot.x))
        screenshot.x = min(ex, maxX)
    
    def drag_frame_right(self, ex, ey):
        '''
        Drag frame right.
        @param ex: the X coordinate of the drag event
        @param ey: the Y coordinate of the drag event
        '''
        screenshot = self.screenshot
        screenshot.rect_width = max(0, ex - screenshot.x)

    def get_drag_point_coords(self):
        '''
        Get drag point coords.
        @return: a 8-tuple containing the eight drag points' coords
        '''
        screenshot = self.screenshot
        return (
            # Top left.
            (screenshot.x - self.drag_point_radius, screenshot.y - self.drag_point_radius),
            # Top right.
            (screenshot.x + screenshot.rect_width - self.drag_point_radius, screenshot.y - self.drag_point_radius),
            # Bottom left.
            (screenshot.x - self.drag_point_radius, screenshot.y + screenshot.rect_height - self.drag_point_radius),
            # Bottom right.
            (screenshot.x + screenshot.rect_width - self.drag_point_radius, screenshot.y + screenshot.rect_height - self.drag_point_radius),
            # Top side.
            (screenshot.x + screenshot.rect_width / 2 - self.drag_point_radius, screenshot.y - self.drag_point_radius),
            # Bottom side.
            (screenshot.x + screenshot.rect_width / 2 - self.drag_point_radius, screenshot.y + screenshot.rect_height - self.drag_point_radius),
            # Left side.
            (screenshot.x - self.drag_point_radius, screenshot.y + screenshot.rect_height / 2 - self.drag_point_radius),
            # Right side.
            (screenshot.x + screenshot.rect_width - self.drag_point_radius, screenshot.y + screenshot.rect_height / 2 - self.drag_point_radius))

    def get_position(self, event):
        '''
        Get drag position.
        @param event: the mouse event
        @return: one of DRAG POS Type Constants
        '''
        screenshot = self.screenshot
        # Get event position.
        (ex, ey) = self.get_event_coord(event)
        # Get drag point coords.
        pWidth = pHeight = self.drag_point_radius* 2
        ((tlX, tlY), (trX, trY), (blX, blY), (brX, brY), (tX, tY), (bX, bY), (lX, lY), (rX, rY)) = self.get_drag_point_coords()
        
        # Calculate drag position.
        if is_collide_rect((ex, ey), (tlX, tlY, pWidth, pHeight)):
            return DRAG_TOP_LEFT_CORNER
        elif is_collide_rect((ex, ey), (trX, trY, pWidth, pHeight)):
            return DRAG_TOP_RIGHT_CORNER
        elif is_collide_rect((ex, ey), (blX, blY, pWidth, pHeight)):
            return DRAG_BOTTOM_LEFT_CORNER
        elif is_collide_rect((ex, ey), (brX, brY, pWidth, pHeight)):
            return DRAG_BOTTOM_RIGHT_CORNER
        elif is_collide_rect((ex, ey), (tX, tY, pWidth, pHeight)) or is_collide_rect((ex, ey), (screenshot.x, screenshot.y, screenshot.rect_width, self.frame_border)):
            return DRAG_TOP_SIDE
        elif is_collide_rect((ex, ey), (bX, bY, pWidth, pHeight)) or is_collide_rect((ex, ey), (screenshot.x, screenshot.y + screenshot.rect_height, screenshot.rect_width, self.frame_border)):
            return DRAG_BOTTOM_SIDE
        elif is_collide_rect((ex, ey), (lX, lY, pWidth, pHeight)) or is_collide_rect((ex, ey), (screenshot.x, screenshot.y, self.frame_border, screenshot.rect_height)):
            return DRAG_LEFT_SIDE
        elif is_collide_rect((ex, ey), (rX, rY, pWidth, pHeight)) or is_collide_rect((ex, ey), (screenshot.x + screenshot.rect_width, screenshot.y, self.frame_border, screenshot.rect_height)):
            return DRAG_RIGHT_SIDE
        elif is_in_rect((ex, ey), (screenshot.x, screenshot.y, screenshot.rect_width, screenshot.rect_height)):
            return DRAG_INSIDE
        else:
            return DRAG_OUTSIDE
        
    def adjust_toolbar(self):
        '''Adjust toolbar position.'''
        screenshot = self.screenshot
        (x, y, screenshot.toolbar_width, screenshot.toolbar_height, depth) = screenshot.toolbar.window.window.get_geometry()
        #print "toolbar:", self.screenshot.toolbar.window.size_request()
        colorbarHeight = screenshot.colorbar.height
        
        screenshot.toolbarX = (screenshot.x + screenshot.rect_width - screenshot.toolbar_width, screenshot.toolbarOffsetX)[screenshot.x + screenshot.rect_width - screenshot.toolbar_width < screenshot.toolbarOffsetX]
        
        if screenshot.y + screenshot.rect_height + screenshot.toolbarOffsetY + screenshot.toolbar_height + colorbarHeight + 5 < screenshot.height:
            screenshot.toolbarY = screenshot.y + screenshot.rect_height + screenshot.toolbarOffsetY
        elif screenshot.y - screenshot.toolbarOffsetY - screenshot.toolbar_height -colorbarHeight - 5 > 0:
            screenshot.toolbarY = screenshot.y - screenshot.toolbarOffsetY - screenshot.toolbar_height
        else:
            screenshot.toolbarY = screenshot.y + screenshot.toolbarOffsetY
        #print "toolbar",screenshot.toolbarX, screenshot.toolbarY
        screenshot.toolbar.window.move(int(screenshot.toolbarX), int(screenshot.toolbarY))
        
    def make_menu(self, coord):
        '''
        show menu when right button press
        @param coord: a tuple containing x and y coordinate.
        '''
        #RightMenu().show(coord)
        self.screenshot.right_menu.show(coord)
    
    def show_toolbar(self):
        '''Show toolbar.'''
        self.screenshot.show_toolbar_flag = True
        self.screenshot.toolbar.show()
        #print "toolbar--:", self.screenshot.toolbar.window.window.get_geometry()
        
    def hide_toolbar(self):
        '''Hide toolbar.'''
        self.screenshot.show_toolbar_flag = False
        self.screenshot.toolbar.hide()

    def show_colorbar(self):
        '''show colorbar '''
        self.screenshot.show_colorbar_flag = True
        self.screenshot.colorbar.show()
        #print "colorbar--:", self.screenshot.colorbar.window.window.get_geometry()
        #print "colorbar:", self.screenshot.colorbar.window.size_request()
    
    def hide_colorbar(self):
        '''hide colorbar'''
        self.screenshot.show_colorbar_flag = False
        self.screenshot.colorbar.hide()
    
    def adjust_colorbar(self):
        '''Adjust Colorbar position '''
        screenshot = self.screenshot
        #color_height = screenshot.colorbar.window.size_request()[1]
        #tool_height = screenshot.toolbar.window.size_request()[1]
        if screenshot.toolbarY < screenshot.y:
            colorbarY = screenshot.toolbarY - screenshot.colorbar.height - 1
            #colorbarY = screenshot.toolbarY - color_height
            #colorbarY = screenshot.toolbarY - 52 -1
        else:
            colorbarY = screenshot.toolbarY + screenshot.toolbar.height + 1
            #colorbarY = screenshot.toolbarY + tool_height
        colorbarX = screenshot.toolbarX
        #print "colorbar", colorbarX, colorbarY
        screenshot.colorbar.window.move(int(colorbarX), int(colorbarY))

    def show_text_window(self, (ex, ey)):
        '''
        Show text window.
        @param (ex, ey): the coordinate of text_window
        '''
        screenshot = self.screenshot
        screenshot.show_text_window_flag = True
        screenshot.text_window = TextWindow(screenshot, "", text_color=screenshot.action_color, font_size=screenshot.font_size)
        screenshot.text_window.connect("button-press-event", self.__text_window_button_press)
        screenshot.text_window.connect("button-release-event", self.__text_window_button_release)
        screenshot.text_window.connect("motion-notify-event", self.__text_window__motion)
        self.draw_area.put(screenshot.text_window, ex, ey)
        screenshot.text_window.show_all()
        self.refresh()
        screenshot.text_window.set_width(int(screenshot.rect_width + screenshot.x - ex
            - 2 * screenshot.text_window.padding_x))
        screenshot.text_window.grab_focus()
        
    def hide_text_window(self):
        '''Hide text window.'''
        screenshot = self.screenshot
        screenshot.show_text_window_flag = False
        screenshot.text_window.destroy()

    def save_text_window(self):
        '''save TextWindow's text'''
        screenshot = self.screenshot
        content = screenshot.text_window.get_text()
        if content != "":
            if screenshot.text_modify_flag: # modify a text
                screenshot.current_text_action.update(screenshot.action_color, screenshot.text_window.get_layout())
                text_x = int(screenshot.text_window.allocation.x)
                text_y = int(screenshot.text_window.allocation.y)
                screenshot.current_text_action.update_coord(text_x, text_y)
                screenshot.text_modify_flag = False
                screenshot.text_action_list.append(screenshot.current_text_action)
                screenshot.action_list.append(screenshot.current_text_action)
            else:                           # new a text
                textAction = TextAction(ACTION_TEXT, 15, screenshot.action_color, screenshot.text_window.get_layout())
                allocation = screenshot.text_window.allocation
                textAction.start_draw((allocation[0], allocation[1]))
                screenshot.text_action_list.append(textAction)
                screenshot.action_list.append(textAction)
            self.hide_text_window()
            self.refresh()
        else:
            self.hide_text_window()

    def __text_window_button_press(self, widget, event):
        '''button press in textview, begin to drag '''
        if event.button == 1:
            widget.drag_flag = True
            #widget.drag_position = (event.x_root, event.y_root)
            widget.drag_position = self.get_event_coord(event)
            widget.drag_origin = (widget.allocation.x, widget.allocation.y)
            self.set_cursor(DRAG_INSIDE)

    def __text_window_button_release(self, widget, event):
        '''button release in textview, stop dragging'''
        if event.button == 1:
            widget.drag_flag = False
            widget.drag_offset = (0, 0)
            widget.drag_position = (0, 0)
            widget.drag_origin = (0, 0)
            self.set_cursor(None)

    def __text_window__motion(self, widget, event):
        '''button motion in textview, dragging'''
        coord = widget.allocation
        monitor_rect = self.screenshot.get_rectangel_in_monitor()
        rect_x = monitor_rect[0] + monitor_rect[2]
        rect_y = monitor_rect[1] + monitor_rect[3]
        (x_root, y_root) = self.get_event_coord(event)
        #rect_x = self.screenshot.x + self.screenshot.rect_width
        #rect_y = self.screenshot.y + self.screenshot.rect_height
        if widget.drag_flag:
            #offset_x = int(event.x_root - widget.drag_position[0])
            #offset_y = int(event.y_root - widget.drag_position[1])
            offset_x = x_root - widget.drag_position[0]
            offset_y = y_root - widget.drag_position[1]
            widget.drag_offset = (offset_x, offset_y)
            des_x = widget.drag_origin[0] + offset_x
            des_y = widget.drag_origin[1] + offset_y
            # make sure the textview in the area
            if des_x + coord[2] > rect_x:
                des_x = rect_x - coord[2]
            elif des_x < self.screenshot.x:
                des_x = self.screenshot.x
            if des_y + coord[3] > rect_y:
                des_y = rect_y - coord[3]
            elif des_y < self.screenshot.y:
                des_y = self.screenshot.y
            self.draw_area.move(widget, des_x, des_y)
    
    def set_cursor(self, cursor_type):
        '''
        set cursor type
        @param cursor_type: one of cursor Type Constants in theme moudle
        '''
        if cursor_type in theme_cursor:
            set_cursor(self.window, theme_cursor[cursor_type])
        else:
            set_cursor(self.window, None)

    def _save_to_file(self):
        ''' Ctrl + s has been pressed'''
        self.screenshot.toolbar.save_to_file()

    def show(self):
        '''show root window'''
        self.window.show_all()
        #self._cr = self.window.window.cairo_create()
        self._cr = self.draw_area.window.cairo_create()
        self.window.window.raise_()

class RightMenu():
    ''' Right Button Menu'''
    def __init__(self, screenshot):
        self.screenshot = screenshot    # a DeepinScreenshot object
        # sub menu in save node
        menu_item = [
            (None, _("save automatically"), self.save_sub_menu_clicked, SAVE_OP_AUTO),
            (None, _("save as"), self.save_sub_menu_clicked, SAVE_OP_AS),
            (None, _("save to clipboard"), self.save_sub_menu_clicked, SAVE_OP_CLIP),
            (None, _("save automatically to file and clipboard"), self.save_sub_menu_clicked, SAVE_OP_AUTO_AND_CLIP)]
        self.save_sub_menu = save_sub_menu = Menu(menu_item, 
            menu_item_select_color=app_theme.get_shadow_color("menu_item_select").get_color_info())
        # right button menu
        self.window = Menu([
            ((app_theme_get_dynamic_pixbuf('image/action_menu/rect_normal.png'),
              app_theme_get_dynamic_pixbuf('image/action_menu/rect_hover.png'),
              app_theme_get_dynamic_pixbuf('image/action_menu/rect_normal.png')),
              _("draw rectangle"), self._menu_click, "rect"),
            ((app_theme_get_dynamic_pixbuf('image/action_menu/ellipse_normal.png'),
              app_theme_get_dynamic_pixbuf('image/action_menu/ellipse_hover.png'),
              app_theme_get_dynamic_pixbuf('image/action_menu/ellipse_normal.png')),
              _("draw ellipse"), self._menu_click, "ellipse"),
            ((app_theme_get_dynamic_pixbuf('image/action_menu/arrow_normal.png'), 
              app_theme_get_dynamic_pixbuf('image/action_menu/arrow_hover.png'), 
              app_theme_get_dynamic_pixbuf('image/action_menu/arrow_normal.png')), 
              _("draw arrow"), self._menu_click, "arrow"),
            ((app_theme_get_dynamic_pixbuf('image/action_menu/line_normal.png'), 
              app_theme_get_dynamic_pixbuf('image/action_menu/line_hover.png'), 
              app_theme_get_dynamic_pixbuf('image/action_menu/line_normal.png')), 
              _("draw line"), self._menu_click, "line"),
            ((app_theme_get_dynamic_pixbuf('image/action_menu/text_normal.png'), 
              app_theme_get_dynamic_pixbuf('image/action_menu/text_hover.png'), 
              app_theme_get_dynamic_pixbuf('image/action_menu/text_normal.png')), 
              _("draw Text"), self._menu_click, "text"),
            None,
            ((app_theme_get_dynamic_pixbuf('image/action_menu/undo_normal.png'), 
              app_theme_get_dynamic_pixbuf('image/action_menu/undo_hover.png'), 
              app_theme_get_dynamic_pixbuf('image/action_menu/undo_normal.png')), 
              _("undo"), self._menu_click, "undo"),
            ((app_theme_get_dynamic_pixbuf('image/action_menu/save_normal.png'), 
              app_theme_get_dynamic_pixbuf('image/action_menu/save_hover.png'), 
              app_theme_get_dynamic_pixbuf('image/action_menu/save_normal.png')), 
              _("save"), save_sub_menu),
            ((app_theme_get_dynamic_pixbuf('image/action_menu/cancel_normal.png'), 
              app_theme_get_dynamic_pixbuf('image/action_menu/cancel_hover.png'), 
              app_theme_get_dynamic_pixbuf('image/action_menu/cancel_normal.png')), 
              _("cancel"), self._menu_click, "cancel"),
            ((app_theme_get_dynamic_pixbuf('image/action_menu/share_normal.png'), 
              app_theme_get_dynamic_pixbuf('image/action_menu/share_hover.png'), 
              app_theme_get_dynamic_pixbuf('image/action_menu/share_normal.png')), 
              _("share"), self._menu_click, "share"),
            ], True,
            menu_item_select_color=app_theme.get_shadow_color("menu_item_select").get_color_info())
        
    def _menu_click(self, name):
        '''menu clicked callback'''
        buttons = self.screenshot.toolbar.toolbox.get_children()
        for each in buttons:
            if each.name == name:
                each.pressed()
                each.released()
                each.clicked()
                return
        # save current input text
        if self.screenshot.show_text_window_flag:
            self.screenshot.window.save_text_window()
        self.screenshot.toolbar.set_button_active(name, True)

    def save_sub_menu_clicked(self, save_op_index):
        '''save sub menu clicked callback'''
        self.screenshot.toolbar._list_menu_click(save_op_index)

    def show(self, coord=(0, 0)):
        ''' show menu '''
        # set current operate icon
        items = self.save_sub_menu.get_menu_items()
        i = 0
        for menu_item in items:
            item = list(menu_item.item)
            if i == self.screenshot.save_op_index:
                item[0] = (
                    app_theme.get_pixbuf("action/selected.png"),
                    app_theme.get_pixbuf("action/selected_hover.png"),
                    app_theme.get_pixbuf("action/selected.png"))
            else:
                item[0] = None
            i += 1
            menu_item.item = tuple(item)
        self.window.show(coord)

class TextWindow(TextView):
    '''TextWindow'''
    def __init__(self, screenshot, content="", text_color="#000000",
                 text_select_color="#FFFFFF",background_select_color="#3399FF",
                 font=DEFAULT_FONT, font_size=DEFAULT_FONT_SIZE):
        '''
        init TextWindow
        @param screenshot: a Screenshot object
        @param content: initialize content, a string type
        @param text_color: color of text in normal status, an hex string
        @param text_select_color: color of text in selected status, an hex string
        @param background_select_color: color of background in selected status, an hex string
        @param font: fontname of text
        @param font_size: fontsize of text
        '''
        super(TextWindow, self).__init__(content, 1, 1, text_color, 
                text_select_color, background_select_color, font, font_size)
        self.screenshot = screenshot
        self.connect("changed", self.__text_changed)
        
        self.drag_flag = False              # a flag if the TextWindow can be dragged
        self.drag_position = (0, 0)         # the start drag point position
        self.drag_offset = (0, 0)           # the offset when dragging
        self.drag_origin = (0, 0)           # the origin position at start drag

        self.set_text(content)
        self.set_background_dash((9.0, 3.0))
        self.adjust_size()

    def adjust_size(self):
        '''set widget size'''
        self.count_size()
        if self.layout_width < 10:
            self.layout_width = 10
        self.set_size_request(self.layout_width+self.padding_x*2, self.layout_height+self.padding_y*2)

    def commit_entry(self, input_text):
        '''
        commit entry
        @param input_text: a text insert to this TextWindow, a string type
        '''
        if not self.is_editable():
            return
        if not isinstance(input_text, unicode):
            try:
                input_text = input_text.decode('utf-8')
            except Exception, e:
                pass
        input_text = input_text.encode('utf-8')
        layout = self._layout.copy()
        if self.buffer.get_has_selection():
            bounds = self.buffer.get_bounds()
            left = self.buffer.get_text(self.buffer.get_start_iter(), bounds[0]).__len__()
            right = self.buffer.get_text(self.buffer.get_start_iter(), bounds[1]).__len__()
            content = layout.get_text()
            layout.set_text(content[0:left] + input_text + content[right:])
        else:
            layout.set_text(layout.get_text() + input_text)
        text_size = layout.get_pixel_size()
        # out of the area, can't insert
        #if self.allocation.x + text_size[0] > self.screenshot.x + self.screenshot.rect_width \
        if self.allocation.y + text_size[1] + 2 * self.padding_y >self.screenshot.y + self.screenshot.rect_height:
            # TODO add tips
            return
        with self.monitor_entry_content():
            if self.buffer.get_has_selection():     # if has select, delete it
                self.buffer.delete_selection(True, self.is_editable())
            self.buffer.insert_at_cursor(input_text)
            self.set_width(int(self.screenshot.rect_width + self.screenshot.x
                - self.allocation.x - 2 * self.padding_x))
            self.adjust_size()
            self.queue_draw()
    
    def set_font_size(self, size):
        '''
        set font size
        @param size: font size, an int num
        @return: if set successfully return True, otherwise return False
        '''
        # if font size too large ,ignore
        layout = self._layout.copy()
        layout.set_font_description(pango.FontDescription("%s %d" % (self.font_type, size)))
        text_size = layout.get_pixel_size()
        if text_size[0] + self.allocation.x + 2 * self.padding_x> self.screenshot.x + self.screenshot.rect_width \
            or text_size[1] + self.allocation.y + 2 * self.padding_y> self.screenshot.y + self.screenshot.rect_height:
            # TODO add tips
            return False
        self.font_size = size
        self.font = pango.FontDescription("%s %d" % (self.font_type, self.font_size))
        self._layout.set_font_description(self.font)
        self.adjust_size()
        return True
    
    def __text_changed(self, w, string):
        '''changed signal callback'''
        self.screenshot.window.refresh()

gobject.type_register(TextWindow)
if __name__ == '__main__':
    #RootWindow().show()
    #TextWindow().show()
    RightMenu().show((100, 100))
    gtk.main()
