#! /usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Download the storage representation of a page content.

This script demonstrates how to get the HTML code of an wiki page from its
path.
'''

from pprint import pprint

from bs4 import BeautifulSoup

from pyfluence import Wiki


if __name__ == '__main__':

    # Use the Confluence REST API wrapper.
    wiki = Wiki.from_chromium()

    # Get the PROJECT space.
    project_space = wiki.get_space(key='PROJECT')

    # Navigate to the page using the page titles.
    my_page = project_space['Page1']['Page2']

    # Print the content.
    pprint(BeautifulSoup(my_page.content, 'lxml').prettify())
