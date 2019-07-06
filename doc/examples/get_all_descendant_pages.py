#! /usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Iterate over all child pages recursively.

This script demonstrates how to access all descendant pages of a specified
Confluence wiki page the pre-order way.
'''


from pyfluence import Wiki


if __name__ == '__main__':
    # Use the Confluence REST API wrapper.
    wiki = Wiki.from_chromium()

    # TODO: Navigate to the page using the page TinyUI (next time).
    use_cases_page = wiki['My Page']

    # Iterate child pages recursively.
    for child in use_cases_page.iter_pages(recurse='pre_order'):
        print('  ' * child.level + child.title)
