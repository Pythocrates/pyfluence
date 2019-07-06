#! /usr/bin/env python3
# -*- coding: utf-8 -*-

'''
This script produces a plot of interdependencies of PROJECT JIRA issues.

It demonstrates how to use a JQL query and how to assemble a graph for
visualization purposes. The resulting plot is created in two formats: the
well-known PDF and the human-readable intermediate format DOT, which is used by
the graphviz application/module to generate graphs in different formats. It can
be also displayed in wiki pages using the appropriate macro.
'''

import pygraphviz as gv

from pyfluence import Session, Wiki


if __name__ == '__main__':
    # Create a session from the Chromium session credentials and use the derived JIRA instance.
    jira = Session.from_chromium().jira

    # We need a query.
    query = 'project=PROJECT&maxResults=1000'

    # Get list of all project issues.
    issues = (
        i for i in jira.search.GET(jql=query).json()['issues']
        if i['fields']['issuelinks'])

    # Create a DAG oriented from left to right.
    g = gv.AGraph(directed=True, name='Issues', rankdir='LR')

    for issue in issues:
        for link in issue['fields']['issuelinks']:
            # Not knowing a priori what kind of link this is, we just try both.
            try:
                g.add_edge(
                    issue['key'],
                    link['outwardIssue']['key'],
                    label=link['type']['outward'])
            except KeyError:
                g.add_edge(
                    issue['key'],
                    link['inwardIssue']['key'],
                    label=link['type']['inward'])

    # Generate files.
    g.draw('issues.dot', format='dot', prog='dot')
    g.draw('issues.pdf', format='pdf', prog='dot')

    # Update the wiki page attachment.
    wiki = Wiki.from_chromium()
    dependency_graph = wiki['my page'] > 'issues.dot'
    dependency_graph.upload(file_path='issues.dot')
