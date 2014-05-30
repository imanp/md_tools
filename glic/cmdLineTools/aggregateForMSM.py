#!/usr/bin/env python
from argparse import ArgumentParser
import glob
import re
from shutil import copyfile

from lib.md_tools import executeCommand
from lib.util import *



#creates a folder named xtc, aggregates the data in a format that is expected for msmbuilder
#for easy backtracking each traj is suffixed with their project name

parser = ArgumentParser()
parser.add_argument("projects",nargs='*',
                    help="Path to projects that we want to include data from")

parser.add_argument("--trajtype",default='tmd_backbone',
                    help="Which of the processed trajectories that we wish to use (the subfolders in the analysis directory)")

args = parser.parse_args()

xtcDir = "XTC"
if not os.path.exists(xtcDir):
    executeCommand(["mkdir",'-p',xtcDir])

index=0

for projectDir in args.projects:

    regex = ".*/(.*)/"
    m = re.match(regex,projectDir)
    projectName = m.group(1)
    path = "%s/analysis/%s/"%(projectDir,args.trajtype)
    xtcs = "%s/*xtc"%(path)
    trajs = [os.path.basename(f) for f in sorted(glob.glob(xtcs))]

    for traj in trajs:
        src = "%s/%s"%(path,traj)
        #create dir structure for msmbuilder
        destDir = "%s/TRAJ%s"%(xtcDir,index)
        executeCommand(["mkdir",'-p',destDir])
        dest="%s/%s_%s"%(destDir,projectName,traj)
        index+=1
        executeCommand(["cp",src,dest])





