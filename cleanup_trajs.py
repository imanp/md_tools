#!/usr/bin/env python
import shlex

from lib.cpcUtil import CpcUtil
from lib.md_tools import executeCommand
from lib.util import *


#gets trajectory files from a production workflow

 #removes the trajectories in the traj dir.
 #useful since they already exist in copernicus and we only need them temporarily for creating analysis trajs



cmd = "rm %s/*"%ProjectDirectories.TRAJ_DIR
if executeCommand(shlex.split(cmd)):
    print "trajectories removed"






