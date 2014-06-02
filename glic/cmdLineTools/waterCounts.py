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
parser.add_argument("title",help="Type in the name of the system")

args = parser.parse_args()

VMD ="/nethome/grant/.bin/vmd"


analysisScript="%s/count_waters.tcl"%os.environ['GLIC_TOOLS']


if not os.path.exists(ProjectDirectories.ANALYSIS_WATER_COUNT_DIR):
    os.makedirs(ProjectDirectories.ANALYSIS_WATER_COUNT_DIR)

# if len(glob.glob("%s/*dat"%ProjectDirectories.ANALYSIS_WATER_COUNT_DIR))>0:
#     print "There is already files in directory %s please remove files and rerun script"%ProjectDirectories.ANALYSIS_WATER_COUNT_DIR
#     sys.exit(0)

index=0
# for trajfile in glob.glob("%s/*xtc"%ProjectDirectories.ANALYSIS_FULL_DIR):
#     print "running trajectory %s"%index
#     gro = "%s/ref.gro"%ProjectDirectories.ANALYSIS_FULL_DIR
#     xtc = trajfile
#
#     datFile ="%s/%s_water_count_%s.dat"%(ProjectDirectories.ANALYSIS_WATER_COUNT_DIR,getProjectName(),index)
#     #change to hole scripts directory
#     cmd =  "%s -dispdev text -e %s -args %s %s %s"%(VMD,analysisScript,gro,xtc,datFile)
#
#     executeCommand(shlex.split(cmd))
#     index+=1



gnuplotInput = []
print "Generating plot"
# gnuplotInput.append('set title "#water between residues 230 and 235 %s"'%args.title)
gnuplotInput.append(""" set ylabel "#water" font "Arial, 8"  """)
gnuplotInput.append("unset xlabel")
gnuplotInput.append("set format x '' ")
gnuplotInput.append("unset key")
gnuplotInput.append("set term pdf enhanced")
outfile = "%s/%s_water_count.pdf"%(ProjectDirectories.ANALYSIS_WATER_COUNT_DIR,getProjectName())
gnuplotInput.append('set output "%s"'%outfile)
gnuplotInput.append("set yrange [0:60]")
gnuplotInput.append("set xrange [0:1000]")
gnuplotInput.append("set ytics 0,10,100 ")
gnuplotInput.append("""set xtics font "Arial, 8" """)
gnuplotInput.append("""set ytics font "Arial, 8" """)
gnuplotInput.append("set mytics 2")
gnuplotInput.append("set mxtics 2")
datFiles = glob.glob("%s/*dat"%ProjectDirectories.ANALYSIS_WATER_COUNT_DIR)
gnuplotInput.append("""set multiplot layout %s,1 title "%s" """%(len(datFiles),args.title))

index = 1

for f in datFiles:

    if len(datFiles) == index:
        # gnuplotInput.append('set xlabel "time (ns)"')
        # gnuplotInput.append("set format x '%g' ")
        pass



    gnuplotInput.append('plot "%s" using ($0*0.5):1 with lines smooth csplines'%f)

    index+=1

gnuplotInput.append("unset multiplot")
inp = ";".join(gnuplotInput)
plot = subprocess.Popen(['gnuplot' ,"-e",inp], stdin=subprocess.PIPE)


print "Done"


index+=1


