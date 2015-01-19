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

from accounts import SinaWeibo
from database import db, SINAWEIBO

from PyQt5.QtCore import QObject, pyqtSlot

class AccountsManager(QObject):
    """Manager of all the SNS accounts"""
    def __init__(self):
        super(AccountsManager, self).__init__()
        self.sina_weibo = self.getSinaWeiboAccount()

    def getSinaWeiboAccount(self):
        sina_weibo = SinaWeibo()
        accounts = db.fetchAccessableAccounts(SINAWEIBO)
        if accounts:
            sina_weibo = SinaWeibo(*accounts[0])
        return sina_weibo

    def setSinaWeiboAccount(self, uid):
        account = db.fetchAccountByUID(SINAWEIBO, uid)
        if account:
            self.sina_weibo = SinaWeibo(*account)

    @pyqtSlot(str)
    def enableAccount(self, accountType):
        if accountType == SINAWEIBO:
            self.sina_weibo.enabled = True

    @pyqtSlot(result="QVariant")
    def getCurrentAccounts(self):
        result = []
        result.append([self.sina_weibo.uid, self.sina_weibo.username])
        return result

    @pyqtSlot(str, result=str)
    def getAuthorizeUrl(self, accountType):
        if accountType == SINAWEIBO:
            return self.sina_weibo.getAuthorizeUrl()

    @pyqtSlot(str, str)
    def handleAuthorizeCode(self, accountType, code):
        if accountType == SINAWEIBO:
            info = self.sina_weibo.getAccountInfoWithCode(code)
            db.saveAccountInfo(SINAWEIBO, info)

    @pyqtSlot(str)
    def share(self, text):
        self.sina_weibo.share(text)
