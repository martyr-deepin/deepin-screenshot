#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2011 ~ 2015 Deepin, Inc.
#               2011 ~ 2015 Wang YaoHua
#
# Author:     Wang YaoHua <mr.asianwang@gmail.com>
# Maintainer: Wang YaoHua <mr.asianwang@gmail.com>
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

import os

from PyQt5.QtGui import QCursor
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

from deepin_menu.menu import Menu, CheckableMenuItem

from i18n import _
from constants import MAIN_DIR

rect_image = os.path.join(MAIN_DIR, "image", "action", "rect_press.svg")
ellipse_image = os.path.join(MAIN_DIR, "image", "action", "ellipse_press.svg")
arrow_image = os.path.join(MAIN_DIR, "image", "action", "arrow_press.svg")
line_image = os.path.join(MAIN_DIR, "image", "action", "line_press.svg")
text_image = os.path.join(MAIN_DIR, "image", "action", "text_press.svg")
share_image = os.path.join(MAIN_DIR, "image", "action", "share_press.svg")
cancel_image = os.path.join(MAIN_DIR, "image", "action", "cancel_press.svg")
save_image = os.path.join(MAIN_DIR, "image", "save", "save_press.svg")

save_sub_menu = [
    CheckableMenuItem("save:radio:_op_auto_save", _("Auto save")),
    CheckableMenuItem("save:radio:_op_save_to_desktop", _("Save to desktop")),
    CheckableMenuItem("save:radio:_op_copy_to_clipboard", _("Copy to clipboard")),
    CheckableMenuItem("save:radio:_op_save_as", _("Save as")),
    CheckableMenuItem("save:radio:_op_copy_and_save", _("Auto Save and Save to Clipboard")),
]

right_click_menu = [
    ("_rectangle", _("Rectangle tool"), (rect_image,)),
    ("_ellipse", _("Ellipse tool"), (ellipse_image,)),
    ("_arrow", _("Arrow tool"), (arrow_image,)),
    ("_line", _("Line tool"), (line_image,)),
    ("_text", _("Text tool"), (text_image,)),
    None,
    ("_save", _("Save"), (save_image,)),
    ("_share", _("Share"), (share_image,)),
    ("_exit", _("Exit"), (cancel_image,)),
]

class MenuController(QObject):
    toolSelected = pyqtSignal(str, arguments=["toolName"])
    saveSelected = pyqtSignal(int, arguments=["saveOption"])
    shareSelected = pyqtSignal()
    exitSelected = pyqtSignal()

    def __init__(self):
        super(MenuController, self).__init__()

    def _menu_item_invoked(self, _id, _checked):
        if _id == "_rectangle":
            self.toolSelected.emit("_rectangle")
        if _id == "_ellipse":
            self.toolSelected.emit("_ellipse")
        if _id == "_arrow":
            self.toolSelected.emit("_arrow")
        if _id == "_line":
            self.toolSelected.emit("_line")
        if _id == "_text":
            self.toolSelected.emit("_text")

        if _id == "save:radio:_op_auto_save":
            self.saveSelected.emit(1)
        if _id == "save:radio:_op_save_to_desktop":
            self.saveSelected.emit(0)
        if _id == "save:radio:_op_copy_to_clipboard":
            self.saveSelected.emit(4)
        if _id == "save:radio:_op_save_as":
            self.saveSelected.emit(2)
        if _id == "save:radio:_op_copy_and_save":
            self.saveSelected.emit(3)

        if _id == "_share":
            self.shareSelected.emit()
        if _id == "_exit":
            self.exitSelected.emit()

    @pyqtSlot(int)
    def show_menu(self, saveOption):
        self.menu = Menu(right_click_menu)
        self.menu.getItemById("_save").setSubMenu(Menu(save_sub_menu))

        self.menu.getItemById("save:radio:_op_auto_save").checked = \
            saveOption == 1
        self.menu.getItemById("save:radio:_op_save_to_desktop").checked = \
            saveOption == 0
        self.menu.getItemById("save:radio:_op_copy_to_clipboard").checked = \
            saveOption == 4
        self.menu.getItemById("save:radio:_op_save_as").checked = \
            saveOption == 2
        self.menu.getItemById("save:radio:_op_copy_and_save").checked = \
            saveOption == 3

        self.menu.itemClicked.connect(self._menu_item_invoked)
        self.menu.showRectMenu(QCursor.pos().x(), QCursor.pos().y())