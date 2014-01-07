#!/usr/bin/env python
from argparse import ArgumentParser
import glob
from lib.md_tools import sorted_nicely
from lib.pdb_util import removeAtom
from lib.versionFile import versionFile


'''
Filters away specified number of occurences of an atom.
Can operate on a list of files

'''

parser = ArgumentParser()
parser.add_argument("pdb",
                    help="list of pdb files, accepts wildcard selections only")
parser.add_argument("atom",
                    help="the atom name to remove")
parser.add_argument("num",
                    help="number of occurences to remove",type=int)

args = parser.parse_args()

files = glob.glob(args.pdb)

files = sorted_nicely(set(files))

for file in files:
    versionFile(file)
    str = removeAtom(file,args.atom,args.num)
    with open(file,"w") as f:
        f.write(str)

