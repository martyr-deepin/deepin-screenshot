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
from collections import namedtuple
from draw import *
from constant import *
from action import TextAction
from nls import _
from dtk.ui.entry import Entry
from dtk.ui.utils import (cairo_state, color_hex_to_cairo,
                          is_left_button, is_right_button,
                          is_double_click, get_content_size)
import dtk.ui.constant as dtk_constant
import status
import gtk
import pango
import gobject

DEFAULT_FONT = dtk_constant.DEFAULT_FONT
DEFAULT_FONT_SIZE = dtk_constant.DEFAULT_FONT_SIZE

Magnifier = namedtuple('Magnifier', 'x y size_content tip rgb')

class RootWindow():
    ''' background window'''
    def __init__(self, screenshot):
        self.screenshot = screenshot
        self.frame_border = 2
        self.drag_point_radius = 4
        self.__frame_color = (0.0, 0.68, 1.0)

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
        self.hotkey_map = { "Escape": self.window.destroy}
        if self.screenshot:
            self.hotkey_map["Ctrl + s"] = self._save_to_file
            self.hotkey_map["Return"] = self.screenshot.save_snapshot
            self.hotkey_map["KP_Enter"] = self.screenshot.save_snapshot
            self.hotkey_map["Ctrl + z"] = self.screenshot.undo

    def _draw_expose(self, widget, event):
        ''' draw area expose'''
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
        ''' button press '''
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
            # edit text, create a new TextView
            if self.screenshot.text_drag_flag:
                current_action = self.screenshot.current_text_action
                # don't draw this  text action
                if current_action in self.screenshot.text_action_list:
                    self.screenshot.text_action_list.remove(current_action)
                if current_action in self.screenshot.action_list:
                    self.screenshot.action_list.remove(current_action)
                del self.screenshot.text_action_info[current_action]
                self.screenshot.draw_text_layout_flag = False   # don't draw text layout
                self.show_text_window((current_action.start_x, current_action.start_y))
                self.screenshot.text_window.set_text(current_action.get_content())
                self.screenshot.text_window.set_font_size(current_action.get_font_size())
                self.screenshot.text_window.adjust_size()
                self.screenshot.colorbar.font_spin.set_value(self.screenshot.text_window.get_font_size())
                self.refresh()
                self.screenshot.text_window.queue_draw()
                self.screenshot.colorbar.color_select.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse(self.screenshot.action_color))
                #self.screenshot.colorbar.font_label.set_text(self.screenshot.font_name)
                
                # set action ACTION_TEXT
                self.screenshot.toolbar.set_button_active("text", True)
                self.screenshot.text_modify_flag = True
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
                print widget.event(release_event)
                self.screenshot.toolbar.save_operate()
    
    def _button_release_event(self, widget, event):
        ''' button release '''
        if self.screenshot is None:
            return
        self._button_released_process.update(event)
        self._button_released_process.process()
    
    def _motion_notify_event(self, widget, event):
        ''' motion notify '''
        #self.update_magnifier(event.x, event.y)
        if self.screenshot is None:
            return
        self._button_motion_process.update(event)
        self._button_motion_process.process()
    
    def _key_press_event(self, widget, event):
        ''' key press '''
        if event.is_modifier or self.screenshot.show_text_window_flag:
            return
        key = get_keyevent_name(event)
        if key in self.hotkey_map:
            self.hotkey_map[key]()
    
    def quit(self, widget=None):
        ''' window destroy'''
        gtk.main_quit()
        pass
    
    def update_magnifier(self, x, y, size='', tip=_("Drag to select area"), rgb="RGB:(255,255,255)"):
        ''' update magnifier '''
        self.magnifier = Magnifier(x, y, size, tip, rgb)

    def _draw_magnifier(self, cr):
        ''' draw the magnifier'''
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
        '''draw mask'''
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
        '''Draw drag point.'''
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
        '''Draw frame.'''
        screenshot = self.screenshot
        cr.set_source_rgb(*self.__frame_color)
        cr.set_line_width(self.frame_border)
        #cr.rectangle(screenshot.x, screenshot.y, screenshot.rect_width, screenshot.rect_height)
        cr.rectangle(*screenshot.get_rectangel_in_monitor())
        cr.stroke()

    def _draw_window_rectangle(self, cr):
        '''Draw window frame.'''
        screenshot = self.screenshot
        cr.set_line_width(4.5)
        cr.set_source_rgb(*(self.__frame_color))
        cr.rectangle(screenshot.x + 1, screenshot.y + 1, screenshot.rect_width - 2, screenshot.rect_height - 2)
        cr.stroke()
    
    def get_event_coord(self, event):     # 获取事件的坐标
        '''Get event coord.'''
        (rx, ry) = event.get_root_coords()
        return (int(rx), int(ry))
    
    def get_event_coord_in_monitor(self, event):
        '''Get event coord in current monitor'''
        (ex, ey) = self.get_event_coord(event)
        return (ex-self.screenshot.monitor_x, ey-self.screenshot.monitor_y)
        
    def drag_frame_top(self, ex, ey):
        '''Drag frame top.'''
        screenshot = self.screenshot
        maxY = screenshot.y + screenshot.rect_height
        screenshot.rect_height = screenshot.rect_height - min(screenshot.rect_height, (ey - screenshot.y))
        screenshot.y = min(ey, maxY) 
    
    def drag_frame_bottom(self, ex, ey):
        '''Drag frame bottom.'''
        screenshot = self.screenshot
        screenshot.rect_height = max(0, ey - screenshot.y)
    
    def drag_frame_left(self, ex, ey):
        '''Drag frame left.'''
        screenshot = self.screenshot
        maxX = screenshot.x + screenshot.rect_width
        screenshot.rect_width = screenshot.rect_width - min(screenshot.rect_width, (ex - screenshot.x))
        screenshot.x = min(ex, maxX)
    
    def drag_frame_right(self, ex, ey):
        '''Drag frame right.'''
        screenshot = self.screenshot
        screenshot.rect_width = max(0, ex - screenshot.x)

    def get_drag_point_coords(self):
        '''Get drag point coords.'''
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
        '''Get drag position.'''
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
        ''' make menu'''
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
        '''Show text window.'''
        screenshot = self.screenshot
        screenshot.show_text_window_flag = True
        screenshot.text_window = TextView(screenshot, "", text_color=screenshot.action_color, font_size=screenshot.font_size)
        screenshot.text_window.connect("button-press-event", self.__text_window_button_press)
        screenshot.text_window.connect("button-release-event", self.__text_window_button_release)
        screenshot.text_window.connect("motion-notify-event", self.__text_window__motion)
        self.draw_area.put(screenshot.text_window, ex, ey)
        screenshot.text_window.show_all()
        self.refresh()
        screenshot.text_window.set_width(int(screenshot.rect_width + screenshot.x - ex))
        screenshot.text_window.grab_focus()
        
    def hide_text_window(self):
        '''Hide text window.'''
        screenshot = self.screenshot
        screenshot.show_text_window_flag = False
        screenshot.text_window.destroy()

    def save_text_window(self):
        '''save TextView text'''
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
        '''button release'''
        if event.button == 1:
            widget.drag_flag = False
            widget.drag_offset = (0, 0)
            widget.drag_position = (0, 0)
            widget.drag_origin = (0, 0)
            self.set_cursor(None)

    def __text_window__motion(self, widget, event):
        '''motion notify'''
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
        ''' set cursor'''
        if cursor_type in theme_cursor:
            set_cursor(self.window, theme_cursor[cursor_type])
        else:
            set_cursor(self.window, None)

    def _save_to_file(self):
        ''' Ctrl + s has been pressed'''
        self.screenshot.toolbar.save_to_file()

    def show(self):
        '''show'''
        self.window.show_all()
        #self._cr = self.window.window.cairo_create()
        self._cr = self.draw_area.window.cairo_create()
        self.window.window.raise_()

class RightMenu():
    ''' Right Button Menu'''
    def __init__(self, screenshot):
        self.screenshot = screenshot
        menu_item = [
            (None, _("save automatically"), self.save_sub_menu_clicked, SAVE_OP_AUTO),
            (None, _("save as"), self.save_sub_menu_clicked, SAVE_OP_AS),
            (None, _("save to clipboard"), self.save_sub_menu_clicked, SAVE_OP_CLIP),
            (None, _("save automatically to file and clipboard"), self.save_sub_menu_clicked, SAVE_OP_AUTO_AND_CLIP)]
        ## set current operate icon
        #current_item = menu_item[self.screenshot.save_op_index] 
        #menu_pixbuf = (
            #app_theme.get_pixbuf("action/selected.png"),
            #app_theme.get_pixbuf("action/selected_hover.png"),
            #app_theme.get_pixbuf("action/selected.png"))
        #menu_item[self.screenshot.save_op_index] = (menu_pixbuf,
            #current_item[1], current_item[2], current_item[3])
        self.save_sub_menu = save_sub_menu = Menu(menu_item, 
            menu_item_select_color=app_theme.get_shadow_color("menu_item_select").get_color_info())
        self.window = Menu([
            ((app_theme_get_dynamic_pixbuf('image/action/rect_normal.png'),
              app_theme_get_dynamic_pixbuf('image/action/rect_hover.png'),
              app_theme_get_dynamic_pixbuf('image/action/rect_press.png')),
              _("draw rectangle"), self._menu_click, "rect"),
            ((app_theme_get_dynamic_pixbuf('image/action/ellipse_normal.png'),
              app_theme_get_dynamic_pixbuf('image/action/ellipse_hover.png'),
              app_theme_get_dynamic_pixbuf('image/action/ellipse_press.png')),
              _("draw ellipse"), self._menu_click, "ellipse"),
            ((app_theme_get_dynamic_pixbuf('image/action/arrow_normal.png'), 
              app_theme_get_dynamic_pixbuf('image/action/arrow_hover.png'), 
              app_theme_get_dynamic_pixbuf('image/action/arrow_press.png')), 
              _("draw arrow"), self._menu_click, "arrow"),
            ((app_theme_get_dynamic_pixbuf('image/action/line_normal.png'), 
              app_theme_get_dynamic_pixbuf('image/action/line_hover.png'), 
              app_theme_get_dynamic_pixbuf('image/action/line_press.png')), 
              _("draw line"), self._menu_click, "line"),
            ((app_theme_get_dynamic_pixbuf('image/action/text_normal.png'), 
              app_theme_get_dynamic_pixbuf('image/action/text_hover.png'), 
              app_theme_get_dynamic_pixbuf('image/action/text_press.png')), 
              _("draw Text"), self._menu_click, "text"),
            None,
            ((app_theme_get_dynamic_pixbuf('image/action/undo_normal.png'), 
              app_theme_get_dynamic_pixbuf('image/action/undo_hover.png'), 
              app_theme_get_dynamic_pixbuf('image/action/undo_press.png')), 
              _("undo"), self._menu_click, "undo"),
            ((app_theme_get_dynamic_pixbuf('image/action/save_normal.png'), 
              app_theme_get_dynamic_pixbuf('image/action/save_hover.png'), 
              app_theme_get_dynamic_pixbuf('image/action/save_press.png')), 
              _("save"), save_sub_menu),
            ((app_theme_get_dynamic_pixbuf('image/action/cancel_normal.png'), 
              app_theme_get_dynamic_pixbuf('image/action/cancel_hover.png'), 
              app_theme_get_dynamic_pixbuf('image/action/cancel_press.png')), 
              _("cancel"), self._menu_click, "cancel"),
            ((app_theme_get_dynamic_pixbuf('image/action/share_normal.png'), 
              app_theme_get_dynamic_pixbuf('image/action/share_hover.png'), 
              app_theme_get_dynamic_pixbuf('image/action/share_press.png')), 
              _("share"), self._menu_click, "share"),
            ], True,
            menu_item_select_color=app_theme.get_shadow_color("menu_item_select").get_color_info())
        
    def _menu_click(self, name):
        '''docstring for _menu_click'''
        buttons = self.screenshot.toolbar.toolbox.get_children()
        for each in buttons:
            if each.name == name:
                each.pressed()
                each.released()
                each.clicked()
                break

    def save_sub_menu_clicked(self, save_op_index):
        '''save sub menu clicked'''
        self.screenshot.toolbar._list_menu_click(save_op_index)
        self.screenshot.toolbar.save_operate()

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

class TextView(Entry):
    '''TextView'''
    def __init__(self, screenshot, content="", text_color="#000000",
                 text_select_color="#FFFFFF",background_select_color="#3399FF",
                 font=DEFAULT_FONT, font_size=DEFAULT_FONT_SIZE):
        super(TextView, self).__init__(content, 0, 0, "#000000", "#FFFFFF", "#0000F0")
        self.screenshot = screenshot
        self.text_color = text_color
        self.text_select_color = text_select_color
        self.background_select_color = background_select_color
        self.font_type = font
        self.font_size = font_size
        self.font = pango.FontDescription("%s %d" % (font, font_size))
        # press Return | KP_Enter
        self.keymap["KP_Enter"] = self.press_return
        self.keymap["Up"] = self.move_to_up
        self.keymap["Down"] = self.move_to_down
        self.keymap["Shift + Up"] = self.select_to_up
        self.keymap["Shift + Down"] = self.select_to_down
        self.connect("press-return", self.entry_press_return)
        self.buffer = gtk.TextBuffer()
        self.buffer.connect("paste-done", self.__paste_done)
        
        surface = cairo.ImageSurface(cairo.FORMAT_RGB24, 0, 0) 
        cr = cairo.Context(surface)
        self.__cr = pangocairo.CairoContext(cr)
        self.__layout = self.__cr.create_layout()
        self.__layout.set_font_description(self.font)
        self.__layout.set_alignment(pango.ALIGN_LEFT)
        self.__layout.set_wrap(pango.WRAP_WORD_CHAR)

        self.__width = self.__height = 0    # widget width and height
        self.__layout_width = -1

        self.drag_flag = False              # drag this
        self.drag_position = (0, 0)
        self.drag_offset = (0, 0)
        self.drag_origin = (0, 0)

        self.set_text(content)
        self.adjust_size()

    def get_text(self):
        '''get text'''
        s = self.buffer.get_start_iter()
        e = self.buffer.get_end_iter()
        self.content = self.buffer.get_text(s, e)
        return self.content

    def set_text(self, text):
        '''set text'''
        if not isinstance(text, unicode):
            try:
                text = text.decode('utf-8')
            except Exception, e:
                pass
        text = text.encode('utf-8')
        self.buffer.set_text(text)
        e = self.buffer.get_end_iter()
        insert = self.buffer.get_iter_at_mark(self.buffer.get_insert())
        self.cusor_index = insert.get_offset()
        self.select_start_index = self.select_end_index = e.get_offset()

        self.__layout.set_text(text)
        self.__count_size()

    def set_width(self, width):
        '''set layout width'''
        if width > 0:
            self.__layout_width = width * pango.SCALE
        else:
            self.__layout_width = -1
        self.__layout.set_width(self.__layout_width)

    def get_width(self):
        '''get layout width '''
        return self.__layout_width

    def get_size(self):
        '''get text size'''
        self.__count_size()
        return (self.__width, self.__height)

    def get_layout(self):
        '''get layout'''
        return self.__layout

    def get_buffer(self):
        '''get buffer'''
        return self.buffer

    def set_buffer(self, buf):
        '''set buffer'''
        self.buffer = buf

    def set_font_size(self, size):
        '''set font size'''
        # if font size too large ,ignore
        layout = self.__layout.copy()
        layout.set_font_description(pango.FontDescription("%s %d" % (self.font_type, size)))
        text_size = layout.get_pixel_size()
        if text_size[0] + self.allocation.x > self.screenshot.x + self.screenshot.rect_width \
            or text_size[1] + self.allocation.y > self.screenshot.y + self.screenshot.rect_height:
            return False
        self.font_size = size
        self.font = pango.FontDescription("%s %d" % (self.font_type, self.font_size))
        self.__layout.set_font_description(self.font)
        self.adjust_size()
        return True

    def get_font_size(self):
        '''get font size'''
        return self.font_size

    def set_text_color(self, color):
        '''set text color'''
        self.text_color = color

    def get_text_color(self):
        '''get text color'''
        return self.text_color

    def __count_size(self):
        '''count widget size'''
        self.__layout.set_text(self.get_text())
        (self.__width, self.__height) = self.__layout.get_pixel_size()

    def adjust_size(self):
        '''set widget size'''
        self.__count_size()
        if self.__width < 10: self.__width = 10
        self.set_size_request(self.__width, self.__height)

    def entry_press_return(self, widget):
        '''press return'''
        self.commit_entry('\n')

    def draw_entry_background(self, cr, rect):
        '''draw background '''
        #print self.buffer.get_selection_bounds()
        #print self.buffer.get_iter_at_mark(self.buffer.get_selection_bound()).get_offset()
        x, y, w, h = rect.x, rect.y, rect.width, rect.height
        #print self.allocation, self.__layout.get_pixel_size()
        cr.set_source_rgba(1.0, 1.0, 1.0, 0.8)
        cr.rectangle(x, y, w, h)
        cr.fill()
        cr.set_source_rgba(0.0, 0.0, 0.0, 1.0)
        cr.set_dash((9.0, 3.0))
        cr.set_line_width(1)
        cr.rectangle(x, y, w, h)
        cr.stroke()
        # draw selection
        if not self.buffer.get_has_selection():
            return
        bounds = self.buffer.get_selection_bounds()
        self.draw_selection_lines(bounds[0], bounds[1], cr, x, y)
    
    def draw_entry_text(self, cr, rect):
        ''' draw text '''
        x, y, w, h = rect.x, rect.y, rect.width, rect.height
        with cairo_state(cr):
            # Clip text area first.
            draw_x = x + self.padding_x
            draw_y = y + self.padding_y
            draw_width = w - self.padding_x * 2
            draw_height = h - self.padding_y * 2
            cr.rectangle(draw_x, draw_y, draw_width, draw_height)
            cr.clip()
            # Create pangocairo context.
            context = pangocairo.CairoContext(cr)
            # Move text.
            cr.move_to(draw_x, draw_y)
            # Draw text.
            cr.set_source_rgb(*color_hex_to_cairo(self.text_color))
            #context.update_layout(layout)
            #context.show_layout(layout)
            #print "get_width", self.__layout.get_width()
            context.update_layout(self.__layout)
            context.show_layout(self.__layout)
            #self.__layout.set_spacing(2)
            #print "text spacing:", self.__layout.get_spacing()

    def draw_entry_cursor(self, cr, rect):
        '''
        Internal function to draw entry cursor.
        '''
        if self.grab_focus_flag and self.select_start_index == self.select_end_index:
            # Init.
            x, y, w, h = rect.x, rect.y, rect.width, rect.height
            # Draw cursor.
            cr.set_source_rgb(*color_hex_to_cairo("#000000"))
            index = self.iter_to_index(self.buffer.get_iter_at_mark(self.buffer.get_insert()))
            pos = self.index_to_pos(index)
            cr.rectangle(pos[0]+x, pos[1]+y, 1, pos[3])
            cr.fill()
            # Tell input method follow cursor position
            self.im.set_cursor_location(gtk.gdk.Rectangle(pos[0]+x, pos[1]+y, 1, pos[3]))
    
    def draw_selection_lines(self, start, end, cr, x, y):
        '''draw selection line background'''
        start_index = self.iter_to_index(start)
        end_index = self.iter_to_index(end)
        cursor = start_index
        while start_index <= cursor <= end_index:
            self.draw_selection_index(cursor, cr, x, y)
            cursor += 1
                
    def draw_selection_index(self, index, cr, x, y):
        '''draw selection iter background '''
        pos = self.index_to_pos(index)
        cr.set_source_rgb(*color_hex_to_cairo(self.background_select_color))
        cr.rectangle(pos[0]+x, pos[1]+y, pos[2], pos[3])
        cr.fill()

    def iter_to_index(self, iter):
        ''' textiter to index'''
        index = self.buffer.get_text(self.buffer.get_start_iter(), iter).__len__()
        return index

    def index_to_pos(self, index):
        '''index to pos'''
        pos = self.__layout.index_to_pos(index)
        pos = list(pos)
        pos[0] /= pango.SCALE
        pos[1] /= pango.SCALE
        pos[2] /= pango.SCALE
        pos[3] /= pango.SCALE
        return pos
    
    def commit_entry(self, input_text):
        ''' commit entry '''
        if not self.is_editable():
            return
        if not isinstance(input_text, unicode):
            try:
                input_text = input_text.decode('utf-8')
            except Exception, e:
                pass
        input_text = input_text.encode('utf-8')
        layout = self.__layout.copy()
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
        if self.allocation.y + text_size[1] >self.screenshot.y + self.screenshot.rect_height:
            return
        if self.buffer.get_has_selection():     # if has select, delete it
            self.buffer.delete_selection(True, self.is_editable())
        self.buffer.insert_at_cursor(input_text)
        self.set_width(int(self.screenshot.rect_width + self.screenshot.x - self.allocation.x))
        self.adjust_size()
        self.screenshot.window.refresh()
        self.queue_draw()

    def backspace(self):
        '''
        Do backspace action.
        '''        
        if self.buffer.get_has_selection():
            self.buffer.delete_selection(True, self.is_editable())
        else:
            self.buffer.backspace(self.buffer.get_iter_at_mark(self.buffer.get_insert()),
                True, self.is_editable())
        self.adjust_size()
        self.screenshot.window.refresh()
        self.queue_draw()

    def delete(self):
        '''
        Delete selected text.
        '''
        insert = self.buffer.get_iter_at_mark(self.buffer.get_insert())
        if insert.is_end():
            return
        if self.buffer.get_has_selection():
            self.buffer.delete_selection(True, self.is_editable())
            self.adjust_size()
            self.screenshot.window.refresh()
            self.queue_draw()
        else:
            self.move_to_right()
            self.backspace()

    def select_all(self):
        '''
        Select all text of entry.
        '''
        self.select_start_index = 0
        self.select_end_index = len(self.content)
        self.buffer.select_range(*self.buffer.get_bounds())
        self.adjust_size()
        self.queue_draw()

    def cut_to_clipboard(self):
        '''
        Cut selected text to clipboard.
        '''
        self.buffer.cut_clipboard(gtk.Clipboard(), self.is_editable())
        self.adjust_size()
        self.screenshot.window.refresh()
        self.queue_draw()

    def copy_to_clipboard(self):
        '''
        Copy selected text to clipboard.
        '''
        self.buffer.copy_clipboard(gtk.Clipboard())
    
    def paste_from_clipboard(self):
        '''
        Paste text to entry from clipboard.
        '''
        clipboard = gtk.Clipboard()
        input_text = clipboard.wait_for_text()
        if input_text is None:
            return
        self.commit_entry(input_text)
        #self.buffer.paste_clipboard(gtk.Clipboard(), None, self.is_editable())
    
    def __paste_done(self, widget, clipboard):
        ''' buffer paste done'''
        self.adjust_size()
        self.queue_draw()

    def move_to_start(self):
        '''
        Move cursor to start position of entry.
        '''
        #self.offset_x = 0
        #self.cursor_index = 0
        self.clear_select_status()
        insert = self.buffer.get_iter_at_mark(self.buffer.get_insert())
        insert.set_line_offset(0)
        self.buffer.move_mark_by_name("insert", insert)
        self.buffer.move_mark_by_name("selection_bound", insert)
        self.queue_draw()
        
    def move_to_end(self):
        '''
        Move cursor to end position of entry.
        '''
        #text_width = self.get_content_width(self.content)
        #rect = self.get_allocation()
        #if text_width > rect.width - self.padding_x * 2 > 0:
            #self.offset_x = text_width - (rect.width - self.padding_x * 2)
        #self.cursor_index = len(self.content)
        
        self.clear_select_status()
        insert = self.buffer.get_iter_at_mark(self.buffer.get_insert())
        insert.forward_to_line_end()
        self.buffer.move_mark_by_name("insert", insert)
        self.buffer.move_mark_by_name("selection_bound", insert)
        self.queue_draw()
        
    def move_to_left(self):
        '''
        Backward cursor one char.
        '''
        # Avoid change focus to other widget in parent.
        if self.keynav_failed(gtk.DIR_LEFT):
            self.get_toplevel().set_focus_child(self)
            
        if self.select_start_index != self.select_end_index:
            self.clear_select_status()
        insert = self.buffer.get_iter_at_mark(self.buffer.get_insert())
        insert.backward_char()
        self.buffer.move_mark_by_name("insert", insert)
        self.buffer.move_mark_by_name("selection_bound", insert)
        self.queue_draw()
            
    def move_to_right(self):
        '''
        Forward cursor one char.
        '''
        # Avoid change focus to other widget in parent.
        if self.keynav_failed(gtk.DIR_RIGHT):
            self.get_toplevel().set_focus_child(self)
                        
        if self.select_start_index != self.select_end_index:
            self.clear_select_status()
        insert = self.buffer.get_iter_at_mark(self.buffer.get_insert())
        insert.forward_char()
        self.buffer.move_mark_by_name("insert", insert)
        self.buffer.move_mark_by_name("selection_bound", insert)
        self.queue_draw()

    def move_to_up(self):
        '''
        Backward cursor one line.
        '''
        # Avoid change focus to other widget in parent.
        if self.keynav_failed(gtk.DIR_UP):
            self.get_toplevel().set_focus_child(self)
            
        if self.select_start_index != self.select_end_index:
            self.clear_select_status()
        insert = self.buffer.get_iter_at_mark(self.buffer.get_insert())
        offset = insert.get_line_offset()   # get current line offset character
        insert.backward_line()
        line_len = insert.get_chars_in_line()
        if offset <= line_len:
            insert.set_line_offset(offset)
        else:
            insert.set_line_offset(line_len-1)
        self.buffer.move_mark_by_name("insert", insert)
        self.buffer.move_mark_by_name("selection_bound", insert)
        self.queue_draw()

    def move_to_down(self):
        '''
        Forward cursor one line.
        '''
        # Avoid change focus to other widget in parent.
        if self.keynav_failed(gtk.DIR_DOWN):
            self.get_toplevel().set_focus_child(self)
            
        if self.select_start_index != self.select_end_index:
            self.clear_select_status()
        insert = self.buffer.get_iter_at_mark(self.buffer.get_insert())
        offset = insert.get_line_offset()
        insert.forward_line()
        line_len = insert.get_chars_in_line()
        if offset <= line_len:
            insert.set_line_offset(offset)
        else:
            insert.set_line_offset(line_len-1) 
        self.buffer.move_mark_by_name("insert", insert)
        self.buffer.move_mark_by_name("selection_bound", insert)
        self.queue_draw()
            
    def select_to_left(self):
        '''
        Select text to left char.
        '''
        insert = self.buffer.get_iter_at_mark(self.buffer.get_insert())
        insert.backward_char()
        self.buffer.move_mark_by_name("insert", insert)
        self.queue_draw()
        
    def select_to_right(self):
        '''
        Select text to right char.
        '''
        insert = self.buffer.get_iter_at_mark(self.buffer.get_insert())
        insert.forward_char()
        self.buffer.move_mark_by_name("insert", insert)
        self.queue_draw()
        
    def select_to_up(self):
        '''
        select text to up line
        '''
        # Avoid change focus to other widget in parent.
        if self.keynav_failed(gtk.DIR_UP):
            self.get_toplevel().set_focus_child(self)
            
        if self.select_start_index != self.select_end_index:
            self.clear_select_status()
        insert = self.buffer.get_iter_at_mark(self.buffer.get_insert())
        offset = insert.get_line_offset()
        insert.backward_line()
        line_len = insert.get_chars_in_line()
        if offset <= line_len:
            insert.set_line_offset(offset)
        else:
            insert.set_line_offset(line_len-1)
        self.buffer.move_mark_by_name("insert", insert)
        self.queue_draw()

    def select_to_down(self):
        '''
        select text to down line
        '''
        # Avoid change focus to other widget in parent.
        if self.keynav_failed(gtk.DIR_DOWN):
            self.get_toplevel().set_focus_child(self)
            
        if self.select_start_index != self.select_end_index:
            self.clear_select_status()
        insert = self.buffer.get_iter_at_mark(self.buffer.get_insert())
        offset = insert.get_line_offset()
        insert.forward_line()
        line_len = insert.get_chars_in_line()
        if offset <= line_len:
            insert.set_line_offset(offset)
        else:
            insert.set_line_offset(line_len-1)
        self.buffer.move_mark_by_name("insert", insert)
        self.queue_draw()
    
    def select_to_start(self):
        '''
        Select text to start position.
        '''
        insert = self.buffer.get_iter_at_mark(self.buffer.get_insert())
        insert.set_line_offset(0)
        self.buffer.move_mark_by_name("insert", insert)
        self.queue_draw()
        
    def select_to_end(self):
        '''
        Select text to end position.
        '''
        insert = self.buffer.get_iter_at_mark(self.buffer.get_insert())
        insert.forward_to_line_end()
        self.buffer.move_mark_by_name("insert", insert)
        self.queue_draw()

    def xy_to_iter(self, x, y):
        '''from xy get iter'''
        index = self.__layout.xy_to_index(x*pango.SCALE, y*pango.SCALE)
        layout_iter = self.__layout.get_iter()
        offset = 0
        while layout_iter.get_index() != index[0]:
            layout_iter.next_char()
            offset += 1
        insert = self.buffer.get_iter_at_mark(self.buffer.get_insert())
        insert.set_offset(offset)
        return insert

    def handle_button_press(self, widget, event):
        '''
        Internal function to handle button press.
        '''
        # Get input focus.
        self.grab_focus()
        # Hide right menu immediately.
        self.right_menu.hide()
        # Select all when double click left button.
        if is_double_click(event):
            self.double_click_flag = True
            self.select_all()
        # Show right menu when click right button.
        elif is_right_button(event):
            if self.right_menu_visible_flag:
                (wx, wy) = self.window.get_root_origin()
                (cx, cy, modifier) = self.window.get_pointer()
                self.right_menu.show((cx + wx, cy + wy))
        # Change cursor when click left button.
        elif is_left_button(event):
            #print "clicked"
            self.left_click_flag = True
            self.left_click_coordindate = (event.x, event.y)
            #print "coord", self.left_click_coordindate
            xy = map(int, self.left_click_coordindate)
            insert = self.xy_to_iter(*xy)
            self.buffer.move_mark_by_name("insert", insert)
            self.buffer.move_mark_by_name("selection_bound", insert)
            self.drag_start_index = self.get_index_at_event(widget, event)
            self.queue_draw()

    def motion_notify_entry(self, widget, event):
        '''
        Internal callback for `motion-notify-event` signal.
        '''
        if not self.double_click_flag and self.left_click_flag:
            xy = map(int, [event.x, event.y])
            insert = self.xy_to_iter(*xy)
            self.buffer.move_mark_by_name("selection_bound", insert)
            self.queue_draw()    

gobject.type_register(TextView)
if __name__ == '__main__':
    #RootWindow().show()
    #TextWindow().show()
    RightMenu().show((100, 100))
    gtk.main()
