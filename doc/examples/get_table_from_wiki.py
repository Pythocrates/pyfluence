#! /usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Download tabular information from the wiki.

This script demonstrates how to retrieve a table from the wiki and extract
information from it.
'''

from pprint import pprint

from bs4 import BeautifulSoup

from pyfluence import Wiki


if __name__ == '__main__':
    # Use the high-level Confluence REST API wrapper.
    wiki = Wiki.from_chromium()

    # Get the PROJECT space.
    project_space = wiki.get_space(key='PROJECT')

    # Navigate to the page using the page titles.
    page = project_space['Page']

    # Print the content.
    soup = BeautifulSoup(page.content, 'lxml')

    # Get the first table, which is supposed to contain the information, and
    # extract the text..
    table = soup.find_all('table')[0]
    table_data = [
        [td.text for td in tr.find_all('td')]
        for tr in table.find_all('tr')]

    # We can also create a dict.
    info = dict((row[1], row[2:]) for row in table_data if row)
    pprint(info)
