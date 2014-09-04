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

def remove_directory(path):
    """equivalent to command `rm -rf path`"""
    if os.path.exists(path):
        for i in os.listdir(path):
            full_path = os.path.join(path, i)
            if os.path.isdir(full_path):
                remove_directory(full_path)
            else:
                os.remove(full_path)
        os.rmdir(path)

def create_directory(directory, remove_first=False):
    '''Create directory.'''
    if remove_first and os.path.exists(directory):
        remove_directory(directory)

    if not os.path.exists(directory):
        os.makedirs(directory)

def update_pot():
    # Read config options.
    config_parser = ConfigParser()
    config_parser.read("locale_config.ini")
    project_name = config_parser.get("locale", "project_name")
    source_dir = config_parser.get("locale", "source_dir")
    locale_dir = os.path.abspath(config_parser.get("locale", "locale_dir"))
    create_directory(locale_dir)

    # Get input arguments.
    include_qml = False
    py_source_files = []
    for root, dirs, files in os.walk(source_dir):
        for each_file in files:
            if each_file.endswith(".qml") and not include_qml:
                include_qml = True
            if each_file.endswith(".py") and not each_file.startswith("."):
                py_source_files.append(os.path.join(root, each_file))

    pot_filepath = os.path.join(locale_dir, project_name + ".pot")
    if os.path.exists(pot_filepath):
        os.remove(pot_filepath)

    if include_qml:
        ts_filepath = os.path.join(locale_dir, project_name + ".ts")

        # Generate ts file
        subprocess.call(
            "deepin-lupdate -recursive %s -ts %s" % (os.path.realpath(source_dir), ts_filepath),
            shell=True)

        # convert to pot file.
        subprocess.call(
            "lconvert -i %s -o %s" % (ts_filepath, pot_filepath),
            shell=True)

        # clean string
        clean_str = ""
        with open(pot_filepath) as fp:
            for line in fp:
                if not line.startswith("msgctxt"):
                    clean_str += line

        with open(pot_filepath, "wb") as fp:
            fp.write(clean_str)

    # Merge pot file.
    if os.path.exists(pot_filepath):
        command = "xgettext -j -k_ -o %s %s" % (pot_filepath, ' '.join(py_source_files))
    else:
        command = "xgettext -k_ -o %s %s" % (pot_filepath, ' '.join(py_source_files))
    subprocess.call(command, shell=True)

if __name__ == "__main__":
    update_pot()

