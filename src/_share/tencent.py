#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = '0.01'
__author__ = 'Juntao Liu (jinuljt@gmail.com)'

'''
Python client SDK for QQ weibo API using OAuth 2.
steel code from Liao Xuefeng (askxuefeng@gmail.com) for sina weibo
'''

import json
import time
import urllib
import urllib2
import logging

def _obj_hook(pairs):
    '''
    convert json object to python object.
    '''
    o = JsonObject()
    for k, v in pairs.iteritems():
        o[str(k)] = v
    return o

class APIError(StandardError):
    '''
    raise APIError if got failed json message.
    '''
    def __init__(self, error_code, msg, request):
        self.error_code = error_code
        self.msg = msg
        self.request = request
        StandardError.__init__(self, msg)

    def __str__(self):
        return 'APIError: %s: %s, request: %s' % (self.error_code, self.msg, self.request)


class JsonObject(dict):
    '''
    general json object that can bind any fields but also act as a dict.
    '''
    def __getattr__(self, attr):
        return self[attr]

    def __setattr__(self, attr, value):
        self[attr] = value

def _encode_params(**kw):
    '''
    Encode parameters.
    '''
    args = []
    for k, v in kw.iteritems():
        qv = v.encode('utf-8') if isinstance(v, unicode) else str(v)
        args.append('%s=%s' % (k, urllib.quote(qv)))
    return '&'.join(args)

def _encode_multipart(**kw):
    '''
    Build a multipart/form-data body with generated random boundary.
    '''
    boundary = '----------%s' % hex(int(time.time() * 1000))
    data = []
    for k, v in kw.iteritems():
        data.append('--%s' % boundary)
        if hasattr(v, 'read'):
            # file-like object:
            ext = ''
            filename = getattr(v, 'name', '')
            n = filename.rfind('.')
            if n != (-1):
                ext = filename[n:].lower()
            content = v.read()
            data.append('Content-Disposition: form-data; name="%s"; filename="hidden"' % k)
            data.append('Content-Length: %d' % len(content))
            data.append('Content-Type: %s\r\n' % _guess_content_type(ext))
            data.append(content)
        else:
            data.append('Content-Disposition: form-data; name="%s"\r\n' % k)
            data.append(v.encode('utf-8') if isinstance(v, unicode) else v)
    data.append('--%s--\r\n' % boundary)
    return '\r\n'.join(data), boundary

_CONTENT_TYPES = { '.png': 'image/png', '.gif': 'image/gif', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.jpe': 'image/jpeg' }

def _guess_content_type(ext):
    return _CONTENT_TYPES.get(ext, 'application/octet-stream')

_HTTP_GET = 0
_HTTP_POST = 1
_HTTP_UPLOAD = 2

def _http_get(api_url, client=None, **kw):
    logging.info('GET %s' % api_url)
    return _http_call(api_url, _HTTP_GET, client, **kw)

def _http_post(api_url, client=None, **kw):
    logging.info('POST %s' % api_url)
    return _http_call(api_url, _HTTP_POST, client, **kw)

def _http_upload(api_url, client=None, **kw):
    logging.info('MULTIPART POST %s' % api_url)
    return _http_call(api_url, _HTTP_UPLOAD, client, **kw)

def _http_call(api_url, method, client, **kw):
    '''
    send an http request and expect to return a json object if no error.
    '''
    params = None
    boundary = None
    if method==_HTTP_UPLOAD:
        params, boundary = _encode_multipart(**kw)
    else:
        params = _encode_params(**kw)

    if client:
        auth_params = _encode_params(
            oauth_consumer_key=client.client_id,
            access_token=client.access_token,
            openid=client.openid,
            oauth_version="2.a",
            scope="all"
            )
        api_url = '%s?%s' % (api_url, auth_params)
    http_url = '%s&%s' % (api_url, params) if method==_HTTP_GET else api_url
    http_body = None if method==_HTTP_GET else params
    req = urllib2.Request(http_url, data=http_body)
    if boundary:
        req.add_header('Content-Type', 'multipart/form-data; boundary=%s' % boundary)
    try:
        resp = urllib2.urlopen(req)
        body = resp.read()
    except urllib2.HTTPError, e:
        body = e.read()
        
    try:
        r = json.loads(body, object_hook=_obj_hook)
        if hasattr(r, 'errcode') and r.errcode != 0:
            raise APIError(r.errcode, getattr(r, 'msg', ''), http_url)
    except ValueError:
        r = body
    return r

class HttpObject(object):

    def __init__(self, client, method):
        self.client = client
        self.method = method

    def __getattr__(self, attr):
        def wrap(**kw):
            if self.client.is_expires():
                raise APIError('10019', 'expired_token', attr)
            #return _http_call('%s%s.json' % (self.client.api_url, attr.replace('__', '/')), self.method, self.client.access_token, self.openid, **kw)
            return _http_call('%s%s' % (self.client.api_url, attr.replace('__', '/')), self.method, self.client, **kw)
        return wrap

class APIClient(object):
    '''
    API client using synchronized invocation.
    '''
    def __init__(self, app_key, app_secret, redirect_uri=None,
                 clientip='127.0.0.1', response_type='code',
                 domain='open.t.qq.com'):
        self.client_id = app_key
        self.client_secret = app_secret
        self.redirect_uri = redirect_uri
        self.response_type = response_type
        self.auth_url = 'https://%s/cgi-bin/oauth2/' % domain
        self.api_url = 'https://%s/api/' % domain
        self.access_token = None
        self.openid = None
        self.expires = 0.0
        self.get = HttpObject(self, _HTTP_GET)
        self.post = HttpObject(self, _HTTP_POST)
        self.upload = HttpObject(self, _HTTP_UPLOAD)

    def set_access_token(self, access_token, openid, expires_in):
        self.access_token = str(access_token)
        self.openid = openid
        self.expires = float(expires_in)

    def get_authorize_url(self, redirect_uri=None):
        '''
        return the authroize url that should be redirect.
        '''
        redirect = redirect_uri if redirect_uri else self.redirect_uri
        if not redirect:
            raise APIError('10013', 'Parameter absent: redirect_uri', 'OAuth2 request')
        return '%s%s?%s' % (self.auth_url, 'authorize', \
                _encode_params(client_id = self.client_id, \
                        response_type = 'code', \
                        redirect_uri = redirect))

    def request_access_token(self, code, redirect_uri=None, ):
        '''
        return access token as object: {"access_token":"your-access-token","expires_in":12345678}, expires_in is standard unix-epoch-time
        '''
        redirect = redirect_uri if redirect_uri else self.redirect_uri
        if not redirect:
            raise APIError('10013', 'Parameter absent: redirect_uri', 'OAuth2 request')
        body = _http_get('%s%s?' % (self.auth_url, 'access_token'), \
                client_id = self.client_id, \
                client_secret = self.client_secret, \
                redirect_uri = redirect, \
                code = code, grant_type = 'authorization_code')
        r = _obj_hook(dict([p.split('=') for p in body.split('&')]))
        r.expires_in = int(r.expires_in) + int(time.time())
        return r

    def refresh_token(self, refresh_token):
        body = _http_get('%s%s?' % (self.auth_url, 'access_token'), \
                client_id = self.client_id, \
                client_secret = self.client_secret, \
                refresh_token = refresh_token, \
                grant_type = 'refresh_token')
        r = _obj_hook(dict([p.split('=') for p in body.split('&')]))
        r.expires_in = int(r.expires_in) + int(time.time())
        return r

    def is_expires(self):
        return not self.access_token or time.time() > self.expires

    def __getattr__(self, attr):
        return getattr(self.get, attr)
