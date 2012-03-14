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

DRAG_INSIDE = 0
DRAG_OUTSIDE = 1
DRAG_TOP_LEFT_CORNER = 2
DRAG_TOP_RIGHT_CORNER = 3
DRAG_BOTTOM_LEFT_CORNER = 4
DRAG_BOTTOM_RIGHT_CORNER = 5
DRAG_TOP_SIDE = 6
DRAG_BOTTOM_SIDE = 7
DRAG_LEFT_SIDE = 8
DRAG_RIGHT_SIDE = 9

SCROT_MODE_NORMAL = 0
SCROT_MODE_FULLSCREEN = 1
SCROT_MODE_WINDOW = 2

DEFAULT_FILENAME = "DeepinScrot-"
DEFAULT_FONT = "文泉驿微米黑"