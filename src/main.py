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
from Xlib import X
from widget import RootWindow, TextWindow
from toolbar import Colorbar, Toolbar

import time
import pygtk
import subprocess

pygtk.require('2.0')
import gtk


class DeepinScreenshot():
    '''Main screenshot.'''
    def __init__(self, save_file=""):
        '''Init Main screenshot.'''
        # Init.
        self.dis = DISPLAY
        self.root =ROOT_WINDOW

        self.action = ACTION_WINDOW
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT
        self.x = self.y = self.rect_width = self.rect_height = 0
        self.buttonToggle = None
        
        self.dragPosition = None
        self.dragStartX = self.dragStartY = self.dragStartOffsetX = self.dragStartOffsetY = 0
        self.dragPointRadius = 4
        
        self.drag_flag = False
        self.show_toolbar_flag = False
        self.show_colorbar_flag = False 
        self.show_text_window_flag = False
        self.textDragOffsetX = self.textDragOffsetY = 0
        self.saveFiletype = 'png'
        self.saveFilename = save_file
        
        self.toolbarOffsetX = 10
        self.toolbarOffsetY = 10
        #self.toolbar_height = 50
        
        self.actionSize = 2
        self.actionColor = "#FF0000"
        self.fontName = "Sans 10"
        
        # default window 
        self.screenshot_window_info = get_screenshot_window_info()   # 获取窗口的x,y 长，宽
        self.window_flag = True

        # keybinding map
        #self.keyBindings = {}
        
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
        self.desktop_background = self.getDesktopSnapshot()      # 获取全屏截图
        
        # Init window.
        ## 创建一个全屏窗口并顶置
        self.window = RootWindow(self)
        
        # Init toolbar window.
        self.toolbar = Toolbar(self.window.window, self)
        
        # Init text window.
        self.text_window = TextWindow(self.window.window, self)
        
        # Init color window.
        self.colorbar = Colorbar(self.window.window, self)
       
        # Show.
        self.window.show()

        #self.toolbar.show()
        #self.colorbar.show()
        
    def isHaveOneToggled(self):             # 是否有工具按钮按下
        buttonList = [self.actionRectangleButton, self.actionEllipseButton, self.actionArrowButton, self.actionLineButton,
                      self.actionTextButton]
        
        for eachButton in buttonList:
            if eachButton.get_active():
                return True
        return False
    
    def getIconIndex(self):                 # 获取画笔尺寸
        '''Get icon index.'''
        return self.iconIndex
        
    def exposeTextViewTag(self, widget, event):     # 文本输入框显示的回调函数
        ''' expose of textView'''
        textBuffer = widget.get_buffer()
        startIter = textBuffer.get_start_iter()
        endIter = textBuffer.get_end_iter()

        self.textTag.set_property("foreground_gdk", gtk.gdk.color_parse(self.actionColor))
        self.textTag.set_property("font", self.fontName)
        textBuffer.apply_tag_by_name("first", startIter, endIter)

    def showTextWindow(self, (ex, ey)):     # 显示文本输入窗口
        '''Show text window.'''
        offset = 5
        self.show_text_window_flag = True
        self.textWindow.show_all()
        self.textWindow.move(ex, ey)
        
    def hideTextWindow(self):               # 隐藏文本输入窗口
        '''Hide text window.'''
        self.show_text_window_flag = False
        self.textView.get_buffer().set_text("")
        self.textWindow.hide_all()
    
    def getInputText(self):                 # 获取输入框文字
        '''Get input text.'''
        textBuffer = self.textView.get_buffer()
        return (textBuffer.get_text(textBuffer.get_start_iter(), textBuffer.get_end_iter())).rstrip(" ")
        
    def set_action_type(self, aType):         # 设置操作类型
        '''Set action. type'''
        self.action = aType    
        self.currentAction = None
    
        
    def getEventCoord(self, event):     # 获取事件的坐标
        '''Get event coord.'''
        (rx, ry) = event.get_root_coords()
        return (int(rx), int(ry))

    def doubleClickRect(self, widget, event):
        '''Handle double click on window.'''
        (ex, ey) = self.getEventCoord(event)
        if isDoubleClick(event) and self.textDragFlag:
            textBuffer = self.textView.get_buffer()
            textBuffer.set_text(self.currentTextAction.get_content())
            self.actionColor = self.currentTextAction.get_color()
            self.fontName = self.currentTextAction.get_fontname()
            modifyBackground(self.colorBox, self.actionColor)
            self.fontLabel.set_label(self.fontName)
            
            self.actionTextButton.set_active(True)
            self.showTextWindow(self.getEventCoord(event))
            self.textModifyFlag = True
       
        if isDoubleClick(event) and self.action == ACTION_SELECT and self.x < ex < self.x + self.rect_width and self.y < ey < self.y + self.rect_height:
            self.saveSnapshot()
            self.buttonRelease(widget, event)

    def saveSnapshotToFile(self, widget=None):
        '''Save file to file.'''
        if self.saveFilename:
            result = parserPath(self.saveFilename)
            self.saveSnapshot(None, *result)
        else:    
            self.dis.ungrab_pointer(X.CurrentTime)
            self._grab_pointer_flag = False
            self._show_file_dialog = True
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
            dialog.set_current_folder(get_pictures_dir())
            dialog.set_current_name("%s%s.%s" % (DEFAULT_FILENAME, get_format_time(), self.saveFiletype))
            optionMenu = gtk.OptionMenu()
            optionMenu.set_size_request(155, -1)
            menu = gtk.Menu()
            menu.set_size_request(155, -1)
            
            pngItem = make_menu_item('PNG (*.png)',
                         lambda item, data: self.setSaveFiletype(dialog, 'png'))
            
            jpgItem = make_menu_item('JPEG (*.jpeg)',
                         lambda item, data: self.setSaveFiletype(dialog, 'jpeg'))
            
            bmpItem = make_menu_item('BMP (*.bmp)',
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
            if self.show_colorbar_flag:
                self.hideColorbar()
                
            dialog.set_modal(True)
            dialog.connect("response", self.file_dialog_response)
            dialog.show_all()

    def file_dialog_response(self, dialog, response):
        if response == gtk.RESPONSE_ACCEPT:
            filename = dialog.get_filename()
            dialog.hide()
            self.saveSnapshot(dialog, filename, self.saveFiletype)
            print "Save snapshot to %s" % (filename)
        elif response == gtk.RESPONSE_REJECT:
            self.adjust_toolbar()
            self.show_toolbar()
            if self.isHaveOneToggled():
                self.showColorbar()
            print 'Closed, no files selected'
            self.root.grab_pointer(1, X.PointerMotionMask|X.ButtonReleaseMask|X.ButtonPressMask,  
                X.GrabModeAsync, X.GrabModeAsync, X.NONE, X.NONE, X.CurrentTime)
            self._grab_pointer_flag = True
            self._show_file_dialog = False
        dialog.destroy()
        
    def setSaveFiletype(self, dialog, filetype):
        ''' save filetype '''
        dialog.set_current_name("%s%s.%s" % (DEFAULT_FILENAME, get_format_time(), filetype))
        self.saveFiletype = filetype
       
    def saveSnapshot(self, widget=None, filename=None, filetype='png'):
        '''Save snapshot.'''
        ## Init cairo.
        #cr = self.window.window.cairo_create()
        
        ## Draw desktop background.
        #self.drawDesktopBackground(cr)
        
        ## Draw action list.
        #for action in self.actionList:
            #action.expose(cr)
        ## Draw text Action list.
        #for eachTextAction in self.textActionList:
            #eachTextAction.expose(cr)
            
        # Get snapshot.
        
        # Save snapshot.
        if self.rect_width == 0 or self.rect_height == 0:
            tipContent = __("Tip area width or heigth cannot be 0")
        else:
            if filename == None:
                # Save snapshot to clipboard if filename is None.
                pixbuf = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, False, 8, int(self.rect_width), int(self.rect_height))
                pixbuf.get_from_drawable(self.window.get_window(), self.window.get_window().get_colormap(),
                    int(self.x), int(self.y), 0, 0, int(self.rect_width), int(self.rect_height))
                clipboard = gtk.clipboard_get()
                clipboard.clear()
                clipboard.set_image(pixbuf)
                tipContent = __("Tip save to clipboard")
            else:
                # Otherwise save to local file.
                tipContent = __("Tip save to file")
                self.make_pic_file(self.desktop_background.subpixbuf(int(self.x), int(self.y), int(self.rect_width), int(self.rect_height)), filename)
            
        # Exit
        self.window.window.set_cursor(None)
        #self.destroy(self.window)
        time.sleep(0.001)
        self.window.destroy()
        
        # tipWindow
        cmd = ('python', 'tipswindow.py', tipContent)
        subprocess.Popen(cmd)

    def make_pic_file(self, pixbuf, filename):
        ''' use cairo make a picture file '''
        surface = cairo.ImageSurface(cairo.FORMAT_RGB24, pixbuf.get_width(), pixbuf.get_height())
        cr = cairo.Context(surface)
        gdkcr = gtk.gdk.CairoContext(cr)
        gdkcr.set_source_pixbuf(pixbuf, 0, 0)
        gdkcr.paint()

        for action in self.actionList:
            if action is not None:
                action.start_x -= self.x
                action.start_y -= self.y
                if not isinstance(action, (TextAction)):
                    action.end_x -= self.x
                    action.end_y -= self.y
                if isinstance(action, (LineAction)):
                    for track in action.track:
                        track[0] -= self.x
                        track[1] -= self.y
                action.expose(cr)
        
        # Draw Text Action list.
        for eachTextAction in self.textActionList:
            if eachTextAction is not None:
                eachTextAction.start_x -= self.x
                eachTextAction.start_y -= self.y
                eachTextAction.expose(cr)
                self.textActionInfo[eachTextAction] = eachTextAction.get_layout_info()
        surface.write_to_png(filename)

        
    def redraw(self, widget, event):
        '''Redraw.'''
        # Init cairo.
        cr = widget.window.cairo_create()
        
        # Draw desktop background.
        self.drawDesktopBackground(cr)
        
        # Draw mask.
        self.drawMask(cr)
        
        # Draw toolbar.
        if self.show_toolbar_flag:
            self.adjust_toolbar()
            self.adjustColorbar()
            
        # Draw action list.
        for action in self.actionList:
            if action != None:
                action.expose(cr)
        
        # Draw Text Action list.
        for eachTextAction in self.textActionList:
            eachTextAction.expose(cr)
            self.textActionInfo[eachTextAction] = eachTextAction.get_layout_info()

        # Draw current action.
        if self.currentAction != None:
            self.currentAction.expose(cr)

        # draw currentText layout
        if self.drawTextLayoutFlag:
            drawAlphaRectangle(cr, *self.currentTextAction.get_layout_info())
    
        #draw magnifier
        if self.action == ACTION_WINDOW and self.rect_width:
            drawMagnifier(cr, self.window, self.currentX, self.currentY,
                           '%d x %d' % (self.rect_width, self.rect_height),
                            #'%s' % (__("Tip Drag")), "RGB: %s" % str(get_coord_rgb(self.window, self.currentX, self.currentY)))
                            '%s' % (__("Tip Drag")), "RGB: %s" % str(get_coord_rgb(self.root, self.currentX, self.currentY)))
            self.drawWindowRectangle(cr)
        elif self.rect_width:
            #Draw frame
            self.drawFrame(cr)
            # Draw drag point.
            self.drawDragPoint(cr)
            if self.y - 35 > 0:
                drawRoundTextRectangle(cr, self.x + 5, self.y - 35, 85, 30, 7,'%d x %d' % (fabs(self.rect_width), fabs(self.rect_height)), 0.7)
            elif self.action in [None, ACTION_SELECT, ACTION_WINDOW, ACTION_INIT]:
                drawRoundTextRectangle(cr, self.x + 5 , self.y + 5 , 85, 30, 7,'%d x %d' % (fabs(self.rect_width), fabs(self.rect_height)), 0.7)
        
        if widget.get_child() != None:
            widget.propagate_expose(widget.get_child(), event)
    
        return True
    
    def getDesktopSnapshot(self):
        '''Get desktop snapshot.'''
        return get_screenshot_pixbuf()
        
    def setCursor(self, position):
        '''Set cursor.'''
        #print "in cusor position:", position
        if position == DRAG_INSIDE:         # TODO 
            setCursor(self.window, gtk.gdk.FLEUR)
        elif position == DRAG_OUTSIDE:
            setCursor(self.window, gtk.gdk.TOP_LEFT_ARROW)
        elif position == DRAG_TOP_LEFT_CORNER:
            self.window.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.TOP_LEFT_CORNER))
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
        
    def undo(self, widget=None):
        '''Undo'''
        if self.textWindow.get_visible():
            self.hideTextWindow()
            
        if self.actionList:
            tempAction = self.actionList.pop()
            if tempAction.get_action_type() == ACTION_TEXT:
                self.textActionList.pop()
                del self.textActionInfo[tempAction]
        else:
            self.window.window.set_cursor(None)
            self.action = ACTION_WINDOW
            self.x = self.y = self.rect_width = self.rect_height = 0
            self.window_flag = True
            self.drag_flag = False
            self.hideToolbar()
            if self.show_colorbar_flag:
                self.setAllInactive()
        self.window.queue_draw()
        
    def drawWindowRectangle(self, cr):
        '''Draw frame.'''
        cr.set_line_width(4.5)
        cr.rectangle(self.x + 1, self.y + 1, self.rect_width - 2, self.rect_height - 2)
        cr.set_source_rgb(*colorHexToCairo(self.frameColor))
        cr.stroke()

    def getCurrentCoord(self, widget):
        '''get Current Coord '''
        (self.currentX, self.currentY) = widget.window.get_pointer()[:2] 
    
def main(name=""):
    ''' main function '''
    gtk.gdk.threads_init()
    s = DeepinScreenshot(name)
    gtk.main()

if __name__ == '__main__':
    main()
