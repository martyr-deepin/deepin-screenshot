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

import config
import urlparse
import pycurl
import StringIO
import urllib
import json
import time
import hashlib
import hmac
import subprocess

CONFIG = config.WeiboConfig()

class OAuth(object):
    '''Weibo OAuth config'''
    def __init__(self, t_type=''):
        self.config = CONFIG
        self.t_type = t_type

    def get(self, opt=None):
        '''get info'''
        return self.config.get(self.t_type, opt)

    def set(self, **kw):
        '''set info'''
        self.config.set(self.t_type, **kw)

    def __getattr__(self, kw):
        ''' __getattr__'''
        return self.get(kw)

class Curl(object):
    '''Curl Class'''
    def twitter_get(self, url, header=None, proxy_host=None, proxy_port=None):
        '''open url with get method for twitter'''
        self.error = None
        crl = pycurl.Curl()
        #crl.setopt(pycurl.VERBOSE,1)
        # this will tell libcurl not to use any signal related code that causes in a multithreaded python script this kind of error.
        crl.setopt(pycurl.NOSIGNAL, 1)

        # set proxy
        if proxy_host:
            crl.setopt(pycurl.PROXY, proxy_host)
        if proxy_port:
            crl.setopt(pycurl.PROXYPORT, proxy_port)
        # set ssl
        crl.setopt(pycurl.SSL_VERIFYPEER, 0)
        crl.setopt(pycurl.SSL_VERIFYHOST, 0)
        crl.setopt(pycurl.SSLVERSION, 3)

        crl.setopt(pycurl.CONNECTTIMEOUT, 10)
        crl.setopt(pycurl.TIMEOUT, 300)
        crl.setopt(pycurl.HTTPPROXYTUNNEL,1)

        if header:
            crl.setopt(pycurl.HTTPHEADER, header)

        crl.fp = StringIO.StringIO()

        if isinstance(url, unicode):
            url = str(url)
        crl.setopt(pycurl.URL, url)
        crl.setopt(crl.WRITEFUNCTION, crl.fp.write)
        try:
            crl.perform()
        except Exception, e:
            self.error = "Connection timed out."
            return None
        crl.close()
        con = crl.fp.getvalue()
        crl.fp.close()
        return con

    def get(self, url, header=None, proxy_host=None, proxy_port=None):
        '''
        open url width get method
        @param url: the url to visit
        @param header: the http header
        @param proxy_host: the proxy host name
        @param proxy_port: the proxy port
        '''
        self.error = None
        crl = pycurl.Curl()
        #crl.setopt(pycurl.VERBOSE,1)
        crl.setopt(pycurl.NOSIGNAL, 1)

        # set proxy
        if proxy_host:
            crl.setopt(pycurl.PROXY, proxy_host)
        if proxy_port:
            crl.setopt(pycurl.PROXYPORT, proxy_port)
        # set ssl
        crl.setopt(pycurl.SSL_VERIFYPEER, 0)
        crl.setopt(pycurl.SSL_VERIFYHOST, 0)
        crl.setopt(pycurl.SSLVERSION, 3)

        crl.setopt(pycurl.CONNECTTIMEOUT, 10)
        crl.setopt(pycurl.TIMEOUT, 300)
        crl.setopt(pycurl.HTTPPROXYTUNNEL,1)

        if header:
            crl.setopt(pycurl.HTTPHEADER, header)

        crl.fp = StringIO.StringIO()

        if isinstance(url, unicode):
            url = str(url)
        crl.setopt(pycurl.URL, url)
        crl.setopt(crl.WRITEFUNCTION, crl.fp.write)
        try:
            crl.perform()
        except Exception, e:
            self.error = "Connection timed out."
            return None
        crl.close()
        #conn = crl.fp.getvalue()
        #print conn
        try:
            back = json.loads(crl.fp.getvalue())
            #back = json.loads(conn)
            crl.fp.close()
            return back
        except:
            return None

    def post(self, url, data, header=None, proxy_host=None, proxy_port=None):
        '''
        open url width post method
        @param url: the url to visit
        @param data: the data to post
        @param header: the http header
        @param proxy_host: the proxy host name
        @param proxy_port: the proxy port
        '''
        self.error = None
        crl = pycurl.Curl()
        #crl.setopt(pycurl.VERBOSE,1)
        crl.setopt(pycurl.NOSIGNAL, 1)

        # set proxy
        if proxy_host:
            crl.setopt(pycurl.PROXY, proxy_host)
        if proxy_port:
            crl.setopt(pycurl.PROXYPORT, proxy_port)
        # set ssl
        crl.setopt(pycurl.SSL_VERIFYPEER, 0)
        crl.setopt(pycurl.SSL_VERIFYHOST, 0)
        crl.setopt(pycurl.SSLVERSION, 3)

        crl.setopt(pycurl.CONNECTTIMEOUT, 10)
        crl.setopt(pycurl.TIMEOUT, 300)
        crl.setopt(pycurl.HTTPPROXYTUNNEL,1)

        if header:
            crl.setopt(pycurl.HTTPHEADER, header)

        crl.fp = StringIO.StringIO()

        crl.setopt(crl.POSTFIELDS, urllib.urlencode(data))  # post data
        #crl.setopt(crl.POSTFIELDS, data)
        if isinstance(url, unicode):
            url = str(url)
        crl.setopt(pycurl.URL, url)
        crl.setopt(crl.WRITEFUNCTION, crl.fp.write)
        try:
            crl.perform()
        except Exception, e:
            self.error = "Connection timed out."
            return None
        crl.close()
        #conn = crl.fp.getvalue()
        #print conn
        try:
            back = json.loads(crl.fp.getvalue())
            #back = json.loads(conn)
            crl.fp.close()
            return back
        except:
            return None

    def upload(self, url, data, header=None, proxy_host=None, proxy_port=None):
        '''
        open url with upload
        @param url: the url to visit
        @param data: the data to upload
        @param header: the http header
        @param proxy_host: the proxy host name
        @param proxy_port: the proxy port
        '''
        self.error = None
        #print "upload:", url, data, header
        crl = pycurl.Curl()
        #crl.setopt(pycurl.VERBOSE,1)
        crl.setopt(pycurl.NOSIGNAL, 1)

        # set proxy
        if proxy_host:
            crl.setopt(pycurl.PROXY, proxy_host)
        if proxy_port:
            crl.setopt(pycurl.PROXYPORT, proxy_port)
        # set ssl
        crl.setopt(pycurl.SSL_VERIFYPEER, 0)
        crl.setopt(pycurl.SSL_VERIFYHOST, 0)
        crl.setopt(pycurl.SSLVERSION, 3)

        crl.setopt(pycurl.CONNECTTIMEOUT, 10)
        crl.setopt(pycurl.TIMEOUT, 300)
        crl.setopt(pycurl.HTTPPROXYTUNNEL,1)

        if header:
            crl.setopt(pycurl.HTTPHEADER, header)

        crl.fp = StringIO.StringIO()

        if isinstance(url, unicode):
            url = str(url)
        crl.setopt(pycurl.URL, url)
        crl.setopt(pycurl.HTTPPOST, data)   # upload file
        crl.setopt(crl.WRITEFUNCTION, crl.fp.write)
        try:
            crl.perform()
        except Exception, e:
            self.error = "An error occured in network connection."
            return None
        crl.close()
        #conn = crl.fp.getvalue()
        #print conn
        try:
            back = json.loads(crl.fp.getvalue())
            #back = json.loads(conn)
            crl.fp.close()
            return back
        except:
            return None

class Weibo(object):
    '''Weibo base class, it must be inherited and refactored'''
    def __init__(self, t_type, webkit):
        '''
        init weibo
        @param t_type: the weibo type, a string text
        @param webkit: a webkit.WebView
        '''
        self.webkit = webkit
        self.t_type = t_type
        self.oauth = OAuth(t_type)
        self.curl = Curl()
        self.curl.error = None
        self.error_code = None
        self.error_msg = ""

    def set_box(self, box):
        '''set a gtk.Box'''
        self.box = box

    def get_box(self):
        '''get a gtk.Box'''
        return self.box

    def get(self, opt=None):
        '''get config value'''
        return self.oauth.get(opt)

    def set(self, **kw):
        '''set config value'''
        self.oauth.set(**kw)

    def get_curl_error(self):
        '''
        get curl error msg
        @return: string text or None
        '''
        return self.curl.error

    def get_error_msg(self):
        '''
        get error message
        @return: a string text
        '''
        if self.error_code in self.errors:
            return self.errors[self.error_code]
        return self.error_msg

    # use webkit open authorize page
    def request_oauth(self):
        '''request oauth access token'''
        self.webkit.load_uri(self.ACCESS_URL)

    def get_access_url(self):
        '''
        get access url
        @return: a url string text
        '''
        return self.ACCESS_URL

    def parse_url(self, uri=''):
        '''
        parse url
        @param uri: a url string text
        @return: a tuple containing the url hostname and parse_qs if parse succedd, otherwise None
        '''
        if not uri:
            return None
        url = urlparse.urlparse(uri)
        if url.fragment:
            query = urlparse.parse_qs(url.fragment, True)
        else:
            query = urlparse.parse_qs(url.query, True)
        return (url.hostname, query)

    def is_callback_url(self, url):
        '''
        check is in callback url now
        @param url: the webkit url now, a string text
        @return: True if the url is in callback, otherwise False
        '''
        if url:
            return url.startswith(self.CALLBACK_URL)
        return False

    # upload image
    def upload(self, upload_data):
        '''
        upload image
        @param upload_data: the data that will post to server
        @return: some info from server
        '''
        return self.curl.upload(self.UPLOAD_URL, upload_data)

class Sina(Weibo):
    '''Sina Weibo'''
    def __init__(self, webkit):
        Weibo.__init__(self, 'Sina', webkit)
        self.APP_KEY = '3703706716'
        self.APP_SECRET = 'c0ecbf8644ac043070449ad0901692b8'
        self.CALLBACK_URL = 'http://www.linuxdeepin.com'
        self.DEEPIN_ID = 2675284423
        self.index_url = 'http://www.weibo.com'

        version = 2
        #self.ACCESS_URL = 'https://api.weibo.com/oauth2/authorize?client_id=%s&redirect_uri=%s&display=mobile' % (self.APP_KEY,self.CALLBACK_URL)
        self.ACCESS_URL = 'https://api.weibo.com/oauth2/authorize?client_id=%s&redirect_uri=%s&display=popup&forcelogin=true' % (self.APP_KEY,self.CALLBACK_URL)
        self.OAUTH2_URL = 'https://api.weibo.com/oauth2/access_token'
        self.USERS_URL = 'https://api.weibo.com/%d/%s' % (version, 'users/show.json')
        self.USER_ID_URL = 'https://api.weibo.com/%d/%s' % (version, 'account/get_uid.json')
        self.UPLOAD_URL = 'https://upload.api.weibo.com/%d/%s' % (version, 'statuses/upload.json')
        self.FRIEND_URL = 'https://api.weibo.com/%d/%s' % (version, 'friendships/create.json')
        self.code = None
        self.__user_id = ""
        self.errors = {
            # system error code
            '10001': 'System error',                                # 系统错误
            '10002': 'Service unavailable',                         # 服务暂停
            '10003': 'Remote service error',                        # 远程服务错误
            '10004': 'IP limit',                                    # IP限制不能请求该资源
            '10007': 'Unsupport mediatype',                         # 不支持的MediaType
            '10009': 'Too many pending tasks, system is busy',      # 任务过多，系统繁忙
            '10010': 'The job has expired',                         # 任务超时
            '10011': 'RPC error',                                   # RPC错误
            '10012': 'Illegal request',                             # 非法请求
            '10013': 'Invalid Weibo user account',                  # 不合法的微博用户
            '10016': 'miss required parameter',                     # 缺失必选参数
            '10018': 'Request body length over limit',              # 请求长度超过限制
            '10022': 'IP requests out of rate limit',               # IP请求频次超过上限
            '10023': 'User requests out of rate limit',             # 用户请求频次超过上限
            # service error code
            '20003': 'User name does not exist',                    # 用户不存在
            '20005': 'Unsupported image type. Currently we only suport JPG, GIF and PNG formats',  # 不支持的图片类型，仅仅支持JPG、GIF、PNG
            '20006': 'Image size too large',                        # 图片太大
            '20008': 'Content is null',                             # 内容为空
            '20012': 'Text too long, please input text less than 140 characters',  # 输入文字太长，请确认不超过140个字符
            '20013': 'Text too long, please input text less than 300 characters',  # 输入文字太长，请确认不超过300个字符
            '20015': 'Account or ip or app is illgal, can not continue',           # 账号、IP或应用非法，暂时无法完成此操作
            '20016': 'Out of limit',                                # 发布内容过于频繁
            '20017': 'Repeat content',                              # 提交相似的信息
            '20018': 'Contain illegal website',                     # 包含非法网址
            '20019': 'Repeat content',                              # 提交相同的信息
            '20020': 'Contain advertising',                         # 包含广告信息
            '20021': 'Content is illegal',                          # 包含非法内容
            '20022': "Your ip's behave in a comic boisterous or unruly manner",    # 此IP地址上的行为异常
            '20032': 'Update success, while server slow now, please wait 1-2 minutes',  # 发布成功，目前服务器可能会有延迟，请耐心等待1-2分钟
            '20104': 'Illegal weibo',                               # 不合法的微博
            '20111': 'Repeated weibo text',                         # 不能发布相同的微博
            '21602': 'Contains forbid world',                       # 含有敏感词
            }

    # first get code, then use this code to access token
    def get_code(self):
        '''get oauth code'''
        self.code = None
        uri = self.webkit.get_property('uri')
        if uri is None:
            return False
            return None
        parse = self.parse_url(uri)
        if parse is None:
            self.code = None
        if 'code' in parse[1]:
            self.code = parse[1]['code'][0]
        else:
            self.code = None
        return self.code

    # second access token
    def access_token(self):
        '''
        access token
        @return: True if access token succeed, otherwise False
        '''
        if self.get_code() is None:
            return False
        url = '%s?client_id=%s&client_secret=%s&grant_type=authorization_code&code=%s&redirect_uri=%s' % (
            self.OAUTH2_URL, self.APP_KEY, self.APP_SECRET, self.code, self.CALLBACK_URL)
        back = self.curl.post(url, [])
        if back is None:
            return False
        if 'access_token' in back:
            if isinstance(back['access_token'], unicode):
                access_token = str(back['access_token'])
            else:
                access_token = back['access_token']
            self.oauth.set(access_token=access_token, expires_in=back['expires_in']+int(time.time()))
            return True
        else:
            return False

    # get user id
    def get_user_id(self):
        '''
        get user id
        @return: a dict containing user id if get succeed, otherwise None
        '''
        access_token = self.oauth.get('access_token')
        if access_token is None:
            return None
        url = '%s?access_token=%s' % (self.USER_ID_URL, access_token)
        back = self.curl.get(url)
        #print "uid:", back
        if back is None:
            return None
        if 'error_code' in back:
            return None
        self.__user_id = str(back['uid'])
        return back

    # get user name
    def get_user_name(self):
        '''
        get user name
        @return: user name if get succeed, otherwise None
        '''
        back = self.get_user_id()
        access_token = self.oauth.get('access_token')
        if access_token is None:
            return None
        if back is None:
            return None
        url = '%s?access_token=%s&uid=%d' % (self.USERS_URL, access_token, back['uid'])
        back = self.curl.get(url)
        #print "user:", back
        if back is None:
            return None
        if 'error_code' in back:
            return None
        return back['name']

    def get_deepin_info(self):
        '''get deepin sina weibo info'''
        access_token = self.oauth.get('access_token')
        if access_token is None:
            return None
        url = '%s?access_token=%s&uid=%d' % (self.USERS_URL, access_token, self.DEEPIN_ID)
        back = self.curl.get(url)
        #print "user:", back
        if back is None:
            return None
        if 'error_code' in back:
            return None
        return (back['name'], back['location'], back['description'], back['following'])

    def friendships_create(self):
        '''add deepin to friend'''
        access_token = self.oauth.get('access_token')
        if access_token is None:
            return None
        url = self.FRIEND_URL
        data = [
            ('access_token', access_token),
            ('uid', self.DEEPIN_ID)]
        back = self.curl.post(url, data)
        #print "user:", back
        if back is None:
            return None
        if 'error_code' in back:
            return None
        return back

    def upload_image(self, img, mesg='', annotations=None):
        '''upload image'''
        access_token = self.oauth.get('access_token')
        if access_token is None:
            return (False, None)
        data = [
            ('access_token', access_token),
            ('pic', (pycurl.FORM_FILE, img)),
            ('status', mesg)]
        if annotations:
            data.append(('annotations', annotations))
        back = self.upload(data)
        if back is None:
            return (False, None)
        if 'error_code' in back:
            self.error_code = str(back["error_code"])
            self.error_msg = back["error"]
            return (False, None)
        url = "http://api.weibo.com/2/statuses/go?access_token=%s&uid=%s&id=%s" % (
                access_token, self.__user_id, back["idstr"])
        return (True, url)

class Tencent(Weibo):
    '''Tencent Weibo'''
    def __init__(self, webkit):
        Weibo.__init__(self, 'Tencent', webkit)
        self.APP_KEY = '801236993'
        self.APP_SECRET = '39083ce577596d739bbabb6f6bd0dba0'
        self.CALLBACK_URL = 'http://www.linuxdeepin.com'
        #self.DEEPIN_ID = "A1311E21F862EE280851CB4244E05120"
        self.DEEPIN_ID = "linux_deepin"
        self.index_url = 'http://t.qq.com'

        self.oauth_version = '2.a'
        self.client_ip = '127.0.0.1'    # TODO clientip
        self.ACCESS_URL = 'https://open.t.qq.com/cgi-bin/oauth2/authorize?client_id=%s&response_type=token&redirect_uri=%s&wap=2' % (self.APP_KEY,self.CALLBACK_URL)
        #self.ACCESS_URL = 'https://open.t.qq.com/cgi-bin/oauth2/authorize?client_id=%s&response_type=token&redirect_uri=%s' % (self.APP_KEY,self.CALLBACK_URL)
        self.USERS_URL = 'https://open.t.qq.com/api/user/info'
        self.UPLOAD_URL = 'https://open.t.qq.com/api/t/add_pic'
        self.OTHER_URL = 'https://open.t.qq.com/api/user/other_info'
        self.FRIEND_URL = 'http://open.t.qq.com/api/friends/add'

        self.errors = {
            #'11'   : 'error clientip',             # clientip错误，必须为用户侧真实ip
            '12'   : 'error content len',          # 微博内容超出长度限制或为空
            '19'   : 'error pic size',            # 图片大小超出限制或为0
            '110'  : 'pic format error',           # 图片格式错误
            '43'   : 'post format error',          # 格式错误、用户无效（非微博用户）
            '44'   : 'forbidden content',          # 有过多脏话
            '45'   : 'forbidden access',           # 禁止访问，如城市，uin黑名单限制等
            '49'   : 'post invliad content',       # 包含垃圾信息：广告，恶意链接、黑名单号码等
            '410'  : 'post content too fast',      # 发表太快，被频率限制
            '412'  : 'content is verifying',      # 源消息审核中
            '413'  : 'post content repeated',      # 重复发表，请不要连续发表重复内容
            '414'  : 'not verify real name',       # 用户未进行实名认证
            '416'  : 'add fail',                   # 服务器内部错误导致发表失败
            '467'  : 'post content repeated',      # 重复发表，请不要连续发表重复内容
            '470'  : 'pic upload error',           # 上传图片失败
            '41001': 'common uin blacklist limit', # 公共uin黑名单限制
            '41002': 'common ip blacklist limit',  # 公共IP黑名单限制
            '41003': 'weibo blacklist limit',      # 微博黑名单限制
            '41004': 'access too fast',            # 单UIN访问微博过快
            '41472': 'add fail'}                  # 服务器内部错误导致发表失败

    def access_token(self):
        '''
        access token
        @return: True if access token succeed, otherwise False
        '''
        url = self.webkit.get_property('uri')
        if url is None:
            return False
        if not url.startswith(self.CALLBACK_URL):
            return False
        back = self.parse_url(url)
        parse = back[1]
        if 'access_token' in parse:
            if isinstance(parse['access_token'][0], unicode):
                access_token = str(parse['access_token'][0])
            else:
                access_token = parse['access_token'][0]
            if isinstance(parse['openid'][0], unicode):
                openid = str(parse['openid'][0])
            else:
                openid = parse['openid'][0]
            if isinstance(parse['openkey'][0], unicode):
                openkey= str(parse['openkey'][0])
            else:
                openkey= parse['openkey'][0]
            self.oauth.set(access_token=access_token,
                expires_in=int(parse['expires_in'][0])+int(time.time()),
                openid=openid, openkey=openkey)
            return True
        return False

    def get_user_name(self):
        '''get user info'''
        access_token = self.oauth.get("access_token")
        openid = self.oauth.get("openid")
        if access_token is None or openid is None:
            return None
        url = '%s?format=json&oauth_consumer_key=%s&access_token=%s&openid=%s&clientip=%s&oauth_version=2.a&scope=all' \
            % (self.USERS_URL, self.APP_KEY, access_token, openid, self.client_ip)
        back = self.curl.get(url)
        #print "user:", back
        if back is None:
            return None
        if back['errcode'] != 0:
            return None
        return back['data']['nick']

    def get_deepin_info(self):
        ''' get deepin tencent weibo info'''
        access_token = self.oauth.get("access_token")
        openid = self.oauth.get("openid")
        if access_token is None or openid is None:
            return None
        #url = '%s?format=json&oauth_consumer_key=%s&access_token=%s&openid=%s&clientip=%s&oauth_version=2.a&scope=all&fopenid=%s' \
            #% (self.OTHER_URL, self.APP_KEY, access_token, openid, self.client_ip, self.DEEPIN_ID)
        url = '%s?format=json&oauth_consumer_key=%s&access_token=%s&openid=%s&clientip=%s&oauth_version=2.a&scope=all&name=%s' \
            % (self.OTHER_URL, self.APP_KEY, access_token, openid, self.client_ip, self.DEEPIN_ID)
        back = self.curl.get(url)
        #print "user:", back
        if back is None:
            return None
        if back['errcode'] != 0:
            return None
        return (back['data']['nick'], back['data']['location'], \
                back['data']['introduction'], back['data']['ismyidol'])

    def friendships_create(self):
        '''add deepin to friend'''
        access_token = self.oauth.get("access_token")
        openid = self.oauth.get("openid")
        if access_token is None or openid is None:
            return None
        url = self.FRIEND_URL
        data = [
            ('format', 'json'),
            ('oauth_consumer_key', self.APP_KEY),
            ('access_token', access_token),
            ('openid', openid),
            ('clientip', self.client_ip),
            ('oauth_version', '2.a'),
            ('scope', 'all'),
            #('fopenids', self.DEEPIN_ID)]
            ('name', self.DEEPIN_ID)]
        back = self.curl.post(url, data)
        #print back
        if back is None or back == '':
            return None
        if back['errcode'] != 0:
            return None
        return back

    def upload_image(self, img, mesg=''):
        '''upload image'''
        access_token = self.oauth.get("access_token")
        openid = self.oauth.get("openid")
        if access_token is None or openid is None:
            return (False, None)
        data = [
            ('oauth_consumer_key', self.APP_KEY),
            ('access_token', access_token),
            ('clientip', self.client_ip),
            ('openid', openid),
            ('scope', 'all'),
            ('oauth_version', '2.a'),
            ('format', 'json'),
            ('pic', (pycurl.FORM_FILE, img)),
            ('content', mesg)]
        back = self.upload(data)
        #print back
        if back is None:
            return (False, None)
        if back['errcode'] != 0:
            self.error_code = str(back['ret']) + str(back['errcode'])
            self.error_msg = back['msg']
            return (False, None)
        url = "http://t.qq.com/p/t/%s" % back['data']['id']
        return (True, url)

class Twitter(Weibo):
    '''Twitter Weibo'''
    def __init__(self, webkit):
        Weibo.__init__(self, 'Twitter', webkit)
        self.APP_KEY = 'r2HHabDu8LDQCELxk2cA'
        self.APP_SECRET = '9e4LsNOvxWVWeEgC5gthL9Q78F7FDsnT7lUIBruyQmI'
        self.CALLBACK_URL = 'http://www.linuxdeepin.com'
        self.DEEPIN_ID = '461799845'
        self.index_url = 'http://twitter.com'

        self.oauth_token_secret = ''
        self.oauth_token = ''
        self.oauth_verifier = ''
        self._access_token_secret = ''
        self._access_token = ''

        version = '1.1'
        self.REQUEST_TOKEN_URL = 'https://api.twitter.com/oauth/request_token'
        self.AUTHORIZE_URL = 'https://api.twitter.com/oauth/authorize'
        self.ACCESS_TOKEN_URL = 'https://api.twitter.com/oauth/access_token'
        self.USERS_URL = 'https://api.twitter.com/%s/users/show.json' % version
        self.UPLOAD_URL = 'https://api.twitter.com/%s/statuses/update_with_media.json' % version
        self.FRIEND_URL = 'https://api.twitter.com/%s/friendships/create.json' % version
        #self.USERS_URL = 'https://api.twitter.com/1/users/show.json'
        #self.UPLOAD_URL = 'https://upload.twitter.com/1/statuses/update_with_media.json'

        self.errors = {}

    def signature_base_string(self, method, params, url, secret_key=''):
        '''
        signature base string
        @param method: the HTTP method, POST or GET
        @param params: a list containing some tuple
        @param url: the target url
        @param secret_key: a key for base64
        @return: a tuple containing the result of signature and request_url with params and http headers
        '''
        http_method = method
        base_url = url
        params.sort()
        url_params = urllib.quote(urllib.urlencode(params))
        base_string = "%s&%s&%s"%(http_method, urllib.quote(base_url, safe=''), url_params)
        #print "base_string:", base_string
        app_secret = self.APP_SECRET
        hmac_sha1 = hmac.new(app_secret+'&'+secret_key, base_string, hashlib.sha1)
        hmac_sha1_string = hmac_sha1.digest()
        signature_base_string = hmac_sha1_string.encode('base64').rstrip()

        request_url = base_url + '?'
        headers = 'Authorization: OAuth'
        for args in params:
            request_url += '%s=%s&' % (args[0], args[1])
            headers += ' %s="%s",' % (args[0], args[1])
        request_url += '%s=%s' % ('oauth_signature', signature_base_string)
        headers += ' %s="%s"' % ('oauth_signature', urllib.quote(signature_base_string, safe=''))

        return (signature_base_string, request_url, headers)

    # first request token, get oauth_token and oauth_token_secret.
    # now get the request token url
    def get_request_token_url(self):
        '''get request_token url'''
        timestamp = str(int(time.time()))
        params = [
            ('oauth_consumer_key', self.APP_KEY), # App Key
            ('oauth_signature_method', 'HMAC-SHA1'),
            ('oauth_timestamp', timestamp),
            ('oauth_nonce', hashlib.md5(timestamp).hexdigest()),
            ('oauth_version', '1.0'),
            ('oauth_callback', self.CALLBACK_URL)]
        request_token = self.signature_base_string("GET", params, self.REQUEST_TOKEN_URL)
        #print request_token
        return request_token[1]

    # now request token get authorize url, and open it in webbrowser.
    def request_token(self):
        '''request token and return authorize url'''
        back = self.curl.twitter_get(self.get_request_token_url())
        #back = self.curl.twitter_get(self.get_request_token_url(), proxy_host="127.0.0.1", proxy_port=8087)
        #print back
        if back is None:
            return None
        url = urlparse.urlparse(back)
        parse = urlparse.parse_qs(url.path, True)
        try:
            self.oauth_token_secret = parse['oauth_token_secret'][0]
            self.oauth_token = parse['oauth_token'][0]
        except KeyError: # request token failed
            return None
        authorize_url = "%s?oauth_token=%s&force_login=true" % (self.AUTHORIZE_URL, self.oauth_token)
        return authorize_url

    # second authorize the oauth_token which is got at the first step.
    # at previous step open the authorize url, then goto callback with oauth_token and oauth_verifier parameter.
    def authorize(self):
        '''authorize and get oauth_token, oauth_verifier'''
        url = self.webkit.get_property('uri')
        if url is None:
            return False
        back = self.parse_url(url)
        if back is None:
            return False
        parse = back[1]
        if 'oauth_token' in parse and 'oauth_verifier' in parse:
            self.oauth_token = parse['oauth_token'][0]
            self.oauth_verifier = parse['oauth_verifier'][0]
            return True
        return False

    # at last access the oauth_token
    # now use oauth_token and oauth_verifier get the access_token url
    def get_access_token_url(self):
        '''get access_token url'''
        timestamp = str(int(time.time()))
        params = [
            ('oauth_consumer_key', self.APP_KEY), # App Key
            ('oauth_signature_method', 'HMAC-SHA1'),
            ('oauth_timestamp', timestamp),
            ('oauth_nonce', hashlib.md5(timestamp).hexdigest()),
            ('oauth_version', '1.0'),
            ('oauth_verifier', self.oauth_verifier),
            ('oauth_token', self.oauth_token)]
        access_token = self.signature_base_string("GET", params, self.ACCESS_TOKEN_URL)
        #print access_token
        return access_token[1]

    # now access the oauth_token
    def access_token(self):
        '''access token'''
        if not self.authorize():
            return False
        back = self.curl.twitter_get(self.get_access_token_url())
        #back = self.curl.twitter_get(self.get_access_token_url(), proxy_host="127.0.0.1", proxy_port=8087)
        if back is None:
            return False
        url = urlparse.urlparse(back)
        parse = urlparse.parse_qs(url.path, True)
        try:
            self._access_token_secret = parse['oauth_token_secret'][0] if not isinstance(parse['oauth_token_secret'][0], unicode) else str(parse['oauth_token_secret'][0])
            self._access_token = parse['oauth_token'][0] if not isinstance(parse['oauth_token'][0], unicode) else str(parse['oauth_token'][0])
            self._user_id = parse['user_id'][0] if not isinstance(parse['user_id'][0], unicode) else str(parse['user_id'][0])
            self._name = parse['screen_name'][0] if not isinstance(parse['screen_name'][0], unicode) else str(parse['screen_name'][0])
            self.oauth.set(
                access_token_secret=self._access_token_secret,
                access_token=self._access_token,
                user_id=self._user_id)
        except KeyError: # access token failed
            return False
        return True

    def get_access_url(self):
        ''' '''
        return self.request_token()

    # use webkit open authorize page
    def request_oauth(self):
        '''request oauth access token'''
        url = self.request_token()
        print "twittr url", url
        if url is None:
            #self.webkit.load_string("<html><body><h1>load failed!</h1></body></html>", "text/html", "UTF-8", "")
            pass
        else:
            self.webkit.load_uri(url)

    def get_user_name(self):
        '''get user name'''
        timestamp = str(int(time.time()))
        try:
            user_id = self.oauth.get('access_token').split('-')[0]
        except:
            user_id = self.oauth.get('user_id')
        access_token = self.oauth.get('access_token')
        access_token_secret = self.oauth.get('access_token_secret')
        if user_id is None or access_token is None or access_token_secret is None:
            return None
        params = [
            ('oauth_consumer_key', self.APP_KEY), # App Key
            ('oauth_signature_method', 'HMAC-SHA1'),
            ('oauth_timestamp', timestamp),
            ('oauth_nonce', hashlib.md5(timestamp).hexdigest()),
            ('oauth_version', '1.0'),
            ('user_id', user_id),
            ('oauth_token', access_token)]
        user_name = self.signature_base_string("GET", params, self.USERS_URL, access_token_secret)
        user_url = "%s?user_id=%s" % (self.USERS_URL, user_id)
        back = self.curl.get(user_url, [user_name[2]])
        #back = self.curl.get(user_url, [user_name[2]], proxy_host="127.0.0.1", proxy_port=8087)
        if back is None:
            return None
        if 'errors' in back or 'error' in back:
            return None
        return back['screen_name']

    def get_deepin_info(self):
        '''get deepin twitter info'''
        timestamp = str(int(time.time()))
        access_token = self.oauth.get('access_token')
        access_token_secret = self.oauth.get('access_token_secret')
        if access_token is None or access_token_secret is None:
            return None
        params = [
            ('oauth_consumer_key', self.APP_KEY), # App Key
            ('oauth_signature_method', 'HMAC-SHA1'),
            ('oauth_timestamp', timestamp),
            ('oauth_nonce', hashlib.md5(timestamp).hexdigest()),
            ('oauth_version', '1.0'),
            ('user_id', self.DEEPIN_ID),
            ('oauth_token', access_token)]
        user_name = self.signature_base_string("GET", params, self.USERS_URL, access_token_secret)
        user_url = "%s?user_id=%s" % (self.USERS_URL, self.DEEPIN_ID)
        back = self.curl.get(user_url, [user_name[2]])
        #back = self.curl.get(user_url, [user_name[2]], proxy_host="127.0.0.1", proxy_port=8087)
        #print back
        if back is None:
            return None
        if 'errors' in back or 'error' in back:
            return None
        return (back['screen_name'], back['location'], back['description'], back['following'])

    def friendships_create(self):
        '''add deepin to friend'''
        timestamp = str(int(time.time()))
        access_token = self.oauth.get('access_token')
        access_token_secret = self.oauth.get('access_token_secret')
        if access_token is None or access_token_secret is None:
            return None
        params = [
            ('oauth_consumer_key', self.APP_KEY), # App Key
            ('oauth_signature_method', 'HMAC-SHA1'),
            ('oauth_timestamp', timestamp),
            ('oauth_nonce', hashlib.md5(timestamp).hexdigest()),
            ('oauth_version', '1.0'),
            ('user_id', self.DEEPIN_ID),
            ('oauth_token', access_token)]
        friend = self.signature_base_string("POST", params, self.FRIEND_URL, access_token_secret)
        url = self.FRIEND_URL
        back = self.curl.post(url, [('user_id', self.DEEPIN_ID)], [friend[2]])
        #back = self.curl.post(url, [('user_id', self.DEEPIN_ID)], [friend[2]], proxy_host="127.0.0.1", proxy_port=8087)
        #print back
        if back is None:
            return None
        if 'errors' in back or 'error' in back:
            return None
        return back

    def upload_image(self, img, mesg=""):
        '''upload image'''
        access_token = self.oauth.get('access_token')
        access_token_secret = self.oauth.get('access_token_secret')
        if access_token is None or access_token_secret is None:
            return None
        timestamp = str(int(time.time()))
        params = [
            ('oauth_consumer_key', self.APP_KEY), # App Key
            ('oauth_signature_method', 'HMAC-SHA1'),
            ('oauth_timestamp', timestamp),
            ('oauth_nonce', hashlib.md5(timestamp).hexdigest()),
            ('oauth_version', '1.0'),
            ('oauth_token', access_token)]
        upload = self.signature_base_string("POST", params, self.UPLOAD_URL, access_token_secret)
        header = upload[2]
        url = self.UPLOAD_URL
        #data = [('meida[]', (pycurl.FORM_FILE, img)), ("status", mesg)]
        #back = self.curl.upload(url, data, [header, 'Expect: '], "127.0.0.1", 8087)
        #back = self.curl.upload(url, data, header)

        curl_cmd = """curl --connect-timeout 10 -k -F media[]="@%s" -F 'status=%s' --request 'POST' '%s' --header '%s' --header '%s'""" %(img, mesg, url, header, "Expect: ")
        #curl_cmd = """curl --connect-timeout 10 -k %s -F media[]="@%s" -F 'status=%s' --request 'POST' '%s' --header '%s' --header '%s'""" %("-x 127.0.0.1:8087", img, mesg, url, header, "Expect: ")
        #print curl_cmd
        try:
            cmd = subprocess.Popen(curl_cmd, shell=True, stdout=subprocess.PIPE)
            if cmd.wait() != 0:
                #print "returncode:", cmd.returncode
                self.curl.error = "An error occured while connecting."
                return (False, None)
        except OSError:
            return (False, None)
        try:
            back = json.loads(cmd.stdout.read())
        except Exception, e:
            print "twitter error:", e
            back = None
        #print back
        if back is None:
            return (False, None)
        if 'errors' in back:
            self.error_code = back["errors"][0]["code"]
            self.error_msg = self.errors[self.error_code] = back["errors"][0]["message"]
            return (False, None)
        url = "http://twitter.com/%s/status/%s" % (back['user']['screen_name'], back['id_str'])
        return (True, url)

if __name__ == '__main__':
    #s = Sina(None)
    #print s.get_user_name()
    #print s.upload_image('logo.ppm', '')

    #t = Tencent(None)
    #print t.get_user_name()
    #print t.upload_image('gtk.png', 'curl微博api上传图片测试')

    t = Twitter(None)
    #print t.request_token()
    #print t.get_access_token_url()
    #url = raw_input("authorize url:")
    #if t.authorize(url):
        #print t.access_token()
    print t.get_user_name()
    #print t.upload_image('logo.ppm', "上传图片api")
