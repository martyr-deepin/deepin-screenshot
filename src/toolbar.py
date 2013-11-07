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
from dtk.ui.button import ImageButton, ToggleButton, ComboButton
from dtk.ui.menu import Menu
from dtk.ui.window import Window
from dtk.ui.spin import SpinBox
from dtk.ui.group import ToggleButtonGroup, ToggleButtonItem
import dtk.ui.tooltip as Tooltip
from nls import _
import utils
import gtk
import config
from constant import *
from _share.config import OperateConfig


class Toolbar(object):
    ''' Toolbar window'''
    def __init__(self, parent=None, screenshot=None):
        '''
        init toolbar
        @param parent: the transient parent for this window
        @param screenshot: a Screenshot object
        '''
        self.screenshot = screenshot
        self.win = screenshot.window
        self.__config = OperateConfig()
        save_op = self.__config.get("save", "save_op")
        if save_op:
            self.screenshot.save_op_index = int(save_op)
        else:
            self.screenshot.save_op_index = SAVE_OP_AUTO

        #toolbar_padding_x = 15
        #toolbar_padding_y = 5
        #toolbar_icon_width = toolbar_icon_height = 28
        #toolbar_icon_num = 10
        #self.height = toolbar_icon_height + toolbar_padding_y * 2
        self.height = 30
        self.width = 279
        #self.width = 240

        self.window = Window(window_type=gtk.WINDOW_POPUP, shadow_visible=False)
        self.window.set_keep_above(True)
        self.window.set_decorated(False)
        self.window.set_transient_for(parent)

        self.toolbox = gtk.HBox(False, 6)
        toolbox_align = gtk.Alignment()
        toolbox_align.set(0, 0.5, 0, 0)
        toolbox_align.set_padding(2, 2, 11, 11)
        toolbox_align.add(self.toolbox)
        self.window.window_frame.pack_start(toolbox_align, True, True)
        #self.window.set_size_request(self.width, self.height)
        self.window.set_size_request(-1, self.height)

        self._toggle_button_list = []
        self.__button_accelerator_dict = {}
        self._toggle_button_group = ToggleButtonGroup([], 6)
        self.toolbox.pack_start(self._toggle_button_group)
        self.create_toggle_button("rect", ACTION_RECTANGLE, 0, _("Draw Rectangle"), "<Alt>1")
        self.create_toggle_button("ellipse", ACTION_ELLIPSE, 1, _("Draw Ellipse"), "<Alt>2")
        self.create_toggle_button("arrow",ACTION_ARROW, 2, _("Draw Arrow"), "<Alt>3")
        self.create_toggle_button("line",ACTION_LINE, 3, _("Draw Line"), "<Alt>4")
        self.create_toggle_button("text",ACTION_TEXT, 4, _("Draw Text"), "<Alt>5")

        self.create_button("undo", _("Undo"), "<Alt>6")

        if self.screenshot.is_subprocess:
            self.create_button("save", _("Save"), "<Alt>7")
        else:
            # pack save and list button
            save_combo_button = ComboButton(
                app_theme.get_pixbuf("action/save_normal.png"),
                app_theme.get_pixbuf("action/save_hover.png"),
                app_theme.get_pixbuf("action/save_press.png"),
                app_theme.get_pixbuf("action/save_normal.png"),
                app_theme.get_pixbuf("action/list_normal.png"),
                app_theme.get_pixbuf("action/list_hover.png"),
                app_theme.get_pixbuf("action/list_press.png"),
                app_theme.get_pixbuf("action/list_normal.png"),)
            save_combo_button.set_name("save")
            save_combo_button.connect("button-clicked", self._button_clicked, "save")
            save_combo_button.connect("arrow-clicked", self._list_menu_show)
            save_tip_text_list = ["Save automatically", "Save as", "Save to clipboard", "Save automatically to file and clipboard"]
            tip_text = save_tip_text_list[self.screenshot.save_op_index]
            save_combo_button.connect("enter-notify-event", self._show_tooltip, _(tip_text))
            self.toolbox.pack_start(save_combo_button)

        self.create_button("cancel", _("Cancel"), "<Alt>8")

        if not self.screenshot.is_subprocess:
            self.create_button("share", _("Share"), "<Alt>9")

        if self.screenshot:
            self._button_clicked_cb = {
                'undo': self.screenshot.undo,
                'save': self.save_operate,
                'cancel': self.win.quit,
                'share': self.share_picture}

    def create_toggle_button(self, name, action, index, text='', accel_key=None):
        '''
        create a togglebutton
        @param name: the button's name, a string
        @param action: one of ACTION Type Constants 
        @param index: the button's index in button list, an int num
        @param text: the button's tooltip text, a string
        '''
        button = ToggleButtonItem(
            (app_theme.get_pixbuf("action/" + name + "_normal.png"),
             app_theme.get_pixbuf("action/" + name + "_press.png"),
             app_theme.get_pixbuf("action/" + name + "_hover.png"),
             app_theme.get_pixbuf("action/" + name + "_press.png"), None),
            index, self._toggle_button_group.set_index, self._toggle_button_group.get_index)
        button.connect("pressed", self._toggle_button_pressed)
        button.connect("toggled", self._toggle_button_toggled, action)
        button.connect("enter-notify-event", self._show_tooltip, text)
        button.set_name(name)
        #self.toolbox.pack_start(button)
        self._toggle_button_group.pack_start(button)
        self._toggle_button_list.append(button)
        if accel_key:
            self.__button_accelerator_dict[gtk.accelerator_name(
                                           *gtk.accelerator_parse(accel_key))] = button

    def create_button(self, name, text='', accel_key=None):
        '''
        make a button
        @param name: the button's name, a string
        @param text: the button's tooltip text, a string
        '''
        button = ImageButton(
            app_theme.get_pixbuf("action/" + name + "_normal.png"),
            app_theme.get_pixbuf("action/" + name + "_hover.png"),
            app_theme.get_pixbuf("action/" + name + "_press.png"))
        button.connect("enter-notify-event", self._show_tooltip, text)
        button.connect("clicked", self._button_clicked, name)
        button.set_name(name)
        #button.set_size_request(28, 28)
        self.toolbox.pack_start(button)
        if accel_key:
            self.__button_accelerator_dict[gtk.accelerator_name(
                                           *gtk.accelerator_parse(accel_key))] = button
        return button

    def _show_tooltip(self, widget, event, text):
        '''the button enter-notify-event callback. Create help tooltip.'''
        #widget.set_has_tooltip(True)
        #widget.set_tooltip_text(text)
        #widget.trigger_tooltip_query()
        Tooltip.text(widget, text)

    def _list_menu_show(self, button, x, y, offset_x, offset_y):
        '''the combo button clicked callback. show combo_buton list menu'''
        menu_item = [
            (None, _("Save automatically"), self._list_menu_click, SAVE_OP_AUTO, button),
            (None, _("Save as"), self._list_menu_click, SAVE_OP_AS, button),
            (None, _("Save to clipboard"), self._list_menu_click, SAVE_OP_CLIP, button),
            (None, _("Save automatically to file and clipboard"), self._list_menu_click, SAVE_OP_AUTO_AND_CLIP, button)]
        # set current operate icon
        current_item = menu_item[self.screenshot.save_op_index] 
        menu_pixbuf = (
            app_theme.get_pixbuf("action/selected.png"),
            app_theme.get_pixbuf("action/selected_hover.png"),
            app_theme.get_pixbuf("action/selected.png"))
        menu_item[self.screenshot.save_op_index] = (menu_pixbuf, 
            current_item[1], current_item[2], current_item[3])
        self.combo_menu = Menu(menu_item, is_root_menu=True, 
            menu_item_select_color=app_theme.get_shadow_color("menu_item_select").get_color_info())
        self.set_all_inactive()
        self.combo_menu.show((x, y), (offset_x, offset_y))
    
    def _list_menu_click(self, save_op_index, button=None):
        '''list menu clicked callback'''
        self.screenshot.save_op_index = save_op_index
        self.__config.set("save", save_op=str(save_op_index))

        # reset the save button's tooltip
        if button:
            item = self.combo_menu.get_menu_items()[save_op_index]
            button.disconnect_by_func(self._show_tooltip)
            button.connect("enter-notify-event", self._show_tooltip, item.item[1])
            self.combo_menu.destroy()
        self.save_operate()

    def _button_clicked(self, widget, name):
        ''' button clicked callback '''
        if self.screenshot is None:
            return
        # save current input text
        if self.screenshot.show_text_window_flag:
            self.win.save_text_window()
        if name in self._button_clicked_cb:
            self._button_clicked_cb[name](widget)

    def _toggle_button_pressed(self, widget):
        ''' toggle button pressed callback '''
        # save current input text
        if self.screenshot.show_text_window_flag:
            self.win.save_text_window()
        widget.released()

    def _toggle_button_toggled(self, widget, action):
        ''' toggle button toggled callback'''
        if self.screenshot is None:
            return
        if widget.get_active():
            self.screenshot.set_action_type(action)
            self.win.set_cursor(action)
            self.win.show_colorbar()
            self.win.adjust_colorbar()
        elif widget.index == widget.get_index():
            self.win.set_cursor(None)
            self.win.hide_colorbar()
            if not self.screenshot.action_list and not self.screenshot.text_action_list and self.screenshot.show_toolbar_flag and not self.screenshot.window_flag:
                self.screenshot.set_action_type(ACTION_SELECT)
            elif self.screenshot.action_list:
                self.screenshot.set_action_type(None)
    
    def set_button_active(self, name, state):
        '''
        set button active
        @param name: the button's name which will set, a string type
        @param state: the state to set, True or False
        '''
        if self._toggle_button_group.is_active():
            button = self._toggle_button_list[self._toggle_button_group.get_index()]
            # if the button has been in this state, ignore
            if button.name == name:
                if button.get_active() == state:
                    return
            else:
                button.set_active(False)
                self._toggle_button_group.set_index(-1)
        i = 0
        for each in self._toggle_button_list:
            if name == each.get_name():
                each.set_active(state)
                self._toggle_button_group.set_index(i)
                break
            i += 1
    
    def has_button_active(self):
        '''
        is has one toggle button active
        @return: True if has one togglebutton active, otherwise False
        '''
        return self._toggle_button_group.is_active()
    
    def save_operate(self, widget=None):
        '''do save operate'''
        screenshot = self.screenshot
        if screenshot.is_subprocess:
            screenshot.save_to_tmp_file()
        else:
            # auto save
            if screenshot.save_op_index == SAVE_OP_AUTO:
                folder = utils.get_pictures_dir()
                filename = "%s%s.%s" % (_(DEFAULT_FILENAME), utils.get_format_time(), "png")
                screenshot.save_snapshot("%s/%s" % (folder, filename))
            # save as
            elif screenshot.save_op_index == SAVE_OP_AS:
                self.save_to_file()
            # copy to clip
            elif screenshot.save_op_index == SAVE_OP_CLIP:
                screenshot.save_snapshot()
            # auto save and copy to clip
            else:
                folder = utils.get_pictures_dir()
                filename = "%s%s.%s" % (_(DEFAULT_FILENAME), utils.get_format_time(), "png")
                screenshot.save_snapshot("%s/%s" % (folder, filename), clip_flag=True)
    
    def share_picture(self, widget):
        '''share picture. share button clicked callback'''
        self.screenshot.share_to_flag = True
        self.screenshot.save_op_index = SAVE_OP_AUTO
        self.save_operate()

    def save_to_file(self):
        ''' save to file '''
        self.win.hide_colorbar()
        self.win.hide_toolbar()
        #dialog = SaveFileDialog('', self.screenshot.window.window,
            #ok_callback=self._save_to_file_cb, cancel_callback=self._save_to_file_cancel)
        dialog = gtk.FileChooserDialog(
            "Save..",
            self.win.window,
            gtk.FILE_CHOOSER_ACTION_SAVE,
            (gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT,
             gtk.STOCK_SAVE, gtk.RESPONSE_ACCEPT))
        dialog.set_action(gtk.FILE_CHOOSER_ACTION_SAVE)
        dialog.set_default_response(gtk.RESPONSE_ACCEPT)
        dialog.set_position(gtk.WIN_POS_MOUSE)
        dialog.set_local_only(True)
        last_folder = self.__config.get("save", "folder")
        if last_folder:
            dialog.set_current_folder(last_folder)
        else:
            dialog.set_current_folder(utils.get_pictures_dir())
        if config.OPTION_FILE:
            dialog.set_current_name(config.OPTION_FILE)
        else:
            dialog.set_current_name("%s%s.%s" % (_(DEFAULT_FILENAME), utils.get_format_time(), "png"))
        response = dialog.run()
        filename = dialog.get_filename()
        if response == gtk.RESPONSE_ACCEPT:
            self.__config.set("save", folder=dialog.get_current_folder())
            self._save_to_file_cb(filename)
        else:
            self._save_to_file_cancel(filename)
        dialog.destroy()

    def _save_to_file_cancel(self, filename):
        ''' save file dialog cancel_callback'''
        self.screenshot.share_to_flag = False
        self.win.adjust_toolbar()
        self.win.show_toolbar()
        if self.has_button_active():
            self.win.show_colorbar()
        
    def _save_to_file_cb(self, filename):
        ''' save file dialog ok_callback'''
        print "save", filename
        self.screenshot.save_snapshot(filename=filename)
    
    def set_all_inactive(self):
        '''set all toggle button inactive'''
        #index = self._toggle_button_group.get_index()
        #if index != -1:
            #self._toggle_button_list[index].set_active(False)
        #for each in self._toggle_button_list:
            #each.set_active(False)
        if self._toggle_button_group.is_active():
            self._toggle_button_group.set_index(-1)
    
    def accel_group_callback(self, group, acceleratable, keyval, modifier):
        accel_name = gtk.accelerator_name(keyval, modifier)
        if accel_name in self.__button_accelerator_dict:
            button = self.__button_accelerator_dict[accel_name]
            button.pressed()
            button.released()
            #button.clicked()
            self.set_button_active(button.get_name(), True)
        
    def show(self):
        ''' show the toolbar '''
        if not self.window.get_visible():
            self.window.show_window()
        #print "toolbox:", self.toolbox.allocation, self.window.allocation

    def hide(self):
        '''hide the toolbar'''
        if self.window.get_visible():
            self.window.hide_all()

class Colorbar(object):
    ''' Colorbar window '''
    def __init__(self, parent=None, screenshot=None):
        '''
        init colorbar
        @param parent: the transient parent for this window
        @param screenshot: a Screenshot object
        '''
        self.screenshot = screenshot
        self.win = self.screenshot.window
        
        self.height = 36
        self.width = 279
        
        self.window = Window(window_type=gtk.WINDOW_POPUP, shadow_visible=False)
        self.window.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_DIALOG)
        self.window.set_keep_above(True)
        self.window.set_transient_for(parent)
        self.window.set_decorated(False)

        #vbox = gtk.VBox(False, 0)
        self.box = gtk.HBox(False, 5)
        self.size_box = gtk.HBox(False, 5)
        self.dynamic_box = gtk.HBox()
        
        colorbox_align = gtk.Alignment()
        #colorbox_align.set(0.5, 0.5, 0, 0)
        colorbox_align.set(0, 0.5, 1, 0)
        colorbox_align.set_padding(2, 2, 11, 11)
        colorbox_align.add(self.box)
        self.window.window_frame.pack_start(colorbox_align, True, True)
        self.window.set_size_request(self.width, self.height)
        #self.window.set_size_request(-1, self.height)

        self.__size_button_dict = {}
        self.create_size_button("small", ACTION_SIZE_SMALL)
        self.create_size_button("normal", ACTION_SIZE_NORMAL)
        self.create_size_button("big", ACTION_SIZE_BIG)
        self.create_size_button("ellipse_fill", ACTION_SIZE_RECTANGLE_ELLIPSE_FILL)
        self.create_size_button("rect_fill", ACTION_SIZE_RECTANGLE_ELLIPSE_FILL)
        self._set_size_button_state("small", True)

        self.size_align = gtk.Alignment()
        #self.size_align.set(0.5,0.5,0,0)
        self.size_align.set(0, 0.5, 1, 0)
        self.size_align.add(self.size_box)
        #self.dynamic_box.pack_start(self.size_align)
        self.box.pack_start(self.dynamic_box)
        
        # font select
        self.font_box = gtk.HBox(False, 5)
        font_img = gtk.image_new_from_pixbuf(app_theme.get_pixbuf("action/text_normal.png").get_pixbuf())
        self.font_spin = SpinBox(self.screenshot.font_size, 8, 72, 1)
        self.font_spin.connect("value-changed", self._font_size_changed)
        self.font_spin.value_entry.set_can_focus(False)
        self.font_box.pack_start(font_img)
        self.font_box.pack_start(self.font_spin)
        self.font_align = gtk.Alignment()
        self.font_align.set(0.5,0.5,0,0)
        self.font_align.add(self.font_box)

        # color select
        #self.color_select = gtk.EventBox()
        self.color_select = gtk.Image()
        pix = app_theme.get_pixbuf("color_big/red.png").get_pixbuf()
        self.color_select.set_from_pixbuf(pix)

        self.box.pack_start(self.color_select, False, False)
        
        # color button
        self.vbox = gtk.VBox(False, 2)
        self.above_hbox = gtk.HBox(False, 2)
        self.below_hbox = gtk.HBox(False, 2)
        self.color_map = {
            'black'       : "#000000",  # 1-1
            'gray_dark'   : "#808080",  # 1-2
            'red'         : "#FF0000",  # 1-3
            'yellow_dark' : "#FF9B00",  # 1-4
            'yellow'      : "#FFFF00",  # 1-5
            'green'       : "#B2E700",  # 1-6
            'green_dark'  : "#008000",  # 1-7
            'wathet_dark' : "#008080",  # 1-8
            'white'       : "#FFFFFF",  # 2-1
            'gray'        : "#C0C0C0",  # 2-2
            'red_dark'    : "#E2004E",  # 2-3
            'pink'        : "#E2007A",  # 2-4
            'pink_dark'   : "#800080",  # 2-5
            'blue_dark'   : "#000080",  # 2-6
            'blue'        : "#0085E1",  # 2-7
            'wathet'      : "#009DE0"}  # 2-8

        self.create_color_button(self.above_hbox, "black")
        self.create_color_button(self.above_hbox, "gray_dark")
        self.create_color_button(self.above_hbox, "red")
        self.create_color_button(self.above_hbox, "yellow_dark")
        self.create_color_button(self.above_hbox, "yellow")
        self.create_color_button(self.above_hbox, "green")
        self.create_color_button(self.above_hbox, "green_dark")
        self.create_color_button(self.above_hbox, "wathet_dark")

        self.create_color_button(self.below_hbox, "white")
        self.create_color_button(self.below_hbox, "gray")
        self.create_color_button(self.below_hbox, "red_dark")
        self.create_color_button(self.below_hbox, "pink")
        self.create_color_button(self.below_hbox, "pink_dark")
        self.create_color_button(self.below_hbox, "blue_dark")
        self.create_color_button(self.below_hbox, "blue")
        self.create_color_button(self.below_hbox, "wathet")

        self.vbox.pack_start(self.above_hbox)
        self.vbox.pack_start(self.below_hbox)
        self.box.pack_start(self.vbox)

    def create_color_button(self, box, name):
        '''
        create color button
        @param box: a gtk.HBox
        @param name: the button's name
        '''
        button = ImageButton(
            app_theme.get_pixbuf("color/" + name + ".png"),
            app_theme.get_pixbuf("color/" + name + "_hover.png"),
            app_theme.get_pixbuf("color/" + name + "_hover.png"))
        button.connect('pressed', lambda w:self._color_button_pressed(name))
        box.pack_start(button)

    def create_toggle_button(self, name):
        '''
        create a togglebutton
        @param name: the button's name
        @return: a dtk.ui.ToggleButton
        '''
        button = ToggleButton(
            app_theme.get_pixbuf("size/" + name + ".png"),
            app_theme.get_pixbuf("size/" + name + "_press.png"),
            app_theme.get_pixbuf("size/" + name + "_hover.png"),
            app_theme.get_pixbuf("size/" + name + "_press.png"))
        button.set_name(name)
        return button

    def create_size_button(self, name, index):
        '''
        create size button
        @param name: the button's name
        @param index: the button's index in button list
        @return: a dtk.ui.ToggleButton
        '''
        button = self.create_toggle_button(name)
        button.connect("pressed", self._size_button_pressed, index)
        #button.connect("toggled", self._size_button_toggled, name)
        button.connect("released", self._size_button_released)
        self.size_box.pack_start(button)
        self.__size_button_dict[name] = button
        return button

    def _font_size_changed(self, widget, value):
        '''font size changed, SpinBox changed callback'''
        self.screenshot.font_size = value
        if self.screenshot.show_text_window_flag:
            if not self.screenshot.text_window.set_font_size(value):
                #print value, self.screenshot.text_window.get_font_size()
                widget.set_value(self.screenshot.text_window.get_font_size())
            self.win.refresh()

    def _color_button_pressed(self, name):
        ''' color button pressed callback'''
        pix = app_theme.get_pixbuf("color_big/" + name + ".png").get_pixbuf()
        self.color_select.set_from_pixbuf(pix)
        if self.screenshot is None:
            return
        self.screenshot.action_color = self.color_map[name]
        if self.screenshot.show_text_window_flag:
            self.screenshot.text_window.set_text_color(self.screenshot.action_color)
            self.win.refresh()

    def _size_button_pressed(self, widget, index):
        ''' size button pressed callback'''
        if self.screenshot is None:
            return
        self.screenshot.action_size = index
        for each in self.__size_button_dict:
            if self.__size_button_dict[each] == widget:
                continue
            else:
                self.__size_button_dict[each].set_active(False)

    def _size_button_released(self, widget):
        ''' size button release callback'''
        if not widget.get_active():
            widget.set_active(True)

    def _set_size_button_state(self, name, state):
        '''
        set size button state
        @param name: the button's name which will set
        @param state: the state to set, True or False
        '''
        for each in self.__size_button_dict.keys():
            if each == name:
                self.__size_button_dict[name].set_active(state)
        
    def show(self):
        ''' show the colorbar'''
        # action is text, show font size set
        if self.screenshot.action == ACTION_TEXT:
            self.window.set_size_request(self.width, self.height)
            self.window.resize(self.width, self.height)
            if self.size_align in self.dynamic_box.get_children():
                self.dynamic_box.remove(self.size_align)
            if self.font_align not in self.dynamic_box.get_children():
                self.dynamic_box.add(self.font_align)
            self.dynamic_box.show_all()
        # show draw size
        else:
            if self.font_align in self.dynamic_box.get_children():
                self.dynamic_box.remove(self.font_align)
            if self.size_align not in self.dynamic_box.get_children():
                self.dynamic_box.add(self.size_align)
            self.dynamic_box.show_all()
            # actin is rectangle or ellispe, show fill button
            # show rect fill button
            if self.screenshot.action == ACTION_RECTANGLE:
                self.window.set_size_request(self.width, self.height)
                self.window.resize(self.width, self.height)
                if self.__size_button_dict['rect_fill'] not in self.size_box.get_children():
                    self.size_box.pack_start(self.__size_button_dict['rect_fill'])
                if self.__size_button_dict['ellipse_fill'] in self.size_box.get_children():
                    self.size_box.remove(self.__size_button_dict['ellipse_fill'])
                if self.__size_button_dict['ellipse_fill'].get_active():
                    self.__size_button_dict['rect_fill'].pressed()
                    self.__size_button_dict['rect_fill'].released()
            
            # show ellipse fill button
            elif self.screenshot.action == ACTION_ELLIPSE:
                self.window.set_size_request(self.width, self.height)
                self.window.resize(self.width, self.height)
                if self.__size_button_dict['ellipse_fill'] not in self.size_box.get_children():
                    self.size_box.pack_start(self.__size_button_dict['ellipse_fill'])
                if self.__size_button_dict['rect_fill'] in self.size_box.get_children():
                    self.size_box.remove(self.__size_button_dict['rect_fill'])
                if self.__size_button_dict['rect_fill'].get_active():
                    self.__size_button_dict['ellipse_fill'].pressed()
                    self.__size_button_dict['ellipse_fill'].released()

            # don't show fill button
            else:
                self.window.set_size_request(self.width, self.height)
                self.window.resize(self.width, self.height)
                if self.__size_button_dict['rect_fill'] in self.size_box.get_children():
                    if self.__size_button_dict['rect_fill'].get_active():
                        self.__size_button_dict['small'].pressed()
                        self.__size_button_dict['small'].released()
                    self.size_box.remove(self.__size_button_dict['rect_fill'])
                if self.__size_button_dict['ellipse_fill'] in self.size_box.get_children():
                    if self.__size_button_dict['ellipse_fill'].get_active():
                        self.__size_button_dict['small'].pressed()
                        self.__size_button_dict['small'].released()
                    self.size_box.remove(self.__size_button_dict['ellipse_fill'])
            self.size_box.show_all()
        if not self.window.get_visible():
            self.window.show_window()
        #print "colorbox:", self.box.allocation, self.window.allocation

    def hide(self):
        '''hide the toolbar'''
        if self.window.get_visible():
            self.window.hide_all()

if __name__ == '__main__':
    #Toolbar().show()
    Colorbar().show()
    gtk.main()
