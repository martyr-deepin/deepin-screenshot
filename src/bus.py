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
import dbus.service
import dbus.mainloop.glib
import os


DBUS_NAME = "com.deepin.screenshot"
OBJECT_PATH = "/com/deepin/screenshot"

dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
bus = dbus.SessionBus()
def is_service_exists():
    request = bus.request_name(DBUS_NAME)
    if request != dbus.bus.REQUEST_NAME_REPLY_PRIMARY_OWNER and\
            request != dbus.bus.REQUEST_NAME_REPLY_ALREADY_OWNER:
        return True
    else:
        return False

class ScreenshotService(dbus.service.Object):
    ''' screenshot dbus service'''
    def __init__(self):
        dbus.service.Object.__init__(self, bus, OBJECT_PATH)
        
    @dbus.service.signal(dbus_interface=DBUS_NAME, signature='us')
    def finish(self, save_type, file_name):
        '''
        it will emit this signal while saved.
        '''
        print "finish"

    @dbus.service.method(dbus_interface=DBUS_NAME, in_signature='', out_signature='i')
    def get_pid(self):
        return os.getpid()

    def emit_finish(self, save_type=0, file_name=''):
        '''
        @param save_type: 0 -> save to clipboard; 1 -> save to file
        @param file_name: it has no effect if save_type is 0
        '''
        self.finish(save_type, file_name)
        
if is_service_exists():
    print "deepin screenshot has run"
    os._exit(1)
SCROT_BUS = ScreenshotService()
