from __future__ import print_function
import os
import sys
import csv
import utils
from   utils import term, cfg, data, jotdir, files

def run_config():
    os.system('vim {}'.format(utils.cfg))
    sys.exit()

def run_list():
    print (term.bold, "All files:", term.normal)
    for f in sorted(os.listdir(jotdir)):
        print ('-', f.rsplit('.',1)[0])
    sys.exit()

def run_view(fname):
    fname_ = fname + '.csv'
    files = os.listdir(jotdir)
    if fname_ not in files:
        print (term.bold, "No such file: {}".format(fname), term.normal)
    else:
        fpath = os.path.join(jotdir, fname_)
        with open(fpath, 'r') as csvfile:
            content = list(csv.reader(csvfile))
            for ln, line in enumerate(content):
                attr, val = line[:-1], line[-1]
                print (ln + 1, ':', val)
    sys.exit()

def parse_args():
    args = utils.get_args()
    if args.config: run_config()
    if args.list:   run_list()
    if args.view:   run_view(args.view[0])
    return args.add

def get_file_info(fname, msg):
    if fname not in files:
        wn = "{}'{}' not in config. Using default properties.{}"
        print (wn.format(term.red, fname, term.normal))
    fprop = utils.get_file_properties(fname)
    return fname, msg, fprop

def update_file(fname, msg, fprop):
    pth = os.path.join(jotdir, fname+'.csv')
    if not os.path.exists(pth):
        count = 1
        print("{}creating new file '{}'{}".format(term.bright_blue, fname, term.normal))
    else:
        count = 1 + sum(1 for line in open(pth))
    info = []
    if fprop['include_count']: info.append(count)
    if fprop['include_timestamp']: info.append(fprop['timestamp'])
    if fprop['include_user']: info.append(fprop['user'])
    info.append(msg)
    with open(pth, 'a+') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(info)

def run():
    if not os.path.exists(jotdir):
        os.mkdir(jotdir)
    args = parse_args()
    info = get_file_info(*args)
    update_file(*info)

if __name__ == '__main__':
    run()
