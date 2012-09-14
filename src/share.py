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
from dtk.ui.dialog import ConfirmDialog
from dtk.ui.browser import WebView
from dtk.ui.slider import Slider
from dtk.ui.titlebar import Titlebar
from dtk.ui.button import Button, CheckButton, LinkButton
from dtk.ui.label import Label
from _share import weibo
from lang import _
from lang import lang as sys_lang
from os.path import exists
import gtk
import webkit
import sys
import threading
import time
import pango
import pangocairo

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
        self.thumb_width = 50
        self.thumb_height = 50
        self.MAX_CHAR = 140
        #print "share file:", self.upload_image

        self.window = Window()
        self.window.set_keep_above(True)
        self.window.set_size_request(600, 480)
        self.window.connect("destroy", self.quit)
        #self.window.set_position(gtk.WIN_POS_CENTER_ALWAYS)
        self.window.set_resizable(False)

        titlebar = Titlebar(["close"], title=_("share to web"))
        titlebar.close_button.connect("clicked", self.quit) 
        self.window.add_move_event(titlebar)
        self.window.window_frame.pack_start(titlebar)

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

        self.__weibo_list = []
        self.sina = weibo.Sina(self.web_view)
        self.qq = weibo.Tencent(self.web_view)
        self.__weibo_list.append(self.sina)
        self.__weibo_list.append(self.qq)
        if sys_lang != 'zh_CN':
            self.twitter = weibo.Twitter(self.web_view)
            self.__weibo_list.append(self.twitter)
        self.__current_weibo = None

        self.window.window_frame.pack_start(self.slider)
        self.init_share_box()

    # webkit load-status, login success, go back
    def web_view_load_status(self, web, status):
        '''web_view notify load-status'''
        state = web.get_property("load-status")
        if state == webkit.LOAD_FAILED: # load failed
            print web.get_property('uri')
            print "load failed\n"
            pass
        else:
            if self.__current_weibo:
                # access token
                #print web.get_property('uri')
                if self.__current_weibo.access_token():
                    self.get_user_info_again()
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

    # login or switch user
    def weibo_login(self, widget, weibo):
        '''weibo login'''
        self.web_view.load_uri("about:blank")
        self.set_slide_index(1)
        self.__current_weibo = weibo
        t = threading.Thread(target=self.__current_weibo.request_oauth)
        t.setDaemon(True)
        t.start()

    def create_ico_image(self, filename):
        ''' create image from file'''
        name = app_theme.get_theme_file_path(filename)
        return gtk.image_new_from_file(name)
    
    def get_user_info_again(self):
        '''recreate label info'''
        box = self.__current_weibo.get_box()
        #print "cuurent weibo:", self.__current_weibo.t_type
        children = box.get_children()
        for child in children:
            child.destroy()
        self.get_user_info(self.__current_weibo)
        box.show_all()

    def get_user_info(self, weibo):
        '''create label info'''
        hbox = weibo.get_box()
        info = weibo.get_user_name()
        #print weibo.t_type, info
        if info:
            label = Label(text=info, label_width=60)
            #check = CheckButton()
            check = gtk.CheckButton()
            check.connect("toggled", self.weibo_check_toggle, weibo)
            check.set_active(True)
            hbox.pack_start(check, False, False)
            hbox.pack_start(label, False, False)
            text = "切换用户"
        else:
            text = "用户登陆"
        button = Button(text)
        button.connect("clicked", self.weibo_login, weibo)
        hbox.pack_start(button, False, False)
        return hbox
    
    def show_tooltip(self, widget, event, text):
        '''Create help tooltip.'''
        widget.set_has_tooltip(True)
        widget.set_tooltip_text(text)
        widget.trigger_tooltip_query()

    def get_user_info_thread(self):
        '''get user name thread'''
        time.sleep(0.1)

        for weibo in self.__weibo_list:
            self.get_user_info(weibo)

        gtk.gdk.threads_enter()
        for weibo in self.__weibo_list:
            weibo.get_box().show_all()
        self.share_box.set_sensitive(True)
        gtk.gdk.threads_leave()
    
    # init share box, create share button, input
    def init_share_box(self):
        '''get weibo info, and create button'''
        weibo_box = gtk.HBox(False, 8)
        self.to_share_weibo = {}
        self.to_share_weibo_res = {}
        self.deepin_info = {}

        for weibo in self.__weibo_list:
            vbox = gtk.VBox(False, 2)
            ico = self.create_ico_image("image/weibo/%s.png" % weibo.t_type)
            ico.add_events(gtk.gdk.ENTER_NOTIFY_MASK)
            ico.connect("enter-notify-event", self.show_tooltip, _(weibo.t_type))
            box = gtk.HBox(False, 2)
            weibo.set_box(box)
            vbox.pack_start(ico, False, False)
            vbox.pack_start(box, False, False)
            weibo_box.pack_start(vbox, False, False)

        self.share_box.pack_start(weibo_box, False, False)

        # create Thumbnail
        if exists(self.upload_image):
            pixbuf = gtk.gdk.pixbuf_new_from_file(self.upload_image)
            pixbuf = pixbuf.scale_simple(self.thumb_width, self.thumb_height, gtk.gdk.INTERP_NEAREST)
            thumb = gtk.image_new_from_pixbuf(pixbuf)
        else:
            thumb = gtk.Image()
            thumb.set_size_request(self.thumb_width, self.thumb_height)

        text_scrolled_win = ScrolledWindow()
        text_view = gtk.TextView()
        text_view.connect("expose-event", self.text_view_expose)
        buf = text_view.get_buffer()
        buf.connect("changed", self.text_view_changed)
        text_scrolled_win.add(text_view)
        self.share_box.pack_start(text_scrolled_win)

        self.input_tip_label = Label(_("还可以输入"))
        self.input_num_label = Label("%d" % self.MAX_CHAR, text_size=18)
        label0 = Label(_("字"))

        button = Button(_("发布"))
        button.connect("clicked", self.share_button_clicked, text_view)
        align = gtk.Alignment() 
        align.set(0.5, 0.5, 1, 1)
        align.set_padding(0, 0, 10, 10)
        align.add(button)
        self.share_box.pack_start(align, False, False)

        # at first, set widget insensitive
        self.share_box.set_sensitive(False)
        t = threading.Thread(target=self.get_user_info_thread)
        t.setDaemon(True)
        t.start()

    # if text is empty, show tip info
    def text_view_expose(self, text_view, event):
        '''text_view expose'''
        buf = text_view.get_buffer()
        text = buf.get_text(*buf.get_bounds())
        if text != "":
            return
        win = text_view.get_window(gtk.TEXT_WINDOW_TEXT)
        cr = win.cairo_create()
        context = pangocairo.CairoContext(cr)
        layout = context.create_layout()
        layout.set_font_description(pango.FontDescription("Snas 10"))
        layout.set_alignment(pango.ALIGN_LEFT)
        layout.set_text(_("please input content"))
        cr.set_source_rgb(0.66, 0.66, 0.66)
        context.update_layout(layout)
        context.show_layout(layout)
    
    # show input char num
    def text_view_changed(self, buf):
        '''text_view changed'''
        count = buf.get_char_count()
        if count <= self.MAX_CHAR:
            self.input_num_label.set_text("%d" % (self.MAX_CHAR - count))
            self.input_num_label.text_color = "#000000"
        else:
            self.input_tip_label = Label(_("已经超过"))
            self.input_num_label.set_text("%d" % (count - self.MAX_CHAR))
            self.input_num_label.text_color = "#FF0000"

    def share_button_clicked(self, button, text_view):
        '''share_button_clicked'''
        # file is not exist.
        if not exists(self.upload_image):
            ConfirmDialog(_("error"), "'%s' %s." % (self.upload_image, _("is not existing"))).show_all()
            return False
        has_share_web = False
        for weibo in self.to_share_weibo:
            if self.to_share_weibo[weibo]:
                has_share_web = True
                break
        # have no web selected
        if not has_share_web:
            ConfirmDialog(_("error"), _("at least choose one web")).show_all()
            return False
        # at first, set widget insensitive
        self.share_box.set_sensitive(False)
        t = threading.Thread(target=self.share_to_weibo_thread, args=(text_view, ))
        t.setDaemon(True)
        t.start()
    
    # upload image thread
    def share_to_weibo_thread(self, text_view):
        '''share in thread'''
        buf = text_view.get_buffer()
        text = buf.get_text(*buf.get_bounds())
        if text.strip() == "":
            text = _("DeepinScreenshot")
        for weibo in self.to_share_weibo:
            if self.to_share_weibo[weibo]:
                self.to_share_weibo_res[weibo] = weibo.upload_image(self.upload_image, text)
                self.deepin_info[weibo] = weibo.get_deepin_info()
        self.share_to_weibo_result()
    
    # show upload result
    @post_gui
    def share_to_weibo_result(self):
        '''result of share to weibo'''
        for weibo in self.to_share_weibo_res:
            if self.to_share_weibo_res[weibo][0]:
                link = LinkButton(_(weibo.t_type), self.to_share_weibo_res[weibo][1])
                text = _("upload successfully")
                label = gtk.Label(text)
                link.show()
                label.show()
                self.result_box.pack_start(link)
                self.result_box.pack_start(label)
                #print text
            else:
                error = _(weibo.get_error_msg()) 
                text = "%s %s.(%s)" % (_(weibo.t_type), _("upload failed"), error)
                label = gtk.Label(text)
                label.show()
                self.result_box.pack_start(label)
                #print text
            # followed
            if self.deepin_info[weibo][3]:
                label = Label(_("followed"))
            else:   # to follow
                button = gtk.Button(_("following"))
                button.connect("clicked", self.friendships_add_button_clicked, weibo)
        button = Button(_("Close"))
        button.connect("clicked", self.quit)
        self.set_slide_index(2)
        # after get user info, set widget sensitive
        #self.share_box.set_sensitive(True)

    def friendships_add_button_clicked(self, widget, weibo):
        '''add friendships'''
        #self.result_box.set_sensitive(False)
        widget.set_sensitive(False)
        t = threading.Thread(target=self.friendships_add_thread, args=(widget, weibo))
        t.setDaemon(True)
        t.start()
    
    def friendships_add_thread(self, button, weibo):
        '''add friendships'''
        weibo.friendships_create()
        # after, set widget sensitive
        #gtk.gdk.threads_enter()
        ##self.result_box.set_sensitive(True)
        #button.set_sensitive(True)
        #gtk.gdk.threads_leave()
    
    # show window
    def show(self):
        '''show'''
        self.window.show_window()

    # close widnow
    def quit(self, widget):
        ''' close '''
        gtk.main_quit()

if __name__ == '__main__':
    filename = ""
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        s = ShareToWeibo(filename)
        s.show()
        if len(sys.argv) > 3:
            try:
                x = int(sys.argv[2])
                y = int(sys.argv[3])
                s.window.move(x, y)
            except:
                pass
        gtk.main()
