import glob
import os
from shutil import copyfile
from glic.protonationStates import ProtonationStates
from lib.md_tools import *
from lib.util import ProjectDirectories, FileNames

pdb2gmxOptions = "-ter -water tip3p -ff amber99sb-ildn -ignh -vsite hydrogen -o %s"

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


def embedProteinIntoMembrane(centerGroup,indexFile=None,membraneSize=288,membraneType='popc'):

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
    mergePdb("membrane_water.pdb",FileNames.CONF)


    # 4. Update the top file with itp files for the membrane etc
    injectLinesIntoTop("topol.top")

    #5. Center the protein on the membrane
    centerProtein(centerGroup,"membrane_water.pdb",indexFile=indexFile,output="membrane_water.pdb")

    #6. Translate the protein so a bit of it sticks out at the bottom of the membrane
    #FIXME making a rough assumption that protein and membrane is well aligned and we only need to translate by 2nm in z direction
    translateProtein("membrane_water.pdb","0 0 -1","-o membrane_water.pdb",indexFile=indexFile)

    #7. Add ions
    genIon("topol.top","-o membrane_water.pdb","membrane_water.pdb")

    #8. Run membed
    grompp("membrane_water.pdb","%s/other/membed.mdp"%baseDir,output="membed.tpr",options="-maxwarn 1")
    cmd = "g_membed -f membed.tpr"
    executeCommand(shlex.split(cmd))


def runMembedSim():
    '''
    Assumes bluntly that all files are in place
    '''

    cmd = "mdrun -s membed.tpr -membed membed.dat -o traj.trr -c membedded.gro -e ener.edr -nt 1 -cpt -1"
    executeCommand(shlex.split(cmd))



def createSystemsFromTemplate(args,protonationString=None):

    '''
        args:ArgumentParser args
    '''

    path = os.path.abspath(args.proteins)

    os.chdir("confs")

    files = glob.glob(path)
#go to the confs directory
    filename = "conf%s.pdb"
    i = 1
    for protein in files:
        name = filename%i
        #note pdb2gmxoptions comes from util.membrane

        #FIXME awful and hacky and not general
        if(os.path.isfile("../mutate.pml")):
            copyfile(protein,"protein.pdb")
            print "Mutating!"
            cmd ="pymol -c ../mutate.pml"
            executeCommand(shlex.split(cmd))

            versionFile("protein.pdb")
            protein = "protein_mutated.pdb"
            print "Done mutating!"



        if protonationString:
            pdb2gmx(protein,pdb2gmxOptions%name,protonationSelections="-asp -glu -his -arg -lys"
                ,protonationStates=protonationString)
        else:
            pdb2gmx(protein,pdb2gmxOptions%name)
        mergePdb(name, "conf0.pdb")
        i += 1

    #take everything but the protein protein part from conf0.gro
    #take the original conf that we are using as a template, merge this protein with the template (non protein)
    #center the protein
    #and we are done!
    cleanupBackups()
    cmd = "rm *.pdb.* topol.top"
    executeCommand(shlex.split(cmd))
    cmd = "rm *itp"
    os.system(cmd)

def runMembed(args,protonationString = None):

    '''
        args:ArgumentParser args
        protonationString: string of all the selections that will be echoed in
    '''

    #project initialization
    indexFile=None
    protein = "protein.pdb"

    #if we have a project we will simply rerun int
    #TODO add checkpointing steps
    if(args.index):
        indexFile = "index.ndx"
        copyfile(args.index,indexFile)

    copyfile(args.protein,protein)


    #1. Do pdb2gmx
    file = FileNames.CONF


    #FIXME awful and hacky and not general
    if(os.path.isfile("mutate.pml")):
        cmd ="pymol -c mutate.pml"
        executeCommand(shlex.split(cmd))
        versionFile("protein.pdb")
        copyfile("protein_mutated.pdb","protein.pdb")


    if protonationString:
        pdb2gmx(protein,pdb2gmxOptions%file,protonationSelections="-asp -glu -his -arg -lys"
            ,protonationStates=protonationString)
    else:
        pdb2gmx(protein,pdb2gmxOptions%file)

    embedProteinIntoMembrane(args.indexGroup,indexFile=indexFile)
    runMembedSim()

    membeddedFile = "membedded.gro"

    updateWaterAndIonCount(membeddedFile,"topol.top")
    updateMembraneCount("POPC",membeddedFile,"topol.top")

    centerProtein(args.indexGroup,membeddedFile,output=membeddedFile)

    #create a pdb file as output

    cmd = "editconf -f %s -o %s/%s"%(membeddedFile,ProjectDirectories.CONF_DIR,"conf0.pdb")
    executeCommand(shlex.split(cmd))

    print("""Structure is embedded into membrane. The file can be found in %s/%s\n \
        Topology is updated to reflect this file\n
          Note that you might need to some more stuff before running the actual simulation \n
          Your system might have a charge imbalance for example.
          """)%(ProjectDirectories.CONF_DIR,"conf0.gro")


#quick and dirty way to do mutataions
def doMutationIfDescriptionExists():

    '''
    Does the mutation via pymol
    outputs a file called protein_mutated.pdb
    copies it to protein.pdb
    '''

