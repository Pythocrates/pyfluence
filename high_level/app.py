# -*- coding: utf-8 -*-

from ..low_level.session import Session


class App:
    def __init__(self, session, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__session = session

    @property
    def session(self):
        return self.__session

    @classmethod
    def from_chromium(cls):
        session = Session.from_chromium()
        return cls.from_session(session=session)

    @classmethod
    def from_firefox(cls):
        session = Session.from_firefox()
        return cls.from_session(session=session)

    @classmethod
    def from_functional_user(cls, username, password):
        session = Session.from_functional_user(
            username=username, password=password)
        return cls(session=session)

    @classmethod
    def from_session(cls, session):
        return cls(session=session)
