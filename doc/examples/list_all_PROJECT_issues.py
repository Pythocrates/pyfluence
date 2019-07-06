#! /usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Access JIRA information.

This script demonstrates how to retrieve different types of information from
JIRA using the low-level JIRA wrapper. The data retrieved are in JSON format
and can be examined by accessing the raw JSON fields.
'''

from pprint import pprint

from pyfluence import Session


if __name__ == '__main__':
    # Create a session from the Chromium session credentials and use the
    # derived JIRA instance.
    jira = Session.from_chromium().jira

    # Get project information.
    print('#### Information about project PROJECT: ####')
    pprint(jira.project.PROJECT.GET().json())

    # Get list of all project issues.
    issues = jira.search.GET(
        jql='project=PROJECT&maxResults=1000').json()['issues']

    pprint(issues[0])
    print(len(issues))

    # Get information on one issue.
    pprint(jira.issue['PROJECT-250'].GET().json())
