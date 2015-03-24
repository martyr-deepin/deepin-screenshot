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

from functools import partial
from PyQt5.QtCore import QObject, QTimer, pyqtSignal

from dbus_services import ServiceAdaptor
from utils.cmdline import processArguments

class AppController(QObject):
	"""The main controller of this application."""
	def __init__(self, mainFunc):
		super(AppController, self).__init__()
		adapter = ServiceAdaptor(self)
		self._mainFunc = mainFunc

	def runWithArguments(self, arguments):
		argValues = processArguments(arguments)
		(delay, fullscreen, topWindow,
		 savePath, startFromDesktop) = argValues
		mainFunc = partial(self._mainFunc, *argValues)

		if delay > 0:
		    notificationsInterface.notify(_("Deepin Screenshot"),
		    _("Deepin Screenshot will start after %s seconds.") % delayValue)

		QTimer.singleShot(max(0, delay * 1000), mainFunc)
