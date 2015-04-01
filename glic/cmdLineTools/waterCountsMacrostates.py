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


# parser = ArgumentParser()
# parser.add_argument("title",help="Type in the name of the system")
#
# args = parser.parse_args()

VMD ="/nethome/grant/.bin/vmd"

analysisScript="%s/count_waters_macrostates.tcl"%os.environ['GLIC_TOOLS']

index=0

# for dir in glob.glob("statesFromMacrostate*"):
#     print "running trajectory %s"%dir
#
#     # cmd = "cd %s"%dir
#     os.chdir(dir)
#     # executeCommand(shlex.split(cmd))
#
#     datFile ="%s_water_count.dat"%(dir)
#     #change to hole scripts directory
#     cmd =  "%s -dispdev text -e %s -args %s"%(VMD,analysisScript,datFile)
#
#     # executeCommand(shlex.split(cmd))
#
#     os.chdir("../")
#     # cmd = "cd ../"
#     # executeCommand(shlex.split(cmd))
#
#     index+=1



gnuplotInput = []
print "Generating plot"
gnuplotInput.append('set title "#water in macrostates between residues 230 and 235"')
gnuplotInput.append(""" set ylabel "#water" font "Arial, 8"  """)
gnuplotInput.append(""" set xlabel "frame" font "Arial, 8"  """)
# gnuplotInput.append("unset xlabel")
# gnuplotInput.append("set format x '' ")
# gnuplotInput.append("unset key")
gnuplotInput.append("set term pdf enhanced")
outfile = "macrosate_water_count.pdf"
# print outfile
gnuplotInput.append('set output "%s"'%outfile)
# gnuplotInput.append("set yrange [0:60]")
# gnuplotInput.append("set xrange [0:1500]")
# gnuplotInput.append("set ytics 0,10,100 ")
# gnuplotInput.append("""set xtics font "Arial, 8" """)
# gnuplotInput.append("""set ytics font "Arial, 8" """)
# gnuplotInput.append("set mytics 2")
# gnuplotInput.append("set mxtics 2")
datFiles = sorted(glob.glob("watercounts/*dat"))
# gnuplotInput.append("""set multiplot layout %s,1 title "%s" """%(len(datFiles),args.title))
#
index = 0
#
str = 'plot '
for f in datFiles:
    print f
#
#     if len(datFiles) == index:
#         # gnuplotInput.append('set xlabel "time (ns)"')
#         # gnuplotInput.append("set format x '%g' ")
#         pass
#
#
#
    str+='"%s" with lines title "cluster %s",'%(f,index)
    # gnuplotInput.append('plot "%s" with lines ;'%f)
#
    index+=1
#
# gnuplotInput.append("unset multiplot")
gnuplotInput.append(str)
inp = ";".join(gnuplotInput)
print inp
plot = subprocess.Popen(['gnuplot' ,"-e",inp], stdin=subprocess.PIPE)
#
#
print "Done"
#
#
# index+=1


