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



if not os.path.exists(ProjectDirectories.ANALYSIS_FULL_DIR):
    os.makedirs(ProjectDirectories.ANALYSIS_FULL_DIR)

#create index file
indexFile = "%s/%s"%(ProjectDirectories.ANALYSIS_FULL_DIR,"index.ndx")

#FIXME creating and index automatically does not work at the moment we get an error reading user input from gromacs. when running this
if not os.path.exists(indexFile):
    firstConf="%s/%s"%(ProjectDirectories.CONF_DIR,FileNames.FIRST_CONF)
    args =["make_ndx","-f","%s"%firstConf, "-o","%s"%indexFile]
    executeInteractiveCommand(args,"ri 229 \n q")

# cmd="cp %s/conf*0.pdb %s/ref.pdb"%(ProjectDirectories.CONF_DIR,ProjectDirectories.ANALYSIS_FULL_DIR)
# executeCommand(shlex.split(cmd))
regex = "(.*)_(\d*).*"
for trajfile in glob.glob("%s/*xtc"%ProjectDirectories.TRAJ_DIR):
    #what index do we have?
    m = re.match(regex,trajfile)
    number = m.group(2)
    tpr = "topol_%s.tpr"%number
    outfile = "%s/%s_%s.xtc"%(ProjectDirectories.ANALYSIS_FULL_DIR,"traj_full",number)
    print outfile
    args=["trjconv","-center","-pbc","mol","-ur","compact","-s","%s/%s"%(ProjectDirectories.TPR_DIR,tpr),"-f", "%s"%trajfile, "-n", "%s"%indexFile ,"-o", "%s"%outfile]
    options = "24 \n 0"  #indexgroup to center on and extract all atoms
    executeInteractiveCommand(args,options)



#get a pdb file to use also






