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
from dtk.ui.button import ImageButton, ToggleButton
from dtk.ui.window import Window
#from dtk.ui.line import VSeparator
from dtk.ui.label import Label
from dtk.ui.box import EventBox
from dtk.ui.color_selection import ColorSelectDialog, ColorButton
from dtk.ui.dialog import SaveFileDialog
import dtk.ui.constant
from lang import __
import utils
import gtk
from constant import *


class Toolbar():
    ''' Toolbar window'''
    def __init__(self, parent=None, screenshot=None):
        self.screenshot = screenshot
        self.win = screenshot.window

        toolbar_padding_x = 5
        toolbar_padding_y = 2
        toolbar_icon_width = toolbar_icon_height = 28
        toolbar_icon_num = 10
        self.window = Window(window_type=gtk.WINDOW_POPUP)
        self.window.set_keep_above(True)
        self.window.set_decorated(False)
        self.window.set_resizable(False)
        self.window.set_transient_for(parent)
        #self.window.set_default_size(284, 32)
        #self.window.set_position(gtk.WIN_POS_CENTER_ALWAYS)
        #self.window.connect("size-allocate", lambda w, a: updateShape(w, a, 2))
        #self.window.connect("expose-event", lambda w, e: exposeBackground(w, e, appTheme.getDynamicPixbuf("bg.png")))
        self.window.set_size_request(
            toolbar_icon_width * toolbar_icon_num + toolbar_padding_x * 2,
            toolbar_icon_height + toolbar_padding_y * 2)

        self.toolbox = gtk.HBox(False, 2)
        self.window.window_shadow.set(0.5, 0.5, 0, 0)
        self.window.window_shadow.set_padding(toolbar_padding_y + 2, toolbar_padding_y, toolbar_padding_x, toolbar_padding_x)
        self.window.window_frame.add(self.toolbox)

        self._toggle_buton_list = []
        self.create_toggle_button("rect", ACTION_RECTANGLE, __("Tip draw rectangle"))
        self.create_toggle_button("ellipse", ACTION_ELLIPSE, __("Tip draw ellipse"))
        self.create_toggle_button("arrow",ACTION_ARROW, __("Tip draw arrow"))
        self.create_toggle_button("line",ACTION_LINE, __("Tip draw line"))
        self.create_toggle_button("text",ACTION_TEXT, __("Tip draw Text"))

        button = ImageButton(
            app_theme.get_pixbuf("action/sep.png"),
            app_theme.get_pixbuf("action/sep.png"),
            app_theme.get_pixbuf("action/sep.png"))
        self.toolbox.pack_start(button)
        #self.toolbox.pack_start(VSeparator())

        self.create_button("undo", __("Tip undo"))
        self.create_button("save", __("Tip save"))
        
        button = ImageButton(
            app_theme.get_pixbuf("action/sep.png"),
            app_theme.get_pixbuf("action/sep.png"),
            app_theme.get_pixbuf("action/sep.png"))
        self.toolbox.pack_start(button)
        #self.toolbox.pack_start(VSeparator())

        self.create_button("cancel", __("Tip cancel"))
        self.create_button("finish", __("Tip finish"))

        if self.screenshot:
            self._button_clicked_cb = {         # TODO 要修改
                'undo': self.screenshot.undo,
                #'save': self.screenshot.saveSnapshotToFile,
                'save': self._save_to_file,
                'cancel': self.win.quit,
                'finish': self.screenshot.saveSnapshot}

    def create_toggle_button(self, name, action, text=''):
        ''' make a togglebutton '''
        button = ToggleButton(
            app_theme.get_pixbuf("action/" + name + "_normal.png"),
            app_theme.get_pixbuf("action/" + name + "_hover.png"),
            app_theme.get_pixbuf("action/" + name + "_press.png"))
        button.connect("pressed", self._toggle_button_pressed)
        button.connect("toggled", self._toggle_button_toggled, action)
        button.connect("released", self._toggle_button_released)
        button.connect("enter-notify-event", self._show_tooltip, text)
        button.set_name(name)
        self.toolbox.pack_start(button)
        self._toggle_buton_list.append(button)

    def create_button(self, name, text=''):
        ''' make a button '''
        button = ImageButton(
            app_theme.get_pixbuf("action/" + name + "_normal.png"),
            app_theme.get_pixbuf("action/" + name + "_hover.png"),
            app_theme.get_pixbuf("action/" + name + "_press.png"))
        button.connect("enter-notify-event", self._show_tooltip, text)
        button.connect("clicked", self._button_clicked, name)
        self.toolbox.pack_start(button)

    def _show_tooltip(self, widget, event, text):
        '''Create help tooltip.'''
        widget.set_has_tooltip(True)
        widget.set_tooltip_text(text)
        widget.trigger_tooltip_query()

    def _button_clicked(self, widget, name):
        ''' button clicked '''
        if self.screenshot is None:
            return
        self._button_clicked_cb[name](widget)

    def _toggle_button_released(self, widget):
        ''' toggle button pressed '''
        if self.screenshot is None:
            return
        self.screenshot.isToggled = False
        for each in self._toggle_buton_list:
            if each.get_active():
                self.screenshot.isToggled = True

    def _toggle_button_pressed(self, widget):
        ''' toggle button pressed '''
        for each in self._toggle_buton_list:
            if each == widget:
                continue
            each.set_active(False)

    def _toggle_button_toggled(self, widget, action):
        ''' toggle button toggled'''
        if self.screenshot is None:
            return
        if widget.get_active():
            self.screenshot.set_action_type(action)
            self.win.show_colorbar()
            self.win.adjust_colorbar()
        else:
            self.win.hide_colorbar()
            if not self.screenshot.action_list and not self.screenshot.text_action_list and self.screenshot.show_toolbar_flag and not self.screenshot.window_flag:
                self.screenshot.set_action_type(ACTION_SELECT)
            elif self.screenshot.action_list and self.screenshot.isToggled or self.screenshot.text_action_list:
                self.screenshot.set_action_type(None)
    
    def set_button_active(self, name, state):
        '''set button active'''
        for each in self._toggle_buton_list:
            if name == each.get_name():
                each.set_active(state)
                break
    
    def _save_to_file(self, widget):
        ''' save to file '''
        SaveFileDialog('', self.screenshot.window.window, ok_callback=self._save_to_file_cb)

    def _save_to_file_cb(self, filename):
        ''' save file dialog ok_callback'''
        print "save", filename
    
    def set_all_inactive(self):
        '''set all button inactive'''
        for each in self._toggle_buton_list:
            each.set_active(False)
    
    def show(self):
        ''' show the toolbar '''
        if not self.window.get_visible():
            self.window.show_window()

    def hide(self):
        '''hide the toolbar'''
        if self.window.get_visible():
            self.window.hide_all()

class Colorbar():
    ''' Colorbar window '''
    def __init__(self, parent=None, screenshot=None):
        self.screenshot = screenshot
        self.win = self.screenshot.window
        
        padding_x = 5
        padding_y = 4
        icon_width = icon_height = 28
        #color_num = 9
        
        self.window = Window(window_type=gtk.WINDOW_POPUP)
        self.window.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_DIALOG)
        self.window.set_keep_above(True)
        self.window.set_transient_for(parent)
        
        self.window.set_decorated(False)
        self.window.set_resizable(False)
        self.window.set_default_size(100, 24)
        #self.window.set_position(gtk.WIN_POS_CENTER_ALWAYS)
        self.window.set_size_request(-1, icon_height + padding_y * 2)

        self.box = gtk.HBox(False, 4)
        self.size_box = gtk.HBox()
        self.dynamic_box = gtk.HBox()

        self.window.window_shadow.set(0.5, 0.5, 0, 0)
        self.window.window_shadow.set_padding(padding_y, padding_y, padding_x, padding_x)
        self.window.window_frame.add(self.box)

        self.create_size_button("small", 2)
        self.create_size_button("normal", 3)
        self.create_size_button("big", 5)

        self.size_align = gtk.Alignment()
        self.size_align.set(0.5,0.5,0,0)
        self.size_align.set_padding(2, 1, 0, 0)
        self.size_align.add(self.size_box)
        #self.dynamic_box.pack_start(self.size_align)
        self.box.pack_start(self.dynamic_box)
        
        # font select
        self.font_label = Label("Sans 10",enable_select=False, text_x_align=dtk.ui.constant.ALIGN_MIDDLE)
        self.font_label.connect("button-press-event", self._select_font_event) 
        self.font_label.connect("enter-notify-event", lambda w, e: utils.setCursor(w, gtk.gdk.HAND2))
        self.font_label.connect("leave-notify-event", lambda w, e: utils.setDefaultCursor(w))
        self.font_label.set_size_request(100, -1)
        #self.dynamic_box.pack_start(self.font_label)

        button = ImageButton(
            app_theme.get_pixbuf("action/color_sep.png"),
            app_theme.get_pixbuf("action/color_sep.png"),
            app_theme.get_pixbuf("action/color_sep.png"))
        self.box.pack_start(button)

        # color select
        self.color_select = gtk.EventBox()
        #self.color_select = ColorButton()

        self.box.pack_start(self.color_select)
        #self.color_select.set_border_width(2)
        self.color_select.set_events(gtk.gdk.BUTTON_PRESS_MASK)
        self.color_select.set_size_request(28,28)
        self.color_select.set_app_paintable(True)
        self.color_select.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("#FF0000"))
        self.color_select.connect('expose-event', self._color_select_expose)
        self.color_select.connect('button-press-event', self._select_color_event)
        self.color_select.connect("enter-notify-event", lambda w, e: utils.setCursor(w, gtk.gdk.HAND2))
        self.color_select.connect("leave-notify-event", lambda w, e: utils.setDefaultCursor(w))
        
        # color button
        self.vbox = gtk.VBox(False, 2)
        self.above_hbox = gtk.HBox(False, 2)
        self.below_hbox = gtk.HBox(False, 2)
        self.color_map = {
            'black'       : "#000000",
            'gray_dark'   : "#808080",
            'red_dark'    : "#800000",
            'yellow_dark' : "#808000",
            'green_dark'  : "#008000",
            'blue_dark'   : "#000080",
            'pink_dark'   : "#800080",
            'wathet_dark' : "#008080",
            'white'       : "#FFFFFF",
            'gray'        : "#C0C0C0",
            'red'         : "#FF0000",
            'yellow'      : "#FFFF00",
            'green'       : "#00FF00",
            'blue'        : "#0000FF",
            'pink'        : "#FF00FF",
            'wathet'      : "#00FFFF"}
        i = 0
        keys = self.color_map.keys()
        for name in keys:
            if i < len(keys)/2:
                self.create_color_button(self.above_hbox, name)
            else:
                self.create_color_button(self.below_hbox, name)
            i += 1
        self.vbox.pack_start(self.above_hbox)
        self.vbox.pack_start(self.below_hbox)
        self.box.pack_start(self.vbox)

    def create_color_button(self, box, name):
        ''' create color button'''
        button = ImageButton(
            app_theme.get_pixbuf("color/" + name + ".png"),
            app_theme.get_pixbuf("color/" + name + "_hover.png"),
            app_theme.get_pixbuf("color/" + name + "_hover.png"))
        button.connect('pressed', self._color_button_pressed, name) 
        box.pack_start(button)

    def create_image_button(self, name):
        '''create ImageButton'''
        button = ImageButton(
            app_theme.get_pixbuf("action/" + name + ".png"),
            app_theme.get_pixbuf("action/" + name + "_hover.png"),
            app_theme.get_pixbuf("action/" + name + "_press.png"))
        return button

    def create_size_button(self, name, index):
        ''' create size button '''
        button = self.create_image_button(name)
        button.connect("pressed", self._size_button_pressed, index)
        self.size_box.pack_start(button)

    def _select_font_event(self, widget, event, data=None):
        ''' select font '''
        if self.screenshot is None:
            return
        self.win.hide_toolbar()
        self.win.hide_colorbar()
        font_dialog = gtk.FontSelectionDialog("font select")
        #font_dialog.set_skip_taskbar_hint(True)
        #if self.showTextWindowFlag:
            #self.fontDialog.set_transient_for(self.textWindow)
        #else:
        font_dialog.set_transient_for(self.win.window)
        font_dialog.set_font_name(widget.text)
        font_dialog.connect("response", self._font_dialog_response)
        font_dialog.set_modal(True)
        font_dialog.show_all()

    def _font_dialog_response(self, widget, response):
        if response == gtk.RESPONSE_OK:
            self.screenshot.font_name = widget.get_font_name()
            self.font_label.set_text(self.screenshot.font_name)
        self.win.show_toolbar()
        self.win.show_colorbar()
        widget.destroy()
        #self.win.window.queue_draw()

    def _color_select_expose(self, widget, event, data=None):
        '''set colorBox border '''
        (x, y, width, height, depth) = widget.window.get_geometry() 
        cr = widget.window.cairo_create()
        cr.set_line_width(2)
        cr.rectangle(0,0,width, height)
        cr.set_source_rgb(0, 0, 0)
        cr.stroke()
        cr.rectangle(2,2,width-4, height-4)
        cr.set_line_width(1)
        cr.set_source_rgb(0xff, 0xff, 0xff)
        cr.stroke()

    def _select_color_event(self, widget, event, data=None):
        ''' select color '''
        self.win.hide_toolbar()
        self.win.hide_colorbar()
        color = ColorSelectDialog(confirm_callback=self._select_color)
        color.set_transient_for(self.win.window)
        #color.set_keep_above(True)
        color.show_all()

    def _select_color(self, color_hex):
        ''' confirm select color '''
        self.color_select.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse(color_hex))
        if self.screenshot is None:
            return
        self.screenshot.action_color = color_hex
        self.win.show_toolbar()
        self.win.show_colorbar()

    def _color_button_pressed(self, widget, name):
        ''' color button pressed'''
        self.color_select.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse(self.color_map[name]))
        if self.screenshot is None:
            return
        self.screenshot.action_color = self.color_map[name]

    def _size_button_pressed(self, widget, index):
        ''' size button pressed'''
        if self.screenshot is None:
            return
        self.screenshot.iconIndex = index
        self.screenshot.actionSize = index

    def show(self):
        ''' show the colorbar'''
        if self.screenshot.action == ACTION_TEXT:
            if self.size_align in self.dynamic_box.get_children():
                self.dynamic_box.remove(self.size_align)
            if self.font_label not in self.dynamic_box.get_children():
                self.dynamic_box.add(self.font_label)
        else:
            if self.font_label in self.dynamic_box.get_children():
                self.dynamic_box.remove(self.font_label)
            if self.size_align not in self.dynamic_box.get_children():
                self.dynamic_box.add(self.size_align)
        if not self.window.get_visible():
            self.window.show_window()

    def hide(self):
        '''hide the toolbar'''
        if self.window.get_visible():
            self.window.hide_all()

if __name__ == '__main__':
    #Toolbar().show()
    Colorbar().show()
    gtk.main()
