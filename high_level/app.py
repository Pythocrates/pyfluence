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
    def from_chromium(cls, host):
        session = Session.from_chromium(host=host)
        return cls.from_session(session=session)

    @classmethod
    def from_firefox(cls, host):
        session = Session.from_firefox(host=host)
        return cls.from_session(session=session)

    @classmethod
    def from_kerberos(cls, host):
        session = Session.from_kerberos(host=host)
        return cls.from_session(session=session)

    @classmethod
    def from_functional_user(cls, username, password, host):
        session = Session.from_functional_user(
            username=username, password=password, host=host)
        return cls(session=session)

    @classmethod
    def from_session(cls, session):
        return cls(session=session)
