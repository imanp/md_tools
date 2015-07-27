#!/usr/bin/env python
from argparse import ArgumentParser
import re
import shlex
from lib.md_tools import executeCommand

from lib.util import *

#TODO add feature to copernicus to fetch files bundled in zip

parser = ArgumentParser()
parser.add_argument("step",choices=['em','equi','prod'],help="what type of simulation to fetch confs for")
args = parser.parse_args()


if args.step == 'em':
    cmd = "cpcc cd %s"%getEmProjectName()

if args.step == 'equi':
    cmd = "cpcc cd %s"%getEquiProjectName()

if args.step == 'prod':
    cmd = "cpcc cd %s"%getProjectName()


executeCommand(shlex.split(cmd))


cmd = "cpcc get mdrun.out.conf"
res = executeCommand(shlex.split(cmd))

lines = res.split("\n")

#remove first and two last lines
del(lines[0])
del(lines[-1])
del(lines[-1])


index = 0
regex =r"(.*)\.(.*)"


for line in lines:
    filename = line.strip().strip(",").split("/")[-1]
    if filename!="None":  #yes this is a none string from the terminal output
        m = re.match(regex,filename)
        filename = "%s_%s.%s"%(m.group(1),index,m.group(2))
        cmd = "cpcc getf mdrun.out.conf[%s]"%index
        res = executeCommand(shlex.split(cmd))

        if args.step == 'em':
            dir = "%s/%s"%(ProjectDirectories.EM_DIR,filename)

        if args.step == 'equi':
            cmd = "%s/%s"%(ProjectDirectories.EQUILIBRATION_DIR,filename)

        if args.step == 'prod':
            cmd = "%s/%s"%(ProjectDirectories.PROD_DIR,filename)

        with open(dir,"w") as f:
            f.write(res)

    index+=1




