#!/usr/bin/python
#-*- coding:utf-8 -*-

from theme import app_theme
from dtk.ui.scrolled_window import ScrolledWindow
import os
from dtk.ui.window import Window
from dtk.ui.dialog import DialogBox
from dtk.ui.browser import WebView
from dtk.ui.slider import Slider
from dtk.ui.titlebar import Titlebar
from dtk.ui.button import Button, CheckButton
from dtk.ui.label import Label
from _share import weibo
import gtk
import webkit

class ShareToWeibo():
    '''share picture to weibo'''
    def __init__(self, filename=""):
        self.upload_image = filename
        print "share file:", self.upload_image

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

    def web_view_load_status(self, web, frame):
        '''web_view notify load-status'''
        state = web.get_property("load-status")
        if state == webkit.LOAD_FAILED: # load failed
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
        self.create_label(self.__current_weibo, box)
        box.show_all()

    def create_label(self, weibo, box=None):
        '''create label info'''
        if box is None:
            hbox = gtk.HBox(False, 2)
        else:
            hbox = box
        info = weibo.get_user_name()
        #print weibo.t_type, info
        if info:
            label = Label(text=info, label_width=60)
            check = CheckButton()
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

    def init_share_box(self):
        '''get weibo info, and create button'''
        weibo_box = gtk.HBox(False, 8)
        self.to_share_weibo = {}
        self.to_share_weibo_res = {}

        vbox = gtk.VBox(False, 2)
        sina_ico = self.create_ico_image("image/weibo/Sina.png")
        sina_ico.add_events(gtk.gdk.ENTER_NOTIFY_MASK)
        sina_ico.connect("enter-notify-event", self.show_tooltip, "新浪微博")
        sina_box = self.create_label(self.sina)
        self.sina.set_box(sina_box)
        vbox.pack_start(sina_ico, False, False)
        vbox.pack_start(sina_box, False, False)
        weibo_box.pack_start(vbox, False, False)

        vbox = gtk.VBox(False, 2)
        qq_ico = self.create_ico_image("image/weibo/Tencent.png")
        qq_ico.connect("enter-notify-event", self.show_tooltip, "腾讯微博")
        qq_box = self.create_label(self.qq)
        self.qq.set_box(qq_box)
        vbox.pack_start(qq_ico, False, False)
        vbox.pack_start(qq_box, False, False)
        weibo_box.pack_start(vbox, False, False)

        vbox = gtk.VBox(False, 2)
        twitter_ico = self.create_ico_image("image/weibo/Twitter.png")
        twitter_ico.connect("enter-notify-event", self.show_tooltip, "Twitter")
        twitter_box = self.create_label(self.twitter)
        self.qq.set_box(twitter_box)
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

    def text_view_expose(self, text_view, event):
        '''text_view expose'''
        buf = text_view.get_buffer()
        text = buf.get_text(*buf.get_bounds())
        if text != '':
            return

    def share_button_clicked(self, button, text_view):
        '''share_button_clicked'''
        buf = text_view.get_buffer()
        text = buf.get_text(*buf.get_bounds())
        for weibo in self.to_share_weibo:
            if self.to_share_weibo[weibo]:
                self.to_share_weibo_res[weibo] = weibo.upload_image(self.upload_image, text)
        for weibo in self.to_share_weibo_res:
            if self.to_share_weibo_res[weibo]:
                text = weibo.t_type + "上传成功"
                label = gtk.Label(text)
                label.show()
                self.result_box.pack_start(label)
                print text
            else:
                text = weibo.t_type + "上传失败"
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
    ShareToWeibo().show()
    gtk.main()
