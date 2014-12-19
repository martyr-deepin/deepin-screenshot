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
from dtk.ui.dialog import ConfirmDialog, DialogLeftButtonBox, DialogRightButtonBox, DialogBox
from dtk.ui.browser import WebView
from dtk.ui.slider import HSlider
from dtk.ui.button import Button, CheckButton, ImageButton
from dtk.ui.line import VSeparator
from dtk.ui.label import Label
from dtk.ui.entry import InputEntry
import dtk.ui.draw as draw
import dtk.ui.tooltip as Tooltip
import dtk.ui.utils as utils
from _share import weibo
from _share.config import COOKIE_FILE
from nls import _
from nls import default_locale
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

class ShareToWeibo(object):
    '''share picture to weibo'''
    def __init__(self, filename=""):
        '''
        init share
        @param filename: the file to share
        '''
        self.upload_image = filename
        self.thumb_width = 188
        self.thumb_height = 168
        self.MAX_CHAR = 140
        #self.__text_frame_color = (0.76, 0.76, 0.76)
        self.__win_width = 602
        open(COOKIE_FILE,'wb').close()

        self.window = DialogBox(_("Share to social networks"), close_callback=gtk.main_quit)
        self.window.set_keep_above(True)
        self.window.set_size_request(self.__win_width+20, 288)
        self.window.set_resizable(False)
        self.window.titlebar.connect("expose-event", self.__expose_top_and_bottome)
        self.window.button_box.connect("expose-event", self.__expose_top_and_bottome)

        # create slider
        self.slider = HSlider()
        self.slider_list = []

        self.share_box = gtk.VBox(False, 2)     # first page, input context
        self.web_box = gtk.VBox(False, 10)      # second page, login
        self.result_box = gtk.VBox(False, 10)   # third page, share result

        share_align = gtk.Alignment()
        share_align.set(0.5, 0.5, 0, 0)
        share_align.add(self.share_box)
        share_align.connect("expose-event", self.__slider_expose)

        # go back button
        web_left_button = ImageButton(
            app_theme.get_pixbuf("share/back_normal.png"),
            app_theme.get_pixbuf("share/back_hover.png"),
            app_theme.get_pixbuf("share/back_press.png"))
        web_left_button.connect("clicked", lambda w: self.set_slide_index(0))
        web_left_button.set_can_focus(False)
        utils.set_clickable_cursor(web_left_button)
        # show url entry
        self.web_url_entry = InputEntry()
        self.web_url_entry.set_editable(False)
        self.web_url_entry.set_size(555, 20)
        self.web_url_entry.entry.right_menu_visible_flag = False
        # alig url entry
        web_navigate_vbox = gtk.VBox(False)
        web_navigate_vbox.pack_start(self.web_url_entry)
        web_navigate_t_align = gtk.Alignment()
        web_navigate_t_align.set(0.0, 0.5, 0, 0)
        web_navigate_t_align.add(web_navigate_vbox)
        # pack back button and url entry
        web_navigate_box = gtk.HBox(False, 7)
        web_navigate_box.pack_start(web_left_button, False, False)
        web_navigate_box.pack_start(web_navigate_t_align)

        web_navigate_align = gtk.Alignment()
        web_navigate_align.set(0.5, 0.5, 0, 0)
        web_navigate_align.set_padding(4, 0, 11, 13)
        web_navigate_align.add(web_navigate_box)

        # create a webkit
        self.web_view = WebView(COOKIE_FILE)
        self.web_view.connect("notify::load-status", self.web_view_load_status)
        self.web_view.connect("load-error", self.web_view_load_error)
        self.web_scrolled_window = ScrolledWindow()
        self.web_scrolled_window.add(self.web_view)
        self.web_scrolled_window.set_size_request(590, 228)

        self.web_box.pack_start(web_navigate_align, False, False)
        self.web_box.pack_start(self.web_scrolled_window)
        #self.web_box.set_size_request(-1, 258)
        web_align = gtk.Alignment()
        web_align.set(0.5, 0.0, 0, 1)
        web_align.add(self.web_box)
        web_align.connect("expose-event", self.__slider_expose)

        res_align = gtk.Alignment()
        res_align.set(0.5, 0.5, 0, 0)
        res_align.add(self.result_box)
        res_align.connect("expose-event", self.__slider_expose)

        self.slider.set_to_page(share_align)
        self.slider_list.append(share_align)
        self.slider_list.append(web_align)
        self.slider_list.append(res_align)

        self.__weibo_list = []
        self.sina = weibo.Sina(self.web_view)
        self.qq = weibo.Tencent(self.web_view)
        self.twitter = weibo.Twitter(self.web_view)
        self.__weibo_list.append(self.sina)
        self.__weibo_list.append(self.qq)
        self.__weibo_list.append(self.twitter)
        self.__current_weibo = None

        self.window.body_box.pack_start(self.slider, True, True)
        self.init_share_box()

    # webkit load-status, login success, go back
    def web_view_load_status(self, web, status):
        '''web_view notify load-status callback'''
        state = web.get_property("load-status")
        url = web.get_property('uri')
        if url:
            self.web_url_entry.set_editable(True)
            self.web_url_entry.set_text(url)
            self.web_url_entry.entry.move_to_start()
            self.web_url_entry.set_editable(False)
        if state == webkit.LOAD_FAILED:  # load failed
            print "load failed",
            print web.get_property('uri')

        elif state == webkit.LOAD_COMMITTED:
            if self.__current_weibo and self.__current_weibo.is_callback_url(url):
                web.stop_loading()  # if go to  callback url, stop loading
                # access token
                #print "load committed", url
                t = threading.Thread(target=self.weibo_login_thread)
                t.setDaemon(True)
                t.start()

    def web_view_load_error(self, web, fram, url, error, data=None):
        web.load_string(
            "<html><body><p><h1>%s</h1></p>%s</body></html>" % (
            _("Unable to load page"),
            _("Problem occurred while loading the URL '%s'") % (url)),
            "text/html", "UTF-8", "")
        print url
        return True

    # login or switch user
    def weibo_login(self, widget, weibo):
        '''weibo button clicked callback'''
        self.web_view.load_uri("about:blank")
        utils.set_cursor(widget)
        self.set_slide_index(1)
        self.__current_weibo = weibo
        t = threading.Thread(target=self.__current_weibo.request_oauth)
        t.setDaemon(True)
        t.start()

    def weibo_login_thread(self):
        '''in webkit login finish, get user info again'''
        self.__current_weibo.access_token()
        self.get_user_info_again()
        gtk.gdk.threads_enter()
        self.set_slide_index(0)
        gtk.gdk.threads_leave()

    def get_user_info_again(self):
        ''' login or switch user, and get user info again'''
        box = self.__current_weibo.get_box()
        #print "cuurent weibo:", self.__current_weibo.t_type
        gtk.gdk.threads_enter()
        children = box.get_children()
        for child in children:
            if child in self.__weibo_check_button_list:
                self.__weibo_check_button_list.remove(child)
            if child in self.__weibo_image_button_list:
                self.__weibo_image_button_list.remove(child)
            child.destroy()
        gtk.gdk.threads_leave()

        self.get_user_info(self.__current_weibo)

        gtk.gdk.threads_enter()
        box.show_all()
        gtk.gdk.threads_leave()

    def set_slide_index(self, index):
        '''
        set slide to index
        @param index: the index of widget in slider, an int num
        '''
        if index >= len(self.slider_list):
            return
        direct = "right"
        if index == 1 and self.window.button_box in self.window.window_frame.get_children():
            #self.slider.set_size_request(-1, 260)
            win = self.window
            if win.left_button_box in win.button_box.get_children():
                win.button_box.remove(win.left_button_box)
            if win.right_button_box in win.button_box.get_children():
                win.button_box.remove(win.right_button_box)
            tmp = gtk.HSeparator()
            tmp.set_size_request(-1, 1)
            tmp.show()
            win.button_box.pack_start(tmp)
            direct = "right"
            #if self.window.button_box in self.window.window_frame.get_children():
                #self.window.window_frame.remove(self.window.button_box)
        elif index == 0:
            #self.slider.set_size_request(-1, 223)
            win = self.window
            for each in win.button_box.get_children():
                each.destroy()
            if win.left_button_box not in win.button_box.get_children():
                win.button_box.pack_start(win.left_button_box)
            if win.right_button_box not in win.button_box.get_children():
                win.button_box.pack_start(win.right_button_box)
            direct = "left"
            #if self.window.button_box not in self.window.window_frame.get_children():
                #self.window.window_frame.pack_start(self.window.button_box, False, False)
        elif index == 2:
            self.window.left_button_box.set_buttons([])
            l = Label("  ")
            l.show()
            self.window.right_button_box.set_buttons([l])
            direct = "right"
            #self.slider.set_size_request(-1, 223)

        self.slider.slide_to_page(self.slider_list[index], direct)

    def weibo_check_toggle(self, button, weibo):
        '''weibo check button toggled callback. check the weibo to share'''
        if button.get_active():
            self.to_share_weibo[weibo] = 1
        else:
            self.to_share_weibo[weibo] = 0

    def create_ico_image(self, name):
        ''' create image from file'''
        pix1 = app_theme_get_dynamic_pixbuf('image/share/%s.png' % name).get_pixbuf()
        pix2 = app_theme_get_dynamic_pixbuf('image/share/%s_no.png' % name).get_pixbuf()
        return (pix1, pix2)

    def get_user_info(self, weibo):
        '''get weibo user info'''
        info = weibo.get_user_name()
        gtk.gdk.threads_enter()
        #self.get_user_error_text = ""
        weibo_hbox = weibo.get_box()
        hbox = gtk.HBox(False)
        vbox = gtk.VBox(False)
        weibo_hbox.pack_start(vbox, False, False)
        vbox.pack_start(hbox)
        #print weibo.t_type, info
        if info:
            self.is_get_user_info[weibo] = 1
            label = Label(text=info, label_width=70, enable_select=False)
            check = CheckButton()
            #check = gtk.CheckButton()
            check.connect("toggled", self.weibo_check_toggle, weibo)
            check.set_active(True)
            check_vbox = gtk.VBox(False)
            check_align = gtk.Alignment(0.5, 0.5, 0, 0)
            check_align.add(check_vbox)
            check_vbox.pack_start(check, False, False)
            button = ImageButton(
                app_theme.get_pixbuf("share/" + weibo.t_type + ".png"),
                app_theme.get_pixbuf("share/" + weibo.t_type + ".png"),
                app_theme.get_pixbuf("share/" + weibo.t_type + ".png"))
            utils.set_clickable_cursor(button)
            button.connect("enter-notify-event", self.show_tooltip, _("Click to switch user"))
            hbox.pack_start(check_align, False, False)
            hbox.pack_start(button, False, False, 5)
            hbox.pack_start(label, False, False)
        else:
            self.is_get_user_info[weibo] = 0
            check = CheckButton()
            #check = gtk.CheckButton()
            check.set_sensitive(False)
            check_vbox = gtk.VBox(False)
            check_align = gtk.Alignment(0.5, 0.5, 0, 0)
            check_align.add(check_vbox)
            check_vbox.pack_start(check, False, False)
            button = ImageButton(
                app_theme.get_pixbuf("share/" + weibo.t_type + "_no.png"),
                app_theme.get_pixbuf("share/" + weibo.t_type + "_no.png"),
                app_theme.get_pixbuf("share/" + weibo.t_type + "_no.png"))
            utils.set_clickable_cursor(button)
            button.connect("enter-notify-event", self.show_tooltip, _("Click to login"))
            hbox.pack_start(check_align, False, False)
            hbox.pack_start(button, False, False, 5)
            # curl time out
            info_error = weibo.get_curl_error()
            if info_error:
                #self.get_user_error_text += "%s:%s." % (weibo.t_type, _(info_error))
                hbox.pack_start(
                    Label(text="(%s)" % _(info_error), label_width=70,enable_select=False,
                    text_color = app_theme.get_color("left_char_num1")), False, False)

        button.connect("clicked", self.weibo_login, weibo)
        self.__weibo_check_button_list.append(check)
        self.__weibo_image_button_list.append(button)
        gtk.gdk.threads_leave()
        return weibo_hbox

    def show_tooltip(self, widget, event, text):
        '''Create help tooltip.'''
        Tooltip.text(widget, text)

    def init_user_info_thread(self, button, text_view):
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
        self.loading_label.destroy()
        gtk.gdk.threads_leave()

    # init share box, create share button, input
    def init_share_box(self):
        '''get weibo info, and create button'''
        self.to_share_weibo = {}
        self.to_share_weibo_res = {}
        self.deepin_info = {}
        self.is_get_user_info = {}
        self.__weibo_check_button_list = []
        self.__weibo_image_button_list = []

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
        text_box = gtk.HBox(False, 2)
        text_vbox = gtk.VBox(False, 2)
        text_bg_vbox = gtk.VBox(False)
        text_bg_align = gtk.Alignment()
        text_bg_align.set(0.5, 0.5, 0, 0)
        text_bg_align.set_padding(5, 5, 16, 5)
        text_bg_align.connect("expose-event", self.text_view_bg_expose)
        text_scrolled_win = gtk.ScrolledWindow()
        text_scrolled_win.set_policy(gtk.POLICY_NEVER, gtk.POLICY_NEVER)
        #text_scrolled_win = ScrolledWindow()
        text_scrolled_win.set_size_request(340, 157)

        text_view = gtk.TextView()
        text_view.set_left_margin(10)
        text_view.set_right_margin(10)
        text_view.set_pixels_above_lines(5)
        text_view.set_pixels_below_lines(5)
        text_view.set_wrap_mode(gtk.WRAP_WORD| gtk.WRAP_CHAR)
        text_view.connect("expose-event", self.text_view_expose)
        buf = text_view.get_buffer()
        text_scrolled_win.add(text_view)
        text_bg_vbox.pack_start(text_scrolled_win)
        text_bg_align.add(text_bg_vbox)

        text_align = gtk.Alignment()
        text_align.set(0.5, 0.5, 0, 0)
        text_align.set_padding(25, 30, 10, 10)

        text_box.pack_start(thumb, False, False, 10)
        text_box.pack_start(text_bg_align)
        text_vbox.pack_start(text_box, False, False, 10)

        text_align.add(text_vbox)
        #tmp_align = gtk.Alignment()
        #tmp_align.set(0.5, 0, 0, 1)
        #self.share_box.pack_start(tmp_align, False, False)
        self.share_box.pack_start(text_align, False, False)

        # dialog button box
        left_box = self.window.left_button_box
        right_box = self.window.right_button_box

        # input tip label
        self.input_num_label = Label("%d" % self.MAX_CHAR,
            text_size=16, text_x_align=pango.ALIGN_CENTER, label_width=50, enable_select=False)
        self.input_num_label.text_color = app_theme.get_color("left_char_num")

        # login box
        #weibo_box = gtk.HBox(False, 1)
        #weibo_box.set_size_request(-1, 50)
        weibo_box_list = []
        self.loading_label = Label("%s..." % _("Loading"), text_size=12,
            label_width=70, enable_select=False)
        weibo_box_list.append(self.loading_label)

        for weibo in self.__weibo_list:
            box = gtk.HBox(False, 2)
            weibo.set_box(box)
            weibo_box_list.append(box)
        left_box.set_buttons(weibo_box_list)

        # share button
        button = Button(_("Share"))
        #button.set_size_request(75, 25)
        button.connect("clicked", self.share_button_clicked, text_view)
        buf.connect("changed", self.text_view_changed, button)  # check char num

        tmp_vbox = gtk.VBox(False)
        tmp_align = gtk.Alignment()
        tmp_align.set(0.5, 0.5, 0, 0)
        tmp_vbox.pack_start(button, False, False)
        #tmp_vbox.pack_start(tmp_align)
        tmp_align.add(tmp_vbox)
        right_box.set_buttons([self.input_num_label, tmp_align])

        # at first, set widget insensitive
        button.set_sensitive(False)
        text_view.set_editable(False)
        t = threading.Thread(target=self.init_user_info_thread, args=(button, text_view))
        t.setDaemon(True)
        t.start()

    # draw text view background
    def text_view_bg_expose(self, widget, event):
        '''draw text view bg'''
        cr = widget.window.cairo_create()
        rect = widget.allocation
        text_pixbuf = app_theme_get_dynamic_pixbuf('image/share/text_view.png').get_pixbuf()
        draw.draw_pixbuf(cr, text_pixbuf, rect.x, rect.y)

    # if text is empty, show tip info
    def text_view_expose(self, text_view, event):
        '''text_view expose'''
        buf = text_view.get_buffer()
        text = buf.get_text(*buf.get_bounds())

        if text == "" and text_view.get_editable() and not text_view.is_focus():
            win = text_view.get_window(gtk.TEXT_WINDOW_TEXT)
            cr = win.cairo_create()
            cr.move_to(10, 5)
            context = pangocairo.CairoContext(cr)
            layout = context.create_layout()
            layout.set_font_description(pango.FontDescription("Snas 10"))
            layout.set_alignment(pango.ALIGN_LEFT)
            layout.set_text(_("Please input text here"))
            cr.set_source_rgb(0.66, 0.66, 0.66)
            context.update_layout(layout)
            context.show_layout(layout)

    # show input char num
    def text_view_changed(self, buf, button):
        '''text_view changed callback'''
        count = buf.get_char_count()
        if count <= self.MAX_CHAR:
            #self.input_tip_label.set_text(_("left"))
            self.input_num_label.set_text("%d" % (self.MAX_CHAR - count))
            self.input_num_label.text_color = app_theme.get_color("left_char_num")
            if not button.is_sensitive():
                button.set_sensitive(True)
        else:
            #self.input_tip_label.set_text(_("exceeds"))
            self.input_num_label.set_text("-%d" % (count - self.MAX_CHAR))
            self.input_num_label.text_color = app_theme.get_color("left_char_num1")
            if button.is_sensitive():
                button.set_sensitive(False)

    def share_button_clicked(self, button, text_view):
        '''share_button_clicked callback'''
        # file is not exist.
        if not exists(self.upload_image):
            d = ConfirmDialog(_("Error"), "%s." % ( _("Picture does not exist.")))
            d.show_all()
            d.set_transient_for(self.window)
            return False
        has_share_web = False
        for weibo in self.to_share_weibo:
            if self.to_share_weibo[weibo]:
                has_share_web = True
                break
        # have no web selected
        if not has_share_web:
            d = ConfirmDialog(_("Error"), _("Please choose at least one platform to share on"))
            d.show_all()
            d.set_transient_for(self.window)
            return False
        # at first, set widget insensitive
        button.set_sensitive(False)
        text_view.set_editable(False)
        #self.window.left_button_box.set_sensitive(False)
        # set weibo checkbutton sensitive
        for check in self.__weibo_check_button_list:
            check.set_sensitive(False)
        # disconnect weibo ico button clicked function
        for img in self.__weibo_image_button_list:
            try:
                img.disconnect_by_func(self.weibo_login)
            except:
                pass
        button.set_label(_("Uploading"))
        t = threading.Thread(target=self.share_to_weibo_thread, args=(text_view, ))
        t.setDaemon(True)
        t.start()

    # upload image thread
    def share_to_weibo_thread(self, text_view):
        '''share in thread'''
        buf = text_view.get_buffer()
        text = buf.get_text(*buf.get_bounds())
        if text.strip() == "":
            text = _("from Deepin Screenshot")
        # get deepin official info
        self.deepin_info[self.sina] = self.sina.get_deepin_info()
        self.deepin_info[self.qq] = self.qq.get_deepin_info()
        if default_locale != 'zh_CN':
            self.deepin_info[self.twitter] = self.twitter.get_deepin_info()
        # upload
        for weibo in self.to_share_weibo:
            if self.to_share_weibo[weibo]:
                self.to_share_weibo_res[weibo] = weibo.upload_image(self.upload_image, text)
        self.share_to_weibo_result()

    # show upload result
    @post_gui
    def share_to_weibo_result(self):
        '''result of share to weibo'''
        font_color = app_theme.get_color("share_result_text")
        res_hbox = gtk.HBox(False)
        res_hbox.set_size_request(-1, 240)

        res_left_box = DialogLeftButtonBox()
        res_right_box = DialogRightButtonBox()

        res_left_box.button_align.set(0.5, 0.0, 0, 1)
        res_right_box.button_align.set(0.5, 0.0, 0, 1)
        res_left_box.button_align.set_padding(5, 9, 19, 0)
        res_right_box.button_align.set_padding(30, 0, 0, 0)

        res_left_box.set_size_request(405, -1)
        res_right_box.set_size_request(195, -1)

        res_hbox.pack_start(res_left_box)
        res_hbox.pack_start(
            VSeparator(app_theme.get_shadow_color("VSeparator").get_color_info(), 0, 0))
        res_hbox.pack_start(res_right_box)

        res_vbox = gtk.VBox(False)
        follow_vbox = gtk.VBox(False)

        tmp_img = gtk.Image()       # only use as a placeholder
        tmp_img.set_size_request(-1, 50)
        res_vbox.pack_start(tmp_img, False, False)

        follow_tip_hbox = gtk.HBox(False)
        img = gtk.image_new_from_file(app_theme.get_theme_file_path("image/share/deepin_logo.png"))
        follow_tip_hbox.pack_start(img, False, False, 5)
        follow_tip_hbox.pack_start(
            Label("%s %s" % (_("Follow"), "Linux Deepin"),
                text_color=app_theme_get_dynamic_color("#5f5f5f"),
                text_size=12, enable_select=False), False, False)
        follow_vbox.pack_start(follow_tip_hbox, False, False, 13)
        for weibo in self.to_share_weibo_res:
            vbox = gtk.VBox(False, 1)
            tip_box = gtk.HBox()
            error_box = gtk.HBox()
            vbox.pack_start(tip_box, False, False)
            vbox.pack_start(error_box, False, False)
            if self.to_share_weibo_res[weibo][0]:   # upload succeed
                img = gtk.image_new_from_file(app_theme.get_theme_file_path("image/share/share_succeed.png"))
                #link = LinkButton(_(weibo.t_type), text_size=13, self.to_share_weibo_res[weibo][1])
                link = Label(_(weibo.t_type), text_size=12,
                    text_color=app_theme.get_color("link_text"))
                #, enable_gaussian=True, gaussian_radious=1, border_radious=0)
                link.add_events(gtk.gdk.BUTTON_PRESS_MASK)
                link.connect("enter-notify-event", lambda w, e: self.__draw_under_line(w))
                link.connect("leave-notify-event", lambda w, e: w.queue_draw())
                link.connect("button-press-event", self.goto_weibo_button_clicked, weibo)
                link_box = gtk.HBox(False)
                link_box.pack_start(link, False, False)
                utils.set_clickable_cursor(link)
                text = _("Share to")
                label = Label(text, text_size=12,
                    text_color=font_color, enable_select=False)
                text = _("Successful")
                label1 = Label(text, text_size=12,
                    text_color=font_color, enable_select=False)
                tip_box.pack_start(img, False, False, 15)
                tip_box.pack_start(label, False, False, 3)
                tip_box.pack_start(link_box, False, False, 3)
                tip_box.pack_start(label1, False, False)
                # only use as a placeholder
                img = gtk.Image()
                img.set_size_request(20, 1)
                error_box.pack_start(img, False, False, 16)
                tmp = Label(" ", text_size=9, label_width=200)
                tmp.set_size_request(200, 1)
                error_box.pack_start(tmp, False, False)
                #print text
            else:   # upload failed
                img = gtk.image_new_from_file(app_theme.get_theme_file_path("image/share/share_failed.png"))
                #text = "% %s %s." % (_(weibo.t_type), _("upload failed"))
                text = _("Share to")
                label1 = Label(text, text_size=12,
                    text_color=font_color, enable_select=False)
                label2 = Label(_(weibo.t_type), text_size=12,
                    text_color=font_color, enable_select=False)
                text = _("Failed")
                label3 = Label(text, text_size=12,
                    text_color=font_color, enable_select=False)
                if weibo.curl.error:
                    error = "(%s)" % _(weibo.curl.error)
                elif weibo.get_error_msg():
                    error = "(%s)" % _(weibo.get_error_msg())
                else:
                    error = "(%s)" % _("Unknown reason")
                #print "%s: %s" % (weibo.t_type, error)
                #print "%s: %s" % (weibo.t_type, weibo.get_error_msg())
                label = Label(text, text_size=12,
                    text_color=font_color, enable_select=False)
                tip_box.pack_start(img, False, False, 15)
                tip_box.pack_start(label1, False, False, 3)
                tip_box.pack_start(label2, False, False, 3)
                tip_box.pack_start(label3, False, False)
                img = gtk.Image()   # only use as a placeholder
                img.set_size_request(20, 20)
                error_box.pack_start(img, False, False, 16)
                error_box.pack_start(Label(error, text_size=9, label_width=200,
                    text_color=font_color, enable_select=False), False, False)
                #print text
            res_vbox.pack_start(vbox, False, False, 10)

        for weibo in self.deepin_info:
            box = gtk.HBox(False, 15)
            # followed
            img = gtk.image_new_from_pixbuf(app_theme.get_pixbuf("share/"+weibo.t_type+".png").get_pixbuf())
            box.pack_start(img, False, False)
            if self.deepin_info[weibo] is not None and self.deepin_info[weibo][3]:
                if not default_locale.startswith("zh_"):
                    button = gtk.image_new_from_pixbuf(
                        app_theme.get_pixbuf("share/followed_en.png").get_pixbuf())
                else:
                    button = gtk.image_new_from_pixbuf(
                        app_theme.get_pixbuf("share/followed.png").get_pixbuf())
            else:   # to follow
                if not default_locale.startswith("zh_"):
                    button = ImageButton(
                        app_theme.get_pixbuf("share/follow_normal_en.png"),
                        app_theme.get_pixbuf("share/follow_hover_en.png"),
                        app_theme.get_pixbuf("share/follow_press_en.png"))
                else:
                    button = ImageButton(
                        app_theme.get_pixbuf("share/follow_normal.png"),
                        app_theme.get_pixbuf("share/follow_hover.png"),
                        app_theme.get_pixbuf("share/follow_press.png"))
                button.connect("clicked", self.friendships_add_button_clicked, weibo, box)
            box.pack_start(button, False, False)
            align = gtk.Alignment()
            align.set(0.0, 0.5, 0, 0)
            align.set_padding(0, 0, 30, 0)
            align.add(box)
            follow_vbox.pack_start(align, False, False, 8)

        res_left_box.set_buttons([res_vbox])
        res_right_box.set_buttons([follow_vbox])

        self.result_box.pack_start(res_hbox, False, False)
        self.result_box.show_all()
        self.set_slide_index(2)

    def goto_weibo_button_clicked(self, widget, event, weibo):
        '''goto my weibo'''
        #print "goto weibo button clicked", weibo.t_type, "xdg-open %s" % self.to_share_weibo_res[weibo][1]
        if weibo in self.to_share_weibo_res:
            if self.to_share_weibo_res[weibo][1]:
                utils.run_command("xdg-open %s" % self.to_share_weibo_res[weibo][1])

    def friendships_add_button_clicked(self, widget, weibo, box):
        '''add friendships'''
        #self.result_box.set_sensitive(False)
        if not self.is_get_user_info[weibo]:
            utils.run_command("xdg-open %s" % weibo.index_url)
            return True

        widget.set_sensitive(False)
        t = threading.Thread(target=self.friendships_add_thread, args=(widget, weibo, box))
        t.setDaemon(True)
        t.start()

    def friendships_add_thread(self, button, weibo, box):
        '''add friendships'''
        if weibo.friendships_create() is not None:
            gtk.gdk.threads_enter()
            button.destroy()
            if not default_locale.startswith("zh_"):
                button = gtk.image_new_from_pixbuf(
                    app_theme.get_pixbuf("share/followed_en.png").get_pixbuf())
            else:
                button = gtk.image_new_from_pixbuf(
                    app_theme.get_pixbuf("share/followed.png").get_pixbuf())
            button.show()
            box.pack_start(button, False, False)
            #button.set_label("已关注")
            gtk.gdk.threads_leave()

    # show window
    def show(self):
        '''show'''
        self.window.show_window()

    # close widnow
    def quit(self, widget):
        ''' close '''
        gtk.main_quit()

    def __slider_expose(self, widget, event):
        ''' slider expose redraw'''
        cr = widget.window.cairo_create()
        rect = widget.allocation
        cr.set_source_rgba(1.0, 1.0, 1.0, 0.8)
        cr.rectangle(rect.x, rect.y, rect.width, rect.height)
        cr.fill()

    def __expose_top_and_bottome(self, widget, event):
        '''titlebar or button_box expose'''
        cr = widget.window.cairo_create()
        rect = widget.allocation
        cr.set_source_rgb(0.89, 0.89, 0.89)
        cr.rectangle(rect.x+2, rect.y+2, rect.width-4, rect.height-4)
        cr.fill()

    def __draw_under_line(self, widget):
        '''draw under line'''
        cr = widget.window.cairo_create()
        with utils.cairo_disable_antialias(cr):
            x, y, w, h = widget.allocation
            # #1A70b1
            cr.set_source_rgba(0.1, 0.43, 0.69, 1.0)
            cr.set_line_width(1)
            cr.move_to(x, y+h-3)
            cr.line_to(x+w, y+h-3)
            cr.stroke()


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
