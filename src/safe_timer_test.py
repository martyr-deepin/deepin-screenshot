#!/usr/bin/env python

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
