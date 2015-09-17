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

from PyQt5.QtCore import QCommandLineParser, QCommandLineOption

def processArguments(arguments):
	parser = QCommandLineParser()
	parser.addHelpOption()
	parser.addVersionOption()

	delayOption = QCommandLineOption(["d", "delay"],
	    "Take a screenshot after NUM seconds", "NUM")
	fullscreenOption = QCommandLineOption(["f", "fullscreen"],
	    "Take a screenshot of the whole screen")
	topWindowOption = QCommandLineOption(["w", "top-window"],
	    "Take a screenshot of the most top window")
	savePathOption = QCommandLineOption(["s", "save-path"],
	    "Specify a path to save the screenshot", "PATH")
	startFromDesktopOption = QCommandLineOption(["i", "icon"],
	    "Indicate that this program's started by clicking desktop file.")
	noNotificationOption = QCommandLineOption(["n", "no-notification"],
	    "Don't send notifications.")

	parser.addOption(delayOption)
	parser.addOption(fullscreenOption)
	parser.addOption(topWindowOption)
	parser.addOption(savePathOption)
	parser.addOption(noNotificationOption)
	parser.addOption(startFromDesktopOption)
	parser.process(arguments)

	delay = int(parser.value(delayOption) or 0)
	fullscreen = bool(parser.isSet(fullscreenOption) or False)
	topWindow = bool(parser.isSet(topWindowOption) or False)
	savePath = str(parser.value(savePathOption) or "")
	startFromDesktop = bool(parser.isSet(startFromDesktopOption) or False)
	noNotification = bool(parser.isSet(noNotificationOption) or False)

	return {"delay": delay,
			"fullscreen": fullscreen,
			"topWindow": topWindow,
			"savePath": savePath,
			"startFromDesktop": startFromDesktop,
			"noNotification": noNotification}