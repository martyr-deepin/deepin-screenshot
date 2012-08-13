#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2011 ~ 2012 Deepin, Inc.
#               2011 ~ 2012 Hou Shaohui
# 
# Author:     Hou Shaohui <houshao55@gmail.com>
# Maintainer: Hou Shaohui <houshao55@gmail.com>
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

import time

from Xlib import display, X, protocol


class EWMH(object):
    
    # List of strings representing all know window types.
    NET_WM_WINDOW_TYPES = (
        "_NET_WM_WINDOW_TYPE_DESKTOP",
        "_NET_WM_WINDOW_TYPE_DOCK",
        "_NET_WM_WINDOW_TYPE_TOOLBAR",
        "_NET_WM_WINDOW_TYPE_MENU",
        "_NET_WM_WINDOW_TYPE_UTILITY",
        "_NET_WM_WINDOW_TYPE_SPLASH",
        "_NET_WM_WINDOW_TYPE_DIALOG",
        "_NET_WM_WINDOW_TYPE_DROPDOWN_MENU",
        "_NET_WM_WINDOW_TYPE_POPUP_MENU",
        "_NET_WM_WINDOW_TYPE_NOTIFICATION",
        "_NET_WM_WINDOW_TYPE_COMBO",
        "_NET_WM_WINDOW_TYPE_DND",
        "_NET_WM_WINDOW_TYPE_NORMAL",
        )
    
    # List of strings representing all know window actions.
    NET_WM_ACTIONS = (
        "_NET_WM_ACTION_MOVE",
        "_NET_WM_ACTION_RESIZE",
        "_NET_WM_ACTION_MINIMIZE",
        "_NET_WM_ACTION_SHADE",
        "_NET_WM_ACTION_STICK",
        "_NET_WM_ACTION_MAXIMIZE_HORZ",
        "_NET_WM_ACTION_MAXIMIZE_VERT",
        "_NET_WM_ACTION_FULLSCREEN",
        "_NET_WM_ACTION_CHANGE_DESKTOP",
        "_NET_WM_ACTION_CLOSE",
        "_NET_WM_ACTION_ABOVE",
        "_NET_WM_ACTION_BELOW",
        )
    
    # Lisgt of strings representing all know window states.
    NET_WM_STATES = (
        "_NET_WM_STATE_MODAL",
        "_NET_WM_STATE_STICKY",
        "_NET_WM_STATE_MAXIMIZED_VERT",
        "_NET_WM_STATE_MAXIMIZED_HORZ",
        "_NET_WM_STATE_SHADED",
        "_NET_WM_STATE_SKIP_TASKBAR",
        "_NET_WM_STATE_SKIP_PAGER",
        "_NET_WM_STATE_HIDDEN",
        "_NET_WM_STATE_FULLSCREEN",
        "_NET_WM_STATE_ABOVE",
        "_NET_WM_STATE_BELOW",
        "_NET_WM_STATE_DEMANDS_ATTENTION",
        )
    
    def __init__(self, _display=None, root=None):
        self.display = _display or display.Display()
        self.root = root or self.display.screen().root
        
        self.__get_attrs = {
            "_NET_CLIENT_LIST"          : self.get_client_list,
            "_NET_CLIENT_LIST_STACKING" : self.get_client_list_stacking,
            "_NET_NUMBER_OF_DESKTOPS"   : self.get_number_of_desktops,
            "_NET_DESKTOP_GEOMETRY"     : self.get_desktop_geometry,
            "_NET_DESKTOP_VIEWPORT"     : self.get_desktop_viewport,
            "_NET_CURRENT_DESKTOP"      : self.get_current_desktop,
            "_NET_ACTIVE_WINDOW"        : self.get_active_window,
            "_NET_WORKAREA"             : self.get_workarea,
            "_NET_SHOWING_DESKTOP"      : self.get_showing_desktop,
            "_NET_WM_NAME"              : self.get_wm_name,
            "_NET_WM_VISIBLE_NAME"      : self.get_wm_visible_name,
            "_NET_WM_DESKTOP"           : self.get_wm_desktop,
            "_NET_WM_WINDOW_TYPE"       : self.get_wm_window_type,
            "_NET_WM_STATE"             : self.get_wm_state,
            "_NET_WM_ALLOWED_ACTIONS"   : self.get_wm_allowed_actions,
            "_NET_WM_PID"               : self.get_wm_pid,
            }
        
        self.__set_attrs = {
            "_NET_NUMBER_OF_DESKTOPS"   : self.set_number_of_desktops,
            "_NET_DESKTOP_GEOMETRY"     : self.set_desktop_geometry,
            "_NET_DESKTOP_VIEWPORT"     : self.set_desktop_viewport,
            "_NET_CURRENT_DESKTOP"      : self.set_current_desktop,
            "_NET_ACTIVE_WINDOW"        : self.set_active_window,
            "_NET_SHOWING_DESKTOP"      : self.set_showing_desktop,
            "_NET_CLOSE_WINDOW"         : self.set_close_window,
            "_NET_MOVERESIZE_WINDOW"    : self.set_moveresize_window,
            "_NET_WM_NAME"              : self.set_wm_name,
            "_NET_WM_VISIBLE_NAME"      : self.set_wm_visible_name,
            "_NET_WM_DESKTOP"           : self.set_wm_desktop,
            "_NET_WM_STATE"             : self.set_wm_state,
            }
        
        
    def __set_property(self, _type, data, win=None, mask=None):
        if not win: win = self.root
        if isinstance(data, str):
            data_size = 8        
        else:    
            data = (data + [0] * (5 - len(data)))[:5]
            data_size = 32
            
        event = protocol.event.ClientMessage(window=win, client_type=self.display.get_atom(_type),
                                             data=(data_size, data))    
        if not mask:
            mask = (X.SubstructureRedirectMask | X.SubstructureNotifyMask)
        self.root.send_event(event, event_mask=mask)    
        
    def __get_property(self, _type, win=None):    
        if not win: win = self.root
        atom = win.get_full_property(self.display.get_atom(_type), X.AnyPropertyType)
        if atom:
            return atom.value
    _get_property = __get_property
        
    def __create_window(self, win_id):    
        if not win_id: return None
        return self.display.create_resource_object("window", win_id)
        
    def get_atom_name(self, atom):    
        try:
            return self.display.get_atom_name(atom)
        except:
            return "UNKNOW"
        
    def set_number_of_desktops(self, value):    
        self.__set_property("_NET_NUMBER_OF_DESKTOPS", [value])
        
    def set_desktop_geometry(self, width, height):    
        self.__set_property("_NET_DESKTOP_GEOMETRY", [width, height])
        
    def set_desktop_viewport(self, width, height):    
        self.__set_property("_NET_DESKTOP_VIEWPORT", [width, height])
        
    def set_current_desktop(self, value):    
        self.__set_property("_NET_CURRENT_DESKTOP", [value, X.CurrentTime])
        
    def set_active_window(self, win):    
        self.__set_property("_NET_ACTIVE_WINDOW", [1, X.CurrentTime, win.id], win)
        
    def set_showing_desktop(self, show):    
        '''
            Set / Unset the mode showing desktop.
           :param show: 1 to set the desktop mode, else 0  
        '''
        self.__set_property("_NET_SHOWING_DESKTOP", [show])
        
    def set_close_window(self, win):    
        self.__set_property("_NET_CLOSE_WINDOW", [int(time.mktime(time.localtime())), 1], win)
        
    def set_wm_name(self, win, name):    
        self.__set_property("_NET_WM_NAME", name, win)
        
    def set_wm_visible_name(self, win, name):    
        self.__set_property("_NET_WM_VISIBLE_NAME", name, win)
        
    def set_wm_desktop(self, win, value):    
        self.__set_property("_NET_WM_DESKTOP", [value, 1], win)
        
    def set_moveresize_window(self, win, gravity=0, x=None, y=None, w=None, h=None):    
        """
        Set the property _NET_MOVERESIZE_WINDOW to move / resize the given window.
        Flags are automatically calculated if x, y, w or h are defined.
        
        :param win: the window object
        :param gravity: gravity (one of the Xlib.X.*Gravity constant or 0)
        :param x: int or None
        :param y: int or None
        :param w: int or None
        :param h: int or None
        """
        
        gravity_flags = gravity | 0b0000100000000000 # indicate source (application)   
        if x is None: x = 0
        else: gravity_flags = gravity_flags | 0b0000010000000000 # indicate presence of x
        
        if y is None: y = 0
        else: gravity_flags = gravity_flags | 0b0000001000000000 # indicate presence of y
        
        if w is None: w = 0
        else: gravity_flags = gravity_flags | 0b0000000100000000 # indicate presence of w
        
        if h is None: h = 0
        else: gravity_flags = gravity_flags | 0b0000000010000000 # indicate presence of h
        
        self.__set_property('_NET_MOVERESIZE_WINDOW', [gravity_flags, x, y, w, h], win)
        
    def set_wm_state(self, win, action, state, state2=0):    
        """
        Set / unset one or two state(s) for the given window (property _NET_WM_STATE).
        
        :param win: the window object
        :param action: 0 to remove, 1 to add or 2 to toggle state(s)
        :param state: a state
        :type state: int or str (see :attr:`NET_WM_STATES`)
        :param state2: a state or 0
        :type state2: int or str (see :attr:`NET_WM_STATES`)
        """
        if not isinstance(state, int):
            state = self.display.get_atom(state, 1)
        if not isinstance(state2, int):    
            state2 = self.display.get_atom(state2, 1)
        self.__set_property("_NET_WM_STATE", [action, state, state2, 1], win)    
        
    def get_client_list(self):    
        return map(self.__create_window, self.__get_property("_NET_CLIENT_LIST"))
    
    def get_client_list_stacking(self):
        return map(self.__create_window, self.__get_property("_NET_CLIENT_LIST_STACKING"))
    
    def get_window_list(self):
        wm_list = self.get_client_list_stacking()
        wm_list.reverse()
        return filter(self.filter_state, filter(self.filter_type, wm_list))
    
    def filter_type(self, window):
        wm_type = "_NET_WM_WINDOW_TYPE_DESKTOP"
        if wm_type in self.get_wm_window_type(window, True):
            return False
        return True
    
    def filter_state(self, window):
        wm_states = ["_NET_WM_STATE_SKIP_TASKBAR", "_NET_WM_STATE_SKIP_PAGER"]
        for wm_state in wm_states:
            if wm_state in self.get_wm_state(window, True):
                return False
        return True    
            
    
    def get_wm_command(self, win):
        return self.__get_property("WM_COMMAND", win).strip("\x00")
    
    def get_number_of_desktops(self):
        return self.__get_property("_NET_NUMBER_OF_DESKTOPS")[0]
    
    def get_desktop_geometry(self):
        return self.__get_property("_NET_DESKTOP_GEOMETRY")
    
    def get_desktop_viewport(self):
        return self.__get_property("_NET_DESKTOP_VIEWPORT")
    
    def get_current_desktop(self):
        return self.__get_property("_NET_CURRENT_DESKTOP")[0]
    
    def get_active_window(self):
        return self.__create_window(self.__get_property("_NET_ACTIVE_WINDOW")[0])
    
    def get_workarea(self):
        return self.__get_property("_NET_WORKAREA")
    
    def get_showing_desktop(self):
        return self.__get_property("_NET_SHOWING_DESKTOP")[0]
    
    def get_wm_name(self, win):
        return self.__get_property("_NET_WM_NAME", win)
    
    def get_wm_visible_name(self, win):
        return self.__get_property("_NET_WM_VISIBLE_NAME", win)
    
    def get_wm_desktop(self, win):
        return self.__get_property("_NET_WM_DESKTOP", win)[0]
    
    def get_wm_window_type(self, win, description=False):
        types = self.__get_property("_NET_WM_WINDOW_TYPE", win)
        if not description:
            return types
        return map(self.get_atom_name, types)
    
    def get_wm_state(self, win, description=False):
        states = self.__get_property("_NET_WM_STATE", win)
        if not description:
            return states
        return map(self.get_atom_name, states)
    
    def get_wm_allowed_actions(self, win, description=False):
        wm_allowed_actions = self.__get_property("_NET_WM_ALLOWED_ACTIONS", win)
        if not description:
            return wm_allowed_actions
        return map(self.get_atom_name, wm_allowed_actions)
    
    def get_wm_pid(self, win):
        return self.__get_property("_NET_WM_PID", win)[0]
        
    def get_readable_properties(self):
        return self.__get_attrs.keys()
    
    def get_property(self, prop, *args, **kwargs):
        f = self.__get_attrs.get(prop)
        if not f:
            raise KeyError("Unknow readable property: %s" % prop)
        return f(self, *args, **kwargs)
    
    def get_writable_properties(self):
        return self.__set_attrs.keys()
    
    def set_property(self, prop, *args, **kwargs):
        f = self.__set_attrs.get(prop)
        if not f:
            raise KeyError("Unknow writable property: %s" % prop)
        return f(self, *args, **kwargs)
