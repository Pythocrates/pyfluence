# -*- coding: utf-8 -*-

from .app import App


class Bitbucket(App):
    @property
    def raw(self):
        '''
        Get the low-level Bitbucket interface.
        '''
        return self._wrapper
