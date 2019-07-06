# -*- coding: utf-8 -*-

from .page import Page


class Space:
    def __init__(self, key, api, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__key = key
        self.__api = api
        self.__response = self.__api.space[self.__key].GET(expand='homepage')

    @property
    def page(self):
        return Page(id_=self.__response.json()['homepage']['id'], api=self.__api, parent=self)

    @property
    def path(self):
        return [self.__key]

    def __getitem__(self, child):
        return self.page[child]
