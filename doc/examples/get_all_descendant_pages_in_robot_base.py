#! /usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Iterate over all child pages recursively.

This script demonstrates how to access all descendant pages of a specified wiki
page the pre-order way.
'''

from pyfluence import Wiki


if __name__ == '__main__':
    # Use the Confluence REST API wrapper.
    wiki = Wiki.from_functional_user(username='user', password='pass')

    # Navigate to the page using the page titles.
    use_cases_page = wiki['Space']['Page']

    # Iterate child pages recursively.
    for child in use_cases_page.iter_pages(recurse='pre_order'):
        print('  ' * child.level + child.title)
