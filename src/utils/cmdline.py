#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2015 Deepin Technology Co., Ltd.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.

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
