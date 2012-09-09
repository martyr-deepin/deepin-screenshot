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

from theme import app_theme
from dtk.ui.scrolled_window import ScrolledWindow
from dtk.ui.window import Window
from dtk.ui.dialog import DialogBox
from dtk.ui.browser import WebView
from dtk.ui.slider import Slider
from dtk.ui.titlebar import Titlebar
from dtk.ui.button import Button, CheckButton
from dtk.ui.label import Label
from _share import weibo
from lang import __
from os.path import exists
import gtk
import webkit
import sys
import threading
import time

gtk.gdk.threads_init()

def post_gui(func):
    def wrap(*a, **kw): 
        gtk.gdk.threads_enter() 
        ret = func(*a, **kw) 
        gtk.gdk.threads_leave() 
        return ret
    return wrap 

class ShareToWeibo():
    '''share picture to weibo'''
    def __init__(self, filename=""):
        self.upload_image = filename
        #print "share file:", self.upload_image

        #self.window = Window()
        self.window = DialogBox("分享到")
        self.window.set_size_request(600, 480)
        self.window.connect("destroy", self.close_callback)
        self.window.set_resizable(False)
        self.slider = Slider()
        self.slider_list = []

        self.share_box = gtk.VBox(False, 2)
        self.web_box = gtk.VBox(False, 10)
        self.result_box = gtk.VBox(False, 10)

        left_button = Button("<--")
        left_button.connect("clicked", lambda w: self.set_slide_index(0))
        self.web_view = WebView()
        self.web_view.connect("notify::load-status", self.web_view_load_status)
        self.web_scrolled_window = ScrolledWindow()
        self.web_scrolled_window.add(self.web_view)
        self.web_scrolled_window.set_size_request(600, 400)

        self.web_box.pack_start(left_button)
        self.web_box.pack_start(self.web_scrolled_window)

        self.slider.append_widget(self.share_box)
        self.slider.append_widget(self.web_box) 
        self.slider.append_widget(self.result_box)
        self.slider_list.append(self.share_box)
        self.slider_list.append(self.web_box)
        self.slider_list.append(self.result_box)

        self.sina = weibo.Sina(self.web_view)
        self.qq = weibo.Tencent(self.web_view)
        self.twitter = weibo.Twitter(self.web_view)
        self.__current_weibo = None

        self.window.body_box.pack_start(self.slider)
        self.init_share_box()

    def web_view_load_status(self, web, status):
        '''web_view notify load-status'''
        state = web.get_property("load-status")
        if state == webkit.LOAD_FAILED: # load failed
            print "load failed\n"
            #frame = web.get_main_frame()
            #web.load_string("<html><body><b>load failed!</b></body></html>", "text/html", "UTF-8", "")
            pass
        else:
            if self.__current_weibo:
                # access token
                #print web.get_property('uri')
                if self.__current_weibo.access_token():
                    self.recreate_label()
                    self.set_slide_index(0)

    def set_slide_index(self, index):
        '''set slide to index'''
        if index >= len(self.slider_list):
            return
        self.slider.slide_to(self.slider_list[index])

    def weibo_check_toggle(self, button, weibo):
        '''weibo check button toggle'''
        if button.get_active():
            self.to_share_weibo[weibo] = 1
        else:
            self.to_share_weibo[weibo] = 0

    def weibo_login(self, widget, weibo):
        '''weibo login'''
        self.web_view.load_uri("about:blank")
        weibo.request_oauth()
        self.set_slide_index(1)
        self.__current_weibo = weibo

    def create_ico_image(self, filename):
        ''' create image from file'''
        name = app_theme.get_theme_file_path(filename)
        return gtk.image_new_from_file(name)
    
    def recreate_label(self):
        '''recreate label info'''
        box = self.__current_weibo.get_box()
        #print "cuurent weibo:", self.__current_weibo.t_type
        children = box.get_children()
        for child in children:
            child.destroy()
        self.create_label(self.__current_weibo)

    @post_gui
    def create_label(self, weibo):
        '''create label info'''
        hbox = weibo.get_box()
        info = weibo.get_user_name()
        #print weibo.t_type, info
        if info:
            label = Label(text=info, label_width=60)
            check = CheckButton()
            check.connect("toggled", self.weibo_check_toggle, weibo)
            #check.set_active(True)
            hbox.pack_start(check, False, False)
            hbox.pack_start(label, False, False)
            text = "切换用户"
        else:
            text = "用户登陆"
        button = Button(text)
        button.connect("clicked", self.weibo_login, weibo)
        hbox.pack_start(button, False, False)
        hbox.show_all()
        return hbox
    
    def show_tooltip(self, widget, event, text):
        '''Create help tooltip.'''
        widget.set_has_tooltip(True)
        widget.set_tooltip_text(text)
        widget.trigger_tooltip_query()

    def __get_user_info_thread(self):
        '''get user name thread'''
        time.sleep(0.1)
        sina_thread = threading.Thread(target=self.create_label, args=(self.sina,))
        qq_thread = threading.Thread(target=self.create_label, args=(self.qq,))
        twitter_thread = threading.Thread(target=self.create_label, args=(self.twitter,))

        sina_thread.setDaemon(True)
        qq_thread.setDaemon(True)
        twitter_thread.setDaemon(True)

        sina_thread.start()
        qq_thread.start()
        twitter_thread.start()

        # wait for all to finish
        for t in [sina_thread, qq_thread, twitter_thread]:
            t.join()
        # after get user info, set widget sensitive
        gtk.gdk.threads_enter()
        self.share_box.set_sensitive(True)
        gtk.gdk.threads_leave()
    
    def init_share_box(self):
        '''get weibo info, and create button'''
        weibo_box = gtk.HBox(False, 8)
        self.to_share_weibo = {}
        self.to_share_weibo_res = {}

        vbox = gtk.VBox(False, 2)
        sina_ico = self.create_ico_image("image/weibo/Sina.png")
        sina_ico.add_events(gtk.gdk.ENTER_NOTIFY_MASK)
        sina_ico.connect("enter-notify-event", self.show_tooltip, "新浪微博")
        #sina_box = self.create_label(self.sina)
        sina_box = gtk.HBox(False, 2)
        self.sina.set_box(sina_box)
        vbox.pack_start(sina_ico, False, False)
        vbox.pack_start(sina_box, False, False)
        weibo_box.pack_start(vbox, False, False)

        vbox = gtk.VBox(False, 2)
        qq_ico = self.create_ico_image("image/weibo/Tencent.png")
        qq_ico.connect("enter-notify-event", self.show_tooltip, "腾讯微博")
        #qq_box = self.create_label(self.qq)
        qq_box = gtk.HBox(False, 2)
        self.qq.set_box(qq_box)
        vbox.pack_start(qq_ico, False, False)
        vbox.pack_start(qq_box, False, False)
        weibo_box.pack_start(vbox, False, False)

        vbox = gtk.VBox(False, 2)
        twitter_ico = self.create_ico_image("image/weibo/Twitter.png")
        twitter_ico.connect("enter-notify-event", self.show_tooltip, "Twitter")
        #twitter_box = self.create_label(self.twitter)
        twitter_box = gtk.HBox(False, 2)
        self.twitter.set_box(twitter_box)
        vbox.pack_start(twitter_ico, False, False)
        vbox.pack_start(twitter_box, False, False)
        weibo_box.pack_start(vbox, False, False)
        self.share_box.pack_start(weibo_box, False, False)

        text_scrolled_win = ScrolledWindow()
        text_view = gtk.TextView()
        text_view.connect("expose-event", self.text_view_expose)
        text_scrolled_win.add(text_view)
        self.share_box.pack_start(text_scrolled_win)

        button = Button("分享")
        button.connect("clicked", self.share_button_clicked, text_view)
        self.window.button_box.remove(self.window.left_button_box)
        self.window.button_box.remove(self.window.right_button_box)
        self.share_box.pack_start(self.window.left_button_box, False, False)
        self.share_box.pack_start(self.window.right_button_box, False, False)
        self.window.right_button_box.pack_start(button, False, False)

        # at first, set widget insensitive
        self.share_box.set_sensitive(False)
        t = threading.Thread(target=self.__get_user_info_thread)
        t.setDaemon(True)
        t.start()

    def text_view_expose(self, text_view, event):
        '''text_view expose'''
        buf = text_view.get_buffer()
        text = buf.get_text(*buf.get_bounds())
        if text != '':
            return

    def share_button_clicked(self, button, text_view):
        '''share_button_clicked'''
        if not exists(self.upload_image):
            # file is not exist.
            return False
        # at first, set widget insensitive
        self.share_box.set_sensitive(False)
        t = threading.Thread(target=self.__share_to_weibo_thread, args=(text_view, ))
        t.setDaemon(True)
        t.start()
    
    def __share_to_weibo_thread(self, text_view):
        '''share in thread'''
        buf = text_view.get_buffer()
        text = buf.get_text(*buf.get_bounds())
        for weibo in self.to_share_weibo:
            if self.to_share_weibo[weibo]:
                self.to_share_weibo_res[weibo] = weibo.upload_image(self.upload_image, text)
        self.__share_to_weibo_result()
        # after get user info, set widget sensitive
        gtk.gdk.threads_enter()
        self.share_box.set_sensitive(True)
        gtk.gdk.threads_leave()
    
    @post_gui
    def __share_to_weibo_result(self):
        '''result of share to weibo'''
        for weibo in self.to_share_weibo_res:
            if self.to_share_weibo_res[weibo][0]:
                text = weibo.t_type + "上传成功" + self.to_share_weibo_res[weibo][1]
                label = gtk.Label(text)
                label.show()
                self.result_box.pack_start(label)
                print text
            else:
                error = __(weibo.get_error_msg()) if weibo.get_error_msg() else ""
                text = weibo.t_type + "上传失败" + error
                label = gtk.Label(text)
                label.show()
                self.result_box.pack_start(label)
                print text
        self.set_slide_index(2)

    def show(self):
        '''show'''
        self.window.show_window()

    def close_callback(self, widget):
        ''' close '''
        gtk.main_quit()

if __name__ == '__main__':
    filename = ""
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        ShareToWeibo(filename).show()
        gtk.main()
