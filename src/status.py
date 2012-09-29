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
    ''' BaseProcess Class. it must be inherited and refactored'''
    def __init__(self, screenshot=None, window=None):
        '''
        init process
        @param screenshot: a Screenshot object
        @param window: a RootWindow object
        '''
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
            ACTION_WINDOW: self.action_window,
            None: self._none_action}
    
    def update(self, event):
        '''
        update event info
        @param event: a gtk.gdk.Event
        '''
        self.event = event
    
    def action_init(self, screenshot, event):
        '''
        process the in event in ACTION_INIT status
        @param screenshot: a Screenshot object
        @param event: a gtk.gdk.Event
        '''
        pass
    
    def action_arrow(self, screenshot, event):
        '''
        process the in event in ACTION_ARROW status
        @param screenshot: a Screenshot object
        @param event: a gtk.gdk.Event
        '''
        pass
    
    def action_ellipse(self, screenshot, event):
        '''
        process the in event in ACTION_ELLIPSE status
        @param screenshot: a Screenshot object
        @param event: a gtk.gdk.Event
        '''
        pass
    
    def action_line(self, screenshot, event):
        '''
        process the in event in ACTION_LINE status
        @param screenshot: a Screenshot object
        @param event: a gtk.gdk.Event
        '''
        pass
    
    def action_rectangle(self, screenshot, event):
        '''
        process the in event in ACTION_RECTANGLE status
        @param screenshot: a Screenshot object
        @param event: a gtk.gdk.Event
        '''
        pass
    
    def action_select(self, screenshot, event):
        '''
        process the in event in ACTION_SELECT status
        @param screenshot: a Screenshot object
        @param event: a gtk.gdk.Event
        '''
        pass
    
    def action_text(self, screenshot, event):
        '''
        process the in event in ACTION_TEXT status
        @param screenshot: a Screenshot object
        @param event: a gtk.gdk.Event
        '''
        pass
    
    def action_window(self, screenshot, event):
        '''
        process the in event in ACTION_WINDOW status
        @param screenshot: a Screenshot object
        @param event: a gtk.gdk.Event
        '''
        pass
    
    def _none_action(self, *arg):
        ''' process the in event in Action None status '''
        pass
    
class ButtonPressProcess(BaseProcess):
    ''' buton press status class'''
    def __init__(self, screenshot=None, window=None):
        BaseProcess.__init__(self, screenshot, window)

    def process(self):
        '''Press process button press event'''
        if self.event is None:
            return
        if self.screenshot.show_text_window_flag:
            allocation = self.screenshot.text_window.allocation
            text_view_x = allocation.x + self.screenshot.monitor_x
            text_view_y = allocation.y + self.screenshot.monitor_y
            # in text view area, ignore
            if text_view_x <= self.event.x_root <= text_view_x + allocation.width \
               and text_view_y <= self.event.y_root <= text_view_y + allocation.height:
                   return
        if self.event.button == BUTTON_EVENT_LEFT:
            self.screenshot.drag_flag = True
            self.func_map[self.screenshot.action](self.screenshot, self.event)
            self.adjust(self.screenshot, self.event)
        elif self.event.button == BUTTON_EVENT_RIGHT:
            ev = self.event
            screenshot = self.screenshot
            if screenshot.window_flag:  # has not select area, press right button quit
                self.win.quit()
            if is_in_rect((ev.x, ev.y), screenshot.get_rectangel()):
                self.win.make_menu((int(ev.x), int(ev.y)))      # popup menu
            else:
                while screenshot.action_list:
                    screenshot.action_list.pop()
                while screenshot.text_action_list:
                    screenshot.text_action_list.pop()
                screenshot.text_action_info.clear()
                screenshot.undo()
    
    def action_window(self, screenshot, event):
        '''Press ACTION_WINDOW '''
        screenshot.window_flag = False

    def action_init(self, screenshot, event):
        '''Press ACTION_INIT '''
        (screenshot.x, screenshot.y) = self.win.get_event_coord(event)

    def action_select(self, screenshot, event):
        '''Press ACTION_SELECT '''
        # Init drag position.
        screenshot.drag_position = self.win.get_position(event)
        # Set cursor.
        self.win.set_cursor(screenshot.drag_position)
        # Get drag coord and offset.
        (screenshot.dragStartX, screenshot.dragStartY) = self.win.get_event_coord(event)
        screenshot.dragStartOffsetX = screenshot.dragStartX - screenshot.x
        screenshot.dragStartOffsetY = screenshot.dragStartY - screenshot.y

    def action_rectangle(self, screenshot, event):
        '''Press ACTION_RECTANGLE '''
        # Just create new action when drag position at inside of select area.
        if self.win.get_position(event) == DRAG_INSIDE:
            screenshot.current_action = RectangleAction(ACTION_RECTANGLE, screenshot.action_size, screenshot.action_color)
            # calculate the coord in the window
            #event_coord = self.win.get_event_coord(event)
            #action_x = event_coord[0] - screenshot.monitor_x
            #action_y = event_coord[1] - screenshot.monitor_y
            (action_x, action_y) = self.win.get_event_coord_in_monitor(event)
            screenshot.current_action.start_draw((action_x, action_y))
    
    def action_ellipse(self, screenshot, event):
        '''Press ACTION_ELLIPSE '''
        # Just create new action when drag position at inside of select area.
        if self.win.get_position(event) == DRAG_INSIDE:
            screenshot.current_action = EllipseAction(ACTION_ELLIPSE, screenshot.action_size, screenshot.action_color)
            # calculate the coord in the window
            #event_coord = self.win.get_event_coord(event)
            #action_x = event_coord[0] - screenshot.monitor_x
            #action_y = event_coord[1] - screenshot.monitor_y
            (action_x, action_y) = self.win.get_event_coord_in_monitor(event)
            screenshot.current_action.start_draw((action_x, action_y))

    def action_arrow(self, screenshot, event):
        '''Press ACTION_ARROW '''
        # Just create new action when drag position at inside of select area.
        if self.win.get_position(event) == DRAG_INSIDE:
            screenshot.current_action = ArrowAction(ACTION_ARROW, screenshot.action_size, screenshot.action_color)
            # calculate the coord in the window
            #event_coord = self.win.get_event_coord(event)
            #action_x = event_coord[0] - screenshot.monitor_x
            #action_y = event_coord[1] - screenshot.monitor_y
            (action_x, action_y) = self.win.get_event_coord_in_monitor(event)
            screenshot.current_action.start_draw((action_x, action_y))

    def action_line(self, screenshot, event):
        '''Press ACTION_LINE '''
        # Just create new action when drag position at inside of select area.
        if self.win.get_position(event) == DRAG_INSIDE:
            screenshot.current_action = LineAction(ACTION_LINE, screenshot.action_size, screenshot.action_color)
            # calculate the coord in the window
            #event_coord = self.win.get_event_coord(event)
            #action_x = event_coord[0] - screenshot.monitor_x
            #action_y = event_coord[1] - screenshot.monitor_y
            (action_x, action_y) = self.win.get_event_coord_in_monitor(event)
            screenshot.current_action.start_draw((action_x, action_y))

    def action_text(self, screenshot, event):
        '''Press ACTION_TEXT '''
        if screenshot.show_text_window_flag:    # complete input text, changed action to None
            self.win.save_text_window()
            self.screenshot.toolbar.set_button_active("text", False)
            self.screenshot.current_text_action = None
        else:   # create a new text
            # calculate the coord in the window
            #event_coord = self.win.get_event_coord(event)
            #action_x = event_coord[0] - screenshot.monitor_x
            #action_y = event_coord[1] - screenshot.monitor_y
            (action_x, action_y) = self.win.get_event_coord_in_monitor(event)
            self.win.show_text_window((action_x, action_y))

    def adjust(self, screenshot, event):
        '''Press adjust '''
        if screenshot.action in [ACTION_RECTANGLE, ACTION_ELLIPSE, ACTION_ARROW, ACTION_LINE] \
            and screenshot.show_toolbar_flag \
            and screenshot.y < screenshot.toolbarY < screenshot.y + screenshot.rect_height:
                self.win.hide_toolbar()
                self.win.hide_colorbar()

        # drag text 
        if screenshot.current_text_action and screenshot.action is None:
            # calculate the coord in the window
            #event_coord = self.win.get_event_coord(event)
            #currentX = event_coord[0] - screenshot.monitor_x
            #currentY = event_coord[1] - screenshot.monitor_y
            currentX, currentY = self.win.get_event_coord_in_monitor(event)
            drawTextX,drawTextY = screenshot.current_text_action.get_layout_info()[:2]
            screenshot.textDragOffsetX = currentX - drawTextX
            screenshot.textDragOffsetY = currentY - drawTextY
            screenshot.text_drag_flag = True 

class ButtonReleaseProcess(BaseProcess):
    ''' button release process'''
    def __init__(self, screenshot=None, window=None):
        BaseProcess.__init__(self, screenshot, window)
        
    def process(self):
        '''Release process button release event'''
        if self.event is None:
            return
        if self.event.button == BUTTON_EVENT_LEFT:
            self.screenshot.text_drag_flag = False
            self.screenshot.drag_flag = False
            self.func_map[self.screenshot.action](self.screenshot, self.event)
            self.adjust(self.screenshot, self.event)

    def action_window(self, screenshot, event):
        '''Release ACTION_WINDOW'''
        if screenshot.rect_width > 5 and screenshot.rect_height > 5:
            self.win.show_toolbar()
            self.win.adjust_toolbar()
            screenshot.action = ACTION_SELECT
            self.win.refresh()
        else:
            screenshot.window_flag = True
            
    def action_init(self, screenshot, event):
        '''Release ACTION_INIT'''
        screenshot.action = ACTION_SELECT
        (ex, ey) = self.win.get_event_coord(event)
        # Adjust rectangle when button release.
        if ex > screenshot.x:
            screenshot.rect_width = ex - screenshot.x
        else:
            screenshot.rect_width = abs(ex - screenshot.x)
            screenshot.x = max(ex, screenshot.monitor_x)
        if ey > screenshot.y:
            screenshot.rect_height = ey - screenshot.y
        else:
            screenshot.rect_height = abs(ey - screenshot.y)
            screenshot.y = max(ey, screenshot.monitor_y)
        # min rect 2 * 2
        if screenshot.rect_width < 2:
            screenshot.rect_width = 2
            if screenshot.rect_width + screenshot.x > screenshot.width:
                screenshot.x = screenshot.width - screenshot.rect_width
        if screenshot.rect_height < 2:
            screenshot.rect_height = 2
            if screenshot.rect_height + screenshot.y > screenshot.height:
                screenshot.y = screenshot.height - screenshot.rect_height

        self.win.refresh()
        self.win.show_toolbar()
        self.win.adjust_toolbar()

    def action_select(self, screenshot, event):
        '''Release ACTION_SELECT '''
        # min rect 2 * 2
        if screenshot.rect_width < 2:
            screenshot.rect_width = 2
            if screenshot.rect_width + screenshot.x > screenshot.width:
                screenshot.x = screenshot.width - screenshot.rect_width
        if screenshot.rect_height < 2:
            screenshot.rect_height = 2
            if screenshot.rect_height + screenshot.y > screenshot.height:
                screenshot.y = screenshot.height - screenshot.rect_height
        self.win.refresh()
    
    def action_rectangle(self, screenshot, event):
        '''Release ACTION_RECTANGLE '''
        if screenshot.current_action:
            # calculate the coord in the window
            #event_coord = self.win.get_event_coord(event)
            #action_x = event_coord[0] - screenshot.monitor_x
            #action_y = event_coord[1] - screenshot.monitor_y
            (action_x, action_y) = self.win.get_event_coord_in_monitor(event)
            screenshot.current_action.end_draw((action_x, action_y), screenshot.get_rectangel_in_monitor())
            screenshot.action_list.append(screenshot.current_action)
            screenshot.current_action = None
            self.win.refresh()

    def action_ellipse(self, screenshot, event):
        '''Release ACTION_ELLIPSE '''
        if screenshot.current_action:
            #event_coord = self.win.get_event_coord(event)
            #action_x = event_coord[0] - screenshot.monitor_x
            #action_y = event_coord[1] - screenshot.monitor_y
            (action_x, action_y) = self.win.get_event_coord_in_monitor(event)
            screenshot.current_action.end_draw((action_x, action_y), screenshot.get_rectangel_in_monitor())
            screenshot.action_list.append(screenshot.current_action)
            screenshot.current_action = None
            self.win.refresh()

    def action_arrow(self, screenshot, event):
        '''Release ACTION_ARROW '''
        if screenshot.current_action:
            #event_coord = self.win.get_event_coord(event)
            #action_x = event_coord[0] - screenshot.monitor_x
            #action_y = event_coord[1] - screenshot.monitor_y
            (action_x, action_y) = self.win.get_event_coord_in_monitor(event)
            screenshot.current_action.end_draw((action_x, action_y), screenshot.get_rectangel_in_monitor())
            screenshot.action_list.append(screenshot.current_action)
            screenshot.current_action = None
            self.win.refresh()

    def action_line(self, screenshot, event):
        '''Release ACTION_LINE '''
        if screenshot.current_action:
            #event_coord = self.win.get_event_coord(event)
            #action_x = event_coord[0] - screenshot.monitor_x
            #action_y = event_coord[1] - screenshot.monitor_y
            (action_x, action_y) = self.win.get_event_coord_in_monitor(event)
            screenshot.current_action.end_draw((action_x, action_y), screenshot.get_rectangel_in_monitor())
            screenshot.action_list.append(screenshot.current_action)
            screenshot.current_action = None
            self.win.refresh()
        
    def adjust(self, screenshot, event):
        '''Release adjust '''
        if screenshot.action in [ACTION_RECTANGLE, ACTION_ELLIPSE, ACTION_ARROW, ACTION_LINE, ACTION_TEXT] \
            and not screenshot.show_toolbar_flag \
            and screenshot.y < screenshot.toolbarY < screenshot.y + screenshot.rect_height:
                self.win.show_toolbar()
                self.win.adjust_toolbar()
                self.win.show_colorbar()
                self.win.adjust_colorbar()

class MotionProcess(BaseProcess):
    ''' Motion process'''
    def __init__(self, screenshot=None, window=None):
        BaseProcess.__init__(self, screenshot, window)
        
    def process(self):
        '''Motion process motion event'''
        if self.event is None:
            return
        self.func_map[self.screenshot.action](self.screenshot, self.event)
        self.adjust(self.screenshot, self.event)

    def action_window(self, screenshot, event):
        '''Motion ACTION_WINDOW'''
        # can drag and has selected area
        if screenshot.drag_flag and not screenshot.window_flag:
            (ex, ey) = self.win.get_event_coord(event)
            screenshot.action = ACTION_INIT
            (screenshot.x, screenshot.y) = self.win.get_event_coord(event)
            self.win.refresh()
        else:   # update magnifier
            size = "%d x %d " % (screenshot.rect_width, screenshot.rect_height)
            rgb = utils.get_coord_rgb(screenshot, event.x, event.y)
            self.win.update_magnifier(event.x, event.y, size=size, rgb=str(rgb))
                
    def action_init(self, screenshot, event):
        '''Motion ACTION_INIT'''
        if screenshot.drag_flag:
            (ex, ey) = self.win.get_event_coord(event)
            (screenshot.rect_width, screenshot.rect_height) = (ex - screenshot.x, ey - screenshot.y)
            self.win.refresh()
        else:
            pass

    def action_select(self, screenshot, event):
        '''Motion ACTION_SELECT '''
        # drag the selected area
        if screenshot.drag_flag:
            (ex, ey) = self.win.get_event_coord(event)
            if screenshot.drag_position == DRAG_INSIDE:
                screenshot.x = min(max(ex - screenshot.dragStartOffsetX, screenshot.monitor_x),
                    screenshot.monitor_x + screenshot.width - screenshot.rect_width)
                screenshot.y = min(max(ey - screenshot.dragStartOffsetY, screenshot.monitor_y),
                    screenshot.monitor_y + screenshot.height - screenshot.rect_height)
            elif screenshot.drag_position == DRAG_TOP_SIDE:
                self.win.drag_frame_top(ex, ey)
            elif screenshot.drag_position == DRAG_BOTTOM_SIDE:
                self.win.drag_frame_bottom(ex, ey)
            elif screenshot.drag_position == DRAG_LEFT_SIDE:
                self.win.drag_frame_left(ex, ey)
            elif screenshot.drag_position == DRAG_RIGHT_SIDE:
                self.win.drag_frame_right(ex, ey)
            elif screenshot.drag_position == DRAG_TOP_LEFT_CORNER:
                self.win.drag_frame_top(ex, ey)
                self.win.drag_frame_left(ex, ey)
            elif screenshot.drag_position == DRAG_TOP_RIGHT_CORNER:
                self.win.drag_frame_top(ex, ey)
                self.win.drag_frame_right(ex, ey)
            elif screenshot.drag_position == DRAG_BOTTOM_LEFT_CORNER:
                self.win.drag_frame_bottom(ex, ey)
                self.win.drag_frame_left(ex, ey)
            elif screenshot.drag_position == DRAG_BOTTOM_RIGHT_CORNER:
                self.win.drag_frame_bottom(ex, ey)
                self.win.drag_frame_right(ex, ey)                      

            self.win.refresh()
            self.win.show_toolbar()
            self.win.adjust_toolbar()
        else:
            screenshot.drag_position = self.win.get_position(event)
            # to avoid set cursor again
            if screenshot.last_drag_position != screenshot.drag_position:
                screenshot.last_drag_position = screenshot.drag_position
                self.win.set_cursor(screenshot.drag_position)
                
    def action_rectangle(self, screenshot, event):
        '''Motion ACTION_RECTANGLE '''
        if screenshot.drag_flag and screenshot.current_action:
            #event_coord = self.win.get_event_coord(event)
            #ex = event_coord[0] - screenshot.monitor_x
            #ey = event_coord[1] - screenshot.monitor_y
            (ex, ey) = self.win.get_event_coord_in_monitor(event)
            screenshot.current_action.drawing((ex, ey), screenshot.get_rectangel_in_monitor())
            self.win.refresh()
        else:
            pass

    def action_ellipse(self, screenshot, event):
        '''Motion ACTION_ELLIPSE '''
        if screenshot.drag_flag and screenshot.current_action:
            #event_coord = self.win.get_event_coord(event)
            #ex = event_coord[0] - screenshot.monitor_x
            #ey = event_coord[1] - screenshot.monitor_y
            (ex, ey) = self.win.get_event_coord_in_monitor(event)
            screenshot.current_action.drawing((ex, ey), screenshot.get_rectangel_in_monitor())
            self.win.refresh()
        else:
            pass

    def action_arrow(self, screenshot, event):
        '''Motion ACTION_ARROW '''
        if screenshot.drag_flag and screenshot.current_action:
            #event_coord = self.win.get_event_coord(event)
            #ex = event_coord[0] - screenshot.monitor_x
            #ey = event_coord[1] - screenshot.monitor_y
            (ex, ey) = self.win.get_event_coord_in_monitor(event)
            screenshot.current_action.drawing((ex, ey), screenshot.get_rectangel_in_monitor())
            self.win.refresh()
        else:
            pass

    def action_line(self, screenshot, event):
        '''Motion ACTION_LINE '''
        if screenshot.drag_flag and screenshot.current_action:
            #event_coord = self.win.get_event_coord(event)
            #ex = event_coord[0] - screenshot.monitor_x
            #ey = event_coord[1] - screenshot.monitor_y
            (ex, ey) = self.win.get_event_coord_in_monitor(event)
            screenshot.current_action.drawing((ex, ey), screenshot.get_rectangel_in_monitor())
            self.win.refresh()
        else:
            pass

    def adjust(self, screenshot, event):
        '''Motion adjust '''
        # can't drag and has not selected area
        if not screenshot.drag_flag and screenshot.window_flag:
            self.win.hide_toolbar()
            (wx, wy) = self.win.get_event_coord(event)
            for each in screenshot.screenshot_window_info:
                if each.x <= wx <= (each.x + each.width) and each.y <= wy <= (each.y + each.height):
                    screenshot.x = each.x
                    screenshot.y = each.y
                    screenshot.rect_width = each.width
                    screenshot.rect_height = each.height
                    break
            self.win.refresh()
                
        # input text over
        if screenshot.action is None:
            (tx, ty) = self.win.get_event_coord_in_monitor(event)       
            # drag text
            if screenshot.text_drag_flag and screenshot.current_text_action:
                layout_info = screenshot.current_text_action.get_layout_info()
                des_x = tx - screenshot.textDragOffsetX
                des_y = ty - screenshot.textDragOffsetY
                if des_x < screenshot.x:    # left
                    des_x = screenshot.x
                elif des_x + layout_info[2] > screenshot.x + screenshot.rect_width:     # right
                    des_x = screenshot.x + screenshot.rect_width - layout_info[2]
                if des_y < screenshot.y:    # top
                    des_y = screenshot.y
                elif des_y + layout_info[3] > screenshot.y + screenshot.rect_height:    # bottom
                    des_y = screenshot.y + screenshot.rect_height - layout_info[3]
                screenshot.current_text_action.update_coord(des_x, des_y)
                screenshot.draw_text_layout_flag = True
                self.win.refresh()
            else:
                for each, info in screenshot.text_action_info.items():
                    if screenshot.text_drag_flag:   # has draged a text already
                        break
                    if info[0] <= tx <= info[0]+info[2] and info[1] <= ty <= info[1]+info[3]:
                        screenshot.current_text_action = each
                        
            if screenshot.current_text_action:
                drawTextX, drawTextY, drawTextWidth, drawTextHeight = screenshot.current_text_action.get_layout_info()
                if drawTextX <= tx <= drawTextX + drawTextWidth and drawTextY <= ty <= drawTextY + drawTextHeight:
                    screenshot.draw_text_layout_flag = True
                    self.win.set_cursor('drag')
                    self.win.refresh()
                elif not screenshot.text_drag_flag:     # drag text over, and not in text rectangle
                    screenshot.draw_text_layout_flag = False    
                    screenshot.current_text_action = None
                    self.win.set_cursor(screenshot.action)
                    self.win.refresh()
