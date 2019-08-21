# -*- coding: utf-8 -*-

import os

import requests
import requests_kerberos

from ...exception import AuthenticationError


class KerberosSessionCookieAuth:
    def __init__(self, subdomain, *args, **kwargs):
        super().__init__(*args, **kwargs)
        r = requests.get(
            'https://{}.{}'.format(
                subdomain,
                os.environ['CONFLUENCE_HOSTNAME']),
            auth=requests_kerberos.HTTPKerberosAuth(),
            verify=False,
        )
        try:
            self.__cookies = {'JSESSIONID': r.cookies['JSESSIONID']}
        except KeyError:
            raise AuthenticationError('Kerberos authentication failed.')

    def __call__(self, request):
        request.prepare_cookies(self.__cookies)
        return request
