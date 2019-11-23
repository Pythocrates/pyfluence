# -*- coding: utf-8 -*-

import shutil

from http.cookiejar import CookiePolicy
import requests


class Session:
    class NoCookies(CookiePolicy):
        ''' A cookie policy blocking any cookies, thus enabling us to use
        request.prepare_cookies, which does not overwrite existing cookie
        headers.
        See: https://stackoverflow.com/a/21714597.
        '''
        def set_ok(self, cookie, request):
            return False

        rfc2965 = False
        netscape = True

    def __init__(self, auth, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__session = requests.Session()
        self.__session.auth = auth()
        self.__session.cookies.set_policy(self.NoCookies())
        self.__session.verify = False  # TODO: change this?

    @staticmethod
    def __compile_uri(base, **kwargs):
        if kwargs:
            return base + '?' + '&'.join(f'{k}={v}' for k, v in kwargs.items())
        else:
            return str(base)

    def get(self, http_request_uri, _requests_params=None, **kwargs):
        '''
        _requests_params allows to define custom headers, form parameters and
        others, which are not converted to REST API parameters but are used by
        the requests module.
        '''
        requests_params = _requests_params or dict()
        return self.__session.get(
            self.__compile_uri(http_request_uri, **kwargs), **requests_params)

    def post(self, http_request_uri, _requests_params=None, **kwargs):
        requests_params = _requests_params or dict()
        return self.__session.post(
            self.__compile_uri(http_request_uri, **kwargs), **requests_params)

    def put(self, http_request_uri, _requests_params=None, **kwargs):
        requests_params = _requests_params or dict()
        return self.__session.put(
            self.__compile_uri(http_request_uri, **kwargs), **requests_params)

    def delete(self, http_request_uri, _requests_params=None, **kwargs):
        requests_params = _requests_params or dict()
        return self.__session.delete(
            self.__compile_uri(http_request_uri, **kwargs), **requests_params)

    def download(self, url, file_path=None):
        '''Download a resource using the session's authorization.'''
        response = self.__session.get(url, stream=True)
        if not file_path:
            file_path = url.split('?')[0].split('/')[-1]
            with open(file_path, 'wb') as out_file:
                response.raw.decode_content = True
                shutil.copyfileobj(response.raw, out_file)

    def read(self, url):
        '''Return as a string a resource using the session's authorization.'''
        response = self.__session.get(url, stream=True)
        response.raw.decode_content = True
