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

def main():
    # Read config options.
    config_parser = ConfigParser()
    config_parser.read("locale_config.ini")
    project_name = config_parser.get("locale", "project_name")
    locale_dir = os.path.abspath(config_parser.get("locale", "locale_dir"))
    mo_locale_dir = os.path.join(locale_dir, "mo")

    for f in os.listdir(locale_dir):
        lang, ext = os.path.splitext(f)
        if ext == ".po":
            mo_dir = os.path.join(mo_locale_dir, lang, "LC_MESSAGES")
            mo_path = os.path.join(mo_dir, "%s.mo" % project_name)
            po_path = os.path.join(locale_dir, f)
            subprocess.call(
                "mkdir -p %s" % mo_dir,
                shell=True
                )

            subprocess.call(
                "msgfmt -o %s %s" % (mo_path, po_path),
                shell=True
                )

            subprocess.call(
                "sudo cp -r %s %s" % (
                    os.path.join(mo_locale_dir, lang),
                    "/usr/share/locale/"),
                shell=True
                )

if __name__ == "__main__":
    main()
