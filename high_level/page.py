# -*- coding: utf-8 -*-

import base64
import struct

from unicodedata import normalize as ucd_norm
from bs4 import BeautifulSoup

from .attachment import Attachment
from .exceptions import AttachmentNotFoundError, PageNotFoundError


def normalize(text):
    return ucd_norm('NFKC', text)


class Page(object):
    '''Page represents a Confluence wiki page.
    Page provides easy access to contents and related features of a wiki page.

    .. automethod:: __init__
    .. automethod:: __getitem__
    '''
    def __init__(self, id_, api, parent=None, *args, **kwargs):
        '''Initialize a new instance.

        :param id_: The ID of the wiki page to be wrapped.
        :type id_: :class:`str`
        :param api: The low-level wrapper instance to be used to access the server.
        :type api: :class:`~pyfluence.low_level.rest_wrapper.RESTWrapper`
        :param parent: The parent of the new page.
        :type parent: :class:`~pyfluence.high_level.page.Page` or :class:`~pyfluence.high_level.space.Space`
        '''
        super(Page, self).__init__(*args, **kwargs)
        self.__id = id_
        self.__api = api
        self.__request_base = self.__api.content[self.__id]
        self.__expand_parameters = set([
            'ancestors',
            'body.storage',
            'children.attachment',
            'children.attachment.body.storage.content',
            'children.page',
            'space',
            'version'])
        self.__response = self.__request_base.GET(
            expand=','.join(self.__expand_parameters))
        self.__json = self.__response.json()
        self.__parent = parent

    @property
    def json(self):
        '''Get the JSON code of the wiki page.

        :returns: :class:`dict` -- The raw content and metadata of the page.

        .. todo:: Maybe update by sending the request again?
        '''
        return self.__json

    def __getitem__(self, title):
        '''Get the child or parent page given its title.

        :param title: The title of the page or '..' for the parent page.
        :type title: :class:`str`
        :returns: :class:`Page` -- the referenced page.
        :raises: :exc:`~pyfluence.high_level.exceptions.PageNotFoundError`
        '''
        if title == '..':
            page = self.parent
        else:
            children = self.json['children']['page']['results']
            try:
                child_id = next(
                    c['id'] for c in children if c['title'] == title)
            except StopIteration:
                raise PageNotFoundError(title)
            else:
                page = Page(id_=child_id, api=self.__api, parent=self)

        return page

    @property
    def id(self):
        '''Get the ID of the wiki page.

        :returns: :class:`str` -- The ID of the page.
        '''
        return self.__id

    @property
    def tiny_ui(self):
        '''Get the TinyUI (tiny unique ID) of the wiki page.

        :returns: :class:`str` -- The shortened unique ID of the page.
        '''
        return base64.b64encode(struct.pack('L', int(self.id))).rstrip('A=')

    @property
    def title(self):
        '''Get the title of the wiki page.

        :returns: :class:`str` -- The title of the page.
        '''
        return self.json['title']

    @property
    def parent(self):
        '''Get the parent of the wiki page.

        :returns: :class:`~pyfluence.high_level.page.Page` or :class:`~pyfluence.high_level.space.Space` -- The parent of the page.
        '''
        return self.__parent

    @property
    def path(self):
        return self.parent.path + [self.title]

    @property
    def level(self):
        return len(self.path) - 2

    def update_attachment(self, attachment_id, file_path):
        _requests_params = {
            'headers': {'X-Atlassian-Token': 'nocheck',},
            'files': [('file', open(file_path, 'rb'))]
        }
        result = self.__request_base['child']['attachment'][attachment_id]['data'].POST(_requests_params=_requests_params)
        return result

    def iter_attachments(self):
        for raw_attachment in self.json['children']['attachment']['results']:
            yield Attachment(id_=raw_attachment['id'], api=self.__api)

#temporary
    @property
    def attachments(self):
        return self.json['children']['attachment']

    def get_attachment_uri_by_title(self, attachment_title):
        attachments = self.json['children']['attachment']['results']
        return next(a['_links']['download'] for a in attachments if a['title'] == attachment_title)

    def get_attachment_id_by_title(self, attachment_title):
        attachments = self.json['children']['attachment']['results']
        return next(a['id'] for a in attachments if a['title'] == attachment_title)

    def read_attachment_by_title(self, attachment_title):
        attachments = self.json['children']['attachment']['results']
        path = next(a['_links']['download'] for a in attachments if a['title'] == attachment_title)
        return self.__api.read_from_path(path=path)

    def get_attachment_by_title(self, title):
        attachments = self.json['children']['attachment']['results']
        try:
            attachment_id = next(a['id'] for a in attachments if a['title'] == title)
        except StopIteration:
            raise AttachmentNotFoundError(title)
        return Attachment(id_=attachment_id, api=self.__api)

    def __gt__(self, title):
        return self.get_attachment_by_title(title)

    def iter_pages(self, recurse=False):
        if recurse in [True, 'pre_order']:
            # The default is pre-order traversal.
            for page in self.iter_pages(recurse=False):
                yield page
                for descendant in page.iter_pages(recurse=recurse):
                    yield descendant
        elif recurse == 'post_order':
            # Post-order traversal.
            for page in self.iter_pages(recurse=False):
                for descendant in page.iter_pages(recurse=recurse):
                    yield descendant
                yield page
        else:
            # Just the immediate children are iterated over.
            for page in self.json['children']['page']['results']:
                yield Page(id_=page['id'], api=self.__api, parent=self)

    @property
    def content(self):
        return self.json['body']['storage']['value']

    @property
    def text(self):
        return [
            normalize(p.text)
            for p in BeautifulSoup(self.content, 'lxml')('p')]

    @content.setter
    def content(self, value):
        _json = {
            'id': self.__json['id'],
            'type': self.__json['type'],
            'title': self.__json['title'],
            'space': {'key': self.__json['space']['key'], },
            'body': {
                'storage': {
                    'value': str(value),
                    'representation': 'storage', }},
            'version': {'number': self.__json['version']['number'] + 1}
        }
# TODO: switch to a better practice
        import json
        _requests_params = {
            'headers': {'Content-Type': 'application/json', },
            'data': json.dumps(_json),
        }
        result = self.__request_base.PUT(_requests_params=_requests_params)
        return result
