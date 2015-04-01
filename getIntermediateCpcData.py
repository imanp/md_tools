#!/usr/bin/env python
from argparse import ArgumentParser
import glob
import re

__author__ = 'iman'

from lib.md_tools import *
from lib.util import *
#given a cpc project dir
# go throught all mdrun blocks and concatenate their trajectories


parser = ArgumentParser()
parser.add_argument("projectDir",help="Project directory")
args = parser.parse_args()

simulations = glob.glob("%s/mdrun/mdrun_*"%args.projectDir)

regex = ".*mdrun_(\d).*"
for sim in simulations:
    m = re.match(regex,sim)
    num = m.group(1)
    outfile = "traj_%s.xtc"%num
    if not os.path.exists(outfile):
        trajs = glob.glob("%s/_persistence/run_*/*xtc"%(sim))
        trajs = [traj for traj in trajs if os.stat(traj).st_size>0 ]
        if len(trajs)>0:
            trajs = sorted(trajs)
            cmd = ["trjcat","-f"]
            cmd.extend(trajs)
            cmd.extend(["-o",outfile])
            executeCommand(cmd)