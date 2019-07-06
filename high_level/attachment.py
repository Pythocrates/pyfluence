# -*- coding: utf-8 -*-

import json


class Attachment:
    def __init__(self, id_, api, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__id = id_
        self.__api = api
        self.__request_base = self.__api.content[self.__id]
        self.__response = self.__request_base.GET()

    @property
    def title(self):
        return self.__response.json()['title']

    @property
    def media_type(self):
        return self.__response.json()['metadata']['mediaType']

    @property
    def comment(self):
        # There is also a comment in 'metadata' but only if it is not an empty string.
        return self.__response.json()['extensions']['comment']

    def read(self):
        path = self.__response.json()['_links']['download']
        return self.__api.read_from_path(path=path)

    def upload(self, file_path):
        container_id = self.__request_base.GET(expand='container').json()['container']['id']
        _requests_params = {
            'headers': {'X-Atlassian-Token': 'nocheck', },
            'files': [('file', open(file_path, 'rb'))]
        }
        result = self.__api.content[container_id].child.attachment[self.__id]['data'].POST(_requests_params=_requests_params)
        return result

    def update(self, data):
        container_id = self.__request_base.GET(expand='container').json()['container']['id']
        _requests_params = {
            'headers': {'X-Atlassian-Token': 'nocheck', },
            'files': {'file': (self.__response.json()['title'], data)},
        }
        result = self.__api.content[container_id].child.attachment[self.__id]['data'].POST(_requests_params=_requests_params)
        return result

    def rename(self, name):
        version = int(self.__response.json()['version']['number'])
        _requests_params = {
            'headers': {
                'X-Atlassian-Token': 'nocheck',
                'Content-Type': 'application/json',
            },
            'data': json.dumps({
                'id': self.__id,
                'type': 'attachment',
                'version': {'number': version + 1, },
                'title': name,
            })
        }
        result = self.__request_base.PUT(_requests_params=_requests_params)
        return result

    def download(self, file_path):
        url = self.__api.host + self.__response.json()['_links']['download']
        self.__api.download(url=url, file_path=file_path)
