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
        
if __name__ == "__main__":
    # Read config options.
    config_parser = ConfigParser()
    config_parser.read("locale_config.ini")
    project_name = config_parser.get("locale", "project_name")
    source_dir = config_parser.get("locale", "source_dir")
    locale_dir = os.path.abspath(config_parser.get("locale", "locale_dir"))
    langs = eval(config_parser.get("locale", "langs"))
    create_directory(locale_dir)
    
    # Get input arguments.
    source_files = []
    for root, dirs, files in os.walk(source_dir):
        for each_file in files:
            if each_file.endswith(".py") and not each_file.startswith("."):
                source_files.append(os.path.join(root, each_file))
                
    pot_filepath = os.path.join(locale_dir, project_name + ".pot")
    
    # Generate pot file.
    subprocess.call(
        "xgettext --from-code=UTF-8 -k_ -o %s %s" % (pot_filepath, ' '.join(source_files)),
        shell=True)
    
    # Generate po files.
    for lang in langs:
        subprocess.call(
            "msginit --no-translator -l %s.UTF-8 -i %s -o %s" % (lang, pot_filepath, os.path.join(locale_dir, "%s.po" % (lang))),
            shell=True
            )
        
    # Replace ASCII with UTF-8.
    for lang in langs:
        po_filepath = os.path.join(locale_dir, "%s.po" % (lang))
        read_file = open(po_filepath, "r")
        whole_thing = read_file.read()
        read_file.close()
        
        write_file = open(po_filepath, "w")
        whole_thing = whole_thing.replace("charset=ASCII", "charset=UTF-8");
        write_file.write(whole_thing);
        write_file.close()
