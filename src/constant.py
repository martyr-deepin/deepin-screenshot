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

'''
ACTION show now status.
@var ACTION_INIT: be selecting area.
@var ACTION_SELECT: has selected area, and has not clicked any button.
@var ACTION_RECTANGLE: rect button has been clicked.
@var ACTION_ELLIPSE: ellipse button has been clicked.
@var ACTION_ARROW: arrow button has been clicked.
@var ACTION_LINE: line button has been clicked.
@var ACTION_PIXELIZE: unused
@var ACTION_TEXT: text button has been clicked.
@var ACTION_STEP: unused
@var ACTION_WINDOW: begin to choose area.
'''
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

'''
DRAG is the mouse drag flag.
@var DRAG_INSIDE: the cursor is inside the area.
@var DRAG_OUTSIDE: the cursor is outside the area.
@var DRAG_TOP_LEFT_CORNER: the cursor is at the top-left of the area.
@var DRAG_TOP_RIGHT_CORNER: the cursor is at the top-right of the area.
@var DRAG_BOTTOM_LEFT_CORNER: the cursor is at the bottom-left of the area.
@var DRAG_BOTTOM_RIGHT_CORNER: the cursor is at the bottom-right of the area.
@var DRAG_TOP_SIDE: the cursor is at the top of the area.
@var DRAG_BOTTOM_SIDE: the cursor is at the bottom of the area.
@var DRAG_LEFT_SIDE: the cursor is at the left of the area.
@var DRAG_RIGHT_SIDE: the cursor is at the right of the area.
'''
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

'''
ACTION_SIZE is the line width of cairo
@var ACTION_SIZE_SMALL: small width.
@var ACTION_SIZE_NORMAL: nornal width.
@var ACTION_SIZE_BIG: big width.
@var ACTION_SIZE_RECTANGLE_ELLIPSE_FILL: fill a rectangle or ellipse.
'''
ACTION_SIZE_SMALL = 2
ACTION_SIZE_NORMAL = 3
ACTION_SIZE_BIG = 5
ACTION_SIZE_RECTANGLE_ELLIPSE_FILL= 100

'''
MAGNIFIER is the magnifier position flag.
@var MAGNIFIER_POS_LEFT: the cursor at left of screen.
@var MAGNIFIER_POS_RIGHT: the cursor at right of screen.
@var MAGNIFIER_POS_TOP: the cursor at top of screen.
@var MAGNIFIER_POS_BOTTOM: the cursor at bottom of screen.
'''
MAGNIFIER_POS_LEFT = (1<<0)
MAGNIFIER_POS_RIGHT= (1<<1)
MAGNIFIER_POS_TOP= (1<<2)
MAGNIFIER_POS_BOTTOM= (1<<3)

'''
@var BUTTON_EVENT_LEFT: left mouse button
@var BUTTON_EVENT_MIDDLE: middle mouse button
@var BUTTON_EVENT_RIGHT: right mouse button
'''
BUTTON_EVENT_LEFT = 1
BUTTON_EVENT_MIDDLE = 2
BUTTON_EVENT_RIGHT = 3

SCREENSHOT_MODE_NORMAL = 0
SCREENSHOT_MODE_FULLSCREEN = 1
SCREENSHOT_MODE_WINDOW = 2

'''
@var DEFAULT_FILENAME: the default filename to save.
@var DEFAULT_FONT: the default fontname.
'''
DEFAULT_FILENAME = "DeepinScreenshot"
DEFAULT_FONT = "文泉驿微米黑"

'''
the save operation
@var SAVE_OP_AUTO: autosave to file.
@var SAVE_OP_AS: saveas custom file.
@var SAVE_OP_CLIP: save to clipboard.
@var SAVE_OP_AUTO_AND_CLIP: autosave to file, and save to clipboard.
@var SAVE_OP_MAX_NUM: the number of the save operation.
'''
SAVE_OP_AUTO = 0
SAVE_OP_AS = 1
SAVE_OP_CLIP = 2
SAVE_OP_AUTO_AND_CLIP = 3
SAVE_OP_MAX_NUM = 4
