#!/usr/bin/env python

from argparse import *
from membrane import *
from shutil import copyfile

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


parser =ArgumentParser()
parser.add_argument("projectName",help="the name of the project")
parser.add_argument("protein",help="A pdb file of your protein structure")
parser.add_argument("index",help="A gromacs ndx file")
parser.add_argument("indexGroup",help="The index group to center the protein to the center of the simulation box",type=int)
parser.add_argument("-m --mutations",help="mutations that we want to perform")
parser.add_argument("-ps --protonation_states",help="a string with the protonation state selections")
args = parser.parse_args()


#project initialization
indexFile = "index.ndx"
protein = "protein.pdb"

os.mkdir(args.projectName)
copyfile(args.index,"%s/%s"%(args.projectName,indexFile))
copyfile(args.protein,"%s/%s"%(args.projectName,protein))

os.chdir(args.projectName)

#embed one protein
embedProteinIntoMembrane(protein,indexFile,args.indexGroup)

runMembedSim()
#now run g_membed

#now do grompp again to get the real tpr



#we know have one protein embedded into the membrane
'''if more protein structures are provided (assuming from the same protein)

extract the non protein part from the previous structure
for each protein, center it and concatenate with the non protein pdb.
this should hopefully give as u descent structure.
perhpaps we need to translate it a bit too.

'''



