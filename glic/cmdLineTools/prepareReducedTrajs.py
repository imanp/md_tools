#!/usr/bin/env python
import glob
import re

from lib.md_tools import *
from lib.util import *


#gets trajectory files from a production workflow

#for each xtx in trajectories dir
#center and minimize into 1ns frames
 #check timesteps and nstxtcout to deduce this

#finds patterns like topol_5.tpr


def prepare(indexFile,selection,outputDir,suffix):
    #FIXME creating and index automatically does not work at the moment we get an error reading user input from gromacs. when running this
    if not os.path.exists(indexFile):
        firstConf="%s/%s"%(ProjectDirectories.CONF_DIR,FileNames.FIRST_CONF)
        args =["make_ndx","-f","%s"%firstConf, "-o","%s"%indexFile]
        executeInteractiveCommand(args,"%s \n q"%selection)


    regex = "(.*)_(\d).*"
    init = True
    for trajfile in glob.glob("%s/*xtc"%ProjectDirectories.ANALYSIS_FULL_DIR):
        #what index do we have?
        m = re.match(regex,trajfile)
        number = m.group(2)
        tpr = "topol_%s.tpr"%number
        outfile = "%s/%s_%s.xtc"%(outputDir,"traj_%s"%suffix,number)
        args=["trjconv","-s","%s/%s"%(ProjectDirectories.TPR_DIR,tpr),"-f", "%s"%trajfile, "-n", "%s"%indexFile ,"-o", "%s"%outfile]
        options = "24"  #indexgroup to center on and extract all atoms
        executeInteractiveCommand(args,options)

        if init:
            args=["trjconv","-dump","1000","-s","%s/%s"%(ProjectDirectories.TPR_DIR,tpr),"-f", "%s"%trajfile, "-n", "%s"%indexFile ,"-o", "%s/ref.pdb"%outputDir]
            options = "24"  #indexgroup to center on and extract all atoms
            executeInteractiveCommand(args,options)
            init=False



if not os.path.exists(ProjectDirectories.ANALYSIS_M2_DIR):
    os.makedirs(ProjectDirectories.ANALYSIS_M2_DIR)

if not os.path.exists(ProjectDirectories.ANALYSIS_TMD_DIR):
    os.makedirs(ProjectDirectories.ANALYSIS_TMD_DIR)

#create index file
m2IndexFile = "%s/%s"%(ProjectDirectories.ANALYSIS_M2_DIR,"index.ndx")
tmdIndexFile = "%s/%s"%(ProjectDirectories.ANALYSIS_TMD_DIR,"index.ndx")
tmd = "ri 197-315"
m2 = "ri 220-245"

if len(glob.glob("%s/*xtc"%ProjectDirectories.ANALYSIS_TMD_DIR))==0:
    prepare(tmdIndexFile,tmd,ProjectDirectories.ANALYSIS_TMD_DIR,'tmd')
if len(glob.glob("%s/*xtc"%ProjectDirectories.ANALYSIS_M2_DIR))==0:
    prepare(m2IndexFile,m2,ProjectDirectories.ANALYSIS_M2_DIR,"m2")







