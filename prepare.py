#!/usr/bin/env python

from argparse import *
import glob
from shutil import copyfile

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


parser =ArgumentParser()
parser.add_argument("proteins",help="protein files, accepts wildcard selections only")
parser.add_argument("indexGroup",help="The index group to center the protein to the center of the simulation box",type=int)
args = parser.parse_args()
#should be run from a project directory


path = os.path.abspath(args.proteins)

os.chdir("confs")

files = glob.glob(path)

#go to the confs directory
filename  ="conf%s.pdb"
i = 1
for file in files:
    name = filename%i
    #note pdb2gmxoptions comes from util.membrane
    pdb2gmx(file,pdb2gmxOptions%name)


    mergePdb(name,"conf0.pdb")
    i+=1

#take everything but the protein protein part from conf0.gro



#take the original conf that we are using as a template, merge this protein with the template (non protein)
#center the protein
#and we are done!

cleanupBackups()

cmd= "rm *.pdb.* topol.top"
executeCommand(shlex.split(cmd))


cmd="rm *itp"
os.system(cmd)











