#!/usr/bin/env python

from argparse import *
from shutil import *

from lib.membrane import *
from lib.util import *

#create a project

'''
    inputs
        project name, the name of the project. a directory will be created in current dir
        structure(s) only proteins!
        index file (needed to center the protein)
        index group (to center on)
        mutations (optional)
        protonation states (optional)
'''

#assuming we are in project dir

parser =ArgumentParser()
parser.add_argument("protein",help="A pdb file of your protein structure")
parser.add_argument("indexGroup",help="The index group to center the protein to the center of the simulation box",type=int)
parser.add_argument("-index",help="A gromacs ndx file")
parser.add_argument("-m --mutations",help="mutations that we want to perform")
parser.add_argument("-ps --protonation_states",help="a string with the protonation state selections")
args = parser.parse_args()



runMembedSim(args)