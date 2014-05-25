#!/usr/bin/env python

from argparse import *
from shutil import *
import sys

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


parser =ArgumentParser()
parser.add_argument("projectName",help="the name of the project")
parser.add_argument("-restart",help="remove old project dir if one already exists",action='store_true')
args = parser.parse_args()


if(os.path.isdir(args.projectName) and args.restart==False):
    print "Project %s please use the -restart flag to overwrite it"%args.projectName
    sys.exit(0)

if(args.restart):
    print "Found previous project named:%s removing it"
    rmtree(args.projectName)

print "Creating project %s"%args.projectName
os.mkdir(args.projectName)
os.chdir(args.projectName)
os.mkdir(ProjectDirectories.MEMBED_DIR)
os.mkdir(ProjectDirectories.EM_DIR)
os.mkdir(ProjectDirectories.EQUILIBRATION_DIR)
os.mkdir(ProjectDirectories.RUN_DIR)
os.mkdir(ProjectDirectories.CONF_DIR)
os.mkdir(ProjectDirectories.TPR_DIR)
os.mkdir(ProjectDirectories.TRAJ_DIR)
os.mkdir(ProjectDirectories.ANALYSIS_DIR)
with open(FileNames.PROJ_INFO,"w") as f:
    f.write(args.projectName)



print "Project %s created."%args.projectName