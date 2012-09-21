#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2011 ~ 2012 Deepin, Inc.
#               2011 ~ 2012 Wang Yong
# 
# Author:     Wang Yong <lazycat.manatee@gmail.com>
# Maintainer: Wang Yong <lazycat.manatee@gmail.com>
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

import subprocess
import os
from ConfigParser import RawConfigParser as ConfigParser

if __name__ == "__main__":
    # Read config options.
    config_parser = ConfigParser()
    config_parser.read("locale_config.ini")
    project_name = config_parser.get("locale", "project_name")
    source_dir = os.path.abspath(config_parser.get("locale", "source_dir"))
    locale_dir = os.path.abspath(config_parser.get("locale", "locale_dir"))
    langs = eval(config_parser.get("locale", "langs"))

    # Generate mo files.
    for lang in langs:
        subprocess.call(
            "mkdir -p %s" % (os.path.join(locale_dir, "%s/LC_MESSAGES/" % (lang))),
            shell=True
            )
        
        subprocess.call(
            "msgfmt -o %s %s" % (
                os.path.join(locale_dir, "%s/LC_MESSAGES/%s.mo" % (lang, project_name)),
                os.path.join(locale_dir, "%s.po" % (lang))),
            shell=True
            )
    
