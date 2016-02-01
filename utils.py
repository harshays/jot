from __future__ import print_function

import os, sys
import copy
import getpass
import json
import csv

from argparse import ArgumentParser
from datetime import datetime as dt 
from blessings import Terminal

class JotCLI(object):
    'To parse CLI arguments'
    options = ('add', 'view', 'reset', 'manual', 'list', 'config')

    @staticmethod
    def get_parser():
        parser = ArgumentParser(description="Jot CLI")
        # arguments with parameters
        parser.add_argument('-a', '--add', nargs=2, help='Format: jot -a {{filename}} "{{content}}"')
        parser.add_argument('-v', '--view', nargs=1, help='View file content')
        parser.add_argument('-r', '--reset', nargs=1, help='Reset a jot file')
        parser.add_argument('-m', '--manual', nargs=1, help='Open jot file')
        # boolean arguments
        parser.add_argument('-l', '--list', action='store_true', help='List all files')
        parser.add_argument('-c', '--config', action='store_true', help='Open config file')
        return parser

    def __init__(self):
        self.parser = self.get_parser()
        self.args = None
        self.term = Terminal()

    def help_and_quit(self, msg):
        'print help and quit'
        print (msg)
        self.parser.print_help()
        sys.exit()

    def parse(self):
        'handle incorrect parses and return tuple of (arg, val)'
        self.args  = self.parser.parse_args()
        true_args  = filter(lambda op: bool(getattr(self.args, op)), self.options)
        if len(true_args) != 1: self.help_and_quit("Only provide one argument")
        return true_args[0], getattr(self.args, true_args[0])

class JotConfig(object):
    'To update and read jot\'s config file'
    pass

class JotUtils(object):
    'helper methods'
    pass