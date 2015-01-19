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
import time
import sqlite3

HOME = os.path.expanduser('~')
XDG_CONFIG_HOME = os.environ.get('XDG_CONFIG_HOME') or \
                  os.path.join(HOME, '.config')
PROJECT_NAME = "deepin-share-service"
CONFIG_DIR = os.path.join(XDG_CONFIG_HOME, PROJECT_NAME)
DATABASE_FILE = os.path.join(CONFIG_DIR, "accounts.db")

if not os.path.exists(CONFIG_DIR): os.makedirs(CONFIG_DIR)

SINAWEIBO = "sinaweibo"
TWITTER = "twitter"

class Database(object):

    def __init__(self):
        object.__init__(self)
        self.db_path = DATABASE_FILE
        self.db_connect = sqlite3.connect(self.db_path)
        self.db_cursor = self.db_connect.cursor()

        for _type in [SINAWEIBO, TWITTER]:
            self.db_cursor.execute(
                '''CREATE TABLE IF NOT EXISTS
                   %s (uid PRIMARY KEY, username, access_token, expires)
                ''' % _type)

    def fetchAccounts(self, accountType):
        self.db_cursor.execute("SELECT * FROM %s" % accountType)
        accounts = self.db_cursor.fetchall()
        return accounts

    def fetchAccountByUID(self, accountType, uid):
        self.db_cursor.execute(
            "SELECT * FROM %s WHERE uid=%s" % (accountType, uid))
        tuples = self.db_cursor.fetchone()
        if tuples:
            return tuples[0]
        else:
            return None

    def fetchAccessableAccounts(self, accountType):
        self.db_cursor.execute("SELECT * FROM %s" % accountType)
        accounts = self.db_cursor.fetchall()
        not_expired_func = lambda x: x[2] and x[3] > time.time()
        return filter(not_expired_func, accounts)

    def saveAccountInfo(self, accountType, info):
        self.db_cursor.execute(
            "INSERT OR REPLACE INTO %s VALUES(?, ?, ?, ?)" % accountType, info)
        self.db_connect.commit()

db = Database()