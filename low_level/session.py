# -*- coding: utf-8 -*-

from functools import partial
import shutil

import requests

from .authentication import ChromiumSessionCookieAuth, FirefoxSessionCookieAuth
from .rest_wrapper import RESTWrapper


class Session(object):
    def __init__(self, host, auth, subdomains, *args, **kwargs):
        '''
        subdomains map the functionality to the subdomain namem e.g.
        {'bitbucket': 'bitbucket'}
        '''
        super(Session, self).__init__(*args, **kwargs)
        self.__session = requests.Session()
        self.__session.auth = auth()
        # TODO: resolve subdomain + host
        # TODO: refactoring: move specific URLs out of Session
        self.__bitbucket = RESTWrapper(
            host='https://{}.{}',
            path=['rest', 'api', '1.0'],
            session=self)
        self.__bitbucket_keys = RESTWrapper(
            host='https://{}.{}',
            path=['rest', 'keys', '1.0'],
            session=self)
        self.__bitbucket_ssh = RESTWrapper(
            host='https://{}.{}',
            path=['rest', 'ssh', '1.0'],
            session=self)
        self.__jira = RESTWrapper(
            host='https://{}.{}',
            path=['rest', 'api', '2'],
            session=self)
        self.__wiki = RESTWrapper(
            host='https://{}.{}',
            path=['rest', 'api'],
            session=self)

    bitbucket = property(lambda self : self.__bitbucket)
    bitbucket_keys = property(lambda self : self.__bitbucket_keys)
    bitbucket_ssh = property(lambda self : self.__bitbucket_ssh)
    jira = property(lambda self : self.__jira)
    wiki = property(lambda self : self.__wiki)

    @classmethod
    def from_firefox(cls):
        return cls(auth=FirefoxSessionCookieAuth)

    @classmethod
    def from_chromium(cls):
        return cls(auth=ChromiumSessionCookieAuth)

    @classmethod
    def from_functional_user(cls, username, password):
        return cls(
            auth=partial(
                requests.auth.HTTPBasicAuth,
                username=username,
                password=password))

    @staticmethod
    def __compile_uri(base, **kwargs):
        if kwargs:
            return base + '?' + '&'.join(
                '{k}={v}'.format(k=k, v=v) for k, v in kwargs.iteritems())
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
