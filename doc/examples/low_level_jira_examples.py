#! /usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Access JIRA information using low-level wrapper.

This script demonstrates how to access raw data in the JIRA using the low-level
wrapper. For accessible structures please consult the Atlassian REST API docs.
'''


from pprint import pprint

from pyfluence import Session


if __name__ == '__main__':
    # Create a session from the Chromium session credentials.
    session = Session.from_chromium()

    # Use the JIRA REST API wrapper.
    jira = session.jira

    # Get user information.
    pprint(jira.user.GET(username='my user').json())    # case-insensitive
    pprint(jira.user.GET(key='my user').json())    # case-sensitive!
    pprint(jira.myself.GET().json())

    # The current user's permissions.
    pprint(jira.mypermissions.GET().json())

    # Get the groups the user belongs to.
    pprint(jira.user.GET(
        key='my user', expand='groups').json()['groups']['items'])

    # Get only the names of the groups the user belongs to.
    pprint(
        [
            g['name']
            for g in jira.user.GET(
                key='my user', expand='groups'
            ).json()['groups']['items']])

    # Get project information.
    pprint(jira.project.PROJECT.GET().json())

    # Get issue information.
    print('#### Information about issue PROJECT-220: ####')
    pprint(jira.issue['PROJECT-220'].GET().json())
