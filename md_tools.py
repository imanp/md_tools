import re
import shlex
import subprocess
from versionFile import *


def pdb2gmx(pdb_structure,options,protonationStates=None,protonationSelections=None):
    '''
        Takes a pdb as input and generates a topology
        Requires all pdb2gmx options as flags

        inputs:
          pdb_structure :String(filename) a pdb file
          options :String pdb2gmx flags
          protonationSelections:String residues to protonate. -asp -glu -lys -his -arg  are the pdb2gmxflags
          protonationStates:String a string to echo into pdb2gmx. Note that this string has to end with a linebreak!
    '''

    args = ['pdb2gmx', '-f', pdb_structure]
    opts = shlex.split(options)
    args = args+opts

    if (protonationSelections and protonationStates):
        protSel = shlex.split(protonationSelections)
        args = args+protSel
        executeInteractiveCommand(args,protonationSelections)
    else:
        executeCommand(args)

    return



def mutate(pdb_structure,mutations):
    '''
        mutates residues
        can do several mutations at once

        uses pymol mutagenesis

        inputs:
            pdb_structure :String(filename) a pdb file
            mutations:List<String,String> a list of tuples, first tuple element
              is the residue selection the second is the mutation to perform
              selections and residue names follows pymol standard
    '''


def genbox(pdb_structure,options):
    '''
    generates a water box around the provided structure
    assumes pdb_structure contains the box dimensions

    inputs:
        pdb_structure :String(filename) a pdb file
    '''

    args = ["genbox", "-cp",pdb_structure,"-cs","spc216"]
    opts = shlex.split(options)
    args = args+opts
    executeCommand(args)

    return


def updateMembraneCount(type,membraneFile,topology):
    '''
      appends the number of lipids to the topology file

      NOTE: expecting membrane file to be a gro file!
    '''

    args = ['grep','-c',"%s     P"%type,membraneFile]
    numLipids = executeCommand(args).rstrip() #rstrip removes new lines

    str = "%s        %s\n"%(type,numLipids)

    versionFile(topology)
    with open(topology,"a") as f:
        f.write(str)

    logCommand("Updated number of %s lipids to %s in %s "%(type,numLipids,topology))

def updateWaterAndIonCount(pdb_structure,topology):
    '''
        checks for number of waters and NA and CL in the given structure and updates
        the toplogy files with the corresponding counts
        inputs:
            pdb_structure :String(filename) a pdb file
            topology:String(filename) a top file
    '''
    toCount = {"OW":0,"NA":0,"CL":0}

    #name mappings in the topology file
    mappings = {"OW":"SOL","NA":"NA","CL":"CL"}

    for elem in toCount:
        args = ["grep","-c",elem,pdb_structure]
        p = subprocess.Popen(args,stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, close_fds=True)
        (stdout,stderr) = p.communicate(input=None)
        count = int(stdout)
        toCount[elem] = count

    with open(topology) as f:
        topologyStr = f.read()

    logStr =''
    for elem in toCount:
        #does the element exist?
        if(toCount[elem]>0):
            newStr = "%s        %s"%(mappings[elem],toCount[elem])
            name = mappings[elem]
            regex = r"(%s\s+)\d+"%name
            w= re.compile(regex)
            m = w.search(topologyStr)
            if m:
                topologyStr =  w.sub(newStr,topologyStr)
            else: #append a string to the toplogyStr
                topologyStr = topologyStr+newStr
            logStr += newStr


    #backup old topology
    versionFile(topology)
    with open(topology,"w") as f:
        f.write(topologyStr)

    logCommand("Updated topology %s with %s"%(topology,logStr))


def grompp(pdb_structure,mdp_file,topology="topol.top",output="topol.tpr",options=""):
    args = ["grompp","-f",mdp_file,"-c",pdb_structure,"-p",topology,"-o",output]+shlex.split(options)

    executeCommand(args)


def genIon(topology, options,pdb_structure,solventGroup=15):
    '''
        adds 0.1 mMolar of NACL and ensures the charges are neutral
         it updates the water and NACL counts in the topology

        NOTE assumes an mdp file is avilable
        NOTE requires interactive feedback for chosing solvent molecules

        inputs:
            pdb_structure :String(filename) a pdb file
            topology:String(filename) a top file
            solventGroup:int The group of continous solvent molecules that we can replace with ions
                            default is 15=SOL
    '''


    mdpDummy,tprDummy=generateDummyMdpAndTpr(pdb_structure,topology)
    args = ["genion","-conc","0.1","-neutral","-s",tprDummy,"-p",topology ]
    opts = shlex.split(options)
    args= args+opts
    executeInteractiveCommand(args,"%s \n"%solventGroup)

    deleteTprAndMdpDummy()


def mergePdb(file,fileToMerge):
    '''
    merges the contents of fileToMerge into file
    backs up file before doing the merge

    All lines starting with ATOM in fileToMerge will be added to the top of the file
    '''

    with open(file,"r") as f:
        lines = f.readlines()
        with open(fileToMerge) as merge:
            str = merge.read()
            #find all lines starting with ATOM
            w = re.compile("^ATOM.*",re.MULTILINE)
            toMerge =  "\n".join(w.findall(str))


    #backup the file
    versionFile(file)
    # #write new file
    with open(file,"w") as f:
        str = "".join(lines[1:4]) + toMerge +'\n'+ "".join(lines[4:])
        f.write(str)

    logCommand("Merged the pdb files %s %s"%(file,fileToMerge))


def translateProtein(pdb_structure,translationVectorString,options,indexFile="index.ndx"):
    args=["editconf","-f",pdb_structure,"-n",indexFile,"-translate"] +shlex.split(translationVectorString)
    opts = shlex.split(options)
    args = args+opts

    executeInteractiveCommand(args,"1\n0\n")


def centerProtein(selectionNum,pdb_structure,topology="topol.top",output="centered.gro",indexFile="index.ndx"):
    """
    Centers the protein in the box.

    selectionNum:int the group to choose for selection in the index file

    #NOTE this combination is applicable for ion channels
    """

    #first we need a dummy mdp
    mdpDummy,tprDummy=generateDummyMdpAndTpr(pdb_structure,topology)

    args = ["trjconv","-f",pdb_structure,"-o",output,"-center","-pbc","mol"
            ,"-ur","compact","-n",indexFile,"-s",tprDummy]

    executeInteractiveCommand(args,"%s \n 0"%selectionNum)

    deleteTprAndMdpDummy()



#extracts the first n pdb columns
def extractPDBcolumns(numColumns,input):
    colPattern = "\S*\s*"*int(numColumns)
    reg = re.compile("^"+colPattern,re.MULTILINE)
    with open(input,"r") as f:
        lines =f.read()
        m = "\n".join(reg.findall(lines))
        return m



def executeCommand(args):

    try:
        ret = subprocess.check_output(args)
        logCommand(" ".join(args))

        #we want to show this info on the terminal
        print ret

        return ret
    except subprocess.CalledProcessError as e:
        print "Error when executing command %s\nCheck the console output for further info"%(" ".join(args))
        exit(1)



def executeInteractiveCommand(args,interactions):

    p = subprocess.Popen(args,stdin=subprocess.PIPE)

    out,err = p.communicate(input=interactions)
    ret = p.returncode

    cmd = "echo -e %s | %s"%(repr(interactions)," ".join(args))
    if ret:
        print "Error when executing the command %s\nCheck the console output for further info"%cmd
        exit(1)
    else:
        logCommand(cmd)
        return out



def generateDummyMdpAndTpr(pdb_structure,topology):
    mdpDummy = "grompp_dummy.mdp"
    tprDummy = "tprdummy.tpr"

    args = ["touch",mdpDummy]
    executeCommand(args)

    grompp(pdb_structure,mdpDummy,topology,tprDummy)

    return (mdpDummy,tprDummy)


def deleteTprAndMdpDummy():
    cmd = "rm grompp_dummy.mdp tprdummy.tpr"
    executeCommand(shlex.split(cmd))

def logCommand(str):
    '''
    appends a string to a README file
    '''
    with open("README",'a') as f:
        f.write(str)
        f.write("\n\n")

