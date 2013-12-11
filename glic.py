#!/usr/bin/env python
from md_tools import *
import os

def injectLinesIntoTop(toplogy="topol.top"):
#inject some lines into the topology file
    versionFile(toplogy)
    baseDir = os.path.dirname(os.path.realpath(__file__))

    with open(toplogy,"rw") as f:
        lines = f.readlines()

    with open(toplogy,"w") as f:
        for line in lines:
            f.write(line)

            if(line.startswith("""#include "amber99sb-ildn.ff/forcefield.itp""")):
                f.write("""#include "%s/other/ffnonbonded.itp"\n"""%baseDir)
                f.write("""#include "%s/other/ffbonded.itp"\n"""%baseDir)

            if(line.startswith("#endif")):
                f.write("""; Include lipid topology\n""")
                f.write("""#include "%s/other/amber99sb-ildn-berger.ff/popc.itp\n"""%baseDir)


def embedProteinIntoMembrane(proteinPdb,indexFile,centerGroup,membraneSize=288,membraneType='popc'):

    '''
    embeds a provided protein into a membrane
    currently specific towards GLIC, needs some more generalization to work with other proteins

    To align the protein correctly make sure you have an index file and also specify which group in it to use
    for centering the protein

    NOTE BOX size of the system is assumed tobe specified in the gro file for the membrane!
    '''

    #base dir of this file, glic.py
    baseDir = os.path.dirname(os.path.realpath(__file__))
    membraneDir = "%s/membranes/%s%s"%(baseDir,membraneType,membraneSize)


    #1. Do pdb2gmx
    pdb2gmx(proteinPdb,"-water tip3p -ff amber99sb-ildn -ignh -vsite hydrogen -o conf.pdb")


    '''
    2. generate a water box. this is done using a file containing the membrane and the overall box size of
    the system

    The vdwraddi will make sure that we do not put water to close to the membrane
    '''
    args = ["cp","%s/vdwradii.dat"%membraneDir,"."]
    executeCommand(args)
    genbox("%s/conf.gro"%membraneDir,"-o membrane_water.pdb")

    #FIXME generalize membrane type
    updateMembraneCount("POPC","%s/conf.gro"%membraneDir,"topol.top")
    updateWaterAndIonCount("membrane_water.pdb","topol.top")

    args = ["rm","vdwradii.dat"]
    executeCommand(args)

    #3. Merge the membrane file and the protein file
    mergePdb("membrane_water.pdb","conf.pdb")

    #4. Update the top file with itp files for the membrane etc
    injectLinesIntoTop("topol.top")

    #5. Center the protein on the membrane
    centerProtein(centerGroup,"membrane_water.pdb",indexFile=indexFile,output="membrane_water.pdb")

    #6. Translate the protein so a bit of it sticks out at the bottom of the membrane
    #FIXME making a rough assumption that protein and membrane is well aligned and we only need to translate by 2nm in z direction
    translateProtein("membrane_water.pdb","0 0 -2","-o membrane_water.pdb",indexFile=indexFile)

    #7. Add ions
    genIon("topol.top","-o membrane_water.pdb","membrane_water.pdb")

    #8. Run membed
    grompp("membrane_water.pdb","%s/other/membed.mdp"%baseDir,output="membed.tpr",options="-maxwarn 1")
    cmd = "g_membed -f membed.tpr"
    executeCommand(shlex.split(cmd))



indexFile ='start/index.ndx'
res229Group = 17
protein = 'start/REF_4HFI.pdb'

#FIXME somewhere in this scheme we need to take the force field dir into account

embedProteinIntoMembrane(protein,indexFile,res229Group)

#TODO execute the emebedding?