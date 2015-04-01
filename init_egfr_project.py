#!/usr/bin/env python
from argparse import ArgumentParser
import glob
import lib.pdb_util as pdb_util
import lib.md_tools as md_tools
import lib.util as util
import os
import lib.membrane as membrane

parser = ArgumentParser()
parser.add_argument("--mutations",
                    help="A comma separated list of mutations to apply, ex: I233S,I240S")

parser.add_argument("--confs",default ="/Users/iman/nethome/iman/Projects/EGFR/EGFR_WT/sim_frames/*pdb",
                    help="starting configurations to use, can use glob pattern ex:*pdb")

args = parser.parse_args()


frames = glob.glob(args.confs)
frames.sort()

scrwl_sequence_file = "scrwl_sequence.txt"
index = 0

membrane.copyItpFiles()
for frame in frames:
    proteinString = md_tools.strip_vsites(pdb_util.findAllAminoAcidLines(frame))
    #proteinString = pdb_util.findAllAminoAcidLines(frame)

    #All files will have the same sequence so we only need to do this once
    if(os.path.isfile(scrwl_sequence_file)==False and args.mutations):
        sequence = md_tools.generateOneLetterSequence(proteinString,args.mutations)
        f= open(scrwl_sequence_file,"w")
        f.write(sequence)

    confFile = "%s/conf_%s.pdb"%(util.ProjectDirectories.CONF_DIR,index)
    with open(confFile,"w") as f:
        f.write(proteinString)

    # if args.mutatations:
    #     #TODO set correct filenames
    #     args = ['Scwrl4','-i',confFile,'-o','confs/test.pdb']
    #     md_tools.executeCommand(args)
    #     args = ['Scwrl4','-i','confs/test.pdb','-o',confFile,'-s',scrwl_sequence_file]
    #     md_tools.executeCommand(args)
    #     index = index+1

    md_tools.pdb2gmx(confFile,"-ff amber99sb-ildn -vsite hydrogens -water tip3p -ignh -o %s"%confFile)


    #TODO grep the last line to get charge imbalances
    boxSize= pdb_util.findPDBBoxSize(frame)
    nonProteinString = pdb_util.findAllNonProtein(frame)
    proteinString = pdb_util.findAllAminoAcidLines(confFile)

    with open(confFile,"w") as f:
        f.write(boxSize)
        f.write("\n")
        f.write(proteinString)
        f.write(nonProteinString)

membrane.injectLinesIntoTop("topol.top")
md_tools.updateMembraneCount("POPC",confFile,"topol.top",fileType="pdb")
md_tools.updateWaterAndIonCount(confFile,"topol.top")

md_tools.cleanupBackups()
