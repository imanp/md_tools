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

#membrane.copyItpFiles()
for index,frame in enumerate(frames):
    proteinString = md_tools.strip_vsites(pdb_util.findAllAminoAcidLines(frame))
    #proteinString = pdb_util.findAllAminoAcidLines(frame)

    #All files will have the same sequence so we only need to do this once
    if(os.path.isfile(scrwl_sequence_file)==False and args.mutations):
        sequence = md_tools.generateOneLetterSequence(proteinString,args.mutations)
        f= open(scrwl_sequence_file,"w")
        f.write(sequence)

    confFile = "%s/conf_%s.pdb"%(util.ProjectDirectories.CONF_DIR,index)
    confMutatedFile = "%s/conf_mutated_%s.pdb"%(util.ProjectDirectories.CONF_DIR,index)
    with open(confFile,"w") as f:
        f.write(proteinString)


    #FIXME awful and hacky and not general
    if(os.path.isfile("mutate.pml")):
        mutateAbsPath = os.path.abspath("mutate.pml")
        os.system("cp %s protein.pdb"%confFile)
        print "Mutating!"
        cmd = "/Applications/MacPyMOL.app/Contents/MacOS/MacPyMOL -c mutate.pml"
        os.system(cmd)
        # logCommand(cmd)
        os.system("cp protein_mutated.pdb %s"%confFile)
        print "Done mutating"
        # logCommand("Mutated protein using the file mutate.pml in root project dir")



    md_tools.pdb2gmx(confFile,"-ff amber99sb-ildn-berger -vsite hydrogens -water tip3p -ignh -o %s"%confFile)


    #TODO grep the last line to get charge imbalances
    boxSize= pdb_util.findPDBBoxSize(frame)
    nonProteinString = pdb_util.findAllNonProtein(frame)
    proteinString = pdb_util.findAllAminoAcidLines(confFile)

    with open(confFile,"w") as f:
        f.write(boxSize)
        f.write("\n")
        f.write(proteinString)
        f.write(nonProteinString)


md_tools.updateMembraneCount("POPC",confFile,"topol.top",fileType="pdb")
membrane.addPOPCfile("topol.top")
md_tools.updateWaterAndIonCount(confFile,"topol.top")
#
md_tools.cleanupBackups()

print "Done! ensure that your system has balanced charges!! you can remove ions with the command removeAtoms.py. then update the topology manually"
