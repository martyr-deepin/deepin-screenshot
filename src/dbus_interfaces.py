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


from PyQt5.QtCore import QVariant, pyqtSignal
from PyQt5.QtDBus import QDBusAbstractInterface, QDBusConnection, QDBusReply

class NotificationsInterface(QDBusAbstractInterface):
    ActionInvoked = pyqtSignal("quint32", str)
    NotificationClosed = pyqtSignal("quint32", "quint32")

    def __init__(self):
        super(NotificationsInterface, self).__init__(
            "org.freedesktop.Notifications",
            "/org/freedesktop/Notifications",
            "org.freedesktop.Notifications",
            QDBusConnection.sessionBus(),
            None)

    def notify(self, summary, body, actions=[]):
        varRPlaceId = QVariant(0)
        varRPlaceId.convert(QVariant.UInt)
        varActions = QVariant(actions)
        varActions.convert(QVariant.StringList)

        msg = self.call("Notify", "Deepin Screenshot", varRPlaceId, "deepin-screenshot", summary, body, varActions, {}, -1)
        reply = QDBusReply(msg)
        return reply.value()

class SocialSharingInterface(QDBusAbstractInterface):
    def __init__(self):
        super(SocialSharingInterface, self).__init__(
            "com.deepin.SocialSharing",
            "/com/deepin/SocialSharing",
            "com.deepin.SocialSharing",
            QDBusConnection.sessionBus(),
            None)

    def share(self, text, pic):
        self.call("Share", text, pic)

notificationsInterface = NotificationsInterface()
socialSharingInterface = SocialSharingInterface()