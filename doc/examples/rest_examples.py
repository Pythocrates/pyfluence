#! /usr/bin/env python3
# -*- coding: utf-8 -*-

'''This script shows some of the different access possibilities of the
low-level wiki wrapper.

The input and output is quite raw and requires some knowledge of the REST API.
'''

from pprint import pprint

from pyfluence import Session


if __name__ == '__main__':

    # Use of the REST API:
    session = Session.from_chromium()
    wiki = session.wiki

    pprint(wiki.content.GET().json())
    pprint(wiki.space.GET().json())
    pprint(wiki.space.PROJECT.GET().text)
    pprint(wiki.space.PROJECT.GET().json())
    pprint(wiki.space.PROJECT.property.GET().json())
    pprint(wiki.space.PROJECT.content.GET().json())
    pprint(wiki.space.PROJECT.content.page.GET(expand='children'))
    pprint(wiki.user.memberof.GET(username='my user').json())

    attachment = wiki.content[343966847].child.attachment.GET(filename='my file').json()
    pprint(attachment['results'][0]['_links']['download'])
    pprint(attachment.keys())

    pprint(wiki.space.PROJECT.content.page.GET().json())
    pprint(wiki.content[343966847].child.page.GET().json())
    pprint(wiki.content[378011688].child.page.GET().json())
    pprint(wiki.content[378011688].child.page.GET().json()['results'][2]['id'])
    html = wiki.content[421889516].GET(
        expand='body.storage').json()['body']['storage']['value']

    # Use BeautifulSoup to extract the table from HTML.
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, 'lxml')
    tables = soup.find_all('table')
    pprint(tables)

    # Download an attachment using the session authorization.
    session.download(
        'https://{}.{}/download/attachments/343966847/wiki.png?api=v2')
    # ... or use a different file name.
    session.download(
        'https://{}.{}/download/attachments/343966847/wiki.png?api=v2',
        file_path='test.png')
