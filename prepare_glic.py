#!/usr/bin/env python

from argparse import *
import glic.glicTools as glicTools

from lib.membrane import *
#create a project

'''
#runs prepares a protein using pdb2gmx
#assumes a template system is created with membed and a file confs/conf0.gro is created
#merges the non protein part of the template with the protein

    inputs
        project name, the name of the project. a directory will be created in current dir
        index group (to center on)
'''

#note should only be run from within a project dir!


parser = ArgumentParser()
parser.add_argument("proteins",
                    help="protein files, accepts wildcard selections only")
parser.add_argument("indexGroup",help="The index group to center the protein to the center of the simulation box",type=int)
parser.add_argument("-m --mutations",help="mutations that we want to perform")
parser.add_argument("--ph",help="the ph value to start this system with",choices=glicTools.phChoices,default=glicTools.phChoices[1])
args = parser.parse_args()


if args.ph:
    protein,protonationStates = glicTools.getProtonationSelections(args.proteins,args.ph)

    args.protein = protein

createSystemsFromTemplate(args,protonationString=protonationStates)











