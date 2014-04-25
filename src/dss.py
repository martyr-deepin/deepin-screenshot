#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2011~2013 Deepin, Inc.
#               2011~2013 Kaisheng Ye
#
# Author:     Kaisheng Ye <kaisheng.ye@gmail.com>
# Maintainer: Kaisheng Ye <kaisheng.ye@gmail.com>
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

import dbus

DDE_DBUS_NAME = "com.deepin.dde.ControlCenter"
DDE_OBJECT_PATH = "/com/deepin/dde/ControlCenter"

def hide():
    try:
        session_bus = dbus.SessionBus()
        obj = session_bus.get_object(DDE_DBUS_NAME, DDE_OBJECT_PATH)
        interface = dbus.Interface(obj, DDE_DBUS_NAME)
        interface.HideImmediately()
    except:
        pass

def show():
    try:
        session_bus = dbus.SessionBus()
        obj = session_bus.get_object(DDE_DBUS_NAME, DDE_OBJECT_PATH)
        interface = dbus.Interface(obj, DDE_DBUS_NAME)
        interface.ShowImmediately()
    except:
        pass
