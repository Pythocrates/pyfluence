# -*- coding: utf-8 -*-

from .app import App


class Bitbucket(App):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__confluence = self.session.confluence

    @property
    def raw(self):
        '''
        Get the low-level Bitbucket interface.
        '''
        return self.session.bitbucket

    @property
    def raw_keys(self):
        '''
        Get the low-level Bitbucket keys interface.
        '''
        return self.session.bitbucket_keys

    @property
    def raw_ssh(self):
        '''
        Get the low-level Bitbucket ssh interface.
        '''
        return self.session.bitbucket_ssh
