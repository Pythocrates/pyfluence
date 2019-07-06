#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from pprint import pprint

from pyfluence import Session


if __name__ == '__main__':

    # Create a session from the Chromium session credentials.
    session = Session.from_chromium()

    # Use the BitBucket REST API wrapper.
    bb = session.bitbucket
    bb_keys = session.bitbucket_keys
    bb_ssh = session.bitbucket_ssh

    pprint(bb.projects.PROJECT.repos.test_this.tags.GET().json())
    pprint(bb.projects.PROJECT.repos.test_this.branches.GET().json())
    pprint(bb_keys.projects.PROJECT.ssh.GET().json())
    pprint(bb_ssh.keys.GET().json())
