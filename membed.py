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



#project initialization
indexFile=None
protein = "protein.pdb"

#if we have a project we will simply rerun int
#TODO add checkpointing steps
if(args.index):
    indexFile = "index.ndx"
    copyfile(args.index,indexFile)

copyfile(args.protein,protein)


embedProteinIntoMembrane(protein,args.indexGroup,indexFile=indexFile)
runMembedSim()

membeddedFile = "membedded.gro"

updateWaterAndIonCount(membeddedFile,"topol.top")
updateMembraneCount("POPC",membeddedFile,"topol.top")

centerProtein(args.indexGroup,membeddedFile,output=membeddedFile)

#create a pdb file as output

cmd = "editconf -f %s -o %s/%s"%(membeddedFile,ProjectDirectories.CONF_DIR,"conf0.gro")
executeCommand(shlex.split(cmd))

#copyfile(membeddedFile,"%s/%s"%(ProjectDirectories.CONF_DIR,"conf0.gro"))

print("""Structure is embedded into membrane. The file can be found in %s/%s\n \
    Topology is updated to reflect this file\n
      Note that you might need to some more stuff before running the actual simulation \n
      Your system might have a charge imbalance for example.
      """)%(ProjectDirectories.CONF_DIR,"conf0.gro")