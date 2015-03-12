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

MENU_ICONS_DIR = os.path.join(MAIN_DIR, "image", "menu_icons")
menu_icon_normal = lambda x: os.path.join(MENU_ICONS_DIR,"%s-symbolic-small-norml.svg" % x)
menu_icon_hover = lambda x: os.path.join(MENU_ICONS_DIR, "%s-symbolic-small-hover.svg" % x)
menu_icon_tuple = lambda x: (menu_icon_normal(x), menu_icon_hover(x))

save_sub_menu = [
    CheckableMenuItem("save:radio:_op_auto_save", _("Autosave")),
    CheckableMenuItem("save:radio:_op_save_to_desktop", _("Save to desktop")),
    CheckableMenuItem("save:radio:_op_copy_to_clipboard", _("Copy to clipboard")),
    CheckableMenuItem("save:radio:_op_save_as", _("Save to specified folder")),
    CheckableMenuItem("save:radio:_op_copy_and_save", _("Autosave and copy to clipboard")),
]

right_click_menu = [
    ("_rectangle", _("Rectangle tool"), menu_icon_tuple("rectangle-tool")),
    ("_ellipse", _("Ellipse tool"), menu_icon_tuple("ellipse-tool")),
    ("_arrow", _("Arrow tool"), menu_icon_tuple("arrow-tool")),
    ("_line", _("Brush tool"), menu_icon_tuple("line-tool")),
    ("_text", _("Text tool"), menu_icon_tuple("text-tool")),
    None,
    ("_save", _("Save"), menu_icon_tuple("save")),
    ("_share", _("Share"), menu_icon_tuple("share")),
    ("_exit", _("Exit"), menu_icon_tuple("exit")),
]

class MenuController(QObject):
    toolSelected = pyqtSignal(str, arguments=["toolName"])
    saveSelected = pyqtSignal(int, arguments=["saveOption"])
    shareSelected = pyqtSignal()
    exitSelected = pyqtSignal()

    preMenuShow = pyqtSignal()
    postMenuHide = pyqtSignal()

    def __init__(self):
        super(MenuController, self).__init__()

    def _menu_unregistered(self):
        self.postMenuHide.emit()

    def _menu_item_invoked(self, _id, _checked):
        self.postMenuHide.emit()

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
        self.preMenuShow.emit()

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
        self.menu.menuDismissed.connect(self._menu_unregistered)
        self.menu.showRectMenu(QCursor.pos().x(), QCursor.pos().y())
