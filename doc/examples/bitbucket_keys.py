#! /usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Access the BitBucket key.
'''

from pprint import pprint

from pyfluence.application import BitbucketApplication


class BitBucketKeys(BitbucketApplication):

    def build_parser(self):
        super(BitBucketKeys, self).build_parser()

    def run(self):
        for value in self.bitbucket.raw_ssh.keys.GET().json()['values']:
            pprint(value)


if __name__ == '__main__':
    BitBucketKeys().run()
