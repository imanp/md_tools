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


parser = ArgumentParser()
parser.add_argument("title",help="Title of the plot")

args = parser.parse_args()

VMD ="/nethome/grant/.bin/vmd"

ANALYSIS_TOOLS_DIR="/data/iman/glic/analysis_tools"
HOLE_SCRIPTS_DIR="%s/hole_scripts"%ANALYSIS_TOOLS_DIR

analysisScript="%s/hole_scripts/pore_channel_xtc.tcl"%ANALYSIS_TOOLS_DIR


if not os.path.exists(ProjectDirectories.ANALYSIS_PORE_DIMENSION_DIR):
    os.makedirs(ProjectDirectories.ANALYSIS_PORE_DIMENSION_DIR)

if len(glob.glob("%s/*xtc"%ProjectDirectories.ANALYSIS_PORE_DIMENSION_DIR))>0:
    print "There is already files in directory %s please remove files and rerun script"%ProjectDirectories.ANALYSIS_FULL_DIR
    sys.exit(0)

index=0
for trajfile in glob.glob("%s/*xtc"%ProjectDirectories.ANALYSIS_FULL_DIR):
    print "running trajectory %s"%index
    gro = "%s/ref.gro"%ProjectDirectories.ANALYSIS_FULL_DIR
    xtc = trajfile

    datFile ="%s/%s_pore_dimension_%s.dat"%(ProjectDirectories.ANALYSIS_PORE_DIMENSION_DIR,getProjectName(),index)
    #change to hole scripts directory
    cmd =  "%s -dispdev text -e %s -args %s %s %s"%(VMD,analysisScript,gro,xtc,datFile)

    #executeCommand(shlex.split(cmd))

    title= "Pore Dimensions %s sample %s"%(args.title,index)
    outfile ="%s/%s_pore_dimension_%s.pdf"%(ProjectDirectories.ANALYSIS_PORE_DIMENSION_DIR,getProjectName(),index)
    cmd = """gnuplot -e "infile='%s'; outfile='%s' ; title='%s'" %s/plot_radius.sh"""%(datFile,outfile,title,os.environ['GLIC_TOOLS'])


    executeCommand(shlex.split(cmd))
    index+=1


