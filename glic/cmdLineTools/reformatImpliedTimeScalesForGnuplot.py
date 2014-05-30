#!/usr/bin/env python

from argparse import *
from shutil import *
import sys

from lib.membrane import *
from lib.util import *

#create a project

'''
    Reformats the implied timescales dat file from MSMBuilder in a structured order to be read in from gnuplot
'''


parser =ArgumentParser()
parser.add_argument("file",help="the implied timescales dat file")
args = parser.parse_args()


#input is a dat file with 2 columns

#column one represents the x axis. for example if we have 10 eigenvalues we have 10 values for x=1

#reformat so that each column has all values for one eigenvalue

currentX = ""
eigenvals = []

with open(args.file,"r") as f:
    for line in f:
        cols = line.split(" ")
        cols = [col.strip() for col in cols]
        if(currentX!=cols[0]):
            vals = []
            eigenvals.append(vals)
            currentX=cols[0]

        vals.append(cols[1])


print len(eigenvals)

with open("impscales.dat","w") as out:
    for eigen in eigenvals:
        out.write(" ".join(eigen))
        out.write("\n")


#output format: each column represents the values for an eigenvalue
gnuplotInput = []
print "Generating plot"
gnuplotInput.append("set logscale y")
gnuplotInput.append('set title "Lagtimes vs implied timescales"')
gnuplotInput.append('set xlabel "time (ns)"')
gnuplotInput.append("unset key")
gnuplotInput.append("set term pdf enhanced")
gnuplotInput.append('set output "impscales.pdf"')
gnuplotInput.append('set format y "10^%T"')
gnuplotInput.append('plot for[i=1:10] "test.dat" using i with lines')

inp = ";".join(gnuplotInput)
plot = subprocess.Popen(['gnuplot' ,"-e",inp], stdin=subprocess.PIPE)


print "Done"






