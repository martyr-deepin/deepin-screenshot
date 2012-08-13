#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2011 Deepin, Inc.
#               2011 Hou Shaohui
#
# Author:     Hou Shaohui <houshao55@gmail.com>
# Maintainer: Hou ShaoHui <houshao55@gmail.com>
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

import gtk, os, sys, time
from main import DeepinScreenshot
from window import getScreenshotPixbuf
from optparse import OptionParser
from tipswindow import countdownWindow
from utils import makeMenuItem, getFormatTime, getPicturesDir, parserPath
from constant import DEFAULT_FILENAME

saveFiletype = "png"

def openFileDialog(fullscreen=True, filetype='png'):
    '''Save file to file.'''
    pixbuf = getScreenshotPixbuf(fullscreen)
    dialog = gtk.FileChooserDialog(
                                   "Save..",
                                   None,
                                   gtk.FILE_CHOOSER_ACTION_SAVE,
                                   (gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT,
                                    gtk.STOCK_SAVE, gtk.RESPONSE_ACCEPT))
    dialog.set_default_response(gtk.RESPONSE_ACCEPT)
    dialog.set_position(gtk.WIN_POS_CENTER)
    dialog.set_local_only(True)
    dialog.set_current_folder(getPicturesDir())
    dialog.set_current_name("%s%s.%s" % (DEFAULT_FILENAME, getFormatTime(), saveFiletype))

    optionMenu = gtk.OptionMenu()
    optionMenu.set_size_request(155, -1)
    menu = gtk.Menu()
    menu.set_size_request(155, -1)
    pngItem = makeMenuItem('PNG (*.png)',
                 lambda item, data: setSaveFiletype(dialog, 'png'))
    jpgItem = makeMenuItem('JPEG (*.jpeg)',
                 lambda item, data: setSaveFiletype(dialog, 'jpeg'))
    bmpItem = makeMenuItem('BMP (*.bmp)',
                 lambda item, data: setSaveFiletype(dialog, 'bmp'))
    menu.append(pngItem)
    menu.append(jpgItem)
    menu.append(bmpItem)
    optionMenu.set_menu(menu)
    hbox = gtk.HBox()
    hbox.pack_end(optionMenu, False, False)
    dialog.vbox.pack_start(hbox, False, False)
    hbox.show_all()                          
    response = dialog.run()
    if response == gtk.RESPONSE_ACCEPT:
        filename = dialog.get_filename()
        pixbuf.save(filename, filetype)
        print "Save snapshot to %s" % (filename)
    elif response == gtk.RESPONSE_REJECT:
        print 'Closed, no files selected'
    dialog.destroy()

def setSaveFiletype(widget, filetype):
    widget.set_current_name("%s%s.%s" % (DEFAULT_FILENAME, getFormatTime(), filetype))
    saveFiletype =filetype
       

def processArguments():
    '''init processArguments '''
    parser = OptionParser(usage="Usage: deepin-screenshot [options] [arg]", version="deepin-screenshot v2.1")
    parser.add_option("-f", "--full", action="store_true", dest="fullscreen", help="Taking the fullscreen shot")
    parser.add_option("-w", "--window", action="store_true", dest="window", help="Taking the currently focused window")
    parser.add_option("-d", "--delay", dest="delay", type="int", help="wait NUM seconds before taking a shot", metavar="NUM")
    parser.add_option("-s", "--save", dest="save_file", help="save screenshot to FILE", metavar="FILE")
    parser.add_option("-a", "--area", help="Grab an area of the screen instead of the entire screen", action="store_true")
    parser.add_option("-e", "--border-effect", action="store_true", dest="border_effect", help="Effect to add to the border")
    parser.add_option("-i", "--interactive", action="store_true" ,help="Interactively set options")
    parser.add_option("-b", "--include-border", action="store_true" ,help="Include the window border with the screenshot")
    parser.add_option("-B", "--remove-border", action="store_true" ,help="Remove the window border from the screenshot")
    parser.add_option("-c", "--clipboard", help="Send the grab directly to the clipboard",  action="store_true")
    parser.add_option("--display",  action="store_true")    
    
    
    
    (options, args) = parser.parse_args()

    if options.fullscreen and options.window:
        parser.error("options -f and -w are mutually exclusive")
    elif options.save_file:
        parserFile = parserPath(str(options.save_file))
        if options.fullscreen:
            if options.delay:
                countdownWindow(options.delay)
            pixbuf = getScreenshotPixbuf(True)
            pixbuf.save(parserFile[0], parserFile[1])
        elif options.window:
            if options.delay:
                countdownWindow(options.delay)
            pixbuf = getScreenshotPixbuf(False)
            pixbuf.save(parserFile[0], parserFile[1])
        else:    
            if options.delay:
                countdownWindow(options.delay)
            DeepinScreenshot(options.save_file)
    elif options.fullscreen:
        if options.delay:
            countdownWindow(options.delay)
            openFileDialog()
        else:
            openFileDialog()
    elif options.window:
        if options.delay:
            countdownWindow(options.delay)
            openFileDialog(False)
        else:
            openFileDialog(False)
    elif options.fullscreen and options.window or options.delay:
        countdownWindow(options.delay)
        DeepinScreenshot()
    else:
         DeepinScreenshot()
        
        

if __name__ == '__main__':
    processArguments()
    
        
        
    


