#!/usr/bin/env python

from argparse import *
import sys
from lib.util import *
from lib.md_tools import *
import os
'''
creates a copernicus project with the same name as this project
sets up an md workflow
submits all available structures to the workflow

Note: assumes there is file named grompp_em.mdp in the project file

 '''


if (not os.path.isfile(FileNames.GROMPP_EM)):
    print "File %s is required to proceed"%FileNames.GROMPP_EM
    sys.exit(1)


#fetch the project name
#assuming its the directory that we are running from
projectName = os.path.basename(os.getcwd())

cmd = "cpcc start %s_em"%projectName
executeCommand(shlex.split(cmd))


cmd="cpcc import gromacs"
executeCommand(shlex.split(cmd))
cmd="cpcc instance gromacs::grompp_multi grompp"
executeCommand(shlex.split(cmd))
cmd="cpcc instance gromacs::mdrun_multi mdrun"
executeCommand(shlex.split(cmd))


cmd ="cpcc transact"
executeCommand(shlex.split(cmd))
cmd="cpcc connect grompp:out.tpr mdrun:in.tpr"
executeCommand(shlex.split(cmd))


#maximum number of cores to user per simulation. if not set simulations will be tuned
cmd="cpcc set mdrun.in.resources[0].max.cores 24"
executeCommand(shlex.split(cmd))

cmd="cpcc setf grompp.in.top[+] topol.top"
executeCommand(shlex.split(cmd))
cmd ="cpcc setf grompp.in.mdp[+] %s"%FileNames.GROMPP_EM
executeCommand(shlex.split(cmd))

#this is a 2d array
cmd ="cpcc setf grompp.in.include[+][+] topol_Protein_chain_A.itp"

#needed for equilibrations
#cmd ="cpcc setf grompp.in.include[+][+] posre_Protein_chain_A.itp"
executeCommand(shlex.split(cmd))

for gro in os.listdir(ProjectDirectories.CONF_DIR):
    cmd="cpcc setf grompp.in.conf[+] %s/%s"%(ProjectDirectories.CONF_DIR,gro)
    executeCommand(shlex.split(cmd))

cmd="cpcc commit"
executeCommand(shlex.split(cmd))

cmd="cpcc activate"
executeCommand(shlex.split(cmd))






