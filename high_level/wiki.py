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
        self.__confluence = self.session.confluence

    @property
    def raw(self):
        '''
        Get the low-level wiki interface.
        '''
        return self.session.wiki

    def get_space(self, key):
        return Space(key=key, api=self.__confluence)

    def get_page_by_tinyui(self, tinyui):
        page_id = struct.unpack(
            'L', base64.b64decode(
                tinyui.replace('-', '/').ljust(11, 'A').ljust(12, '=')))[0]
        return Page(id_=page_id, api=self.__confluence)

    def get_attachment_by_id(self, att_id):
        return Attachment(id_='att{i}'.format(i=att_id), api=self.__confluence)

    def __getitem__(self, key):
        return self.get_space(key=key)

    def read_uri(self, uri):
        return self.session.read(uri)
