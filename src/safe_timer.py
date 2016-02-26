#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2015 Deepin Technology Co., Ltd.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.

import threading

from PyQt5 import QtCore


class SafeTimer(QtCore.QObject):
    '''This class is used to replace QTimer.
    Sometimes, QTimer fails to trigger its callback slot.
    This class creates a thread and put the timer in that thread.
    '''

    timeout = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        QtCore.QObject.__init__(self, parent=parent)
        self._thread = QtCore.QThread(parent=parent)
        self.moveToThread(self._thread)
        self._interval = 0
        self._repeat = 0
        self._done = 0
        self._finished = threading.Event()

    def interval(self):
        return self._interval

    def setInterval(self, interval):
        assert interval >= 0, "interval of SafeTimer cannot be a negative number"
        self._interval = interval

    def repeat(self):
        return self._repeat

    def setRepeat(self, repeat):
        assert repeat >= 0, "repeat time cannot be a negative number"
        self._repeat = repeat

    def start(self):
        '''Start timer'''
        self._finished.wait(self._interval)
        while self._done < self._repeat:
            if not self._finished.is_set():
                print("Will emit timeout signal")
                self.timeout.emit()
                self._done += 1

        self._finished.set()

    def stop(self):
        '''Stop the timer if it has not been triggered'''
        self._finished.set()

    def isActive(self):
        '''Returns True if the timer is running, otherwise False.'''
        return not self._finished.set()

    @staticmethod
    def singleShot(interval, callback):
        '''This static function calls a slot after a given time interval.'''
        t = SafeTimer()
        t.setInterval(interval)
        t.setRepeat(1)
        t.timeout.connect(callback)
        t.start()
