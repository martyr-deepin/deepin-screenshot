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

from snspy import APIClient, TwitterMixin

from account_base import AccountBase
from database import db, TWITTER

APP_KEY = 'r2HHabDu8LDQCELxk2cA'
APP_SECRET = '9e4LsNOvxWVWeEgC5gthL9Q78F7FDsnT7lUIBruyQmI'
CALLBACK_URL = 'http://www.linuxdeepin.com'

class Twitter(AccountBase):
    def __init__(self, uid=None):
        super(Twitter, self).__init__()
        self._initClient()
        if uid: self.setUID(uid)

    def _initClient(self):
        self._client = APIClient(TwitterMixin,
                                 app_key = APP_KEY,
                                 app_secret = APP_SECRET,
                                 redirect_uri = CALLBACK_URL)

    def setUID(self, uid):
        self._uid = uid
        (token, expires) = self.getAccessToken()
        self._client.set_access_token(token, expires)

    def getAccessToken(self):
        account = db.fetchAccountByUID(TWITTER, self._uid)
        if account:
            return (account[2], account[3])
        else:
            return '', 0.0

    def _share(self, text, pic):
        if pic:
            with open(pic) as _pic:
                self._client.statuses.upload.post(status=text, pic=_pic)
        else:
            self._client.statuses.update.post(status=text)

    def share(self, text, pic=''):
        if not self.enabled: return

        if self._client.is_expires():
            self._text = text
            self._pic = pic
            self.authorize()
        else:
            self._share(text, pic)
            self._text = None
            self._pic = None

    def reshare(self):
        if self._text:
            self.share(self._text, self._pic)

    def authorize(self):
        url = self._client.get_authorize_url()

        self._browser.setAccount(self)
        self._browser.openUrl(url)

    def authorizedCallback(self, code):
        self._browser.hide()

        token_info = self._client.request_access_token(code)
        account_info = self._client.users.show.get(uid=token_info["uid"])
        info = (token_info["uid"], account_info["name"],
                token_info["access_token"], token_info["expires"])
        db.saveAccountInfo(TWITTER, info)
        self.reshare()