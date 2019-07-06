# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup


class Table:
    def __init__(self, header, header_vertical=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__header = list(header)
        self.__header_vertical = header_vertical
        self.__body = list()

    @property
    def n_columns(self):
        return len(self.__header)

    @property
    def n_rows(self):
        return len(self.__body)

    def add_row(self, row):
        self.__body.append(row)

    def __str__(self):
        table = BeautifulSoup('<table class="relative-table" style="width:100%;"><colgroup></colgroup><tbody></tbody></table>', 'html.parser')
        width = 100. / self.n_columns
        for i in range(self.n_columns):
            table.colgroup.append(table.new_tag('col', style='width:{p:3.2f}%;'.format(p=width)))
        rotated = {'class': 'rotated'}
        table.tbody.append(table.new_tag('tr', **(rotated if self.__header_vertical else {})))
        for header_entry in self.__header:
            table.tbody('tr')[-1].append(table.new_tag('th'))
            table.tbody('tr')[-1]('th')[-1].string = header_entry
        for row in self.__body:
            table.tbody.append(table.new_tag('tr'))
            for column in row:
                table.tbody('tr')[-1].append(table.new_tag('td'))
                table.tbody('tr')[-1]('td')[-1].string = column

        return str(table)
