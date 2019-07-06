# -*- coding: utf-8 -*-

from .application import Application
from .. import Wiki


class WikiApplication(Application):
    _app_class = Wiki

    @property
    def wiki(self):
        return self._app
