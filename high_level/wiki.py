# -*- coding: utf-8 -*-

import base64
import struct

from .attachment import Attachment
from .page import Page
from .space import Space
from .app import App


class Wiki(App):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def raw(self):
        '''
        Get the low-level wiki interface.
        '''
        return self._wrapper

    def get_space(self, key):
        return Space(key=key, api=self._wrapper)

    def get_page_by_tinyui(self, tinyui):
        page_id = struct.unpack(
            'L', base64.b64decode(
                tinyui.replace('-', '/').ljust(11, 'A').ljust(12, '=')))[0]
        return Page(id_=page_id, api=self._wrapper)

    def get_attachment_by_id(self, att_id):
        return Attachment(id_='att{i}'.format(i=att_id), api=self._wrapper)

    def __getitem__(self, key):
        return self.get_space(key=key)

    def read_uri(self, uri):
        return self._wrapper.read(uri)
