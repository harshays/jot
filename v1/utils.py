from __future__ import print_function

import json
import os
import copy
import getpass
import sys

from argparse  import ArgumentParser
from datetime  import datetime as dt
from blessings import Terminal

def get_data(fname):
    with open(fname, 'r') as f:
        data = json.load(f)
    return data

def get_dir(dir_name, folder_name):
    directory = os.path.expanduser(dir_name)
    folder_path = os.path.join(directory, folder_name)
    return folder_path

def get_config_path(config_name):
    dirn = os.path.dirname(os.path.abspath(__file__))
    pth = os.path.join(dirn, config_name)
    return pth

def get_parser():
    parser = ArgumentParser(description="Jot CLI")
    parser.add_argument('-a', '--add', nargs=2, help='Format: jot -a {{filename}} "{{content}}"')
    parser.add_argument('-c','--config', action='store_true', help='Change config')
    parser.add_argument('-l', '--list', action='store_true', help='List all file')
    parser.add_argument('-v', '--view', nargs=1, help='View file content')
    return parser

def get_args():
    parser = get_parser()
    try:
        args = parser.parse_args()
        options = list(map(bool, [args.config, args.add, args.list, args.view]))
        if sum(options) != 1:
            raise SystemExit
        return args
    except SystemExit:
        print ("{}invalid format, try again or".format(term.red),
                "enter jot --help{}".format( term.normal))
        sys.exit()

term   = Terminal()
cfg    = get_config_path('config.json')
data   = get_data(cfg)
jotdir = get_dir(data['Jot']['directory'], data['Jot']['folder_name'])
files  = data['JotFiles']

def get_file_properties(fname):
    dct = files['default'].copy()
    if fname in files:
        dct.update(files[fname])
    dct['timestamp'] = dt.now().strftime(dct['timestamp_format'])
    dct['user'] = getpass.getuser()
    return dct
