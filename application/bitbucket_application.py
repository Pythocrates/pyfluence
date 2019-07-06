# -*- coding: utf-8 -*-

from .application import Application
from .. import Bitbucket


class BitbucketApplication(Application):
    _app_class = Bitbucket

    @property
    def bitbucket(self):
        return self._app
