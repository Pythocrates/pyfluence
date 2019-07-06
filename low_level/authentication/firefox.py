# -*- coding: utf-8 -*-

import os
import sqlite3

import configparser


class FirefoxSessionCookieAuth:
    '''Uses a Firefox session for authentication.'''

    token_name = 'seraph.confluence'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__obtain_token_key_from_firefox()

    def __call__(self, request):
        request.prepare_cookies({self.token_name: self.__token_key})
        return request

    def __obtain_token_key_from_firefox(self):
        profiles_ini_path = os.path.expanduser(
            '~/.mozilla/firefox/profiles.ini')
        default_profile_path = self.__find_default_profile_path(
            ini_path=profiles_ini_path)
        cookie_file_path = os.path.join(default_profile_path, 'cookies.sqlite')
        self.__token_key = self.__retrieve_token_key(
            db_path=cookie_file_path,
            name=self.token_name)

    @staticmethod
    def __find_default_profile_path(ini_path):
        parser = configparser.SafeConfigParser()
        parser.read(ini_path)
        for section in parser.sections():
            if parser.has_option(section, 'Default'):
                try:
                    path = parser.get(section, 'Path')
                    if parser.getboolean(section, 'IsRelative'):
                        path = os.path.join(os.path.dirname(ini_path), path)

                    return os.path.abspath(os.path.expanduser(path))
                except configparser.NoOptionError:
                    pass

    @staticmethod
    def __retrieve_token_key(db_path, name):
        '''Retrieve key from the Firefox cookie database.'''
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        rows = cursor.execute(
            'SELECT value FROM moz_cookies WHERE name == "{name}"'.format(
                name=name))
        value = next(rows)[0]
        return value
