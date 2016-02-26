#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2015 Deepin Technology Co., Ltd.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.

import gettext

LOCALE_DIR="/usr/share/locale"

_ = None
try:
    _ = gettext.translation("deepin-screenshot", LOCALE_DIR).gettext
except Exception, e:
    _ = lambda i : i
