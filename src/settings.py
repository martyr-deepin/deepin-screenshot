#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2015 Deepin Technology Co., Ltd.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.

import os

from PyQt5.QtCore import QSettings, QVariant, QDir

class ScreenshotSettings(QSettings):
    def __init__(self):
        super(ScreenshotSettings, self).__init__()
        self.showOSD = False
        self.tmpImageFile = ""
        self.tmpSaveFile = ""
        self.tmpBlurFile = ""
        self.tmpMosaiceFile = ""

        self._init_settings()

    def _init_settings(self):
        if os.path.exists(self.fileName()):
            self.addOption("showOSD", "show", True)
            return

        '''save the user's last choice of save directory'''
        self.setOption("save", "save_op", QVariant(0))
        self.setOption("save", "folder", QVariant(QDir.home().absolutePath()))
        '''save the user's last choice of toolbar directory'''
        self.setOption("common_color_linewidth", "color_index", QVariant(3))
        self.setOption("common_color_linewidth", "linewidth_index", QVariant(2))
        self.setOption("rect", "color_index", QVariant(3))
        self.setOption("rect", "linewidth_index", QVariant(2))
        self.setOption("ellipse", "color_index", QVariant(3))
        self.setOption("ellipse", "linewidth_index", QVariant(2))
        self.setOption("arrow", "color_index", QVariant(3))
        self.setOption("arrow", "linewidth_index", QVariant(2))
        self.setOption("line", "color_index", QVariant(3))
        self.setOption("line", "linewidth_index", QVariant(2))
        self.setOption("text", "color_index", QVariant(3))
        self.setOption("text", "fontsize_index", QVariant(12))
        self.setOption("showOSD", "show", True)

    def addOption(self, group_name, op_name, specificValue):
        '''add a new group in old configure file'''
        keys = self.allKeys()
        show_group_exist = 0
        check_key = group_name+"/"+op_name
        for i in keys:
            if check_key == i:
                show_group_exist = 1
                return
        if show_group_exist == 0:
            self.beginGroup(group_name)
            self.setValue(op_name, QVariant(specificValue))
            self.endGroup()

    def getOption(self, group_name, op_name):
        self.beginGroup(group_name)
        op_index = self.value(op_name)
        self.endGroup()

        return op_index

    def setOption(self, group_name, op_name, op_index):
        self.beginGroup(group_name)
        self.setValue(op_name, QVariant(op_index))
        self.endGroup()
