# -*- coding: utf-8 -*-


class App:
    def __init__(self, wrapper, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__wrapper = wrapper

    @property
    def _wrapper(self):
        return self.__wrapper
