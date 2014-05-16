#!/usr/bin/env python
import shlex

from lib.cpcUtil import CpcUtil
from lib.md_tools import executeCommand
from lib.util import *


#gets trajectory files from a production workflow

cmd = "cpcc cd %s"%getProjectName()
executeCommand(shlex.split(cmd))

if not os.path.exists(ProjectDirectories.TRAJ_DIR):
    os.makedirs(ProjectDirectories.TRAJ_DIR)

print "Fetching trajectories please wait"
files =CpcUtil.fetchData("mdrun.out.xtc",ProjectDirectories.TRAJ_DIR)

if len(files)>0:
    print "fetched %s trajectories. you can see the results in the %s"%(len(files),ProjectDirectories.TRAJ_DIR)

else:
    "No trajectories found"






