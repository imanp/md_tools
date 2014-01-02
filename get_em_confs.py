#!/usr/bin/env python
import re
import shlex
from lib.md_tools import executeCommand

from lib.util import *

#TODO add feature to copernicus to fetch files bundled in zip

cmd = "cpcc cd %s"%getEmProjectName()
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

        with open("%s/%s"%(ProjectDirectories.EM_DIR,filename),"w") as f:
            f.write(res)

    index+=1




