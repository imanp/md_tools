#!/usr/bin/env python

from md_tools import *
import sys
import copy

args=copy.copy(sys.argv)
args.pop(0)
if(len(args)<2):
	print "Usage extractPdbColumns numColumns input"
	exit(1)


print extractPDBcolumns(args[0],args[1])

