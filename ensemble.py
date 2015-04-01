#!/usr/bin/env python

'''
Given a set of conformations from same setup. prepare them for simulations
can do mutations and alter ph and if needed adding v-sites


INPUT
========
- set of pdb files assumed to be from same simulation, only conformations should differ, pdb files are assumed to include the protein and solvent
- ph
- mutations


process
==========
for each structure
1. extract protein do pdb2gmx, here we set protonation states also
2. merge output of pdb2gmx and solvent
3. include necessary itp files in topology file
4. update topology with correct solvent count (NA CL lipids, water)

'''
from argparse import ArgumentParser
import glob
import os
from shutil import copyfile
from glic import glicTools
from lib import membrane
from lib.md_tools import *
from lib.membrane import pdb2gmxOptions, injectLinesIntoTop
from lib.pdb_util import findAllAminoAcidLines
from lib.util import MDToolsDirectories


parser = ArgumentParser()
parser.add_argument("proteins",
                    help="protein files, accepts wildcard selections only")
#defult ph 7
parser.add_argument("--ph",help="the ph value to start this system with",choices=glicTools.phChoices)
args = parser.parse_args()


protonationString=None
if args.ph:
    protonationString = glicTools.getProtonationSelections(args.proteins,args.ph)



#copy in itp files
membrane.copyItpFiles()

path = os.path.abspath(args.proteins)

os.chdir("confs")

files = glob.glob(path)

files = sorted_nicely(set(files))


index=0
# proteinFileName = "conf%s.pdb"
#we just prefix the regular filename of the starting file with conf
proteinFileName = "conf_%s"

for system in files:
    currentProtein = proteinFileName%os.path.basename(system)

    #we only want to do pdb2gmx on the protein not the rest of the stuff
    str = findAllAminoAcidLines(system)
    str = strip_vsites(str)
    with open(currentProtein,"w") as f:
        f.write(str)

    #FIXME awful and hacky and not general
    if(os.path.isfile("../mutate.pml")):
        mutateAbsPath = os.path.abspath("../mutate.pml")
        os.system("cp %s protein.pdb"%currentProtein)
        print "Mutating!"
        cmd = "/Applications/MacPyMOL.app/Contents/MacOS/MacPyMOL -c ../mutate.pml"
        os.system(cmd)
        logCommand(cmd)
        os.system("cp protein_mutated.pdb %s"%currentProtein)
        print "Done mutating"
        logCommand("Mutated protein using the file mutate.pml in root project dir")

    if protonationString:
        pdb2gmx(currentProtein,pdb2gmxOptions%currentProtein,protonationSelections="-asp -glu -his -arg -lys"
            ,protonationStates=protonationString)
    else:
        pdb2gmx(currentProtein,pdb2gmxOptions%currentProtein)

    #assuming that the provided files includes the whole system
    mergeProteinAndMembranePdb(currentProtein,system)
    index+=1


#only need to do this for one topology file
updateMembraneCount("POPC",currentProtein,"topol.top",fileType="pdb")
updateWaterAndIonCount(currentProtein,"topol.top")
injectLinesIntoTop("topol.top")



#TODO
#ensureCorrectSolventOrder(currentProtein,"topol.top")


os.system("mv topol.top *.itp ../")

os.system(r"rm \#* conf*.pdb.* topol.top.*")

print "Done however you need to ensure that the molecule order in the top file is correct and that your system has balanced charges"