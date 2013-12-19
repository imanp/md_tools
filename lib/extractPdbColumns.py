#!/usr/bin/env python

import sys
import copy

from lib.md_tools import *


args=copy.copy(sys.argv)
args.pop(0)
if(len(args)<2):
	print "Usage extractPdbColumns numColumns input"
	exit(1)


print extractPDBcolumns(args[0],args[1])

