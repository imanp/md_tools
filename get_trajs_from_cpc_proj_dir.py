#!/usr/bin/env python
from argparse import ArgumentParser
import glob
import re

from lib.md_tools import executeCommand
from lib.util import *



#gets trajectory files from a production workflow

parser = ArgumentParser()
parser.add_argument("cpcProjectDir",
                    help="path to the project directory")

args = parser.parse_args()

projectDir = "%s/%s"%(args.cpcProjectDir,getProjectName())

#list all files in
mdruns = glob.glob("%s/mdrun/mdrun_*"%projectDir)
mdruns = sorted(mdruns)


if not os.path.exists(ProjectDirectories.TRAJ_DIR):
    os.makedirs(ProjectDirectories.TRAJ_DIR)


regex = ".*mdrun_(\d*)"
for dir in mdruns:
    #get the mdrun number
    m = re.match(regex,dir)
    number = m.group(1)
    runs = "%s/_persistence/*run_*/*xtc"%(dir)
    xtc = []

    for f in glob.glob(runs):
        st=os.stat(f)
        if st.st_size>0:
            xtc.append(f)
    if len(xtc)==0:
        print "no runs found in %s"%runs
    else:
        outfile = "%s/traj_%s.xtc"%(ProjectDirectories.TRAJ_DIR,number)
        xtc = sorted(xtc)
        cmd = ["trjcat" , "-f"] + xtc +["-o",outfile]
        executeCommand(cmd)


        #do a trjcat here and store it in the tpr dir


# for dir in mdruns:
#     #get the mdrun number
#     m = re.match(regex,dir)
#     number = m.group(1)
#     tpr = "%s/_persistence/run_001/topol.tpr"%(dir)
#
#
#     tprout = "topol_%s.tpr"%number
#     cmd = ["cp" ,tpr,"%s/%s"%(ProjectDirectories.TPR_DIR,tprout)]
#     executeCommand(cmd)
#

        #do a trjcat here and store it in the tpr dir

