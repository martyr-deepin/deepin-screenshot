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

from snspy import APIClient, SinaWeiboMixin

from account_base import AccountBase


APP_KEY = '3703706716'
APP_SECRET = 'c0ecbf8644ac043070449ad0901692b8'
CALLBACK_URL = 'http://www.linuxdeepin.com'

class SinaWeibo(AccountBase):
    def __init__(self, uid='', username='', access_token='', expires=0):
        super(SinaWeibo, self).__init__()
        self.uid = uid
        self.username = username

        self._client = APIClient(SinaWeiboMixin,
                                 app_key = APP_KEY,
                                 app_secret = APP_SECRET,
                                 redirect_uri = CALLBACK_URL)
        self._client.set_access_token(access_token, expires)

    def valid(self):
        return not self._client.is_expires()

    def share(self, text, pic=None):
        if pic:
            with open(pic) as _pic:
                self._client.statuses.upload.post(status=text, pic=_pic)
        else:
            self._client.statuses.update.post(status=text)

    def getAuthorizeUrl(self):
        return self._client.get_authorize_url()

    def getAccountInfoWithCode(self, code):
        token_info = self._client.request_access_token(code)
        account_info = self._client.users.show.get(uid=token_info["uid"])
        info = (token_info["uid"], account_info["name"],
                token_info["access_token"], token_info["expires"])
        return info