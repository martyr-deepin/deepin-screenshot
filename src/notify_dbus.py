#!/usr/bin/env python
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

import dbus
from deepin_utils.file import get_parent_dir

image_path = "%s/theme/logo/deepin-screenshot.png" % get_parent_dir(__file__, 2)

def notify(app_name, replaces_id, app_icon, summary,
           body, actions=[], hints={"image-path": image_path}, timeout=3500):
    session_bus = dbus.SessionBus()
    obj = session_bus.get_object('org.freedesktop.Notifications', '/org/freedesktop/Notifications')
    interface = dbus.Interface(obj, 'org.freedesktop.Notifications')
    interface.Notify(app_name, replaces_id, app_icon, summary,
                     body, actions, hints, timeout)
