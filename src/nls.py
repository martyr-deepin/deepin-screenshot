#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2011 ~ 2012 Deepin, Inc.
#               2011 ~ 2012 Hou Shaohui
#
# Author:     Hou Shaohui <houshao55@gmail.com>
# Maintainer: Hou Shaohui <houshao55@gmail.com>
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

import gettext
import os
import locale

default_locale = locale.getdefaultlocale()[0]

def get_parent_dir(filepath, level=1):
    '''Get parent dir.'''
    parent_dir = os.path.realpath(filepath)

    while(level > 0):
        parent_dir = os.path.dirname(parent_dir)
        level -= 1

    return parent_dir

LOCALE_DIR=os.path.join(get_parent_dir(__file__, 2), "locale", "mo")
if not os.path.exists(LOCALE_DIR):
    LOCALE_DIR="/usr/share/locale"

_ = None
try:
    _ = gettext.translation("deepin-screenshot", LOCALE_DIR).gettext
except Exception, e:
    _ = lambda i : i

