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
        p = subprocess.Popen(args,stdin=subprocess.PIPE)
        p.communicate(input=protonationStates)
        ret = p.returncode
    else:
        print " ".join(args)
        ret = subprocess.call(args)

    #we have an error
    if ret:
        print "Error when doing pdb2gmx check the console output for further info"
        exit(1)

    else:
        print "Successfully called command:"

        cmd = " ".join(args)
        if(protonationStates and protonationSelections):
            # the r prefix prints the string as a raw string and repr ensures the string
            #var is a raw string
            cmd = r"""echo -e %s | %s"""%(repr(protonationStates),cmd)

        print cmd
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
    ret = subprocess.call(args)

    #we have an error
    if ret:
        print "Error when doing genbox check the console output for further info"
        exit(1)

    else:
        print "Successfully called command:"
        cmd = " ".join(args)
        print cmd
    return


def updateMembraneCount(type,numLipids,topology):
    '''
      appends the number of lipids to the topology file
    '''

    str = "%s        %s\n"%(type,numLipids)

    versionFile(topology)
    with open(topology,"a") as f:
        f.write(str)

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


    #backup old topology
    versionFile(topology)
    with open(topology,"w") as f:
        f.write(topologyStr)

    print "Successfully updated topology"


#if we do not find it the toplogy file has never been updated
    #alter the toplogy file


def grompp(pdb_structure,mdp_file,topology,output=topol.tpr):
    args = ["grompp","-f",mdp_file,"-c",pdb_structure,"-p",topology,"-o",output]

    ret = subprocess.call(args)

    if ret:
        print "Error when doing genbox check the console output for further info"
        exit(1)

    else:
        print "Successfully called command:"
        cmd = " ".join(args)
        print cmd





def genIon(topology,tpr, options):
    '''
        adds 0.1 mMolar of NACL and ensures the charges are neutral
         it updates the water and NACL counts in the topology

        NOTE assumes an mdp file is avilable
        NOTE requires interactive feedback for chosing solvent molecules

        inputs:
            pdb_structure :String(filename) a pdb file
            topology:String(filename) a top file
    '''

    args = ["genion","-conc","0.1","-neutral","-s",tpr,"-p",topology ]
    opts = shlex.split(options)
    args= args+opts
    ret = subprocess.call(args)

    if ret:
        print "Error when doing genion check the console output for further info"
        exit(1)

    else:
        print "Successfully called command:"
        cmd = " ".join(args)
        print cmd


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


def translateProtein(pdb_structure,translationVectorString,options):
    args=["editconf","-f",pdb_structure,"-n","index.ndx","-translate",translationVectorString]
    opts = shlex.split(options)
    args = args+opts

    p = subprocess.Popen(args,stdin=subprocess.PIPE)
    p.communicate(input="1\n0\n")  #assuming selection 1 means protein
    ret = p.returncode


    if ret:
        print "Error when doing editconf check the console output for further info"
        exit(1)

    else:
        print "Successfully called command:"
        cmd = " ".join(args)
        print cmd

def centerProtein(selectionNum,pdb_structure,topology="topol.top",output="centered.gro"):
    """
    Centers the protein in the box.

    selectionNum:int the group to choose for selection in the index file

    #NOTE this combination is applicable for ion channels
    """

    #first we need a dummy mdp
    mdpDummy = "grompp_dummy.mdp"
    tprDummy = "tprdummy.tpr"

    args = ["touch",mdpDummy]
    executeCommand(args)

    grompp(pdb_structure,mdpDummy,topology,tprDummy)

    args = ["trjconv","-f",pdb_structure,"-o",output,"-center","-pbc","mol"
            ,"-ur","compact","-n","index.ndx","-s",tprDummy]

    p = subprocess.Popen(args,stdin=subprocess.PIPE)
    p.communicate(input="%s \n 0"%selectionNum)

    args = ["rm","grompp_dummy.mdp"]
    executeCommand(args)



#extracts the first n pdb columns
def extractPDBcolumns(numColumns,input):
    colPattern = "\S*\s*"*int(numColumns)
    reg = re.compile("^"+colPattern,re.MULTILINE)
    with open(input,"r") as f:
        lines =f.read()
        m = "\n".join(reg.findall(lines))
        return m



def executeCommand(args):
    ret = subprocess.call(args)

    if ret:
        print "Error when executing command %s, please check the console output for further info"%(" ".join(args))
        exit(1)

def executeInteractiveCommand(args,interactions):
    pass

def logCommand(str):
    pass