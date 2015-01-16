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

class AccountsManager(object):
    """Manager of all the SNS accounts"""
    def __init__(self):
        super(AccountsManager, self).__init__()
        self._sina_weibo = self.getSinaWeiboAccount()

    def hasValidAccount(self):
        return self._sina_weibo.valid()

    def getSinaWeiboAccount(self):
        sina_weibo = SinaWeibo()
        accounts = db.fetchAccessableAccounts(SINAWEIBO)
        if accounts:
            sina_weibo = SinaWeibo(*accounts[0])
        return sina_weibo

    def setSinaWeiboAccount(self, uid):
        account = db.fetchAccountByUID(SINAWEIBO, uid)
        if account:
            self._sina_weibo = SinaWeibo(*account)

    def getAuthorizeUrl(self, accountType):
        if accountType == SINAWEIBO:
            return self._sina_weibo.getAuthorizeUrl()

    def handleAuthorizeCode(self, accountType, code):
        if accountType == SINAWEIBO:
            info = self._sina_weibo.getAccountInfoWithCode(code)
            db.saveAccountInfo(SINAWEIBO, info)

    def share(self, text, pics=None):
        self._sina_weibo.enabled = True
        self._sina_weibo.share(text, pics)