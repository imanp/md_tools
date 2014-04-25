#!/usr/bin/env python
from argparse import ArgumentParser
import lib.md_tools


'''
Filters away specified number of occurences of an atom.
Can operate on a list of files

'''

parser = ArgumentParser()
parser.add_argument("pdb",
                    help="pdb file")
parser.add_argument("--mutations",
                    help="A comma separated list of mutations to apply, ex: I233S,I240S")

args = parser.parse_args()

str = lib.md_tools.generateSequence(args.pdb,args.mutations)

print str