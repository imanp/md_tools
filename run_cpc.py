#!/usr/bin/env python

from argparse import *
import glob
import sys
from lib.cpcUtil import CpcUtil
from lib.util import *
from lib.md_tools import *
import os
'''
creates a copernicus project with the same name as this project
sets up an md workflow
submits all available structures to the workflow

Note: assumes there is file named grompp_em.mdp in the project file

 '''


parser = ArgumentParser()
parser.add_argument("step",choices=['em','equi','prod'],help="what type of simulation to prepare")
parser.add_argument("-max",help="maximum number of cores for each run",default=24,type=int)
args = parser.parse_args()

maxCores = 24
print args
if args.max:
    maxCores = args.max



if args.step == "em":
    if (not os.path.isfile(FileNames.GROMPP_EM)):
        print "File %s is required to proceed"%FileNames.GROMPP_EM
        sys.exit(1)


    filePathList =  glob.glob("%s/%s"%(ProjectDirectories.CONF_DIR,"conf*.*"))
    filePathList = sorted_nicely(set(filePathList))

    CpcUtil.buildMDWorkflow(getEmProjectName(),FileNames.GROMPP_EM,filePathList,maxCores=maxCores)

elif args.step == "prod":
    if (not os.path.isfile(FileNames.GROMPP_PROD)):
        print "File %s is required to proceed"%FileNames.GROMPP_PROD
        sys.exit(1)


    filePathList =  glob.glob("%s/%s"%(ProjectDirectories.EQUILIBRATION_DIR,"conf*.*"))
    filePathList = sorted_nicely(set(filePathList))

    cmdLine = "\"-npme 42\""
    CpcUtil.buildMDWorkflow(getProjectName(),FileNames.GROMPP_PROD,filePathList,maxCores=maxCores,cmdLine=cmdLine)








