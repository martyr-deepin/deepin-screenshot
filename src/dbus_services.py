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

from PyQt5.QtCore import Q_CLASSINFO, pyqtSlot
from PyQt5.QtDBus import QDBusConnection, QDBusAbstractAdaptor

DBUS_NAME = "com.deepin.DeepinScreenshot"
DBUS_PATH = "/com/deepin/DeepinScreenshot"
session_bus = QDBusConnection.sessionBus()

def is_service_exist():
    return not session_bus.registerService(DBUS_NAME)

def register_object(object):
    return session_bus.registerObject(DBUS_PATH, object)

class ServiceAdaptor(QDBusAbstractAdaptor):

    Q_CLASSINFO("D-Bus Interface", DBUS_NAME)
    Q_CLASSINFO("D-Bus Introspection",
                '  <interface name="com.deepin.DeepinScreenshot">\n'
                '    <method name="RunWithArguments">\n'
                '      <arg direction="in" type="as" name="arguments"/>\n'
                '    </method>\n'
                '  </interface>\n')

    def __init__(self, parent):
        super(ServiceAdaptor, self).__init__(parent)
        self.parent = parent

    @pyqtSlot("QStringList")
    def RunWithArguments(self, arguments):
        return self.parent.runWithArguments(arguments)
