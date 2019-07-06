# -*- coding: utf-8 -*-

import configparser
import os
import sqlite3

from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from requests.auth import AuthBase
import secretstorage


class ChromiumSessionCookieAuth(AuthBase):
    '''Uses a Chromium session for authentication.'''

    # The crowd token key is used for JIRA, the seraph for Wiki. Don't know about the other components.
    token_names = ['seraph.confluence', 'crowd.token_key']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__cookies = dict((name, self.__obtain_token_key_from_chromium(name=name)) for name in self.token_names)

    def __call__(self, request):
        request.prepare_cookies(self.__cookies)
        return request

    @classmethod
    def __obtain_token_key_from_chromium(cls, name):
        safe_storage_pass = cls.__get_safe_storage_password()
        encrypted_token_key = cls.__get_encrypted_token_key(name=name)
        if encrypted_token_key:
            return cls.__decrypt_token_key(encrypted=encrypted_token_key, password=safe_storage_pass)
        else:
            return None

    @staticmethod
    def __get_safe_storage_password():
        '''Extract the Chromium safe storage password from the secret storage.'''
        bus = secretstorage.dbus_init()
        collection = secretstorage.get_default_collection(bus)
        for item in collection.get_all_items():
            if item.get_label() == 'Chromium Safe Storage':
                return item.get_secret()
        else:
            raise Exception('Chromium password not found!')

    @staticmethod
    def __get_encrypted_token_key(name):
        '''Retrieve encrypted key from the Chromium cookie database.'''
        cookie_file = os.path.join(os.environ['HOME'], '.config', 'chromium', 'Default', 'Cookies')
        conn = sqlite3.connect(cookie_file)
        cursor = conn.cursor()
        rows = cursor.execute('SELECT encrypted_value FROM cookies WHERE name == "{name}"'.format(name=name))
        all_rows = list(rows)
        if all_rows:
            encrypted = all_rows[0][0]
        else:
            encrypted = None
        return encrypted

    @staticmethod
    def __decrypt_token_key(encrypted, password):
        key = PBKDF2(bytes(password).encode('utf8'), b'saltysalt', 16, 1)
        cipher = AES.new(key, AES.MODE_CBC, IV=16 * b' ')

        # Strip away the first three characters (Chromium prepends a version string).
        decrypted = cipher.decrypt(encrypted[3:])

        # Strip away left-over bytes.
        return decrypted[:-ord(decrypted[-1])]



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
        profiles_ini_path = os.path.expanduser('~/.mozilla/firefox/profiles.ini')
        default_profile_path = self.__find_default_profile_path(ini_path=profiles_ini_path)
        cookie_file_path = os.path.join(default_profile_path, 'cookies.sqlite')
        self.__token_key = self.__retrieve_token_key(db_path=cookie_file_path, name=self.token_name)

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
        rows = cursor.execute('SELECT value FROM moz_cookies WHERE name == "{name}"'.format(name=name))
        value = next(rows)[0]
        return value
