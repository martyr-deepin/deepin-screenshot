#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2015 Deepin Technology Co., Ltd.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.

import sys

from PyQt5 import QtCore

from safe_timer import SafeTimer

def timerCallback():
    print("timer callback")
    #sys.exit(0)
    #QtCore.QCoreApplication.instance().exit(0)

if __name__ == '__main__':
    app = QtCore.QCoreApplication([])
#    t = SafeTimer()
#    t.setInterval(1)
#    t.setRepeat(2)
#    t.timeout.connect(timerCallback)
#    t.start()
    SafeTimer.singleShot(1, timerCallback)
    app.exec_()
