#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2011 Deepin, Inc.
#               2011 Wang Yong
#
# Author:     Wang Yong <lazycat.manatee@gmail.com>
# Maintainer: Wang Yong <lazycat.manatee@gmail.com>
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


ACTION_INIT = 0
ACTION_SELECT = 1
ACTION_RECTANGLE = 2
ACTION_ELLIPSE = 3
ACTION_ARROW = 4
ACTION_LINE = 5
ACTION_PIXELIZE = 6
ACTION_TEXT = 7
ACTION_STEP = 8
ACTION_WINDOW = 9

DRAG_INSIDE = 10
DRAG_OUTSIDE = 11
DRAG_TOP_LEFT_CORNER = 12
DRAG_TOP_RIGHT_CORNER = 13
DRAG_BOTTOM_LEFT_CORNER = 14
DRAG_BOTTOM_RIGHT_CORNER = 15
DRAG_TOP_SIDE = 16
DRAG_BOTTOM_SIDE = 17
DRAG_LEFT_SIDE = 18
DRAG_RIGHT_SIDE = 19

ACTION_SIZE_SMALL = 2
ACTION_SIZE_NORMAL = 3
ACTION_SIZE_BIG = 5
ACTION_SIZE_RECTANGLE_ELLIPSE_FILL= 100

MAGNIFIER_POS_LEFT = (1<<0)
MAGNIFIER_POS_RIGHT= (1<<1)
MAGNIFIER_POS_TOP= (1<<2)
MAGNIFIER_POS_BOTTOM= (1<<3)

BUTTON_EVENT_LEFT = 1
BUTTON_EVENT_MIDDLE = 2
BUTTON_EVENT_RIGHT = 3

SCREENSHOT_MODE_NORMAL = 0
SCREENSHOT_MODE_FULLSCREEN = 1
SCREENSHOT_MODE_WINDOW = 2

DEFAULT_FILENAME = "DeepinScreenshot"
DEFAULT_FONT = "文泉驿微米黑"

SAVE_OP_AUTO = 0
SAVE_OP_AS = 1
SAVE_OP_CLIP = 2
SAVE_OP_AUTO_AND_CLIP = 3
SAVE_OP_MAX_NUM = 4
