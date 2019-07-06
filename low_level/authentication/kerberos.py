# -*- coding: utf-8 -*-

import os

import requests
import requests_kerberos


class KerberosSessionCookieAuth:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        r = requests.get(
            'https://confluence.{}'.format(os.environ['CONFLUENCE_HOSTNAME']),
            auth=requests_kerberos.HTTPKerberosAuth(),
            verify=False,
        )
        self.__cookies = {'JSESSIONID': r.cookies['JSESSIONID']}

    def __call__(self, request):
        request.prepare_cookies(self.__cookies)
        return request
