#!/usr/bin/env python

from argparse import *
import glob
from membrane import *

#note! has to be run from within a project

parser = ArgumentParser()
parser.add_argument("proteins",help="All the protein files that we wish to add membranes to")
args = parser.parse_args()


files = glob.glob(args.proteins)



createSystemsFromEmbedded(files)

