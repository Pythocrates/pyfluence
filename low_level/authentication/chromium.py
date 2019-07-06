# -*- coding: utf-8 -*-

import os
import sqlite3

from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from requests.auth import AuthBase
import secretstorage


class ChromiumSessionCookieAuth(AuthBase):
    '''Uses a Chromium session for authentication.'''

    # The crowd token key is used for JIRA, the seraph for Wiki.
    # Don't know about the other components.
    token_names = ['seraph.confluence', 'crowd.token_key']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__cookies = dict(
            (name, self.__obtain_token_key_from_chromium(name=name))
            for name in self.token_names)

    def __call__(self, request):
        request.prepare_cookies(self.__cookies)
        return request

    @classmethod
    def __obtain_token_key_from_chromium(cls, name):
        safe_storage_pass = cls.__get_safe_storage_password()
        encrypted_token_key = cls.__get_encrypted_token_key(name=name)
        if encrypted_token_key:
            return cls.__decrypt_token_key(
                encrypted=encrypted_token_key,
                password=safe_storage_pass)
        else:
            return None

    @staticmethod
    def __get_safe_storage_password():
        'Extract the Chromium safe storage password from the secret storage.'
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
        cookie_file = os.path.join(
            os.environ['HOME'], '.config', 'chromium', 'Default', 'Cookies')
        conn = sqlite3.connect(cookie_file)
        cursor = conn.cursor()
        rows = cursor.execute(
            'SELECT encrypted_value FROM cookies WHERE name == "{name}"'
            ''.format(name=name))
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

        # Strip away the first three characters (Chromium prepends a version
        # string).
        decrypted = cipher.decrypt(encrypted[3:])

        # Strip away left-over bytes.
        return decrypted[:-ord(decrypted[-1])]
