#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2015 Deepin Technology Co., Ltd.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.

import os

dirname = os.path.dirname
abspath = os.path.abspath

MAIN_DIR = dirname(dirname(abspath(__file__)))
MAIN_QML = os.path.join(dirname(abspath(__file__)), "Main.qml")
OSD_QML = os.path.join(dirname(abspath(__file__)), "OSD.qml")
GTK_CLIP = os.path.join(MAIN_DIR, "src/gtk-clip")
