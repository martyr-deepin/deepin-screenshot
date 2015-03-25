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

import tempfile
from functools import partial
from copy import deepcopy

from PyQt5.QtWidgets import qApp
from PyQt5.QtCore import QObject, QTimer, QUrl
from PyQt5.QtMultimedia import QSoundEffect

from i18n import _
from settings import ScreenshotSettings
from app_context import AppContext
from dbus_services import ServiceAdaptor
from dbus_interfaces import notificationsInterface
from utils.cmdline import processArguments
from constants import SOUND_FILE

class AppController(QObject):
    """The main controller of this application."""
    def __init__(self):
        super(AppController, self).__init__()
        ServiceAdaptor(self)

        self.contexts = []
        self._initQuitTimer()

    def _initQuitTimer(self):
        self._quitTimer = QTimer()
        self._quitTimer.setInterval(10 * 1000)
        self._quitTimer.setSingleShot(True)
        self._quitTimer.timeout.connect(self._checkContexts)

    def _checkContexts(self):
        if (self.contexts):
            self._quitTimer.start()
        else:
            qApp.quit()

    def _contextNeedSound(self, context):
        self.soundEffect.play()

    def _contextFinished(self, context):
        self.contexts.remove(context)
        self._checkContexts()

    def _createContextSettings(self):
        settings = ScreenshotSettings()
        settings.tmpImageFile = "%s.png" % tempfile.mktemp()
        settings.tmpBlurFile = "%s-blur.png" % tempfile.mktemp()
        settings.tmpMosaiceFile = "%s-mosaic.png" % tempfile.mktemp()
        settings.tmpSaveFile = "%s-save.png" % tempfile.mktemp()

        return settings

    def runWithArguments(self, arguments):
        (delay, fullscreen, topWindow,
         savePath, startFromDesktop) = processArguments(arguments)

        self.soundEffect = QSoundEffect()
        self.soundEffect.setSource(QUrl(SOUND_FILE))
        self.soundEffect.play()

        context = AppContext(deepcopy(locals()))
        context.settings = self._createContextSettings()
        context.finished.connect(partial(self._contextFinished, context))
        context.needSound.connect(partial(self._contextNeedSound, context))
        self.contexts.append(context)

        if delay > 0:
            notificationsInterface.notify(_("Deepin Screenshot"),
            _("Deepin Screenshot will start after %s seconds.") % delay)

        QTimer.singleShot(max(0, delay * 1000), context.main)
