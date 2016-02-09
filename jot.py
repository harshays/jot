from __future__ import print_function
from datetime   import datetime as dt
from blessings  import Terminal
from utils      import JotCLI, JotConfig, JotUtils, FILE_DIR
import os 
import subprocess
import getpass
import pandas as pd

class Jot(object):

    funcs = {
        'count': lambda df, fp: int(len(df) + 1),
        'timestamp': lambda df, fp: dt.now().strftime(fp['timestamp_format']),
        'user': lambda df, fp: getpass.getuser()
    }

    def if_file_exists(func):
        'only call function if filename valid'
        def _func(*args, **kw):
            self, fname = args[0], args[1]
            if not self.utils.file_exists(fname):
                self.utils.prettyprint('No such file: '+fname, 'red')
                return
            return func(*args, **kw)
        return _func

    def __init__(self, config_path):
        self.config_obj  = JotConfig(config_path)
        self.jot_dir = self.config_obj.dir
        self.cfg_dir = self.config_obj.fpath
        self.cli     = JotCLI()
        self.utils   = JotUtils(self.jot_dir, '.csv')

    def parse_and_call(self):
        action, args = self.cli.parse()
        func = getattr(self, action, None)
        if func: return (func(*args) if isinstance(args, list) else func())
        self.prettyprint('No such action: '+action)

    def add(self, fname, msg):
        'jot'
        msg = msg.replace('\n', ' ').strip()
        columns = self.config_obj.get_file_cols(fname)
        fexists = self.utils.file_exists(fname)
        if not fexists: self.utils.prettyprint("Adding new file: "+fname, 'green')
        fpath = self.utils.get_fpath(fname)
        fprops = self.config_obj.get_file_config(fname)
        df = pd.read_csv(fpath, header=None) if fexists else pd.DataFrame(columns=columns)
        row = [self.funcs[col](df, fprops) for col in columns[:-1]] + [msg]
        df.loc[len(df)] = row
        self.utils.write_df(fname, df)

    @if_file_exists
    def view(self, fname):
        'view file content'
        df = pd.read_csv(self.utils.get_fpath(fname), header=None)
        df.columns = self.config_obj.get_file_cols(fname)
        print (df.to_string(index=False))

    @if_file_exists
    def reset(self, fname):
        'reset count, clean messages'
        fpath = self.utils.get_fpath(fname)
        columns = self.config_obj.get_file_cols(fname)
        df = pd.read_csv(fpath, header=None)
        df.columns = columns
        df['message'] = df['message'].str.strip().str.replace('\n', ' ')
        if 'count' in columns: df['count'] = pd.Series(range(1, len(df)+1))
        self.utils.write_df(fname, df)

    @if_file_exists
    def manual(self, fname):
        'open jot file in vim'
        fpath = self.utils.get_fpath(fname)
        os.system('vim {}'.format(fpath))

    def search(self, kw):
        'search for keywords in all files'
        for keyword in [k.strip() for k in kw.split(',')]:
            self.utils.prettyprint("Keyword: "+keyword, 'bold')
            grep = subprocess.Popen(['grep', '-Ri', keyword, self.jot_dir], stdout=subprocess.PIPE)
            for result in grep.stdout.readlines():
                fpath, msg = result.split(':', 1)
                msg = msg.replace('\n', '')
                fname = fpath.rsplit('/', 1)[-1].split('.')[0]
                print ('    {}: {}'.format(fname, msg))
            print ('\n')

    def list(self):
        'list all jot files'
        for num, jfile in enumerate(self.utils.all_files(), 1):
            self.utils.prettyprint('{}. {}'.format(num, jfile), 'bold')

    def config(self):
        'edit config in vim'
        os.system('vim {}'.format(self.cfg_dir))


def run():
    config_path = os.path.join(FILE_DIR, 'config.json')
    jot = Jot(config_path)
    jot.parse_and_call()

if __name__ == '__main__':
    run()




