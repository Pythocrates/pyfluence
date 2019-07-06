# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup


class Cell(list):
    class Text:
        def __init__(self, text):
            super().__init__()
            self.__text = text

        def html(self, soup):
            return self.__text

    class Link:
        def __init__(self, ref, name):
            super().__init__()
            self.__ref = ref
            self.__name = name

        def html(self, soup):
            link = soup.new_tag('a')
            link['href'] = self.__ref
            link.string = self.__name
            return link

    def add_text(self, text):
        self.append(self.Text(text=text))
        return self

    def add_link(self, ref, name=None, sep=', '):
        if len(self):
            self.add_text(sep)
        self.append(self.Link(ref=ref, name=name or ref))
        return self


class HTMLTable:
    def __init__(self, header, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__header = header
        self.__body = list()

    @property
    def n_rows(self):
        return len(self.__body)

    @property
    def n_cols(self):
        return len(self.__header)

    def add_empty_row(self):
        self.__body.append([Cell() for i in self.__header])

    def add_row(self, row_values):
        self.__body.append([Cell().add_text(value) for value in row_values])

    def __getitem__(self, index):
        return self.__body[index]

    def html(self):
        # We provide our own soup.
        soup = BeautifulSoup(
            '''<table class="relative-table" style="width:100%">
            <colgroup></colgroup><tbody></tbody></table>''',
            'html.parser')
        table = soup.table
        colgroup = table.colgroup
        table.tbody.append(soup.new_tag('tr'))
        header = table.tbody.tr
        width = 100. / self.n_cols
        for col in self.__header:
            colgroup.append(
                soup.new_tag('col', style='width:{p:3.2f}%'.format(p=width)))
            header.append(soup.new_tag('th'))
            for item in col:
                header('th')[-1].append(item)

        for row in self.__body:
            table.tbody.append(soup.new_tag('tr'))
            tr = table.tbody('tr')[-1]
            for col in row:
                tr.append(soup.new_tag('td'))
                td = tr('td')[-1]
                for item in col:
                    td.append(item.html(soup=soup))

        return soup.prettify()
