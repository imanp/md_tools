#!/usr/bin/env python


#cals the pore_channel tcl script for each simulation and stores the results
#the pore_channel script calculates the pore dimension

#given a gro file and an xtc for a glic system this script will calculate the pore radius of M@
from argparse import ArgumentParser
import glob

import os
import sys

from lib.md_tools import *
from lib.util import *
import numpy as np


#note should be run from the same folder as you are holding your msm files
parser = ArgumentParser()
parser.add_argument("title",help="Title of the plot")
parser.add_argument("clustersDir",help="folder with xtc files, one for each cluster,for proper sorting file names \
                                       are expected to follow the convention State_NUM.xtc")

args = parser.parse_args()

VMD ="/nethome/grant/.bin/vmd"

ANALYSIS_TOOLS_DIR="/data/iman/glic/analysis_tools"
HOLE_SCRIPTS_DIR="%s/hole_scripts"%ANALYSIS_TOOLS_DIR

analysisScript="%s/hole_scripts/pore_channel_xtc.tcl"%ANALYSIS_TOOLS_DIR


PORE_DIMENSIONS_DIR = "pore_dimensions"
if not os.path.exists(PORE_DIMENSIONS_DIR):
    os.makedirs(PORE_DIMENSIONS_DIR)


index=0
clusterXTCs = glob.glob("%s/*xtc"%args.clustersDir)
clusterXTCs.sort()
for trajfile in clusterXTCs:
    print "running trajectory %s"%index
    gro = "ref.gro"
    xtc = trajfile

    datFile ="%s/cluster_%s_pore_dimension.dat"%(PORE_DIMENSIONS_DIR,index)
    #change to hole scripts directory
    cmd =  "%s -dispdev text -e %s -args %s %s %s"%(VMD,analysisScript,gro,xtc,datFile)
    print cmd
    executeCommand(shlex.split(cmd))

    title= "Pore Dimensions %s cluster %s"%(args.title,index)
    outfile ="%s/cluster_%s_pore_dimension.png"%(PORE_DIMENSIONS_DIR,index)
    cmd = """gnuplot -e "infile='%s'; outfile='%s' ; title='%s'" %s/plot_radius.sh"""%(datFile,outfile,title,os.environ['GLIC_TOOLS'])

    executeCommand(shlex.split(cmd))

    index+=1


