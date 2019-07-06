# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod
from argparse import ArgumentParser


class Application(object):
    '''
    This is the base class for Confluence applications coming with the basic
    available authentication options.
    '''
    __metaclass__ = ABCMeta

    def __init__(self, *args, **kwargs):
        super(Application, self).__init__(*args, **kwargs)
        self.build_parser()
        # TODO: remove args -> property is defined below
        args = self._args = self.parser.parse_args()
        if bool(args.user) ^ bool(getattr(args, 'pass')):
            self.parser.error('--user and --pass must be given together')

        # Use the Confluence REST API wrapper.
        if args.user:
            self._app = self._app_class.from_functional_user(
                username=args.user, password=getattr(args, 'pass'))
        elif args.chromium:
            self._app = self._app_class.from_chromium()
        elif args.firefox:
            self._app = self._app_class.from_firefox()

    @property
    def args(self):
        return self._args

    @property
    def parser(self):
        return self._parser

    def build_parser(self):
        '''
        Create a parser expecting the correct options and parameters.
        '''
        self._parser = ArgumentParser()
        cred_group = self._parser.add_mutually_exclusive_group(required=True)
        cred_group.add_argument(
            '-c', '--chromium', action='store_true',
            help='use Chromium session')
        cred_group.add_argument(
            '-f', '--firefox', action='store_true',
            help='use Firefox session')
        cred_group.add_argument(
            '-u', '--user', type=str,
            help='user name for password authentication')
        self._parser.add_argument(
            '-p', '--pass', type=str,
            help='password for password authentication')

    @abstractmethod
    def run(self):
        '''
        This function contains the main functionality of the application.
        '''
