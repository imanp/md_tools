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


def prepare(indexFile,selection,outputDir,suffix,options="11",index=True,fromTrajs=ProjectDirectories.ANALYSIS_PROTEIN_DIR):
    if index:
        #FIXME creating and index automatically does not work at the moment we get an error reading user input from gromacs. when running this
        if not os.path.exists(indexFile):
            firstConf="%s/%s"%(ProjectDirectories.ANALYSIS_PROTEIN_DIR,"ref.pdb")
            args =["make_ndx","-f","%s"%firstConf, "-o","%s"%indexFile]
            executeInteractiveCommand(args,"%s \n q"%selection)


    regex = "(.*)_(\d*).*"
    init = True
    for trajfile in glob.glob("%s/*xtc"%fromTrajs):
        #what index do we have?
        m = re.match(regex,trajfile)
        number = m.group(2)
        tpr = "topol_%s.tpr"%number
        outfile = "%s/%s_%s.xtc"%(outputDir,"traj_%s"%suffix,number)
        args=["trjconv","-s","%s/%s"%(ProjectDirectories.TPR_DIR,tpr),"-f", "%s"%trajfile,"-o", "%s"%outfile]
        if index:
            args+=[ "-n", "%s"%indexFile ]

        executeInteractiveCommand(args,options)
        if init:
            args=["trjconv","-dump","1000","-s","%s/%s"%(ProjectDirectories.TPR_DIR,tpr),"-f", "%s"%trajfile,"-o", "%s/ref.pdb"%outputDir]
            if index:
                args+=["-n", "%s"%indexFile]
            executeInteractiveCommand(args,options)
            init=False



if not os.path.exists(ProjectDirectories.ANALYSIS_M2_DIR):
    os.makedirs(ProjectDirectories.ANALYSIS_M2_DIR)

if not os.path.exists(ProjectDirectories.ANALYSIS_TMD_DIR):
    os.makedirs(ProjectDirectories.ANALYSIS_TMD_DIR)

if not os.path.exists(ProjectDirectories.ANALYSIS_PROTEIN_DIR):
    os.makedirs(ProjectDirectories.ANALYSIS_PROTEIN_DIR)

if not os.path.exists(ProjectDirectories.ANALYSIS_TMD_BACKBONE_DIR):
    os.makedirs(ProjectDirectories.ANALYSIS_TMD_BACKBONE_DIR)

if not os.path.exists(ProjectDirectories.ANALYSIS_M2_BACKBONE_DIR):
    os.makedirs(ProjectDirectories.ANALYSIS_M2_BACKBONE_DIR)


#create index file
proteinIndexFile = "%s/%s"%(ProjectDirectories.ANALYSIS_PROTEIN_DIR,"index.ndx")
m2IndexFile = "%s/%s"%(ProjectDirectories.ANALYSIS_M2_DIR,"index.ndx")
tmdIndexFile = "%s/%s"%(ProjectDirectories.ANALYSIS_TMD_DIR,"index.ndx")
tmd = "r 197-217 | r 221-244 | r 254-281 | r 285-314 &! r 243 &! r 277"  #excluding loops!
m2 = "r 220-245"

if len(glob.glob("%s/*xtc"%ProjectDirectories.ANALYSIS_PROTEIN_DIR))==0:
    prepare(proteinIndexFile,tmd,ProjectDirectories.ANALYSIS_PROTEIN_DIR,'protein',options="1",index=False,fromTrajs=ProjectDirectories.ANALYSIS_FULL_DIR)
else:
    print "There is already files in directory %s please remove files and rerun script"%ProjectDirectories.ANALYSIS_PROTEIN_DIR


if len(glob.glob("%s/*xtc"%ProjectDirectories.ANALYSIS_TMD_DIR))==0:
    prepare(tmdIndexFile,tmd,ProjectDirectories.ANALYSIS_TMD_DIR,'tmd')
else:
    print "There is already files in directory %s please remove files and rerun script"%ProjectDirectories.ANALYSIS_TMD_DIR

if len(glob.glob("%s/*xtc"%ProjectDirectories.ANALYSIS_M2_DIR))==0:
    prepare(m2IndexFile,m2,ProjectDirectories.ANALYSIS_M2_DIR,"m2")
else:
    print "There is already files in directory %s please remove files and rerun script"%ProjectDirectories.ANALYSIS_M2_DIR


m2BackboneIndexFile = "%s/%s"%(ProjectDirectories.ANALYSIS_M2_BACKBONE_DIR,"index.ndx")
tmdBackboneIndexFile = "%s/%s"%(ProjectDirectories.ANALYSIS_TMD_BACKBONE_DIR,"index.ndx")
tmd_backbone = """r 197-217 | r 221-244 | r 254-281 | r 285-314 &! r 243 &! r 277 & "backb" """
m2_backbone = 'r 220-245 & "backb"'

if len(glob.glob("%s/*xtc"%ProjectDirectories.ANALYSIS_TMD_BACKBONE_DIR))==0:
    prepare(tmdBackboneIndexFile,tmd_backbone,ProjectDirectories.ANALYSIS_TMD_BACKBONE_DIR,"tmd_backbone")
else:
    print "There is already files in directory %s please remove files and rerun script"%ProjectDirectories.ANALYSIS_TMD_BACKBONE_DIR

if len(glob.glob("%s/*xtc"%ProjectDirectories.ANALYSIS_M2_BACKBONE_DIR))==0:
    prepare(m2BackboneIndexFile,m2_backbone,ProjectDirectories.ANALYSIS_M2_BACKBONE_DIR,"m2_backbone")
else:
    print "There is already files in directory %s please remove files and rerun script"%ProjectDirectories.ANALYSIS_M2_BACKBONE_DIR






