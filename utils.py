from __future__ import print_function
import os 
import sys
import json
from   argparse  import ArgumentParser
from   blessings import Terminal

FILE_DIR = os.path.dirname(os.path.realpath(__file__))

class JotCLI(object):
    'To parse CLI arguments'
    options = ('add', 'view', 'reset', 'manual', 'search', 'list', 'config')

    @staticmethod
    def get_parser():
        parser = ArgumentParser(description="Jot CLI")
        # arguments with parameters
        parser.add_argument('-a', '--add', nargs=2, help='Format: jot -a {{filename}} "{{content}}"')
        parser.add_argument('-v', '--view', nargs=1, help='View file content')
        parser.add_argument('-r', '--reset', nargs=1, help='Reset a jot file')
        parser.add_argument('-m', '--manual', nargs=1, help='Open jot file')
        parser.add_argument('-s', '--search', nargs=1, help='search jot files using comma-separated keywords')
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
        print (self.term.bold+msg+self.term.normal)
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

    columns = ['count', 'timestamp', 'user']
    
    def __init__(self, fpath='./config.json'):
        self.fpath = fpath if fpath else os.path.join(FILE_DIR, 'config.json')
        self.cfg   = self.read_config()
        self.dir   = self.get_dir()

    def read_config(self):
        'read config json file'
        with open(self.fpath, 'r') as f:
            return json.load(f)

    def get_dir(self):
        'get jot folder path'
        d, f = [self.cfg['Jot'][x] for x in ['directory', 'folder_name']]
        return os.path.join(os.path.expanduser(d), f)

    def get_file_config(self, fname):
        'get file properties'
        keys = ['include_'+k for k in ['timestamp', 'count', 'user']] + ['timestamp_format']
        default = self.cfg['JotFiles']['default']
        default.update(self.cfg['JotFiles'].get(fname, {}))
        return {k:v for k,v in default.items() if k in keys}

    def get_file_cols(self, fname):
        'get file csv columns'
        fprops = self.get_file_config(fname)
        cols = [prop for prop in self.columns if fprops['include_'+prop]]
        cols.append('message')
        return cols

class JotUtils(object):
    'helper methods'

    def prettyprint(self, msg, msg_type='bold'):
        msg_type = getattr(self.term, msg_type)
        print (msg_type+msg+self.term.normal)

    def __init__(self, jot_dir, suffix):
        self.dir = jot_dir
        self.suffix = suffix
        self.term = Terminal()

    def get_fpath(self, fname, fld=None):
        'get file path'
        if not fld: fld = self.dir
        return os.path.join(fld, fname+self.suffix)

    def file_exists(self, fname, fld=None):
        'check if file exists'
        fpath = self.get_fpath(fname, fld)
        return os.path.exists(fpath)

    def write_df(self, fname, df):
        'write dataframe to csv file'
        fpath = self.get_fpath(fname)
        with open(fpath, 'w') as f:
            f.write(df.to_csv(index=False, header=None))

    def all_files(self):
        return [f for f in os.listdir(self.dir) if f.endswith(self.suffix)]
