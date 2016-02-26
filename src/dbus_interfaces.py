#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2015 Deepin Technology Co., Ltd.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.


from PyQt5.QtCore import QVariant, pyqtSignal
from PyQt5.QtDBus import QDBusAbstractInterface, QDBusConnection, QDBusReply

from i18n import _

class ScreenshotInterface(QDBusAbstractInterface):
    def __init__(self):
        super(ScreenshotInterface, self).__init__(
            "com.deepin.DeepinScreenshot",
            "/com/deepin/DeepinScreenshot",
            "com.deepin.DeepinScreenshot",
            QDBusConnection.sessionBus(),
            None)

    def runWithArguments(self, arguments):
        arguments = QVariant(arguments)
        arguments.convert(QVariant.StringList)
        self.call("RunWithArguments", arguments)

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

        msg = self.call("Notify",
            "Deepin Screenshot",
            varRPlaceId,
            "deepin-screenshot",
            summary,
            body, varActions, {}, -1)

        reply = QDBusReply(msg)
        if reply.isValid():
            return reply.value()
        else:
            return None

class SocialSharingInterface(QDBusAbstractInterface):
    def __init__(self):
        super(SocialSharingInterface, self).__init__(
            "com.deepin.SocialSharing",
            "/com/deepin/SocialSharing",
            "com.deepin.SocialSharing",
            QDBusConnection.sessionBus(),
            None)

    def share(self, text, pic):
        self.call("Share", _("Deepin Screenshot"),
         "deepin-screenshot", text, pic)

class HotZoneInterface(QDBusAbstractInterface):
    def __init__(self):
        super(HotZoneInterface, self).__init__(
            "com.deepin.daemon.Zone",
            "/com/deepin/daemon/Zone",
            'com.deepin.daemon.Zone',
            QDBusConnection.sessionBus(),
            None)

    def enableZone(self):
        self.asyncCall("EnableZoneDetected", True)

    def disableZone(self):
        self.asyncCall("EnableZoneDetected", False)

class ControlCenterInterface(QDBusAbstractInterface):
    def __init__(self):
        super(ControlCenterInterface, self).__init__(
            "com.deepin.dde.ControlCenter",
            "/com/deepin/dde/ControlCenter",
            "com.deepin.dde.ControlCenter",
            QDBusConnection.sessionBus(),
            None)
        sessionBus = QDBusConnection.sessionBus()
        self._control_center_exists = not sessionBus.registerService(
            self.service())
        sessionBus.unregisterService(self.service())

    def showImmediately(self):
        if self._control_center_exists:
            try:
                self.asyncCall("ShowImmediately")
            except:
                pass

    def hideImmediately(self):
        if self._control_center_exists:
            try:
                self.asyncCall("HideImmediately")
            except:
                pass

class FileManagerInterface(QDBusAbstractInterface):
    def __init__(self):
        super(FileManagerInterface, self).__init__(
            "org.freedesktop.FileManager1",
            "/org/freedesktop/FileManager1",
            "org.freedesktop.FileManager1",
            QDBusConnection.sessionBus(),
            None)

    def showItems(self, items, startupId=""):
        urize = lambda x: "file://%s" % x.replace("file://", "")
        uris = QVariant(map(urize, items))
        uris.convert(QVariant.StringList)
        self.call("ShowItems", uris, "")

class SoundEffectInteface(QDBusAbstractInterface):
    def __init__(self):
        super(SoundEffectInteface, self).__init__(
            "com.deepin.daemon.SoundEffect",
            "/com/deepin/daemon/SoundEffect",
            "com.deepin.daemon.SoundEffect",
            QDBusConnection.sessionBus(),
            None)

    def play(self):
        self.asyncCall("PlaySystemSound", "camera-shutter")

hotZoneInterface = HotZoneInterface()
screenshotInterface = ScreenshotInterface()
notificationsInterface = NotificationsInterface()
socialSharingInterface = SocialSharingInterface()
controlCenterInterface = ControlCenterInterface()
soundEffectInterface = SoundEffectInteface()
