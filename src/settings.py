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

from PyQt5.QtCore import QSettings, QVariant, QDir

class ScreenshotSettings(QSettings):
    def __init__(self):
        super(ScreenshotSettings, self).__init__()
        self.showOSD = False
        self.tmpImageFile = ""

        self._init_settings()

    def _init_settings(self):
        if os.path.exists(self.fileName()): return

        '''save the user's last choice of save directory'''
        self.beginGroup("save")
        self.setValue("save_op", QVariant(0))
        self.setValue("folder", QVariant(QDir.home().absolutePath()))
        self.endGroup()
        '''save the user's last choice of toolbar directory'''
        self.beginGroup("common_color_linewidth")
        self.setValue("color_index", QVariant(3))
        self.setValue("linewidth_index", QVariant(2))
        self.endGroup()
        self.beginGroup("rect")
        self.setValue("color_index", QVariant(3))
        self.setValue("linewidth_index", QVariant(2))
        self.endGroup()
        self.beginGroup("ellipse")
        self.setValue("color_index", QVariant(3))
        self.setValue("linewidth_index", QVariant(2))
        self.endGroup()
        self.beginGroup("line")
        self.setValue("color_index", QVariant(3))
        self.setValue("linewidth_index", QVariant(2))
        self.endGroup()
        self.beginGroup("arrow")
        self.setValue("color_index", QVariant(3))
        self.setValue("linewidth_index", QVariant(2))
        self.endGroup()
        self.beginGroup("text")
        self.setValue("color_index", QVariant(3))
        self.setValue("fontsize_index", QVariant(12))
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
