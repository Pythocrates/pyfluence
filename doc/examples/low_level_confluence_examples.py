#! /usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Access wiki information using low-level wrapper.

This script demonstrates how to access raw data in the wiki using the low-level
wrapper. For accessible structures please consult the Atlassian REST API docs.
'''

from pprint import pprint

from pyfluence import Session


if __name__ == '__main__':
    # Create a session from the Chromium session credentials.
    session = Session.from_chromium()

    # Use the Confluence REST API wrapper.
    wiki = session.confluence

    # Get user information.
    pprint(wiki.user.GET(username='user').json())    # case-sensitive!

    # Get a content overview.
    pprint(wiki.content.GET().json())

    # Get a space overview.
    pprint(wiki.space.GET().json())

    # Get the XHTML content of the homepage.
    pprint(wiki.space.PROJECT.GET(expand='homepage.body.storage').json()[
        'homepage']['body']['storage']['value'])

    # Show the children of the homepage.
    pprint(wiki.space.PROJECT.GET(expand='homepage.children.page').json())
    # Get the ID of the first child.
    child_id = wiki.space.PROJECT.GET(expand='homepage.children.page').json()[
        'homepage']['children']['page']['results'][0]['id']

    # Show the content of the first child.
    pprint(wiki.content[child_id].GET(expand='body.storage').json()[
        'body']['storage']['value'])

    # Show all user of a group.
    pprint(wiki.group['my-group'].member.GET().json())
