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

from theme import app_theme, theme_cursor
from dtk.ui.window import Window
from dtk.ui.entry import Entry 
from dtk.ui.scrolled_window import ScrolledWindow 
from dtk.ui.keymap import get_keyevent_name
from collections import namedtuple
from draw import *
from constant import *
from lang import __
import status
import gtk


Magnifier = namedtuple('Magnifier', 'x y size_content tip rgb')

class RootWindow():
    ''' background window'''
    def __init__(self, screenshot=None):
        self.screenshot = screenshot
        self.frame_border = 2
        self.drag_point_radius = 4
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
        self.window.connect("destroy", self.quit)
        #self.window.connect("expose-event", lambda w, e: self.getCurrentCoord(w))   # 获取当前坐标
        #self.window.connect("expose-event", self._expose_event)
        self.window.connect("button-press-event", self._button_press_event)
        
        self.window.connect("button-press-event", self._button_double_clicked)
        self.window.connect("button-release-event", self._button_release_event)
        self.window.connect("motion-notify-event", self._motion_notify_event)
        self.window.connect("key-press-event", self._key_press_event)
        
        self.draw_area = gtk.DrawingArea()
        self.draw_area.connect("expose-event", self._draw_expose)
        self.window.add(self.draw_area)
        self.magnifier = None
        
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
        cr = widget.window.cairo_create()
        # draw background
        if self.screenshot:
            cr.set_source_pixbuf(self.screenshot.desktop_background, 0, 0)
            cr.paint()
        # draw mask
        self._draw_mask(cr)
        # toolbar
        if self.screenshot.show_toolbar_flag:
            self.adjust_toolbar()
            self.adjust_colorbar()
        # Draw action list.
        for action in self.screenshot.action_list:
            if action != None:
                action.expose(cr)
        # Draw current action.
        if self.screenshot.current_action is not None:
            self.screenshot.current_action.expose(cr)

        # ACTION_WINDOW draw magnifier and window frame
        if self.magnifier and self.screenshot.action == ACTION_WINDOW:
            self._draw_magnifier(cr)
            self._draw_window_rectangle(cr)
        # action is not ACTION_WINDOW draw frame
        if self.screenshot.action != ACTION_WINDOW and self.screenshot.rect_width:
            self._draw_frame(cr)
            self._draw_drag_point(cr)
            # draw size tip
            if self.screenshot.y - 35 > 0:
                draw_round_text_rectangle(cr, self.screenshot.x + 5, self.screenshot.y - 35,
                    85, 30, 7,
                    '%d x %d' % (fabs(self.screenshot.rect_width), fabs(self.screenshot.rect_height)), 0.7)
            elif self.screenshot.action in [None, ACTION_SELECT, ACTION_WINDOW, ACTION_INIT]:
                draw_round_text_rectangle(cr, self.screenshot.x + 5 , self.screenshot.y + 5 ,
                    85, 30, 7,
                    '%d x %d' % (fabs(self.screenshot.rect_width), fabs(self.screenshot.rect_height)), 0.7)
        # update text action info
        for each_text_action in self.screenshot.text_action_list:
            self.screenshot.text_action_info[each_text_action] = each_text_action.get_layout_info()
        # draw current text layout
        if self.screenshot.draw_text_layout_flag and self.screenshot.current_text_action:
            draw_alpha_rectangle(cr, *self.screenshot.current_text_action.get_layout_info())

    def _expose_event(self, widget, event):
        ''' expose '''
        if self.screenshot is None:
            return False
    
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
            # edit text
            if self.screenshot.text_drag_flag:
                text_buffer = self.screenshot.text_window.entry.get_buffer()
                text_buffer.set_text(self.screenshot.current_text_action.get_content())
                self.screenshot.action_color = self.screenshot.current_text_action.get_color()
                self.screenshot.font_name = self.screenshot.current_text_action.get_fontname()
                #modifyBackground(self.colorBox, self.actionColor)
                self.screenshot.colorbar.color_select.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse(self.screenshot.action_color))
                self.screenshot.colorbar.font_label.set_text(self.screenshot.font_name)
                
                # set action ACTION_TEXT
                self.screenshot.toolbar.set_button_active("text", True)
                self.show_text_window((ex, ey))
                self.screenshot.text_modify_flag = True
            # save snapshot
            if self.screenshot.action == ACTION_SELECT and self.screenshot.x < ex < self.screenshot.x + self.screenshot.rect_width and self.screenshot.y < ey < self.screenshot.y + self.screenshot.rect_height:
                self.screenshot.save_snapshot()
    
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
        if event.is_modifier:
            return
        key = get_keyevent_name(event)
        if key in self.hotkey_map:
            self.hotkey_map[key]()
    
    def quit(self, widget=None):
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
        
        draw_font(cr, self.magnifier.size_content, 3.0, "#FFFFFF", x + offset_x, y + offset_y + pixbuf_heigth + 4)
        draw_font(cr, self.magnifier.rgb, 3.0, "#FFFFFF", x + offset_x, y + offset_y + pixbuf_heigth + 7.5)
        draw_font(cr, self.magnifier.tip, 3.0, "#FFFFFF", x + offset_x, y + offset_y + pixbuf_heigth + 11)
        cr.restore()
    
    def refresh(self):
        ''' refresh this window'''
        #self.window.queue_draw()
        self.draw_area.queue_draw()

    def _draw_background(self, cr):
        ''' draw background '''
        cr.set_source_pixbuf(self.pix, 0, 0)
        cr.paint()

    def _draw_mask(self, cr):
        '''draw mask'''
        if self.screenshot is None:
            return
        screenshot = self.screenshot
        #cr = self._cr
        # Adjust value when create selection area.
        if screenshot.rect_width > 0:
            x = screenshot.x
            rect_width = screenshot.rect_width
        else:
            x = screenshot.x + screenshot.rect_width
            rect_width = fabs(screenshot.rect_width)

        if screenshot.rect_height > 0:
            y = screenshot.y
            rect_height = screenshot.rect_height
        else:
            y = screenshot.y + screenshot.rect_height
            rect_height = fabs(screenshot.rect_height)
        
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
        # Draw left top corner.
        cr.arc(screenshot.x, screenshot.y, self.drag_point_radius, 0, 2 * pi)
        cr.fill()
        # Draw right top corner.
        cr.arc(screenshot.x + screenshot.rect_width, screenshot.y, self.drag_point_radius, 0, 2 * pi)
        cr.fill()
        # Draw left bottom corner.
        cr.arc(screenshot.x, screenshot.y + screenshot.rect_height, self.drag_point_radius, 0, 2 * pi)
        cr.fill()
        # Draw right bottom corner.
        cr.arc(screenshot.x + screenshot.rect_width, screenshot.y + screenshot.rect_height, self.drag_point_radius, 0, 2 * pi)
        cr.fill()
        # Draw top side.
        cr.arc(screenshot.x + screenshot.rect_width / 2, screenshot.y, self.drag_point_radius, 0, 2 * pi)
        cr.fill()
        # Draw bottom side.
        cr.arc(screenshot.x + screenshot.rect_width / 2, screenshot.y + screenshot.rect_height, self.drag_point_radius, 0, 2 * pi)
        cr.fill()
        # Draw left side.
        cr.arc(screenshot.x, screenshot.y + screenshot.rect_height / 2, self.drag_point_radius, 0, 2 * pi)
        cr.fill()
        # Draw right side.
        cr.arc(screenshot.x + screenshot.rect_width, screenshot.y + screenshot.rect_height / 2, self.drag_point_radius, 0, 2 * pi)
        cr.fill()

    def _draw_frame(self, cr):
        '''Draw frame.'''
        screenshot = self.screenshot
        cr.set_source_rgb(*self.__frame_color)
        cr.set_line_width(self.frame_border)
        cr.rectangle(screenshot.x, screenshot.y, screenshot.rect_width, screenshot.rect_height)
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
        
        # Calcuate drag position.
        if is_in_rect((ex, ey), (screenshot.x, screenshot.y, screenshot.rect_width, screenshot.rect_height)):
            return DRAG_INSIDE
        elif is_collide_rect((ex, ey), (tlX, tlY, pWidth, pHeight)):
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
        else:
            return DRAG_OUTSIDE
        
    def adjust_toolbar(self):
        '''Adjust toolbar position.'''
        screenshot = self.screenshot
        (x, y, screenshot.toolbar_width, screenshot.toolbar_height, depth) = screenshot.toolbar.window.window.get_geometry()
        colorbarHeight = 32
        
        screenshot.toolbarX = (screenshot.x + screenshot.rect_width - screenshot.toolbar_width, screenshot.toolbarOffsetX)[screenshot.x + screenshot.rect_width - screenshot.toolbar_width < screenshot.toolbarOffsetX]
        
        if screenshot.y + screenshot.rect_height + screenshot.toolbarOffsetY + screenshot.toolbar_height + colorbarHeight + 5 < screenshot.height:
            screenshot.toolbarY = screenshot.y + screenshot.rect_height + screenshot.toolbarOffsetY
        elif screenshot.y - screenshot.toolbarOffsetY - screenshot.toolbar_height -colorbarHeight - 5 > 0:
            screenshot.toolbarY = screenshot.y - screenshot.toolbarOffsetY - screenshot.toolbar_height
        else:
            screenshot.toolbarY = screenshot.y + screenshot.toolbarOffsetY
        screenshot.toolbar.window.move(int(screenshot.toolbarX), int(screenshot.toolbarY))
        
    def show_toolbar(self):
        '''Show toolbar.'''
        self.screenshot.show_toolbar_flag = True
        self.screenshot.toolbar.show()
        
    def hide_toolbar(self):
        '''Hide toolbar.'''
        self.screenshot.show_toolbar_flag = False
        self.screenshot.toolbar.hide()

    def show_colorbar(self):
        '''show colorbar '''
        self.screenshot.show_colorbar_flag = True
        self.screenshot.colorbar.show()
    
    def hide_colorbar(self):
        '''hide colorbar'''
        self.screenshot.show_colorbar_flag = False
        self.screenshot.colorbar.hide()
    
    def adjust_colorbar(self):
        '''Adjust Colorbar position '''
        screenshot = self.screenshot
        if screenshot.toolbarY < screenshot.y:
            colorbarY = screenshot.toolbarY - screenshot.toolbar_height - 8
        else:
            colorbarY = screenshot.toolbarY + screenshot.toolbar_height + 5
        colorbarX = screenshot.toolbarX
        screenshot.colorbar.window.move(int(colorbarX), int(colorbarY))

    def show_text_window(self, (ex, ey)):
        '''Show text window.'''
        offset = 5
        screenshot = self.screenshot
        screenshot.show_text_window_flag = True
        screenshot.text_window.window.move(ex, ey)
        screenshot.text_window.show()
        
    def hide_text_window(self):
        '''Hide text window.'''
        screenshot = self.screenshot
        screenshot.show_text_window_flag = False
        screenshot.text_window.set_text("")
        screenshot.text_window.hide()

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
        #self.entry = Entry()
        self.entry= gtk.TextView()           # TODO 输入框控件
        scroll_window.add_with_viewport(self.entry)
        #scroll_window.add(self.entry)
        #scroll_window.add_child(self.entry)
        #scrollWindow.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        #scrollWindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC) 
        self.entry.set_size_request(300, 60)

        self.window.window_frame.add(scroll_window)
    
    def get_text(self):                 # 获取输入框文字
        '''Get input text.'''
        text_buffer = self.entry.get_buffer()
        return (text_buffer.get_text(text_buffer.get_start_iter(), text_buffer.get_end_iter())).rstrip(" ")
        
    def set_text(self, text):
        '''Set text'''
        text_buffer = self.entry.get_buffer()
        text_buffer.set_text(text)
    
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
