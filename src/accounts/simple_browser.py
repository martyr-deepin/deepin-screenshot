#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2014 ~ 2015 Deepin, Inc.
#               2014 ~ 2015 Wang Yaohua
#
# Author:     Wang Yaohua <mr.asianwang@gmail.com>
# Maintainer: Wang Yaohua <mr.asianwang@gmail.com>
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
from PyQt5.QtCore import Qt, QUrl, QUrlQuery, pyqtSlot
from PyQt5.QtQuick import QQuickView
from PyQt5.QtGui import QSurfaceFormat, QColor

class SimpleBrowser(QQuickView):
    def __init__(self):
        QQuickView.__init__(self)
        self._account = None

        surface_format = QSurfaceFormat()
        surface_format.setAlphaBufferSize(8)

        self.setColor(QColor(0, 0, 0, 0))
        self.setFlags(Qt.FramelessWindowHint)
        self.setResizeMode(QQuickView.SizeRootObjectToView)
        self.setFormat(surface_format)

        parentDir = os.path.dirname(os.path.abspath(__file__))
        qmlPath = os.path.join(parentDir, "sources/Browser.qml")
        self.setSource(QUrl.fromLocalFile(qmlPath))

        self.rootObject().urlChanged.connect(self.urlChangedSlot)

    def setAccount(self, account):
        self._account = account

    def openUrl(self, url):
        self.rootObject().setUrl(url)
        self.show()

    @pyqtSlot("QUrl")
    def urlChangedSlot(self, url):
        if url.hasQuery() and self._account:
            query = QUrlQuery(url)
            code = query.queryItemValue("code")
            if code:
                self._account.authorizedCallback(code)