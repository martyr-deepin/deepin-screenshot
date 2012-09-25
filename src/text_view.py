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
from dtk.ui.entry import Entry
import dtk.ui.constant as dtk_constant
import gtk
import gobject
import pango
import pangocairo
import cairo
from dtk.ui.utils import (cairo_state, color_hex_to_cairo,
                          is_left_button, is_right_button, is_double_click, )

DEFAULT_FONT = dtk_constant.DEFAULT_FONT
DEFAULT_FONT_SIZE = dtk_constant.DEFAULT_FONT_SIZE

class TextView(Entry):
    '''TextView'''
    def __init__(self, content="", padding_x=5, padding_y=2,
                 text_color="#000000",
                 text_select_color="#FFFFFF",
                 background_select_color="#0000F0",
                 font=DEFAULT_FONT, font_size=DEFAULT_FONT_SIZE):
        super(TextView, self).__init__(content, padding_x, padding_y, 
              text_color, text_select_color, background_select_color, font_size)
        self.font_type = font
        self.font = pango.FontDescription("%s %d" % (font, font_size))
        # press Return | KP_Enter
        self.keymap["KP_Enter"] = self.press_return
        self.keymap["Up"] = self.move_to_up
        self.keymap["Down"] = self.move_to_down
        self.keymap["Shift + Up"] = self.select_to_up
        self.keymap["Shift + Down"] = self.select_to_down
        self.keymap["Ctrl + A"] = self.select_all
        self.keymap["Ctrl + X"] = self.cut_to_clipboard
        self.keymap["Ctrl + C"] = self.copy_to_clipboard
        self.keymap["Ctrl + V"] = self.paste_from_clipboard
        self.connect("press-return", self.entry_press_return)
        self.buffer = gtk.TextBuffer()
        
        surface = cairo.ImageSurface(cairo.FORMAT_RGB24, 0, 0) 
        cr = cairo.Context(surface)
        pango_cr = pangocairo.CairoContext(cr)
        self._layout = pango_cr.create_layout()
        self._layout.set_font_description(self.font)
        self._layout.set_alignment(pango.ALIGN_LEFT)
        self._layout.set_wrap(pango.WRAP_WORD_CHAR)

        self.layout_width = self.layout_height = 0    # widget width and height
        self._layout_width = -1
        self.background_dash = None

        self.set_text(content)
        self.adjust_size()

    def get_text(self):
        '''get text'''
        return self.buffer.get_text(*self.buffer.get_bounds())

    def set_text(self, text):
        '''set text'''
        if text is None:
            return 
        if not isinstance(text, unicode):
            try:
                text = text.decode('utf-8')
            except Exception, e:
                pass
        text = text.encode('utf-8')
        with self.monitor_entry_content():
            self.buffer.set_text(text)
            e = self.buffer.get_end_iter()
            insert = self.buffer.get_iter_at_mark(self.buffer.get_insert())
            self.cursor_index = insert.get_offset()     # get layout cursor index
            self._layout.set_text(text)
            self.count_size()

            self.queue_draw()

    def set_width(self, width):
        '''set layout width'''
        if width > 0:
            self._layout_width = width * pango.SCALE
        else:
            self._layout_width = -1
        self._layout.set_width(self._layout_width)

    def get_width(self):
        '''get layout width '''
        return self._layout_width

    def get_size(self):
        '''get text size'''
        self.count_size()
        return (self.layout_width, self.layout_height)

    def set_layout(self, layout):
        '''set layout'''
        self._layout = layout

    def get_layout(self):
        '''get layout'''
        return self._layout

    def get_buffer(self):
        '''get buffer'''
        return self.buffer

    def set_buffer(self, buf):
        '''set buffer'''
        self.buffer = buf

    def set_font_size(self, size):
        '''set font size'''
        self.font_size = size
        self.font = pango.FontDescription("%s %d" % (self.font_type, self.font_size))
        self._layout.set_font_description(self.font)
        self.adjust_size()

    def get_font_size(self):
        '''get font size'''
        return self.font_size

    def set_text_color(self, color):
        '''set text color'''
        self.text_color = color

    def get_text_color(self):
        '''get text color'''
        return self.text_color

    def set_background_dash(self, dash=None):
        '''set the cairo dash of background'''
        self.background_dash = dash

    def count_size(self):
        '''count widget size'''
        self._layout.set_text(self.get_text())
        (self.layout_width, self.layout_height) = self._layout.get_pixel_size()

    def adjust_size(self):
        '''set widget size'''
        self.count_size()
        allocation = self.allocation
        if self.layout_width < 10:
            self.layout_width = 10
        if self.layout_width < allocation.width:
            self.layout_width = allocation.width
        if self.layout_height < allocation.height:
            self.layout_height = allocation.height
        self.set_size_request(self.layout_width+self.padding_x*2, self.layout_height+self.padding_y*2)
        new_allocation = gtk.gdk.Rectangle(allocation.x, allocation.y, self.layout_width, self.layout_height)
        self.set_allocation(new_allocation)

    def entry_press_return(self, widget):
        '''press return'''
        self.commit_entry('\n')

    def draw_entry_background(self, cr, rect):
        '''draw background '''
        x, y, w, h = rect.x, rect.y, rect.width, rect.height
        cr.set_source_rgba(1.0, 1.0, 1.0, 0.8)
        cr.rectangle(x, y, w, h)
        cr.fill()
        cr.set_source_rgba(0.0, 0.0, 0.0, 1.0)
        if self.background_dash:
            cr.set_dash(self.background_dash)
        cr.set_line_width(1)
        cr.rectangle(x, y, w, h)
        cr.stroke()
    
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
            context.update_layout(self._layout)
            context.show_layout(self._layout)
        # draw selection
        if not self.buffer.get_has_selection():
            return
        bounds = self.buffer.get_selection_bounds()
        self.draw_selection_lines(bounds[0], bounds[1], cr, x, y)

    def draw_entry_cursor(self, cr, rect):
        '''
        Internal function to draw entry cursor.
        '''
        if self.grab_focus_flag and not self.buffer.get_has_selection():
            # Init.
            x, y, w, h = rect.x, rect.y, rect.width, rect.height
            # Draw cursor.
            cr.set_source_rgb(*color_hex_to_cairo("#000000"))
            index = self.iter_to_index(self.buffer.get_iter_at_mark(self.buffer.get_insert()))
            pos = self.index_to_pos(index)
            cr.rectangle(pos[0]+x+self.padding_x, pos[1]+y+self.padding_y, 1, pos[3])
            cr.fill()
            # Tell input method follow cursor position
            self.im.set_cursor_location(gtk.gdk.Rectangle(pos[0]+x, pos[1]+y, 1, pos[3]))
    
    def draw_selection_lines(self, start, end, cr, x, y):
        '''draw selection line background'''
        cursor = start
        while cursor.in_range(start, end):
            self.draw_selection_index(cursor, cr, x, y)
            cursor.forward_char()
                
    def draw_selection_index(self, index, cr, x, y):
        '''draw selection iter background '''
        pos = self.index_to_pos(self.iter_to_index(index))
        cr.rectangle(pos[0]+x+self.padding_x, pos[1]+y+self.padding_y, pos[2], pos[3])
        # Draw selection background
        cr.set_source_rgb(*color_hex_to_cairo(self.background_select_color))
        cr.fill()
        # Create pangocairo context.
        context = pangocairo.CairoContext(cr)
        # Move text.
        cr.move_to(pos[0]+x+self.padding_x, pos[1]+y+self.padding_y)
        # Draw text.
        layout = self._layout.copy()
        index1 = index.copy()
        index1.forward_char()
        t = self.buffer.get_text(index, index1)
        layout.set_text(t)
        cr.set_source_rgb(*color_hex_to_cairo(self.text_select_color))
        context.update_layout(layout)
        context.show_layout(layout)

    def iter_to_index(self, iter):
        ''' textiter to index'''
        index = self.buffer.get_text(self.buffer.get_start_iter(), iter).__len__()
        return index

    def index_to_pos(self, index):
        '''index to pos'''
        pos = self._layout.index_to_pos(index)
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
        with self.monitor_entry_content():
            if self.buffer.get_has_selection():     # if has select, delete it
                self.buffer.delete_selection(True, self.is_editable())
            self.buffer.insert_at_cursor(input_text)
            self.adjust_size()
            self.queue_draw()

    def backspace(self):
        '''
        Do backspace action.
        '''        
        if not self.is_editable():
            return
        with self.monitor_entry_content():
            if self.buffer.get_has_selection():     # if has select, delete it
                self.buffer.delete_selection(True, self.is_editable())
            else:                                   # else delete the previous char
                self.buffer.backspace(self.buffer.get_iter_at_mark(self.buffer.get_insert()),
                    True, self.is_editable())
            self.adjust_size()
            self.queue_draw()

    def delete(self):
        '''
        Delete selected text.
        '''
        if not self.is_editable():
            return
        with self.monitor_entry_content():
            insert = self.buffer.get_iter_at_mark(self.buffer.get_insert())
            if insert.is_end():     # if is end, do none
                return
            if self.buffer.get_has_selection():
                self.buffer.delete_selection(True, self.is_editable())
                self.adjust_size()
                self.queue_draw()
            else:
                self.move_to_right()
                self.backspace()

    def select_all(self):
        '''
        Select all text of entry.
        '''
        self.buffer.select_range(*self.buffer.get_bounds())
        self.queue_draw()

    def cut_to_clipboard(self):
        '''
        Cut selected text to clipboard.
        '''
        self.buffer.cut_clipboard(gtk.Clipboard(), self.is_editable())
        self.adjust_size()
        if self.is_editable:
            self.emit("changed", self.get_text())
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
        if self.is_editable():
            with self.monitor_entry_content():
                clipboard = gtk.Clipboard()    
                clipboard.request_text(lambda clipboard, text, data: self.commit_entry(text))

    def move_to_start(self):
        '''
        Move cursor to start position of entry.
        '''
        insert = self.buffer.get_iter_at_mark(self.buffer.get_insert())
        insert.set_line_offset(0)
        self.buffer.move_mark_by_name("insert", insert)
        self.buffer.move_mark_by_name("selection_bound", insert)
        self.queue_draw()
        
    def move_to_end(self):
        '''
        Move cursor to end position of entry.
        '''
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
            
        insert = self.buffer.get_iter_at_mark(self.buffer.get_insert())
        offset = insert.get_line_offset()
        insert.forward_line()
        line_len = insert.get_chars_in_line()
        if offset <= line_len:
            insert.set_line_offset(offset)
        else:
            if insert.get_line() == self.buffer.get_line_count()-1:
                insert.set_line_offset(line_len) 
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
            
        insert = self.buffer.get_iter_at_mark(self.buffer.get_insert())
        offset = insert.get_line_offset()
        insert.forward_line()
        line_len = insert.get_chars_in_line()
        if offset <= line_len:
            insert.set_line_offset(offset)
        else:
            if insert.get_line() == self.buffer.get_line_count()-1:
                insert.set_line_offset(line_len) 
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
        index = self._layout.xy_to_index(x*pango.SCALE, y*pango.SCALE)
        layout_iter = self._layout.get_iter()
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
            self.left_click_flag = True
            self.left_click_coordindate = (event.x, event.y)
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
