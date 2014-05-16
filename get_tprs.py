#!/usr/bin/env python
import re
import shlex
from lib.md_tools import executeCommand

from lib.util import *

#gets tpr files from a production workflow

cmd = "cpcc cd %s"%getProjectName()
executeCommand(shlex.split(cmd))


cmd = "cpcc get mdrun.in.tpr"
res = executeCommand(shlex.split(cmd))

lines = res.split("\n")

#remove first and two last lines
del(lines[0])
del(lines[-1])
del(lines[-1])


index = 0
regex =r"(.*)\.(.*)"

if not os.path.exists(ProjectDirectories.TPR_DIR):
    os.makedirs(ProjectDirectories.TPR_DIR)

#TODO use CpcUtil.fetchData()
for line in lines:
    filename = line.strip().strip(",").split("/")[-1]
    if filename!="None":  #yes this is a none string from the terminal output
        m = re.match(regex,filename)
        filename = "%s_%s.%s"%(m.group(1),index,m.group(2))
        print filename
        cmd = "cpcc getf mdrun.in.tpr[%s]"%index
        res = executeCommand(shlex.split(cmd))

        with open("%s/%s"%(ProjectDirectories.TPR_DIR,filename),"w") as f:
            f.write(res)

    index+=1




