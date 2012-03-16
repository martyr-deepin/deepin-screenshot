#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2011 Deepin, Inc.
#               2011 Wang Yong
#
# Author:     Wang Yong <lazycat.manatee@gmail.com>
#             Zhang Cheng <zhangcheng@linuxdeepin.com>
#             Hou ShaoHui <houshaohui@linuxdeepin.com>

# Maintainer: Wang Yong <lazycat.manatee@gmail.com>
#             Zhang Cheng <zhangcheng@linuxdeepin.com>
#             Hou Shaohui <houshaohui@linuxdeepin.com>
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

from action import *
from utils import *
from math import *
from draw import *
from constant import *
from keymap import *
from window import *
from lang import __

import pango
import sys
import time
import gtk
import pygtk
import os
import glib
import subprocess

pygtk.require('2.0')

class DeepinScreenshot(object):
    '''Main scrot.'''
	
    def __init__(self, save_file=""):
        '''Init Main scrot.'''

        # Init.
        self.action = ACTION_WINDOW
        self.width = self.height = 0
        self.x = self.y = self.rectWidth = self.rectHeight = 0
        self.buttonToggle = None
        
        self.frameColor = "#00AEFF"# "#FFFF0" 
        self.frameLineWidth = 2
        self.dragPosition = None
        self.dragStartX = self.dragStartY = self.dragStartOffsetX = self.drawStartOffsetY = 0
        self.dragPointRadius = 4
        
        self.dragFlag = False
        self.showToolbarFlag = False
        self.showColorbarFlag = False 
        self.showTextWindowFlag = False
        self.textDragOffsetX = self.textDragOffsetY = 0
        self.saveFiletype = 'png'
        self.saveFilename = save_file
        
        self.toolbarOffsetX = 10
        self.toolbarOffsetY = 10
        #self.toolbarHeight = 50
        
        self.actionSize = 2
        self.actionColor = "#FF0000"
        self.fontName = "Sans 10"
        
        # default window 
        self.scrotWindowInfo = getScrotWindowInfo()
        self.windowFlag = True

        # keybinding map
        self.keyBindings = {}
        
        # Init action list.
        self.currentAction = None
        self.actionList = []
        self.currentTextAction = None
        self.textActionList = []
        self.textActionInfo = {}
        self.textDragFlag = False
        self.textModifyFlag = False
        self.drawTextLayoutFlag = False

        
        # Get desktop background.
        self.desktopBackground = self.getDesktopSnapshot() 
        
        # Init window.
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.fullscreen()
        self.window.set_icon_from_file("../theme/logo/deepin-scrot.ico")
        self.window.set_keep_above(True)
        
        # Init event handle.
        self.window.add_events(gtk.gdk.KEY_RELEASE_MASK)
        self.window.add_events(gtk.gdk.POINTER_MOTION_MASK)
        self.window.add_events(gtk.gdk.BUTTON_PRESS_MASK)
        self.window.add_events(gtk.gdk.BUTTON_RELEASE_MASK)
        self.window.connect("destroy", self.destroy)
        self.window.connect("expose-event", lambda w, e: self.getCurrentCoord(w))
        self.window.connect("expose-event", self.redraw)
        self.window.connect("button-press-event", self.buttonPress)
        
        self.window.connect("button-press-event", self.doubleClickRect)
        self.window.connect("button-release-event", self.buttonRelease)
        self.window.connect("motion-notify-event", self.motionNotify)
        self.window.connect("key-press-event", self.keyPress)
        
        # Register key binding.
        self.registerKeyBinding("Escape", lambda : self.destroy(self.window))
        self.registerKeyBinding("C-s", self.saveSnapshotToFile)
        self.registerKeyBinding("Return", self.saveSnapshot)
        self.registerKeyBinding("C-z", self.undo)
        
        # Init toolbar window.
        self.initToolbar()
        
        # Init text window.
        self.initTextWindow()
        
        # Init color window.
        self.initColorWindow()
       
        # Show.
        self.window.show_all()
        
        gtk.main()
        
    
    def initColorWindow(self):
        ''' init ColorWindow'''
        paddingX = 5
        paddingY = 4
        iconWidth = iconHeight = 28
        self.colorNum = 9
        self.iconIndex = 2
        
        self.colorbarWindow = gtk.Window(gtk.WINDOW_POPUP)
        self.colorbarWindow.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_DIALOG)
        self.colorbarWindow.set_keep_above(True)
        self.colorbarWindow.set_transient_for(self.window)
        
        self.colorbarWindow.set_decorated(False)
        self.colorbarWindow.set_resizable(False)
        self.colorbarWindow.set_default_size(100, 24)

        self.colorbarWindow.set_size_request(
            -1,
                # iconWidth * self.colorNum + paddingX * 2,
                iconHeight + paddingY * 2 )

        self.colorbarBox = gtk.HBox(False, 4)
        self.sizeBox = gtk.HBox()
        self.dynamicBox = gtk.HBox()
        self.colorbarAlign = gtk.Alignment()
        self.colorbarAlign.set(0.5,0.5,0,0)
        self.colorbarAlign.set_padding(paddingY, paddingY, paddingX, paddingX)
        self.colorbarAlign.add(self.colorbarBox)
        self.colorbarWindow.add(self.colorbarAlign)


        self.colorbarWindow.connect("size-allocate", lambda w, a: updateShape(w, a, 2))
        self.colorbarWindow.connect('expose-event', lambda w,e: exposeBackground(w, e, appTheme.getDynamicPixbuf("color_bg.png")))
        
    
        self.smallSizeButton = self.createSizeButton('small', 2)
        self.smallSizeButton.connect('button-press-event', lambda w, e: self.setIconIndex(2))

        self.normalSizeButton = self.createSizeButton('normal', 3)
        self.normalSizeButton.connect('button-press-event', lambda w, e: self.setIconIndex(3))

        self.bigSizeButton = self.createSizeButton('big', 5)
        self.bigSizeButton.connect('button-press-event', lambda w, e: self.setIconIndex(5))
        
        self.sizeAlign = gtk.Alignment()
        self.sizeAlign.set(0.5,0.5,0,0)
        self.sizeAlign.set_padding(2, 1, 0, 0)
        self.sizeAlign.add(self.sizeBox)
        self.dynamicBox.pack_start(self.sizeAlign)
        self.colorbarBox.pack_start(self.dynamicBox)
        
        self.fontLabel = gtk.Label("Sans 10")
        self.fontEvent = gtk.EventBox()
        self.fontEvent.add(self.fontLabel)
        self.fontEvent.set_visible_window(False)
        self.fontEvent.connect("button-press-event", lambda w, e: self.openFontDialog()) 
        setClickableCursor(self.fontEvent)
        self.fontEvent.set_size_request(100, -1)

        separatorLabel = gtk.Label()
        drawSeparator(separatorLabel, 'sep')
        self.colorbarBox.pack_start(separatorLabel)
        
        self.colorBox = gtk.EventBox()

        self.colorbarBox.pack_start(self.colorBox)
        self.colorBox.set_events(gtk.gdk.BUTTON_PRESS_MASK)
        self.colorBox.set_size_request(28,28)
        self.colorBox.set_app_paintable(True)
        setClickableCursor(self.colorBox)
        self.colorBox.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("#FF0000"))
        self.colorBox.connect('expose-event', lambda w, e:self.setColorboxBorder(w))
        self.colorBox.connect('button-press-event', self.colorSetEvent)

        self.vbox = gtk.VBox(False, 2)
        self.aboveHbox = gtk.HBox(False, 2)
        self.belowHbox = gtk.HBox(False, 2)
        self.colorMap = {'black'       : "#000000",
                         'gray_dark'   : "#808080",
                         'red_dark'    : "#800000",
                         'yellow_dark' : "#808000",
                         'green_dark'  : "#008000",
                         'blue_dark'   : "#000080",
                         'pink_dark'   : "#800080",
                         'wathet_dark' : "#008080",
                         'white'       : "#FFFFFF",
                         'gray'        : "#C0C0C0",
                         'red'         : "#FF0000",
                         'yellow'      : "#FFFF00",
                         'green'       : "#00FF00",
                         'blue'        : "#0000FF",
                         'pink'        : "#FF00FF",
                         'wathet'      : "#00FFFF"}

        blackButton = self.createColorButton('black')
        blackButton.connect('button-press-event', lambda w,e: self.setButtonColor('black'))

        grayDarkButton = self.createColorButton('gray_dark')
        grayDarkButton.connect('button-press-event', lambda w,e: self.setButtonColor('gray_dark'))

        redDarkButton = self.createColorButton('red_dark')
        redDarkButton.connect('button-press-event', lambda w,e: self.setButtonColor('red_dark'))

        yellowDarkButton = self.createColorButton('yellow_dark')
        yellowDarkButton.connect('button-press-event', lambda w,e: self.setButtonColor('yellow_dark'))

        greenDarkButton = self.createColorButton('green_dark')
        greenDarkButton.connect('button-press-event', lambda w,e: self.setButtonColor('green_dark'))

        blueDarkButton = self.createColorButton('blue_dark')
        blueDarkButton.connect('button-press-event', lambda w,e: self.setButtonColor('blue_dark'))

        pinkDarkButton = self.createColorButton('pink_dark')
        pinkDarkButton.connect('button-press-event', lambda w,e: self.setButtonColor('pink_dark'))
        wathetDarkButton = self.createColorButton('wathet_dark')
        wathetDarkButton.connect('button-press-event', lambda w,e: self.setButtonColor('wathet_dark'))


        self.vbox.pack_start(self.aboveHbox)

        whiteButton  = self.createColorButton('white', False)
        whiteButton.connect('button-press-event', lambda w,e: self.setButtonColor('white'))

        grayButton =  self.createColorButton('gray', False)
        grayButton.connect('button-press-event', lambda w,e: self.setButtonColor('gray'))

        redButton = self.createColorButton('red', False)
        redButton.connect('button-press-event', lambda w,e: self.setButtonColor('red'))

        yellowButton = self.createColorButton('yellow', False)
        yellowButton.connect('button-press-event', lambda w,e: self.setButtonColor('yellow'))

        greenButton = self.createColorButton('green', False)
        greenButton.connect('button-press-event', lambda w,e: self.setButtonColor('green'))

        blueButton = self.createColorButton('blue', False)
        blueButton.connect('button-press-event', lambda w,e: self.setButtonColor('blue'))

        pinkButton = self.createColorButton('pink', False)
        pinkButton.connect('button-press-event', lambda w,e: self.setButtonColor('pink'))
        
        wathetButton = self.createColorButton('wathet', False)
        wathetButton.connect('button-press-event', lambda w,e: self.setButtonColor('wathet'))

        self.vbox.pack_start(self.belowHbox)
        self.colorbarBox.pack_start(self.vbox)
        
    def openFontDialog(self):
        '''open font dialog.'''
        self.fontDialog = gtk.FontSelectionDialog("font select")
        if self.showTextWindowFlag:
            self.fontDialog.set_transient_for(self.textWindow)
        else:
            self.fontDialog.set_transient_for(self.window)
        self.hideToolbar()
        self.hideColorbar()
        self.fontDialog.set_font_name(self.fontName)
        response = self.fontDialog.run()
        if response == gtk.RESPONSE_OK:
            self.fontName = self.fontDialog.get_font_name()
            self.fontLabel.set_label(self.fontDialog.get_font_name())
        
        self.adjustToolbar()
        self.showToolbar()
        self.showColorbar()
        self.fontDialog.destroy()
       
    def colorSetEvent(self, widget, event):
        '''colorBox button_press event'''
        self.colorDialog = gtk.ColorSelectionDialog('Select color')
        self.colorDialog.set_keep_above(True)
        if self.showTextWindowFlag:
            self.colorDialog.set_transient_for(self.textWindow)
        else:
            self.colorDialog.set_transient_for(self.window)
        colorsel = self.colorDialog.colorsel
        colorsel.set_has_palette(True)
        #colorsel.connect("color_changed", self.colorChanged)
        self.hideToolbar()
        self.hideColorbar()
        response = self.colorDialog.run()
        if response == gtk.RESPONSE_OK:
            self.actionColor = gdkColorToString(colorsel.get_current_color())
            modifyBackground(self.colorBox, self.actionColor)

        self.adjustToolbar()
        self.showToolbar()
        self.showColorbar()
        self.colorDialog.destroy()
    
    def setColorboxBorder(self, widget):
        '''set colorBox border '''
        (x, y, width, height, depth) = widget.window.get_geometry() 
        cr = widget.window.cairo_create()
        cr.set_line_width(2)
        cr.rectangle(0,0,width, height)
        cr.set_source_rgb(*colorHexToCairo("#000000"))
        cr.stroke()
        cr.rectangle(2,2,width-4, height-4)
        cr.set_line_width(1)
        cr.set_source_rgb(*colorHexToCairo("#FFFFFF"))
        cr.stroke()
        
    def initToolbar(self):
        '''Init toolbar.'''
        # Init window.
        # Use WINDOW_POPUP to ignore Window Manager's policy,
        # otherwise toolbar window won't move to place you want, such as, desktop environment have global menu.
        self.toolbarPaddingX = 5
        self.toolbarPaddingY = 2
        self.toolbarIconWidth = self.toolbarIconHeight = 28
        self.toolbarIconNum = 10
        self.toolbarWindow = gtk.Window(gtk.WINDOW_POPUP)
        self.toolbarWindow.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_DIALOG)
        self.toolbarWindow.set_keep_above(True)
        self.toolbarWindow.set_decorated(False)
        self.toolbarWindow.set_resizable(False)
        self.toolbarWindow.set_transient_for(self.window)
        self.toolbarWindow.set_default_size(100, 24)
        self.toolbarWindow.connect("size-allocate", lambda w, a: updateShape(w, a, 2))
        self.toolbarWindow.connect("expose-event", lambda w, e: exposeBackground(w, e, appTheme.getDynamicPixbuf("bg.png")))
        self.toolbarWindow.set_size_request(
            self.toolbarIconWidth * self.toolbarIconNum + self.toolbarPaddingX * 2,
            self.toolbarIconHeight + self.toolbarPaddingY * 2)
        
        # Add action button.
        self.toolBox = gtk.HBox(False, 2)
        self.toolAlign = gtk.Alignment()
        self.toolAlign.set(0.5, 0.5, 0, 0)
        self.toolAlign.set_padding(self.toolbarPaddingY + 2, self.toolbarPaddingY, self.toolbarPaddingX, self.toolbarPaddingX)
        self.toolAlign.add(self.toolBox)
        self.toolbarWindow.add(self.toolAlign)
        
        self.actionRectangleButton = self.createActionButton("rect", __("Tip draw rectangle"))
        self.actionRectangleButton.connect("button-press-event", lambda w, e: self.setOtherInactive(w))
        self.actionRectangleButton.connect('toggled', lambda w: self.buttonToggled(w))
        self.actionRectangleButton.connect("button-release-event", lambda w, e: self.toggleReleaseEvent())
        

        
        self.actionEllipseButton = self.createActionButton("ellipse", __("Tip draw ellipse"))
        self.actionEllipseButton.connect("button-press-event", lambda w, e: self.setOtherInactive(w))
        self.actionEllipseButton.connect('toggled', lambda w: self.buttonToggled(w))
        self.actionEllipseButton.connect("button-release-event", lambda w, e: self.toggleReleaseEvent())
        
        self.actionArrowButton = self.createActionButton("arrow", __("Tip draw arrow"))
        self.actionArrowButton.connect("button-press-event", lambda w, e: self.setOtherInactive(w))
        self.actionArrowButton.connect('toggled', lambda w: self.buttonToggled(w))
        self.actionArrowButton.connect("button-release-event", lambda w, e: self.toggleReleaseEvent())
        
        self.actionLineButton = self.createActionButton("line", __("Tip draw line"))
        self.actionLineButton.connect("button-press-event", lambda w, e: self.setOtherInactive(w))
        self.actionLineButton.connect('toggled', lambda w: self.buttonToggled(w))
        self.actionLineButton.connect("button-release-event", lambda w, e: self.toggleReleaseEvent())

        self.actionTextButton = self.createActionButton("text", __("Tip draw text"))
        self.actionTextButton.connect("button-press-event", lambda w, e: self.setOtherInactive(w))
        self.actionTextButton.connect("toggled", lambda w: self.buttonToggled(w))
        self.actionTextButton.connect("button-release-event", lambda w, e: self.toggleReleaseEvent())
        separatorLabel = gtk.Button()
        drawSeparator(separatorLabel, 'sep')
        self.toolBox.pack_start(separatorLabel)

        self.actionUndoButton = self.createOtherButton("undo", __("Tip undo"))
        self.actionUndoButton.connect("button-press-event", lambda w, e: self.undo())
        
        self.actionSaveButton = self.createOtherButton("save", __("Tip save"))
        self.actionSaveButton.connect("button-press-event", lambda w, e: self.saveSnapshotToFile())
        
        separatorLabel = gtk.Button()
        drawSeparator(separatorLabel, 'sep')
        self.toolBox.pack_start(separatorLabel)

        self.actionCancelButton = self.createOtherButton("cancel", __("Tip cancel"))
        self.actionCancelButton.connect("button-press-event", lambda w, e: self.destroy(self.window))

        self.actionFinishButton = self.createOtherButton("finish",__("Tip finish"))
        self.actionFinishButton.connect("button-press-event", lambda w, e: self.saveSnapshot())
      
    def setOtherInactive(self, button):
        buttonList = [self.actionRectangleButton, self.actionEllipseButton, self.actionArrowButton, self.actionLineButton,
                      self.actionTextButton]
        
        for eachButton in buttonList:
            if eachButton == button:
                continue
            eachButton.set_active(False)
    
    def setAllInactive(self):
        buttonList = [self.actionRectangleButton, self.actionEllipseButton, self.actionArrowButton, self.actionLineButton,
                      self.actionTextButton]
        
        for eachButton in buttonList:
            eachButton.set_active(False)
        
    def isHaveOneToggled(self):
        buttonList = [self.actionRectangleButton, self.actionEllipseButton, self.actionArrowButton, self.actionLineButton,
                      self.actionTextButton]
        
        for eachButton in buttonList:
            if eachButton.get_active():
                return True
        return False
    
    def toggleReleaseEvent(self):
        buttonList = [self.actionRectangleButton, self.actionEllipseButton, self.actionArrowButton, self.actionLineButton,
                      self.actionTextButton]
        self.isToggled = False
        
        for eachButton in buttonList:
            if eachButton.get_active():
                self.isToggled = True
    
    def buttonToggled(self, widget):
        '''the button toggled'''
        if widget.get_active():
            if widget == self.actionRectangleButton:
                self.setActionType(ACTION_RECTANGLE)
            elif widget == self.actionEllipseButton:
                self.setActionType(ACTION_ELLIPSE)
            elif widget == self.actionArrowButton:
                self.setActionType(ACTION_ARROW)
            elif widget == self.actionLineButton:
                self.setActionType(ACTION_LINE)
            elif widget == self.actionTextButton:
                self.setActionType(ACTION_TEXT)
            
            self.showColorbar()

        else:
            self.hideColorbar()
            if not self.actionList and not self.textActionList and self.showToolbarFlag and not self.windowFlag:
                self.setActionType(ACTION_SELECT)
            elif self.actionList and self.isToggled or self.textActionList:
                self.setActionType(None)
        
    def setIconIndex(self, index):
        '''Set icon index.'''
        self.iconIndex = index
        self.actionSize = index
        self.colorbarWindow.queue_draw()
        
    def getIconIndex(self):
        '''Get icon index.'''
        return self.iconIndex
        
    def initTextWindow(self):
        '''Init text window.'''
        # Init window.
        # Use WINDOW_POPUP to ignore Window Manager's policy,
        # otherwise text window won't move to place you want, such as, desktop environment have global menu.
        self.textWindow = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.textWindow.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_DIALOG)
        self.textWindow.connect("size-allocate", lambda w, a: updateShape(w, a, 3))
        self.textWindow.set_decorated(False)
        self.textWindow.connect("expose-event", lambda w, e: exposeBackground(w, e, appTheme.getDynamicPixbuf("bg.png")))
        self.textWindow.set_keep_above(True)
        self.textWindow.set_resizable(False)
        self.textWindow.set_transient_for(self.window)

        self.textAlign = gtk.Alignment()
        self.textAlign.set(0.5, 0.5, 0, 0)
        self.textAlign.set_padding(10, 10, 10, 10)
        self.textVbox = gtk.VBox()

        scrollWindow = gtk.ScrolledWindow()
        scrollWindow.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        scrollWindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC) 

        self.textView = gtk.TextView()

        textBuffer = self.textView.get_buffer()
        self.textView.connect("expose-event", self.exposeTextViewTag)
        
        self.textTag = textBuffer.create_tag("first",
                                        foreground_gdk=gtk.gdk.color_parse(self.actionColor),
                                        font=self.fontName)
        textBuffer.apply_tag(self.textTag, textBuffer.get_start_iter(), textBuffer.get_end_iter())
        
        self.textView.set_cursor_visible(True)
        self.textView.set_wrap_mode(gtk.WRAP_WORD)
        self.textView.set_size_request(300, 60)
        
        scrollWindow.add(self.textView)
        self.textVbox.pack_start(scrollWindow)
        self.textAlign.add(self.textVbox)
        self.textWindow.add(self.textAlign)
        self.textWindow.set_focus(self.textView)
    
    def exposeTextViewTag(self, widget, event):
        ''' expose of textView'''
        textBuffer = widget.get_buffer()
        startIter = textBuffer.get_start_iter()
        endIter = textBuffer.get_end_iter()

        self.textTag.set_property("foreground_gdk", gtk.gdk.color_parse(self.actionColor))
        self.textTag.set_property("font", self.fontName)
        textBuffer.apply_tag_by_name("first", startIter, endIter)

    def showTextWindow(self, (ex, ey)):
        '''Show text window.'''
        offset = 5
        self.showTextWindowFlag = True
        self.textWindow.show_all()
        self.textWindow.move(ex, ey)
        
    def hideTextWindow(self):
        '''Hide text window.'''
        self.showTextWindowFlag = False
        self.textView.get_buffer().set_text("")
        self.textWindow.hide_all()
    
    def getInputText(self):
        '''Get input text.'''
        textBuffer = self.textView.get_buffer()
        return (textBuffer.get_text(textBuffer.get_start_iter(), textBuffer.get_end_iter())).rstrip(" ")
        
    def setActionType(self, aType):
        '''Set action. type'''
        self.action = aType    
        self.currentAction = None
        
    def createActionButton(self, iconName, helpText):
        '''Create action button.'''
        actionButton = gtk.ToggleButton()
        drawSimpleButton(actionButton, iconName, helpText)
        self.toolBox.pack_start(actionButton)
        
        return actionButton
    
    def createOtherButton(self, iconName, helpText):
        ''' no toggle button'''
        Button = gtk.Button()
        drawSimpleButton(Button, iconName, helpText)
        self.toolBox.pack_start(Button)
        return Button
    
    def createSizeButton(self, iconName, index):
        ''' size button'''
        Button = gtk.Button()
        drawSizeButton(Button, iconName, index, self.getIconIndex)
        self.sizeBox.pack_start(Button)
        return Button
    
    def createColorButton(self, iconName, above = True):
        button = gtk.Button()
        drawColorButton(button, iconName)
        
        if above:
            self.aboveHbox.pack_start(button)
        else:
            self.belowHbox.pack_start(button)
        return button
    
    def setButtonColor(self, colorName):
        modifyBackground(self.colorBox, self.colorMap[colorName])
        self.actionColor = self.colorMap[colorName]
        
    def showToolbar(self):
        '''Show toolbar.'''
        self.showToolbarFlag = True
        self.toolbarWindow.show_all()
        
    def hideToolbar(self):
        '''Hide toolbar.'''
        self.showToolbarFlag = False
        self.toolbarWindow.hide_all()
    
    def showColorbar(self):
        '''show colorbar '''
        if self.action == ACTION_TEXT:
            containerRemoveAll(self.dynamicBox)
            self.dynamicBox.add(self.fontEvent)
        else:
            containerRemoveAll(self.dynamicBox)
            self.dynamicBox.add(self.sizeAlign)
        self.showColorbarFlag = True
        self.adjustColorbar()
        self.colorbarWindow.show_all()
    
    def hideColorbar(self):
        '''hide colorbar'''
        self.showColorbarFlag = False
        self.colorbarWindow.hide_all()
  
    def adjustToolbar(self):
        '''Adjust toolbar position.'''
        (x, y, self.toolbarWidth, self.toolbarHeight, depth) = self.toolbarWindow.window.get_geometry()
        colorbarHeight = 32
        
        self.toolbarX = (self.x + self.rectWidth - self.toolbarWidth, self.toolbarOffsetX)[self.x + self.rectWidth - self.toolbarWidth < self.toolbarOffsetX]
        
        if self.y + self.rectHeight + self.toolbarOffsetY + self.toolbarHeight + colorbarHeight + 5 < self.height:
            self.toolbarY = self.y + self.rectHeight + self.toolbarOffsetY
        elif self.y - self.toolbarOffsetY - self.toolbarHeight -colorbarHeight - 5 > 0:
            self.toolbarY = self.y - self.toolbarOffsetY - self.toolbarHeight
        else:
            self.toolbarY = self.y + self.toolbarOffsetY
            
        self.toolbarWindow.move(int(self.toolbarX), int(self.toolbarY))
    
    def adjustColorbar(self):
        '''Adjust Colorbar position '''
        if self.toolbarY < self.y:
            colorbarY =  self.toolbarY - self.toolbarHeight - 8
        else:
            colorbarY = self.toolbarY + self.toolbarHeight + 5
        colorbarX = self.toolbarX
        self.colorbarWindow.move(int(colorbarX), int(colorbarY))
        
    def getEventCoord(self, event):
        '''Get event coord.'''
        (rx, ry) = event.get_root_coords()
        return (int(rx), int(ry))
        
    def buttonPress(self, widget, event):
        '''Button press.'''
        self.dragFlag = True
        if self.action == ACTION_WINDOW:
                self.windowFlag = False
            
        elif self.action == ACTION_INIT:
            (self.x, self.y) = self.getEventCoord(event)
            
        elif self.action == ACTION_SELECT:
            # Init drag position.
            self.dragPosition = self.getPosition(event)
            
            # Set cursor.
            self.setCursor(self.dragPosition)
            
            # Get drag coord and offset.
            (self.dragStartX, self.dragStartY) = self.getEventCoord(event)
            self.dragStartOffsetX = self.dragStartX - self.x
            self.dragStartOffsetY = self.dragStartY - self.y
        elif self.action == ACTION_RECTANGLE:
            # Just create new action when drag position at inside of select area.
            if self.getPosition(event) == DRAG_INSIDE:
                self.currentAction = RectangleAction(ACTION_RECTANGLE, self.actionSize, self.actionColor)
                self.currentAction.startDraw(self.getEventCoord(event))
        elif self.action == ACTION_ELLIPSE:
            # Just create new action when drag position at inside of select area.
            if self.getPosition(event) == DRAG_INSIDE:
                self.currentAction = EllipseAction(ACTION_ELLIPSE, self.actionSize, self.actionColor)
                self.currentAction.startDraw(self.getEventCoord(event))
        elif self.action == ACTION_ARROW:
            # Just create new action when drag position at inside of select area.
            if self.getPosition(event) == DRAG_INSIDE:
                self.currentAction = ArrowAction(ACTION_ARROW, self.actionSize, self.actionColor)
                self.currentAction.startDraw(self.getEventCoord(event))
        elif self.action == ACTION_LINE:
            # Just create new action when drag position at inside of select area.
            if self.getPosition(event) == DRAG_INSIDE:
                self.currentAction = LineAction(ACTION_LINE, self.actionSize, self.actionColor)
                self.currentAction.startDraw(self.getEventCoord(event))
        elif self.action == ACTION_TEXT:
            
            if self.textWindow.get_visible():
                content = self.getInputText()
                if content != "":
                    if self.textModifyFlag:
                        self.currentTextAction.update(self.actionColor, self.fontName, content)
                        self.textModifyFlag = False
                    else:
                        textAction = TextAction(ACTION_TEXT, 15, self.actionColor, self.fontName, content)
                        textAction.startDraw(self.textWindow.get_window().get_origin())
                        self.textActionList.append(textAction)
                        self.actionList.append(textAction)
                    self.hideTextWindow()
                    self.setAllInactive()
                    
                    self.window.queue_draw()
                else:
                    self.hideTextWindow()
                    self.setAllInactive()
            else:
                self.showTextWindow(self.getEventCoord(event))
        if self.action in [ACTION_RECTANGLE, ACTION_ELLIPSE, ACTION_ARROW, ACTION_LINE] and self.showToolbarFlag and self.y < self.toolbarY < self.y + self.rectHeight:
            self.hideToolbar()
            self.hideColorbar()

        if self.currentTextAction and self.action == None:
            currentX, currentY = self.getEventCoord(event)
            drawTextX,drawTextY = self.currentTextAction.getLayoutInfo()[:2]
            self.textDragOffsetX = currentX - drawTextX
            self.testDragOffsetY = currentY - drawTextY
            self.textDragFlag = True 
    
    def motionNotify(self, widget, event):
        '''Motion notify.'''
        if self.dragFlag:
            # print "motionNotify: %s" % (str(event.get_root_coords()))
            (ex, ey) = self.getEventCoord(event)
            
            if self.action == ACTION_WINDOW and not self.windowFlag: 
                
                self.action = ACTION_INIT
                (self.x, self.y) = self.getEventCoord(event)
                self.window.queue_draw()
                
            elif self.action == ACTION_INIT:
                (self.rectWidth, self.rectHeight) = (ex - self.x, ey - self.y)
                self.window.queue_draw()
            elif self.action == ACTION_SELECT:
                
                if self.dragPosition == DRAG_INSIDE:
                    self.x = min(max(ex - self.dragStartOffsetX, 0), self.width - self.rectWidth)
                    self.y = min(max(ey - self.dragStartOffsetY, 0), self.height - self.rectHeight)
                elif self.dragPosition == DRAG_TOP_SIDE:
                    self.dragFrameTop(ex, ey)
                elif self.dragPosition == DRAG_BOTTOM_SIDE:
                    self.dragFrameBottom(ex, ey)
                elif self.dragPosition == DRAG_LEFT_SIDE:
                    self.dragFrameLeft(ex, ey)
                elif self.dragPosition == DRAG_RIGHT_SIDE:
                    self.dragFrameRight(ex, ey)
                elif self.dragPosition == DRAG_TOP_LEFT_CORNER:
                    self.dragFrameTop(ex, ey)
                    self.dragFrameLeft(ex, ey)
                elif self.dragPosition == DRAG_TOP_RIGHT_CORNER:
                    self.dragFrameTop(ex, ey)
                    self.dragFrameRight(ex, ey)
                elif self.dragPosition == DRAG_BOTTOM_LEFT_CORNER:
                    self.dragFrameBottom(ex, ey)
                    self.dragFrameLeft(ex, ey)
                elif self.dragPosition == DRAG_BOTTOM_RIGHT_CORNER:
                    self.dragFrameBottom(ex, ey)
                    self.dragFrameRight(ex, ey)                      
                self.window.queue_draw()
                
            elif self.action == ACTION_RECTANGLE:
                self.currentAction.drawing((ex, ey), (self.x, self.y, self.rectWidth, self.rectHeight))
                
                self.window.queue_draw()
            elif self.action == ACTION_ELLIPSE:
                self.currentAction.drawing((ex, ey), (self.x, self.y, self.rectWidth, self.rectHeight))
                
                self.window.queue_draw()
            elif self.action == ACTION_ARROW:
                self.currentAction.drawing((ex, ey), (self.x, self.y, self.rectWidth, self.rectHeight))
                
                self.window.queue_draw()
            elif self.action == ACTION_LINE:
                self.currentAction.drawing((ex, ey), (self.x, self.y, self.rectWidth, self.rectHeight))
                
                self.window.queue_draw()
        else:
            if self.action == ACTION_SELECT:
                self.setCursor(self.getPosition(event))
           
            elif self.action == ACTION_WINDOW:
                setPixbufCursor(self.window, "start_cursor.png")
            
            elif self.action in (ACTION_RECTANGLE, ACTION_ELLIPSE):
                setCursor(self.window, gtk.gdk.TCROSS)
            
            elif self.action == ACTION_LINE:
                setCursor(self.window, gtk.gdk.PENCIL)
            elif self.action == ACTION_TEXT:
                setCursor(self.window, gtk.gdk.XTERM)
            else:
                self.window.window.set_cursor(None)
                
            if self.windowFlag:
                self.hideToolbar()
                (wx, wy) = self.getEventCoord(event)
                for eachCoord in self.scrotWindowInfo:
                    if eachCoord.x < wx < (eachCoord.x + eachCoord.width) and eachCoord.y < wy < (eachCoord.y + eachCoord.height):
                        self.x = eachCoord.x
                        self.y = eachCoord.y
                        self.rectWidth = eachCoord.width
                        self.rectHeight = eachCoord.height
                self.window.queue_draw()
                
        if self.action == None:

            (tx, ty) = self.getEventCoord(event)       
            if self.textDragFlag:
                self.currentTextAction.updateCoord(tx - self.textDragOffsetX, ty - self.textDragOffsetY - 10)
                self.drawTextLayoutFlag = True
                self.window.queue_draw()
            else:
                for eachAction, info in self.textActionInfo.items():
                    if info[0] < tx < info[0]+info[2] and info[1] < ty < info[1]+info[3]:
                        self.currentTextAction = eachAction
                        
            if self.currentTextAction:
                drawTextX, drawTextY, drawTextWidth, drawTextHeight = self.currentTextAction.getLayoutInfo()
                if drawTextX < tx < drawTextX + drawTextWidth and drawTextY < ty < drawTextY + drawTextHeight:
                    self.drawTextLayoutFlag = True
                    setCursor(self.window, gtk.gdk.FLEUR)
                    self.window.queue_draw()
                else:
                    self.drawTextLayoutFlag = False    
                    self.currentTextAction = None
                    self.window.window.set_cursor(None)
                    self.window.queue_draw()
                            
    def buttonRelease(self, widget, event):
        '''Button release.'''
        self.textDragFlag = False
        self.dragFlag = False
        # print "buttonRelease: %s" % (str(event.get_root_coords()))
        if self.action == ACTION_WINDOW:
            if self.rectWidth > 5 and self.rectHeight > 5:
                self.showToolbar()
                self.action = ACTION_SELECT
                self.window.queue_draw()
            else:
                self.windowFlag = True
            
        elif self.action == ACTION_INIT:
            self.action = ACTION_SELECT
            (ex, ey) = self.getEventCoord(event)
            
            # Adjust value when button release.
            if ex > self.x:
                self.rectWidth = ex - self.x
            else:
                self.rectWidth = fabs(ex - self.x)
                self.x = ex
                
            if ey > self.y:
                self.rectHeight = ey - self.y
            else:
                self.rectHeight = fabs(ey - self.y)
                self.y = ey
                
            self.window.queue_draw()
            
            self.showToolbar()
        elif self.action == ACTION_SELECT:
            pass
        elif self.action == ACTION_RECTANGLE:
            self.currentAction.endDraw(self.getEventCoord(event), (self.x, self.y, self.rectWidth, self.rectHeight))
            self.actionList.append(self.currentAction)
            self.currentAction = None
            
            self.window.queue_draw()
        elif self.action == ACTION_ELLIPSE:
            self.currentAction.endDraw(self.getEventCoord(event), (self.x, self.y, self.rectWidth, self.rectHeight))
            self.actionList.append(self.currentAction)
            self.currentAction = None
            
            self.window.queue_draw()
        elif self.action == ACTION_ARROW:
            self.currentAction.endDraw(self.getEventCoord(event), (self.x, self.y, self.rectWidth, self.rectHeight))
            self.actionList.append(self.currentAction)
            self.currentAction = None
            
            self.window.queue_draw()
        elif self.action == ACTION_LINE:
            self.currentAction.endDraw(self.getEventCoord(event), (self.x, self.y, self.rectWidth, self.rectHeight))
            self.actionList.append(self.currentAction)
            self.currentAction = None
            self.window.queue_draw()
        
        if self.action in [ACTION_RECTANGLE, ACTION_ELLIPSE, ACTION_ARROW, ACTION_LINE, ACTION_TEXT] and not self.showToolbarFlag and self.y < self.toolbarY < self.y + self.rectHeight:
            self.adjustToolbar()
            self.showToolbar()
            self.adjustColorbar()
            self.showColorbar()

    def doubleClickRect(self, widget, event):
        '''Handle double click on window.'''
        (ex, ey) = self.getEventCoord(event)
        if isDoubleClick(event) and self.textDragFlag:
            textBuffer = self.textView.get_buffer()
            textBuffer.set_text(self.currentTextAction.getContent())
            self.actionColor = self.currentTextAction.getColor()
            self.fontName = self.currentTextAction.getFontname()
            modifyBackground(self.colorBox, self.actionColor)
            self.fontLabel.set_label(self.fontName)
            
            self.actionTextButton.set_active(True)
            self.showTextWindow(self.getEventCoord(event))
            self.textModifyFlag = True
       
        if isDoubleClick(event) and self.action == ACTION_SELECT and self.x < ex < self.x + self.rectWidth and self.y < ey < self.y + self.rectHeight:
            self.saveSnapshot()
            self.buttonRelease(widget, event)

    def registerKeyBinding(self, keyEventName, callback):
        '''Register a keybinding'''
        self.keyBindings[keyEventName] = callback

    def unregisterKeyBinding(self, keyEventName):
        '''Unregister a keybinding'''
        if self.keyBindings.has_key(keyEventName):
            del self.keyBindings[keyEventName]
            
    def keyPress(self, widget, event):
        '''process key press event'''
        keyEventName = getKeyEventName(event)
        if self.keyBindings.has_key(keyEventName):
            self.keyBindings[keyEventName]()

    def saveSnapshotToFile(self):
        '''Save file to file.'''
        if self.saveFilename:
            result = parserPath(self.saveFilename)
            self.saveSnapshot(*result)
        else:    
            dialog = gtk.FileChooserDialog(
                "Save..",
                self.window,
                gtk.FILE_CHOOSER_ACTION_SAVE,
                (gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT,
                 gtk.STOCK_SAVE, gtk.RESPONSE_ACCEPT))
            dialog.set_action(gtk.FILE_CHOOSER_ACTION_SAVE)
            dialog.set_default_response(gtk.RESPONSE_ACCEPT)
            dialog.set_position(gtk.WIN_POS_MOUSE)
            dialog.set_local_only(True)
            dialog.set_current_folder(getPicturesDir())
            dialog.set_current_name("%s%s.%s" % (DEFAULT_FILENAME, getFormatTime(), self.saveFiletype))
            optionMenu = gtk.OptionMenu()
            optionMenu.set_size_request(155, -1)
            menu = gtk.Menu()
            menu.set_size_request(155, -1)
            
            pngItem = makeMenuItem('PNG (*.png)',
                         lambda item, data: self.setSaveFiletype(dialog, 'png'))
            
            jpgItem = makeMenuItem('JPEG (*.jpeg)',
                         lambda item, data: self.setSaveFiletype(dialog, 'jpeg'))
            
            bmpItem = makeMenuItem('BMP (*.bmp)',
                         lambda item, data: self.setSaveFiletype(dialog, 'bmp'))
            
            menu.append(pngItem)
            menu.append(jpgItem)
            menu.append(bmpItem)
            optionMenu.set_menu(menu)
            hbox = gtk.HBox()
            hbox.pack_end(optionMenu, False, False)
            dialog.vbox.pack_start(hbox, False, False)
            hbox.show_all()                          
            
            self.hideToolbar()
            if self.showColorbarFlag:
                self.hideColorbar()
                
            response = dialog.run()
            if response == gtk.RESPONSE_ACCEPT:
                filename = dialog.get_filename()
                self.saveSnapshot(filename, self.saveFiletype)
                print "Save snapshot to %s" % (filename)
            elif response == gtk.RESPONSE_REJECT:
                self.adjustToolbar()
                self.showToolbar()
                
                if self.isHaveOneToggled():
                    self.showColorbar()
                print 'Closed, no files selected'
            dialog.destroy()
        
    def setSaveFiletype(self, dialog, filetype):
        ''' save filetype '''
        dialog.set_current_name("%s%s.%s" % (DEFAULT_FILENAME, getFormatTime(), filetype))
        self.saveFiletype = filetype
       
    def saveSnapshot(self, filename=None, filetype='png'):
        '''Save snapshot.'''
        # Init cairo.
        cr = self.window.window.cairo_create()
        
        # Draw desktop background.
        self.drawDesktopBackground(cr)
        
        # Draw action list.
        for action in self.actionList:
            action.expose(cr)
        # Draw text Action list.
        for eachTextAction in self.textActionList:
            eachTextAction.expose(cr)
            
        # Get snapshot.
        pixbuf = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, False, 8, int(self.rectWidth), int(self.rectHeight))
        pixbuf.get_from_drawable(
            self.window.get_window(), self.window.get_window().get_colormap(),
            self.x, self.y,
            0, 0,
            int(self.rectWidth), int(self.rectHeight))
        
        # Save snapshot.
        if filename == None:
            # Save snapshot to clipboard if filename is None.
            clipboard = gtk.clipboard_get()
            clipboard.set_image(pixbuf)
            clipboard.store()
            tipContent = __("Tip save to clipboard")
        else:
            # Otherwise save to local file.
            pixbuf.save(filename, filetype)
            tipContent = __("Tip save to file")
            
        

        
        # Exit
        self.window.window.set_cursor(None)
        self.destroy(self.window)
        
         # tipWindow
        cmd = ('python', 'tipswindow.py', tipContent)
        subprocess.Popen(cmd)

        
    def redraw(self, widget, event):
        '''Redraw.'''
        # Init cairo.
        cr = widget.window.cairo_create()
        
        # Draw desktop background.
        self.drawDesktopBackground(cr)
        
        # Draw mask.
        self.drawMask(cr)
        
        # Draw toolbar.
        if self.showToolbarFlag:
            self.adjustToolbar()
            self.adjustColorbar()
            
        # Draw action list.
        for action in self.actionList:
            if action != None:
                action.expose(cr)
        
        # Draw Text Action list.
        for eachTextAction in self.textActionList:
            eachTextAction.expose(cr)
            self.textActionInfo[eachTextAction] = eachTextAction.getLayoutInfo()

        # Draw current action.
        if self.currentAction != None:
            self.currentAction.expose(cr)

        # draw currentText layout
        if self.drawTextLayoutFlag:
            drawAlphaRectangle(cr, *self.currentTextAction.getLayoutInfo())
    
        #draw magnifier
        if self.action == ACTION_WINDOW and self.rectWidth:
            drawMagnifier(cr, self.window, self.currentX, self.currentY,
                           '%d x %d' % (self.rectWidth, self.rectHeight),
                            '%s' % (__("Tip Drag")), "RGB: %s" % str(getCoordRGB(self.window, self.currentX, self.currentY)))
            self.drawWindowRectangle(cr)
        elif self.rectWidth:
            #Draw frame
            self.drawFrame(cr)
            # Draw drag point.
            self.drawDragPoint(cr)
            if self.y - 35 > 0:
                drawRoundTextRectangle(cr, self.x + 5, self.y - 35, 85, 30, 7,'%d x %d' % (fabs(self.rectWidth), fabs(self.rectHeight)), 0.7)
            elif self.action in [None, ACTION_SELECT, ACTION_WINDOW, ACTION_INIT]:
                drawRoundTextRectangle(cr, self.x + 5 , self.y + 5 , 85, 30, 7,'%d x %d' % (fabs(self.rectWidth), fabs(self.rectHeight)), 0.7)
        
        if widget.get_child() != None:
            widget.propagate_expose(widget.get_child(), event)
    
        return True
    
    def drawDesktopBackground(self, cr):
        '''Draw desktop.'''
        drawPixbuf(cr, self.desktopBackground)    
        
    def drawMask(self, cr):
        '''Draw mask.'''
        # Adjust value when create selection area.
        if self.rectWidth > 0:
            x = self.x
            rectWidth = self.rectWidth
        else:
            x = self.x + self.rectWidth
            rectWidth = fabs(self.rectWidth)

        if self.rectHeight > 0:
            y = self.y
            rectHeight = self.rectHeight
        else:
            y = self.y + self.rectHeight
            rectHeight = fabs(self.rectHeight)
        
        # Draw top.
        cr.set_source_rgba(0, 0, 0, 0.5)
        cr.rectangle(0, 0, self.width, y)
        cr.fill()

        # Draw bottom.
        cr.set_source_rgba(0, 0, 0, 0.5)
        cr.rectangle(0, y + rectHeight, self.width, self.height - y - rectHeight)
        cr.fill()

        # Draw left.
        cr.set_source_rgba(0, 0, 0, 0.5)
        cr.rectangle(0, y, x, rectHeight)
        cr.fill()

        # Draw right.
        cr.set_source_rgba(0, 0, 0, 0.5)
        cr.rectangle(x + rectWidth, y, self.width - x - rectWidth, rectHeight)
        cr.fill()
        
    def drawFrame(self, cr):
        '''Draw frame.'''
        cr.set_source_rgb(*colorHexToCairo(self.frameColor))
        cr.set_line_width(self.frameLineWidth)
        cr.rectangle(self.x, self.y, self.rectWidth, self.rectHeight)
        cr.stroke()
        
    def drawDragPoint(self, cr):
        '''Draw drag point.'''
        # Draw left top corner.
        cr.set_source_rgb(*colorHexToCairo(self.frameColor))
        cr.arc(self.x, self.y, self.dragPointRadius, 0, 2 * pi)
        cr.fill()
        
        # Draw right top corner.
        cr.set_source_rgb(*colorHexToCairo(self.frameColor))
        cr.arc(self.x + self.rectWidth, self.y, self.dragPointRadius, 0, 2 * pi)
        cr.fill()
        
        # Draw left bottom corner.
        cr.set_source_rgb(*colorHexToCairo(self.frameColor))
        cr.arc(self.x, self.y + self.rectHeight, self.dragPointRadius, 0, 2 * pi)
        cr.fill()
        
        # Draw right bottom corner.
        cr.set_source_rgb(*colorHexToCairo(self.frameColor))
        cr.arc(self.x + self.rectWidth, self.y + self.rectHeight, self.dragPointRadius, 0, 2 * pi)
        cr.fill()
        
        # Draw top side.
        cr.set_source_rgb(*colorHexToCairo(self.frameColor))
        cr.arc(self.x + self.rectWidth / 2, self.y, self.dragPointRadius, 0, 2 * pi)
        cr.fill()
        
        # Draw bottom side.
        cr.set_source_rgb(*colorHexToCairo(self.frameColor))
        cr.arc(self.x + self.rectWidth / 2, self.y + self.rectHeight, self.dragPointRadius, 0, 2 * pi)
        cr.fill()
        
        # Draw left side.
        cr.set_source_rgb(*colorHexToCairo(self.frameColor))
        cr.arc(self.x, self.y + self.rectHeight / 2, self.dragPointRadius, 0, 2 * pi)
        cr.fill()
        
        # Draw right side.
        cr.set_source_rgb(*colorHexToCairo(self.frameColor))
        cr.arc(self.x + self.rectWidth, self.y + self.rectHeight / 2, self.dragPointRadius, 0, 2 * pi)
        cr.fill()
        
    def getDesktopSnapshot(self):
        '''Get desktop snapshot.'''
        rootWindow = gtk.gdk.get_default_root_window() 
        [self.width, self.height] = rootWindow.get_size() 
        pixbuf = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, False, 8, self.width, self.height)
        return pixbuf.get_from_drawable(rootWindow, rootWindow.get_colormap(), 0, 0, 0, 0, self.width, self.height) 
        
    def destroy(self, widget, data=None):
        '''Destroy main window.'''
        self.window.window.set_cursor(None)
        gtk.main_quit()
        
    def getDragPointCoords(self):
        '''Get drag point coords.'''
        return (
            # Top left.
            (self.x - self.dragPointRadius, self.y - self.dragPointRadius),
            # Top right.
            (self.x + self.rectWidth - self.dragPointRadius, self.y - self.dragPointRadius),
            # Bottom left.
            (self.x - self.dragPointRadius, self.y + self.rectHeight - self.dragPointRadius),
            # Bottom right.
            (self.x + self.rectWidth - self.dragPointRadius, self.y + self.rectHeight - self.dragPointRadius),
            # Top side.
            (self.x + self.rectWidth / 2 - self.dragPointRadius, self.y - self.dragPointRadius),
            # Bottom side.
            (self.x + self.rectWidth / 2 - self.dragPointRadius, self.y + self.rectHeight - self.dragPointRadius),
            # Left side.
            (self.x - self.dragPointRadius, self.y + self.rectHeight / 2 - self.dragPointRadius),
            # Right side.
            (self.x + self.rectWidth - self.dragPointRadius, self.y + self.rectHeight / 2 - self.dragPointRadius),
            )
        
    def getPosition(self, event):
        '''Get drag position.'''
        # Get event position.
        (ex, ey) = self.getEventCoord(event)
        
        # Get drag point coords.
        pWidth = pHeight = self.dragPointRadius * 2
        ((tlX, tlY), (trX, trY), (blX, blY), (brX, brY), (tX, tY), (bX, bY), (lX, lY), (rX, rY)) = self.getDragPointCoords()
        
        # Calcuate drag position.
        if isInRect((ex, ey), (self.x, self.y, self.rectWidth, self.rectHeight)):
            return DRAG_INSIDE
        elif isCollideRect((ex, ey), (tlX, tlY, pWidth, pHeight)):
            return DRAG_TOP_LEFT_CORNER
        elif isCollideRect((ex, ey), (trX, trY, pWidth, pHeight)):
            return DRAG_TOP_RIGHT_CORNER
        elif isCollideRect((ex, ey), (blX, blY, pWidth, pHeight)):
            return DRAG_BOTTOM_LEFT_CORNER
        elif isCollideRect((ex, ey), (brX, brY, pWidth, pHeight)):
            return DRAG_BOTTOM_RIGHT_CORNER
        elif isCollideRect((ex, ey), (tX, tY, pWidth, pHeight)) or isCollideRect((ex, ey), (self.x, self.y, self.rectWidth, self.frameLineWidth)):
            return DRAG_TOP_SIDE
        elif isCollideRect((ex, ey), (bX, bY, pWidth, pHeight)) or isCollideRect((ex, ey), (self.x, self.y + self.rectHeight, self.rectWidth, self.frameLineWidth)):
            return DRAG_BOTTOM_SIDE
        elif isCollideRect((ex, ey), (lX, lY, pWidth, pHeight)) or isCollideRect((ex, ey), (self.x, self.y, self.frameLineWidth, self.rectHeight)):
            return DRAG_LEFT_SIDE
        elif isCollideRect((ex, ey), (rX, rY, pWidth, pHeight)) or isCollideRect((ex, ey), (self.x + self.rectWidth, self.y, self.frameLineWidth, self.rectHeight)):
            return DRAG_RIGHT_SIDE
        else:
            return DRAG_OUTSIDE
        
    def setCursor(self, position):
        '''Set cursor.'''
        if position == DRAG_INSIDE:
            setCursor(self.window, gtk.gdk.FLEUR)
        elif position == DRAG_OUTSIDE:
            setCursor(self.window, gtk.gdk.TOP_LEFT_ARROW)
        elif position == DRAG_TOP_LEFT_CORNER:
            setCursor(self.window, gtk.gdk.TOP_LEFT_CORNER)
        elif position == DRAG_TOP_RIGHT_CORNER:
            setCursor(self.window, gtk.gdk.TOP_RIGHT_CORNER)
        elif position == DRAG_BOTTOM_LEFT_CORNER:
            setCursor(self.window, gtk.gdk.BOTTOM_LEFT_CORNER)
        elif position == DRAG_BOTTOM_RIGHT_CORNER:
            setCursor(self.window, gtk.gdk.BOTTOM_RIGHT_CORNER)
        elif position == DRAG_TOP_SIDE:
            setCursor(self.window, gtk.gdk.TOP_SIDE)
        elif position == DRAG_BOTTOM_SIDE:
            setCursor(self.window, gtk.gdk.BOTTOM_SIDE)
        elif position == DRAG_LEFT_SIDE:
            setCursor(self.window, gtk.gdk.LEFT_SIDE)
        elif position == DRAG_RIGHT_SIDE:
            setCursor(self.window, gtk.gdk.RIGHT_SIDE)
            
    def dragFrameTop(self, ex, ey):
        '''Drag frame top.'''
        maxY = self.y + self.rectHeight
        self.rectHeight = self.rectHeight - min(self.rectHeight, (ey - self.y))
        self.y = min(ey, maxY) 
    
    def dragFrameBottom(self, ex, ey):
        '''Drag frame bottom.'''
        self.rectHeight = max(0, ey - self.y)
    
    def dragFrameLeft(self, ex, ey):
        '''Drag frame left.'''
        maxX = self.x + self.rectWidth
        self.rectWidth = self.rectWidth - min(self.rectWidth, (ex - self.x))
        self.x = min(ex, maxX)
    
    def dragFrameRight(self, ex, ey):
        '''Drag frame right.'''
        self.rectWidth = max(0, ex - self.x)
        
    def undo(self):
        '''Undo'''
        if self.textWindow.get_visible():
            self.hideTextWindow()
            
        if self.actionList:
            tempAction = self.actionList.pop()
            if tempAction.getActionType() == ACTION_TEXT:
                self.textActionList.pop()
                del self.textActionInfo[tempAction]
        else:
            self.window.window.set_cursor(None)
            self.action = ACTION_WINDOW
            self.x = self.y = self.rectWidth = self.rectHeight = 0
            self.windowFlag = True
            self.dragFlag = False
            self.hideToolbar()
            if self.showColorbarFlag:
                self.setAllInactive()
        self.window.queue_draw()
        
    def drawWindowRectangle(self, cr):
        '''Draw frame.'''
        cr.set_line_width(4.5)
        cr.rectangle(self.x + 1, self.y + 1, self.rectWidth - 2, self.rectHeight - 2)
        cr.set_source_rgb(*colorHexToCairo(self.frameColor))
        cr.stroke()
    def getCurrentCoord(self, widget):
        '''get Current Coord '''
        (self.currentX, self.currentY) = widget.window.get_pointer()[:2] 
    
if __name__ == "__main__":
    MainScrot()
