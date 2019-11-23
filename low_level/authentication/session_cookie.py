# -*- coding: utf-8 -*-


class SessionCookieAuth:
    '''Uses an explicitly given session cookie.'''

    def __init__(self, cookies, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__cookies = cookies

    def __call__(self, request):
        request.prepare_cookies(self.__cookies)
        return request
