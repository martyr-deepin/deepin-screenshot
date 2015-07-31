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
import os
import tempfile

from PyQt5.QtWidgets import qApp
from PyQt5.QtCore import QObject, QTimer, QUrl
from PyQt5.QtMultimedia import QSoundEffect
from PyQt5.QtQml import QQmlApplicationEngine

from i18n import _
from settings import ScreenshotSettings
from app_context import AppContext
from dbus_services import ServiceAdaptor
from dbus_interfaces import notificationsInterface
from utils.cmdline import processArguments
from constants import SOUND_FILE, OSD_QML
from safe_timer import SafeTimer


def validFormat(suffixname):
    pictureformat = [".bmp",".jpg",".jpeg",".png",".pbm",".pgm",".ppm",".xbm",".xpm"]
    return suffixname in pictureformat

class AppController(QObject):
    """The main controller of this application."""
    def __init__(self):
        super(AppController, self).__init__()
        ServiceAdaptor(self)

        self.contexts = []
        self._osdVisible = False
        self._initQuitTimer()

    def _initQuitTimer(self):
        self._quitTimer = QTimer()
        self._quitTimer.setInterval(10 * 1000)
        self._quitTimer.setSingleShot(True)
        self._quitTimer.timeout.connect(self._checkContexts)

    def _checkContexts(self):
        if (self.contexts) or self._osdVisible:
            self._quitTimer.start()
        else:
            qApp.quit()

    def _contextNeedSound(self):
        self._sound.play()

    def _contextFinished(self):
        sender = self.sender()
        if sender in self.contexts:
            # TODO: the remove _doesn't_ get the sender object
            # garbage collected, there must be some reference cycles.
            self.contexts.remove(sender)
        self._checkContexts()

    def _contextNeedOSD(self, area):
        def _osdClosed():
            self._osdVisible = False

        self._osdVisible = True
        self._qmlEngine = QQmlApplicationEngine()
        self._qmlEngine.load(QUrl(OSD_QML))
        osd = self._qmlEngine.rootObjects()[0]
        osd.setX(area.x() + (area.width() - osd.width()) / 2)
        osd.setY(area.y() + (area.height() - osd.height()) / 2)
        osd.showTips()
        osd.closed.connect(_osdClosed)

    def _createContextSettings(self):
        settings = ScreenshotSettings()
        settings.tmpImageFile = "%s.png" % tempfile.mktemp()
        settings.tmpBlurFile = "%s-blur.png" % tempfile.mktemp()
        settings.tmpMosaiceFile = "%s-mosaic.png" % tempfile.mktemp()
        settings.tmpSaveFile = "%s-save.png" % tempfile.mktemp()

        return settings


    def runWithArguments(self, arguments):
        for _context in self.contexts:
            if _context.isActive():
                return 1

        argValues = processArguments(arguments)
        delay = argValues["delay"]

        savePathValue = argValues["savePath"]
        if savePathValue != "":
            pic_name = os.path.basename(savePathValue)
            if pic_name == "":
                return 1
            else :
                if os.path.exists(os.path.dirname(savePathValue)):
                    pic_name_stuffix = os.path.splitext(pic_name)[1]
                    if not validFormat(pic_name_stuffix):
                        return 1
                else:
                    return 1

        self._sound = QSoundEffect()
        self._sound.setSource(QUrl.fromLocalFile(SOUND_FILE))
        self._sound.setLoopCount(1)
        self._sound.setVolume(0.4)

        context = AppContext(argValues)
        context.settings = self._createContextSettings()
        context.finished.connect(self._contextFinished)
        context.needSound.connect(self._contextNeedSound)
        context.needOSD.connect(self._contextNeedOSD)
        self.contexts.append(context)

        if delay > 0:
            notificationsInterface.notify(_("Deepin Screenshot"),
            _("Deepin Screenshot will start after %s seconds.") % delay)
            '''If run the program frequently, the QTimer sometimes do not invoke the event, so replace QTimer with SafeTimer'''
            SafeTimer.singleShot(delay, context.main)
        else:
            context.main()

        return 0
