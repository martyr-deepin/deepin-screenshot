#!/usr/bin/python
#-*- coding:utf-8 -*-

# Copyright (C) 2011 ~ 2012 Deepin, Inc.
#               2011 ~ 2012 Long Changjin
# 
# Author:     Long Changjin <admin@longchangjin.cn>
# Maintainer: Long Changjin <admin@longchangjin.cn>
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

from constant import *
from action import *
import utils

class BaseProcess():
    ''' BaseProcess Class'''
    def __init__(self, screenshot=None, window=None):
        self.screenshot = screenshot
        self.win = window
        self.event = None
        self.func_map = {
            ACTION_INIT: self.action_init,
            ACTION_ARROW: self.action_arrow,
            ACTION_ELLIPSE: self.action_ellipse,
            ACTION_LINE: self.action_line,
            ACTION_RECTANGLE: self.action_rectangle,
            ACTION_SELECT: self.action_select,
            ACTION_TEXT: self.action_text,
            ACTION_WINDOW: self.action_window}
    
    def update(self, event):
        self.event = event
    
    def action_init(self, screenshot, event):
        pass
    
    def action_arrow(self, screenshot, event):
        pass
    
    def action_ellipse(self, screenshot, event):
        pass
    
    def action_line(self, screenshot, event):
        pass
    
    def action_rectangle(self, screenshot, event):
        pass
    
    def action_select(self, screenshot, event):
        pass
    
    def action_text(self, screenshot, event):
        pass
    
    def action_window(self, screenshot, event):
        pass
    
class ButtonPressProcess(BaseProcess):
    ''' buton press status class'''
    def __init__(self, screenshot=None, window=None):
        BaseProcess.__init__(self, screenshot, window)

    def process(self):
        ''' process button press event'''
        if self.event is None:
            return
        self.screenshot.drag_flag = True
        self.func_map[self.screenshot.action](self.screenshot, self.event)
        self.adjust(self.screenshot, self.event)
    
    def action_window(self, screenshot, event):
        ''' ACTION_WINDOW '''
        screenshot.window_flag = False

    def action_init(self, screenshot, event):
        ''' ACTION_INIT '''
        (screenshot.x, screenshot.y) = self.win.get_event_coord(event)

    def action_select(self, screenshot, event):
        ''' ACTION_SELECT '''
        # Init drag position.
        screenshot.dragPosition = self.win.get_position(event)
        # Set cursor.
        #screenshot.setCursor(screenshot.dragPosition)
        # Get drag coord and offset.
        (screenshot.dragStartX, screenshot.dragStartY) = self.win.get_event_coord(event)
        screenshot.dragStartOffsetX = screenshot.dragStartX - screenshot.x
        screenshot.dragStartOffsetY = screenshot.dragStartY - screenshot.y

    def action_rectangle(self, screenshot, event):
        ''' ACTION_RECTANGLE '''
        # Just create new action when drag position at inside of select area.
        if screenshot.get_position(event) == DRAG_INSIDE:
            screenshot.currentAction = RectangleAction(ACTION_RECTANGLE, screenshot.actionSize, screenshot.actionColor)
            screenshot.currentAction.start_draw(screenshot.get_event_coord(event))
    
    def action_ellipse(self, screenshot, event):
        ''' ACTION_ELLIPSE '''
        # Just create new action when drag position at inside of select area.
        if screenshot.get_position(event) == DRAG_INSIDE:
            screenshot.currentAction = EllipseAction(ACTION_ELLIPSE, screenshot.actionSize, screenshot.actionColor)
            screenshot.currentAction.start_draw(self.win.get_event_coord(event))

    def action_arrow(self, screenshot, event):
        ''' ACTION_ARROW '''
        # Just create new action when drag position at inside of select area.
        if screenshot.get_position(event) == DRAG_INSIDE:
            screenshot.currentAction = ArrowAction(ACTION_ARROW, screenshot.actionSize, screenshot.actionColor)
            screenshot.currentAction.start_draw(self.win.get_event_coord(event))

    def action_line(self, screenshot, event):
        ''' ACTION_LINE '''
        # Just create new action when drag position at inside of select area.
        if screenshot.get_position(event) == DRAG_INSIDE:
            screenshot.currentAction = LineAction(ACTION_LINE, screenshot.actionSize, screenshot.actionColor)
            screenshot.currentAction.start_draw(self.win.get_event_coord(event))

    def action_text(self, screenshot, event):
        ''' ACTION_TEXT '''
        if screenshot.textWindow.get_visible():
            content = screenshot.getInputText()
            if content != "":
                if screenshot.textModifyFlag:
                    screenshot.currentTextAction.update(screenshot.actionColor, screenshot.fontName, content)
                    screenshot.textModifyFlag = False
                else:
                    textAction = TextAction(ACTION_TEXT, 15, screenshot.actionColor, screenshot.fontName, content)
                    textAction.start_draw(screenshot.textWindow.get_window().get_origin())
                    screenshot.textActionList.append(textAction)
                    screenshot.actionList.append(textAction)
                screenshot.hideTextWindow()
                screenshot.setAllInactive()
                
                self.win.window.queue_draw()
            else:
                screenshot.hideTextWindow()
                screenshot.setAllInactive()
        else:
            screenshot.showTextWindow(self.win.get_event_coord(event))

    def adjust(self, screenshot, event):
        ''' adjust '''
        if screenshot.action in [ACTION_RECTANGLE, ACTION_ELLIPSE, ACTION_ARROW, ACTION_LINE] and screenshot.show_toolbar_flag and screenshot.y < screenshot.toolbarY < screenshot.y + screenshot.rect_height:
            screenshot.hideToolbar()
            screenshot.hideColorbar()

        if screenshot.currentTextAction and screenshot.action is None:
            currentX, currentY = screenshot.get_event_coord(event)
            drawTextX,drawTextY = screenshot.currentTextAction.get_layout_info()[:2]
            screenshot.textDragOffsetX = currentX - drawTextX
            screenshot.textDragOffsetY = currentY - drawTextY
            screenshot.textDragFlag = True 

class ButtonReleaseProcess(BaseProcess):
    ''' button release process'''
    def __init__(self, screenshot=None, window=None):
        BaseProcess.__init__(self, screenshot, window)
        
    def process(self):
        ''' process button release event'''
        if self.event is None:
            return
        self.screenshot.textDragFlag = False
        self.screenshot.drag_flag = False
        self.func_map[self.screenshot.action](self.screenshot, self.event)
        self.adjust(self.screenshot, self.event)

    def action_window(self, screenshot, event):
        ''' ACTION_WINDOW'''
        if screenshot.rect_width > 5 and screenshot.rect_height > 5:
            self.win.show_toolbar()
            self.win.adjust_toolbar()
            screenshot.action = ACTION_SELECT
            self.win.window.queue_draw()
        else:
            screenshot.window_flag = True
            
    def action_init(self, screenshot, event):
        ''' ACTION_INIT'''
        screenshot.action = ACTION_SELECT
        (ex, ey) = self.win.get_event_coord(event)
        # Adjust value when button release.
        if ex > screenshot.x:
            screenshot.rect_width = ex - screenshot.x
        else:
            screenshot.rect_width = fabs(ex - screenshot.x)
            screenshot.x = ex
        if ey > screenshot.y:
            screenshot.rect_height = ey - screenshot.y
        else:
            screenshot.rect_height = fabs(ey - screenshot.y)
            screenshot.y = ey

        self.win.show_toolbar()
        self.win.adjust_toolbar()
        self.win.show_colorbar()
        self.win.adjust_colorbar()
        self.win.window.queue_draw()

    def action_select(self, screenshot, event):
        ''' ACTION_SELECT '''
        pass
    
    def action_rectangle(self, screenshot, event):
        ''' ACTION_RECTANGLE '''
        if screenshot.currentAction:
            screenshot.currentAction.end_draw(screenshot.getEventCoord(event), (screenshot.x, screenshot.y, screenshot.rect_width, screenshot.rect_height))
            screenshot.actionList.append(screenshot.currentAction)
            screenshot.currentAction = None
            self.win.window.queue_draw()

    def action_ellipse(self, screenshot, event):
        ''' ACTION_ELLIPSE '''
        if screenshot.currentAction:
            screenshot.currentAction.end_draw(screenshot.getEventCoord(event), (screenshot.x, screenshot.y, screenshot.rect_width, screenshot.rect_height))
            screenshot.actionList.append(screenshot.currentAction)
            screenshot.currentAction = None
            self.win.window.queue_draw()

    def action_arrow(self, screenshot, event):
        ''' ACTION_ARROW '''
        if screenshot.currentAction:
            screenshot.currentAction.end_draw(screenshot.getEventCoord(event), (screenshot.x, screenshot.y, screenshot.rect_width, screenshot.rect_height))
            screenshot.actionList.append(screenshot.currentAction)
            screenshot.currentAction = None
            self.win.window.queue_draw()

    def action_line(self, screenshot, event):
        ''' ACTION_LINE '''
        if screenshot.currentAction:
            screenshot.currentAction.end_draw(screenshot.getEventCoord(event), (screenshot.x, screenshot.y, screenshot.rect_width, screenshot.rect_height))
            screenshot.actionList.append(screenshot.currentAction)
            screenshot.currentAction = None
            self.win.window.queue_draw()
        
    def adjust(self, screenshot, event):
        if screenshot.action in [ACTION_RECTANGLE, ACTION_ELLIPSE, ACTION_ARROW, ACTION_LINE, ACTION_TEXT] and not screenshot.show_toolbar_flag and screenshot.y < screenshot.toolbarY < screenshot.y + screenshot.rect_height:
            self.win.show_toolbar()
            self.win.adjust_toolbar()
            self.win.show_colorbar()
            self.win.adjust_colorbar()

class MotionProcess(BaseProcess):
    ''' Motion process'''
    def __init__(self, screenshot=None, window=None):
        BaseProcess.__init__(self, screenshot, window)
        
    def process(self):
        ''' process motion event'''
        if self.event is None:
            return
        self.func_map[self.screenshot.action](self.screenshot, self.event)
        self.adjust(self.screenshot, self.event)

    def action_window(self, screenshot, event):
        ''' ACTION_WINDOW'''
        size = "%d x %d " % (screenshot.rect_width, screenshot.rect_height)
        rgb = utils.get_coord_rgb(screenshot.root, event.x, event.y)
        self.win.update_magnifier(event.x, event.y, size=size, rgb=str(rgb))

        # can drag and has not selected area
        if screenshot.drag_flag and not screenshot.window_flag:
            (ex, ey) = self.win.get_event_coord(event)
            screenshot.action = ACTION_INIT
            (screenshot.x, screenshot.y) = self.win.get_event_coord(event)
            self.win.window.queue_draw()
        else:
            #setCursor(screenshot.window, gtk.gdk.PENCIL)
            pass
                
    def action_init(self, screenshot, event):
        ''' ACTION_INIT'''
        if screenshot.drag_flag:
            (ex, ey) = self.win.get_event_coord(event)
            (screenshot.rect_width, screenshot.rect_height) = (ex - screenshot.x, ey - screenshot.y)
            self.win.window.queue_draw()
        else:
            #setCursor(screenshot.window, gtk.gdk.PENCIL)
            pass

    def action_select(self, screenshot, event):
        '''ACTION_SELECT '''
        # drag the selected area
        if screenshot.drag_flag:
            (ex, ey) = self.win.get_event_coord(event)
            if screenshot.dragPosition == DRAG_INSIDE:
                screenshot.x = min(max(ex - screenshot.dragStartOffsetX, 0), screenshot.width - screenshot.rect_width)
                screenshot.y = min(max(ey - screenshot.dragStartOffsetY, 0), screenshot.height - screenshot.rect_height)
            elif screenshot.dragPosition == DRAG_TOP_SIDE:
                self.win.drag_frame_top(ex, ey)
            elif screenshot.dragPosition == DRAG_BOTTOM_SIDE:
                self.win.drag_frame_bottom(ex, ey)
            elif screenshot.dragPosition == DRAG_LEFT_SIDE:
                self.win.drag_frame_left(ex, ey)
            elif screenshot.dragPosition == DRAG_RIGHT_SIDE:
                self.win.drag_frame_right(ex, ey)
            elif screenshot.dragPosition == DRAG_TOP_LEFT_CORNER:
                self.win.drag_frame_top(ex, ey)
                self.win.drag_frame_left(ex, ey)
            elif screenshot.dragPosition == DRAG_TOP_RIGHT_CORNER:
                self.win.drag_frame_top(ex, ey)
                self.win.drag_frame_right(ex, ey)
            elif screenshot.dragPosition == DRAG_BOTTOM_LEFT_CORNER:
                self.win.drag_frame_bottom(ex, ey)
                self.win.drag_frame_left(ex, ey)
            elif screenshot.dragPosition == DRAG_BOTTOM_RIGHT_CORNER:
                self.win.drag_frame_bottom(ex, ey)
                self.win.drag_frame_right(ex, ey)                      

            self.win.show_toolbar()
            self.win.adjust_toolbar()
            self.win.show_colorbar()
            self.win.adjust_colorbar()
            
            self.win.window.queue_draw()
        else:
            #setCursor(screenshot.window, gtk.gdk.PENCIL)
            pass
                
    def action_rectangle(self, screenshot, event):
        ''' ACTION_RECTANGLE '''
        if screenshot.drag_flag and screenshot.currentAction:
            (ex, ey) = self.win.get_event_coord(event)
            screenshot.currentAction.drawing((ex, ey), (screenshot.x, screenshot.y, screenshot.rect_width, screenshot.rect_height))
            self.win.window.queue_draw()
        else:
            #setCursor(screenshot.window, gtk.gdk.PENCIL)
            pass

    def action_ellipse(self, screenshot, event):
        ''' ACTION_ELLIPSE '''
        if screenshot.drag_flag and screenshot.currentAction:
            (ex, ey) = self.win.get_event_coord(event)
            screenshot.currentAction.drawing((ex, ey), (screenshot.x, screenshot.y, screenshot.rect_width, screenshot.rect_height))
            self.win.window.queue_draw()
        else:
            #setCursor(screenshot.window, gtk.gdk.PENCIL)
            pass

    def action_arrow(self, screenshot, event):
        ''' ACTION_ARROW '''
        if screenshot.drag_flag and screenshot.currentAction:
            (ex, ey) = self.win.get_event_coord(event)
            screenshot.currentAction.drawing((ex, ey), (screenshot.x, screenshot.y, screenshot.rect_width, screenshot.rect_height))
            self.win.window.queue_draw()
        else:
            #setCursor(screenshot.window, gtk.gdk.PENCIL)
            pass

    def action_line(self, screenshot, event):
        ''' ACTION_LINE '''
        if screenshot.drag_flag and screenshot.currentAction:
            (ex, ey) = self.win.get_event_coord(event)
            screenshot.currentAction.drawing((ex, ey), (screenshot.x, screenshot.y, screenshot.rect_width, screenshot.rect_height))
            self.win.window.queue_draw()
        else:
            #setCursor(screenshot.window, gtk.gdk.PENCIL)
            pass

    def adjust(self, screenshot, event):
        ''' adjust '''
        # can't drag and has not selected area
        if not screenshot.drag_flag and screenshot.window_flag:
            #screenshot.hideToolbar()
            (wx, wy) = self.win.get_event_coord(event)
            for each in screenshot.screenshot_window_info:
                if each.x < wx < (each.x + each.width) and each.y < wy < (each.y + each.height):
                    screenshot.x = each.x
                    screenshot.y = each.y
                    screenshot.rect_width = each.width
                    screenshot.rect_height = each.height
            self.win.window.queue_draw()
                
        # input text over
        if screenshot.action is None:
            (tx, ty) = self.win.get_event_coord(event)       
            if screenshot.textDragFlag:
                screenshot.currentTextAction.update_coord(tx - screenshot.textDragOffsetX, ty - screenshot.textDragOffsetY)
                screenshot.drawTextLayoutFlag = True
                self.win.window.queue_draw()
            else:
                for eachAction, info in screenshot.textActionInfo.items():
                    if info[0] < tx < info[0]+info[2] and info[1] < ty < info[1]+info[3]:
                        screenshot.currentTextAction = eachAction
                        
            if screenshot.currentTextAction:
                drawTextX, drawTextY, drawTextWidth, drawTextHeight = screenshot.currentTextAction.get_layout_info()
                if drawTextX <= tx <= drawTextX + drawTextWidth and drawTextY <= ty <= drawTextY + drawTextHeight:
                    screenshot.drawTextLayoutFlag = True
                    #setCursor(self.window, gtk.gdk.FLEUR)
                    self.win.window.queue_draw()
                else:
                    screenshot.drawTextLayoutFlag = False    
                    screenshot.currentTextAction = None
                    self.win.window.window.set_cursor(None)
                    self.win.window.queue_draw()
