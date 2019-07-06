#! /usr/bin/env python3
# -*- coding: utf-8 -*-

'''Generate a table of Confluence user group memberships.

This script demonstrates how to read user information for specified
Conflucence users and how to compile this information into a table in a
pre-existing wiki page. This script overwrites the existing page!
'''

import logging

from pyfluence.high_level.table import Table
from pyfluence.application import WikiApplication


FORMAT = '[%(levelname)s] %(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('MembershipReporter')
logger.setLevel(logging.DEBUG)


class GroupMembershipReporter(WikiApplication):
    def build_parser(self):
        super().build_parser()
        self.parser.add_argument(
            '-P', '--prefix', type=str,
            help='the prefix of the groups to be consulted', required=True)
        self.parser.add_argument(
            '-o', '--output', type=str,
            help='the tinyUI of the report page', required=True)

    def run(self):
        '''
        Find all matching groups and their members, and create a report table.
        '''
        groups = set()
        has_more_results = True
        start_index = 0
        index_step = 1000
        while has_more_results:
            response = self.wiki.raw.group.GET(
                start=start_index,
                limit=index_step).json()
            groups.update(
                g['name']
                for g in response['results']
                if g['name'].startswith(self.args.prefix))
            has_more_results = 'next' in response['_links']
            start_index += index_step
        logger.debug('Fetched the groups.')

        users = set()
        for group in groups:
            response = self.wiki.raw.group[group].member.GET(
                limit=index_step).json()
            users.update(u['username'] for u in response['results'])
        logger.debug('Fetched the group users.')

        all_groups = set()
        user_groups = dict()
        for m in users:
            user_groups[m] = [
                i['name']
                for i in
                self.wiki.raw.user.memberof.GET(username=m).json()['results']]
            all_groups.update(user_groups[m])
        logger.debug('Compiled membership information.')

        all_groups = sorted(all_groups)
        logger.info(
            'Found {0} groups and {1} users.'.format(len(groups), len(users)))

        # Create a raw HTML table.
        users = sorted(users, key=lambda x: x.upper())
        table = Table(header=['Group'] + users, header_vertical=True)
        for group in all_groups:
            table.add_row(
                [group] + [
                    ('x' if group in user_groups[u] else '-')
                    for u in users])
        logger.debug('Created table.')

        report_page = self.wiki.get_page_by_tinyui(self.args.output)
        report_page.content = table
        logger.debug('Uploaded table.')


if __name__ == '__main__':
    GroupMembershipReporter().run()
