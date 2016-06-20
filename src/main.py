#! /usr/bin/env python2
# -*- coding: utf-8 -*-
#
# Copyright (C) 2015 Deepin Technology Co., Ltd.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.

import os
import sys
import signal

from OpenGL import GL
from PyQt5 import QtCore
from PyQt5.QtCore import QCoreApplication
if os.name == 'posix':
    QCoreApplication.setAttribute(QtCore.Qt.AA_X11InitThreads, True)

from PyQt5.QtWidgets import QApplication
app = QApplication(sys.argv)
app.setOrganizationName("Deepin")
app.setApplicationName("Deepin Screenshot")
app.setApplicationVersion("3.1.0")
app.setQuitOnLastWindowClosed(False)

from app_controller import AppController
from dbus_services import is_service_exist, register_object
from dbus_interfaces import screenshotInterface

if __name__ == "__main__":
    if is_service_exist():
        screenshotInterface.runWithArguments(app.arguments())
        # TODO: maybe there will never be a situation that
        # the following should be executed.
        # notificationsInterface.notify(_("Deepin Screenshot"),
        #     _("Deepin Screenshot has been started!"))
    else:
        controller = AppController()

        returncode = controller.runWithArguments(app.arguments())
        if returncode == 0:
            register_object(controller)
            signal.signal(signal.SIGINT, signal.SIG_DFL)
            sys.exit(app.exec_())
        else:
            sys.exit(1)
