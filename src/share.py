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

from theme import app_theme, app_theme_get_dynamic_color, app_theme_get_dynamic_pixbuf
from dtk.ui.scrolled_window import ScrolledWindow
from dtk.ui.window import Window
from dtk.ui.dialog import ConfirmDialog, DialogLeftButtonBox, DialogRightButtonBox
from dtk.ui.browser import WebView
from dtk.ui.slider import Slider
from dtk.ui.titlebar import Titlebar
from dtk.ui.button import Button, CheckButton, LinkButton, ImageButton
from dtk.ui.line import HSeparator, VSeparator
from dtk.ui.label import Label
import dtk.ui.tooltip as Tooltip
import dtk.ui.utils as utils
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
        self.thumb_width = 188
        self.thumb_height = 168
        self.MAX_CHAR = 140
        self.__text_frame_color = (0.76, 0.76, 0.76)
        #print "share file:", self.upload_image
        self.__win_width = 602

        self.window = Window()
        self.window.set_keep_above(True)
        self.window.set_size_request(self.__win_width, 288)
        self.window.connect("destroy", self.quit)
        #self.window.set_position(gtk.WIN_POS_CENTER_ALWAYS)
        self.window.set_resizable(False)

        titlebar = Titlebar(["close"], app_name=_("share to web"))
        #titlebar.title_align.set(0, 0.5, 0, 0)
        titlebar.close_button.connect("clicked", self.quit) 
        self.window.add_move_event(titlebar)
        self.window.window_frame.pack_start(titlebar)

        slider_align = gtk.Alignment()
        slider_align.set(0.5, 0.5, 0, 0)
        slider_align.set_padding(5, 5, 5, 5)

        slider_vbox = gtk.VBox(False)
        slider_align.add(slider_vbox)

        self.slider = Slider()
        self.slider.set_size_request(self.__win_width, 240)
        #self.slider.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color(1.0, 0.0, 0.0))
        self.slider_list = []
        slider_vbox.pack_start(self.slider, False, False)

        self.share_box = gtk.VBox(False, 2)
        self.web_box = gtk.VBox(False, 10)
        self.result_box = gtk.VBox(False, 10)

        self.share_box.set_size_request(self.__win_width, -1)
        self.web_box.set_size_request(self.__win_width, -1)
        self.result_box.set_size_request(self.__win_width, -1)

        share_align = gtk.Alignment()
        share_align.set(0.5, 0.5, 0, 0)
        share_align.add(self.share_box)

        #web_left_button = gtk.Button("<--")
        web_left_button = ImageButton(
            app_theme.get_pixbuf("share/go_back.png"),
            app_theme.get_pixbuf("share/go_back.png"),
            app_theme.get_pixbuf("share/go_back.png"))
        web_left_button.connect("clicked", lambda w: self.set_slide_index(0))
        web_left_button.set_can_focus(False)
        utils.set_clickable_cursor(web_left_button)
        self.web_url_entry = gtk.Entry()
        self.web_url_entry.set_editable(False)
        self.web_url_entry.set_size_request(-1, 22)
        web_navigate_box = gtk.HBox(False,2)
        web_navigate_box.pack_start(web_left_button, False, False)
        web_navigate_box.pack_start(self.web_url_entry)
        self.web_view = WebView()
        self.web_view.connect("notify::load-status", self.web_view_load_status)
        self.web_scrolled_window = ScrolledWindow()
        self.web_scrolled_window.add(self.web_view)
        self.web_scrolled_window.set_size_request(590, 240)

        self.web_box.pack_start(web_navigate_box, False, False)
        self.web_box.pack_start(self.web_scrolled_window)

        self.slider.append_widget(share_align)
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

        #self.window.window_frame.pack_start(self.slider)
        self.window.window_frame.pack_start(slider_align)
        self.init_share_box()

    # webkit load-status, login success, go back
    def web_view_load_status(self, web, status):
        '''web_view notify load-status'''
        state = web.get_property("load-status")
        url = web.get_property('uri')
        if url:
            self.web_url_entry.set_text(url)
        if state == webkit.LOAD_FAILED: # load failed
            print web.get_property('uri')
            print "load failed\n"
            pass
        elif state == webkit.LOAD_COMMITTED:
            if self.__current_weibo and self.__current_weibo.is_callback_url(url):
                # access token
                #print web.get_property('uri')
                if self.__current_weibo.access_token():
                    web.stop_loading()
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

    def create_ico_image(self, name):
        ''' create image from file'''
        pix1 = app_theme_get_dynamic_pixbuf('image/share/%s.png' % name).get_pixbuf()
        pix2 = app_theme_get_dynamic_pixbuf('image/share/%s_no.png' % name).get_pixbuf()
        return (pix1, pix2)
    
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
        self.get_user_error_text = ""
        weibo_hbox = weibo.get_box()
        hbox = gtk.HBox(False)
        align = gtk.Alignment()
        align.set(0.5, 0.5, 0, 0)
        vbox = gtk.VBox(False)
        weibo_hbox.pack_start(align, False, False)
        align.add(vbox)
        vbox.pack_start(hbox)
        info = weibo.get_user_name()
        #print weibo.t_type, info
        gtk.gdk.threads_enter()
        if info:
            label = Label(text=info, label_width=70, enable_select=False)
            check = CheckButton()
            #check = gtk.CheckButton()
            check.connect("toggled", self.weibo_check_toggle, weibo)
            check.set_active(True)
            button = ImageButton(
                app_theme.get_pixbuf("share/" + weibo.t_type + ".png"),
                app_theme.get_pixbuf("share/" + weibo.t_type + ".png"),
                app_theme.get_pixbuf("share/" + weibo.t_type + ".png"))
            utils.set_clickable_cursor(button)
            #button.connect("enter-notify-event", self.show_tooltip, "点击图标切换帐号")
            button.connect("enter-notify-event", self.show_tooltip, _("clicked to switch user"))
            hbox.pack_start(check, False, False)
            hbox.pack_start(button, False, False, 5)
            hbox.pack_start(label, False, False)
        else:
            info_error = weibo.get_curl_error()
            if info_error:
                self.get_user_error_text += "%s:%s." % (weibo.t_type, info_error)
            check = CheckButton()
            #check = gtk.CheckButton()
            check.set_sensitive(False)
            button = ImageButton(
                app_theme.get_pixbuf("share/" + weibo.t_type + "_no.png"),
                app_theme.get_pixbuf("share/" + weibo.t_type + "_no.png"),
                app_theme.get_pixbuf("share/" + weibo.t_type + "_no.png"))
            utils.set_clickable_cursor(button)
            #button.connect("enter-notify-event", self.show_tooltip, "点击图标设置帐号")
            button.connect("enter-notify-event", self.show_tooltip, _("clicked to login"))
            hbox.pack_start(check, False, False)
            hbox.pack_start(button, False, False)
        button.connect("clicked", self.weibo_login, weibo)
        gtk.gdk.threads_leave()
        return weibo_hbox
    
    def show_tooltip(self, widget, event, text):
        '''Create help tooltip.'''
        #widget.set_has_tooltip(True)
        #widget.set_tooltip_text(text)
        #widget.trigger_tooltip_query()
        Tooltip.text(widget, text)

    def get_user_info_thread(self, button, text_view):
        '''get user name thread'''
        time.sleep(0.1)

        for weibo in self.__weibo_list:
            self.get_user_info(weibo)

        gtk.gdk.threads_enter()
        #self.share_box.set_sensitive(True)
        button.set_sensitive(True)
        text_view.set_editable(True)
        for weibo in self.__weibo_list:
            weibo.get_box().show_all()
            weibo.get_box().queue_draw()
        if self.get_user_error_text:
            ConfirmDialog(_("error"), self.get_user_error_text).show_all()
        gtk.gdk.threads_leave()
    
    # init share box, create share button, input
    def init_share_box(self):
        '''get weibo info, and create button'''
        self.to_share_weibo = {}
        self.to_share_weibo_res = {}
        self.deepin_info = {}

        # create Thumbnail
        if exists(self.upload_image):
            pixbuf = gtk.gdk.pixbuf_new_from_file(self.upload_image)
            pix_w = pixbuf.get_width()
            pix_h = pixbuf.get_height()
            if pix_w > pix_h:
                pix_s_w = self.thumb_width
                pix_s_h = int(pix_h / (float(pix_w) / self.thumb_width))
            else:
                pix_s_h = self.thumb_height
                pix_s_w = int(pix_w / (float(pix_h) / self.thumb_height))
            pixbuf = pixbuf.scale_simple(pix_s_w, pix_s_h, gtk.gdk.INTERP_TILES)
            thumb = gtk.image_new_from_pixbuf(pixbuf)
        else:
            thumb = gtk.Image()
        thumb.set_size_request(self.thumb_width, self.thumb_height)

        # weibo context input
        #self.text_pixbuf = app_theme_get_dynamic_pixbuf('image/share/text.png').get_pixbuf()
        self.text_pixbuf = app_theme_get_dynamic_pixbuf('image/share/text_view.png').get_pixbuf()
        text_box = gtk.HBox(False, 2)
        text_vbox = gtk.VBox(False, 2)
        text_scrolled_win = ScrolledWindow()
        text_scrolled_win.set_size_request(360, 167)

        text_view = gtk.TextView()
        text_view.set_left_margin(10)
        text_view.set_right_margin(10)
        text_view.set_pixels_above_lines(5)
        text_view.set_pixels_below_lines(5)
        text_view.set_border_window_size(gtk.TEXT_WINDOW_LEFT, 14)
        text_view.set_wrap_mode(gtk.WRAP_WORD| gtk.WRAP_CHAR)
        text_view.connect("expose-event", self.text_view_expose)
        buf = text_view.get_buffer()
        text_scrolled_win.add(text_view)

        text_align = gtk.Alignment() 
        text_align.set(0.5, 0.5, 0, 0)
        text_align.set_padding(0, 0, 10, 10)

        text_box.pack_start(thumb, False, False)
        text_box.pack_start(text_scrolled_win)
        text_vbox.pack_start(text_box, False, False, 10)
        text_vbox.pack_start(
            HSeparator(app_theme.get_shadow_color("hSeparator").get_color_info(), 0, 0), False, False, 5)
        text_align.add(text_vbox)
        tmp_align = gtk.Alignment()
        tmp_align.set(0.5, 0, 0, 1)
        self.share_box.pack_start(tmp_align, False, False)
        self.share_box.pack_start(text_align, False, False)

        left_box = DialogLeftButtonBox()
        right_box = DialogRightButtonBox()

        left_box.button_align.set(0.0, 0.0, 0, 1)
        right_box.button_align.set(1.0, 0.0, 0, 1)
        # input tip label
        self.input_tip_label = Label(_("left"), text_size=12, enable_select=False)
        self.input_num_label = Label("%d" % self.MAX_CHAR,
            text_size=18, text_x_align=pango.ALIGN_CENTER, label_width=40, enable_select=False)
        label0 = Label(_("chars"), text_size=12, enable_select=False)
        self.input_tip_label.text_color = app_theme_get_dynamic_color("#828282")
        label0.text_color = app_theme_get_dynamic_color("#828282")

        # login box
        weibo_box = gtk.HBox(False, 1)
        weibo_box.set_size_request(-1, 50)
        weibo_box_list = []

        for weibo in self.__weibo_list:
            box = gtk.HBox(False, 2)
            weibo.set_box(box)
            weibo_box_list.append(box)
        left_box.set_buttons(weibo_box_list)

        # share button
        button = Button(_("Tweet"))
        button.set_size_request(75, 25)
        button.connect("clicked", self.share_button_clicked, text_view)
        buf.connect("changed", self.text_view_changed, button)  # check char num

        tmp_vbox = gtk.VBox(False)
        tmp_align = gtk.Alignment()
        tmp_align.set(0.5, 0.5, 0, 0)
        tmp_vbox.pack_start(button, False, False)
        #tmp_vbox.pack_start(tmp_align)
        tmp_align.add(tmp_vbox)
        right_box.set_buttons([self.input_tip_label, self.input_num_label, label0, tmp_align])
        weibo_box.pack_start(left_box, True, True)
        weibo_box.pack_start(right_box, True, True)

        self.share_box.pack_start(weibo_box, False, False)

        # at first, set widget insensitive
        #self.share_box.set_sensitive(False)
        button.set_sensitive(False)
        text_view.set_editable(False)
        t = threading.Thread(target=self.get_user_info_thread, args=(button, text_view))
        t.setDaemon(True)
        t.start()

    # if text is empty, show tip info
    def text_view_expose(self, text_view, event):
        '''text_view expose'''
        buf = text_view.get_buffer()
        text = buf.get_text(*buf.get_bounds())

        win = text_view.get_window(gtk.TEXT_WINDOW_TEXT)
        cr = win.cairo_create()
        cr.set_source_pixbuf(self.text_pixbuf.subpixbuf(14, 0, 346, 167), 0, 0)
        cr.paint()
        
        if text == "" and text_view.get_editable():
            cr.move_to(10, 5)
            context = pangocairo.CairoContext(cr)
            layout = context.create_layout()
            layout.set_font_description(pango.FontDescription("Snas 10"))
            layout.set_alignment(pango.ALIGN_LEFT)
            layout.set_text(_("please input content"))
            cr.set_source_rgb(0.66, 0.66, 0.66)
            context.update_layout(layout)
            context.show_layout(layout)
        
        # left
        win = text_view.get_window(gtk.TEXT_WINDOW_LEFT)
        if win:
            cr = win.cairo_create()
            cr.set_source_pixbuf(self.text_pixbuf.subpixbuf(0, 0, 14, 167), 0, 0)
            cr.paint()
    
    # show input char num
    def text_view_changed(self, buf, button):
        '''text_view changed'''
        count = buf.get_char_count()
        if count <= self.MAX_CHAR:
            self.input_tip_label.set_text(_("left"))
            self.input_num_label.set_text("%d" % (self.MAX_CHAR - count))
            self.input_num_label.text_color = app_theme_get_dynamic_color("#000000")
            if not button.is_sensitive():
                button.set_sensitive(True)
        else:
            self.input_tip_label.set_text(_("more than"))
            self.input_num_label.set_text("%d" % (count - self.MAX_CHAR))
            self.input_num_label.text_color = app_theme_get_dynamic_color("#FF0000")
            if button.is_sensitive():
                button.set_sensitive(False)

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
        #self.share_box.set_sensitive(False)
        button.set_sensitive(False)
        t = threading.Thread(target=self.share_to_weibo_thread, args=(text_view, ))
        t.setDaemon(True)
        t.start()
    
    # upload image thread
    def share_to_weibo_thread(self, text_view):
        '''share in thread'''
        buf = text_view.get_buffer()
        text = buf.get_text(*buf.get_bounds())
        if text.strip() == "":
            text = "%s %s" % (_("come from"), _("DeepinScreenshot"))
        for weibo in self.to_share_weibo:
            if self.to_share_weibo[weibo]:
                self.to_share_weibo_res[weibo] = weibo.upload_image(self.upload_image, text)
                self.deepin_info[weibo] = weibo.get_deepin_info()
        self.share_to_weibo_result()
    
    # show upload result
    @post_gui
    def share_to_weibo_result(self):
        '''result of share to weibo'''
        res_hbox = gtk.HBox(False)
        res_hbox.set_size_request(-1, 240)

        left_box = DialogLeftButtonBox()
        right_box = DialogRightButtonBox()

        left_box.button_align.set(0.5, 0.0, 0, 1)
        right_box.button_align.set(0.5, 0.0, 0, 1)
        right_box.button_align.set_padding(30, 0, 0, 0)

        left_box.set_size_request(410, -1)
        right_box.set_size_request(192, -1)
        
        res_hbox.pack_start(left_box)
        res_hbox.pack_start(
            VSeparator(app_theme.get_shadow_color("vSeparator").get_color_info(), 0, 0))
        res_hbox.pack_start(right_box)

        res_vbox = gtk.VBox(False)
        follow_vbox = gtk.VBox(False)

        #tmp_align = gtk.Alignment()
        #tmp_align.set(0.5, 1.0, 0, 1)
        #tmp_align.set_padding(80, 0, 0, 0)
        #res_vbox.pack_start(tmp_align, False, False)
        #tmp_align = gtk.Alignment()
        #tmp_align.set(0, 0, 0, 0)
        ##tmp_align.set_padding(50, 0, 0, 0)
        #follow_vbox.pack_start(tmp_align, False, False, 50)
        tmp_img = gtk.Image()
        tmp_img.set_size_request(-1, 60) 
        res_vbox.pack_start(tmp_img, False, False)

        follow_tip_hbox = gtk.HBox(False)
        img = gtk.image_new_from_file(app_theme.get_theme_file_path("image/share/deepin_logo.png"))
        follow_tip_hbox.pack_start(img, False, False, 5)
        follow_tip_hbox.pack_start(
            Label("关注Linux Deepin", text_color=app_theme_get_dynamic_color("#5f5f5f"),
            text_size=12, enable_select=False), False, False)
        follow_vbox.pack_start(follow_tip_hbox, False, False, 20)
        for weibo in self.to_share_weibo_res:
            vbox = gtk.VBox(False, 1)
            tip_box = gtk.HBox()
            error_box = gtk.HBox()
            vbox.pack_start(tip_box, False, False)
            vbox.pack_start(error_box, False, False)
            if self.to_share_weibo_res[weibo][0]:   # upload succeed
                img = gtk.image_new_from_file(app_theme.get_theme_file_path("image/share/share_succeed.png"))
                #link = LinkButton(_(weibo.t_type), text_size=13, self.to_share_weibo_res[weibo][1])
                link = Label(_(weibo.t_type), text_size=13, 
                    text_color=app_theme.get_color("link_text"))
                #, enable_gaussian=True, gaussian_radious=1, border_radious=0)
                link.add_events(gtk.gdk.BUTTON_PRESS_MASK)
                link.connect("button-press-event", 
                    lambda w, e: utils.run_command("xdg-open %s" % self.to_share_weibo_res[weibo][1]))
                utils.set_clickable_cursor(link)
                text = _("upload to")
                label = Label(text, text_size=13, 
                    text_color=app_theme_get_dynamic_color("#5f5f5f"), enable_select=False)
                text = _("succeed")
                label1 = Label(text, text_size=13, 
                    text_color=app_theme_get_dynamic_color("#5f5f5f"), enable_select=False)
                tip_box.pack_start(img, False, False, 15)
                tip_box.pack_start(label, False, False)
                tip_box.pack_start(link, False, False)
                tip_box.pack_start(label1, False, False)
                #print text
            else:   # upload failed
                img = gtk.image_new_from_file(app_theme.get_theme_file_path("image/share/share_failed.png"))
                #text = "% %s %s." % (_(weibo.t_type), _("upload failed"))
                text = _("upload to")
                label1 = Label(text, text_size=13, 
                    text_color=app_theme_get_dynamic_color("#5f5f5f"), enable_select=False)
                label2 = Label(_(weibo.t_type), text_size=13, 
                    text_color=app_theme_get_dynamic_color("#5f5f5f"), enable_select=False)
                text = _("failed")
                label3 = Label(text, text_size=13, 
                    text_color=app_theme_get_dynamic_color("#5f5f5f"), enable_select=False)
                error = "(%s)" % _(weibo.get_error_msg()) 
                label = Label(text, text_size=13, 
                    text_color=app_theme_get_dynamic_color("#5f5f5f"), enable_select=False)
                tip_box.pack_start(img, False, False, 15)
                tip_box.pack_start(label1, False, False)
                tip_box.pack_start(label2, False, False)
                tip_box.pack_start(label3, False, False)
                img = gtk.Image()
                img.set_size_request(20, 20)
                error_box.pack_start(img, False, False, 15)
                error_box.pack_start(Label(error, text_size=9,
                    text_color=app_theme_get_dynamic_color("#5f5f5f"), enable_select=False), False, False)
                #print text
            res_vbox.pack_start(vbox, False, False, 10)

            box = gtk.HBox(False, 15)
            # followed
            img = gtk.image_new_from_pixbuf(app_theme.get_pixbuf("share/"+weibo.t_type+".png").get_pixbuf())
            box.pack_start(img, False, False)
            if self.deepin_info[weibo] is not None and self.deepin_info[weibo][3]:
                button = gtk.image_new_from_pixbuf(app_theme.get_pixbuf("share/followed.png").get_pixbuf())
            else:   # to follow
                button = ImageButton(
                    app_theme.get_pixbuf("share/follow_normal.png"),
                    app_theme.get_pixbuf("share/follow_hover.png"),
                    app_theme.get_pixbuf("share/follow_press.png"))
                button.connect("clicked", self.friendships_add_button_clicked, weibo)
            box.pack_start(button, False, False)
            align = gtk.Alignment()
            align.set(0.0, 0.5, 0, 0)
            align.set_padding(0, 0, 30, 0)
            align.add(box)
            follow_vbox.pack_start(align, False, False, 10)
        # close button
        button = Button(_("Close"))
        button.connect("clicked", self.quit)
        button_box = gtk.HBox(False, 15)
        button_align = gtk.Alignment()
        button_align.set(0.0, 0.5, 0, 0)
        button_align.set_padding(0, 0, 55, 0)
        button_box.pack_start(button, False, False)
        button_align.add(button_box)
        res_vbox.pack_start(button_align, False, False)

        left_box.set_buttons([res_vbox])
        right_box.set_buttons([follow_vbox])

        self.result_box.pack_start(res_hbox, False, False)
        self.result_box.show_all()
        self.set_slide_index(2)

    def friendships_add_button_clicked(self, widget, weibo):
        '''add friendships'''
        #self.result_box.set_sensitive(False)
        widget.set_sensitive(False)
        t = threading.Thread(target=self.friendships_add_thread, args=(widget, weibo))
        t.setDaemon(True)
        t.start()
    
    def friendships_add_thread(self, button, weibo):
        '''add friendships'''
        if weibo.friendships_create() is not None:
            gtk.gdk.threads_enter()
            button.set_label("已关注")
            gtk.gdk.threads_leave()
    
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
