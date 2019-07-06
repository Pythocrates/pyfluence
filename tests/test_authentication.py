#! /usr/bin/env python


import unittest

from pyfluence.low_level.authentication import ChromiumSessionCookieAuth as Auth


class ChromiumSessionCookieAuthTest(unittest.TestCase):
    def test_initialization(self, *args, **kwargs):
        auth = Auth()
        self.assertIsNotNone(auth)


if __name__ == '__main__':
    unittest.main()
