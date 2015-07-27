#!/usr/bin/env python
from argparse import ArgumentParser
import lib.md_tools
from lib.md_tools import *

'''
Filters away specified number of occurences of an atom.
Can operate on a list of files

'''

parser = ArgumentParser()
parser.add_argument("pdb",
                    help="pdb file")

parser.add_argument("-o",
                    help="output file name")

args = parser.parse_args()

if not args.o:
    output = "conf_no_vsites.pdb"

else:
    output = args.o

f = open(args.pdb,"r")
str = strip_vsites(f.read())

with open(output,"w") as out:
    out.write(str)


print "Done. Files saved as %s"%output