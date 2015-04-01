import collections
import re
import shlex
import subprocess
import lib.versionFile as versionFile
import lib.pdb_util as pdb_util
import lib.util as util


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
        executeInteractiveCommand(args,protonationStates)
    else:
        executeCommand(args)
    return



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


def updateMembraneCount(type,membraneFile,topology,fileType="gro"):
    '''
      appends the number of lipids to the topology file

      NOTE: expecting membrane file to be a gro file!
    '''
    if type =="POPC":
        pattern = "POPC"

    if type == "DOPC":
        pattern = "DOPC"

    if fileType == "pdb":
        pattern =  "P   %s"%pattern
    else:
        pattern = "%s     P"%type
    args = ['grep','-c',pattern,membraneFile]

    numLipids = executeCommand(args).rstrip() #rstrip removes new lines

    str = "%s        %s\n"%(type,numLipids)

    regex =r"%s        \d*"%type
    #versionFile(topology)

    with open(topology,"r") as f:
        topologyStr = f.read()

    #only find the molecules section, extract it and do the update there. Then replace
    #this section in the topologyStr
    updateSectionRegex = re.compile(r"(\[ molecules \][\s\S].*#mols\s*)((\D*\s*\d*\n)*)")
    matches = updateSectionRegex.search(topologyStr)
    updateSectionStr = matches.group(2)

    w= re.compile(regex)
    m = w.search(topologyStr)

    if(m):
        newStr = re.sub(m.group(0),str.rstrip("\n"),updateSectionStr)
    else:
        newStr = updateSectionStr+str

    newStr = matches.group(1)+newStr
    topologyStr = re.sub(re.escape(matches.group(0)),newStr,topologyStr)

    with open(topology,"w") as f:
        f.write(topologyStr)


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

    #only find the molecules section, extract it and do the update there. Then replace
    #this section in the topologyStr
    updateSectionRegex = re.compile(r"(\[ molecules \][\s\S].*#mols\s*)((\D*\s*\d*\n)*)")
    matches = updateSectionRegex.search(topologyStr)
    updateSectionStr = matches.group(2)

    logStr =''
    updateStr = ''
    for elem in toCount:
        #does the element exist?
        if(toCount[elem]>0):
            newStr = "%s        %s"%(mappings[elem],toCount[elem])
            name = mappings[elem]
            regex = r"(%s\s+)\d+"%name
            w= re.compile(regex)
            m = w.search(updateSectionStr)
            if m:
                updateStr =  w.sub(newStr,updateSectionStr)
            else: #append a string to the toplogyStr
                if(updateStr):
                    updateStr += newStr.strip()+"\n"
                else:
                    updateStr += updateSectionStr+newStr.strip()+"\n"
            logStr += newStr

    updateStr = matches.group(1)+updateStr
    topologyStr = re.sub(re.escape(matches.group(0)),updateStr,topologyStr)

    #backup old topology
    #versionFile(topology)
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
        toMerge = pdb_util.findAllAtomLines(fileToMerge)


    #backup the file
    versionFile(file)
    # #write new file
    with open(file,"w") as f:
        str = "".join(lines[1:4]) + toMerge +'\n'+ "".join(lines[4:])
        f.write(str)

    logCommand("Merged the pdb files %s %s"%(file,fileToMerge))


def mergeProteinAndMembranePdb(file,fileToMerge):
    '''
    Merges all amino acid lines in file with non protein atoms in filetoMerge
    the box size of fileToMerge is kept and the boxsize of file is discarded
    '''
    boxSize = pdb_util.findPDBBoxSize(fileToMerge)
    lines = pdb_util.findAllNonProtein(fileToMerge)
    toMerge = pdb_util.findAllAminoAcidLines(file)


    #backup the file
    versionFile(file)
    # #write new file
    with open(file,"w") as f:
        str = boxSize.strip() +'\n' + toMerge.strip() +'\n'+ lines.strip()
        f.write(str)

    logCommand("Merged the non Amino acid lines of %s with all the atoms in %s"%(file,fileToMerge))


def translateProtein(pdb_structure,translationVectorString,options,indexFile=None):
    args=["editconf","-f",pdb_structure,"-translate"]+shlex.split(translationVectorString)
    if indexFile:
        args+=["-n",indexFile]
    opts = shlex.split(options)
    args = args+opts

    executeInteractiveCommand(args,"1\n0\n")


def centerProtein(selectionNum,pdb_structure,topology="topol.top",output="centered.gro",indexFile=None):
    """
    Centers the protein in the box.

    selectionNum:int the group to choose for selection in the index file

    #NOTE this combination is applicable for ion channels
    """

    #first we need a dummy mdp
    mdpDummy,tprDummy=generateDummyMdpAndTpr(pdb_structure,topology)

    args = ["trjconv","-f",pdb_structure,"-o",output,"-center","-pbc","mol"
            ,"-ur","compact","-s",tprDummy]
    if indexFile:
        args +=["-n",indexFile]

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
        logCommand(" ".join(args))
        ret = subprocess.check_output(args)

        # #we want to show this info on the terminal
        # print ret

        return ret
    except subprocess.CalledProcessError as e:
        print "Error when executing command %s\nCheck the console output for further info"%(" ".join(args))
        exit(1)



def executeInteractiveCommand(args,interactions):
    cmd = "echo -e %s | %s"%(repr(interactions)," ".join(args))
    logCommand(cmd)
    #print cmd
    p = subprocess.Popen(args,stdin=subprocess.PIPE)

    out,err = p.communicate(interactions)
    ret = p.returncode
    print out
    print err

    if ret:
        print "Error when executing the command %s\nCheck the console output for further info"%cmd
        exit(1)
    else:
        return out


def strip_vsites(inputStr):
    '''
    Reads an and filters away all the vsite lines
    '''
    lines = inputStr.split("\n")

    outputLines = []
    exp= "MN[1-9]|[1-9]M.."
    for line in lines:
        match = re.search(exp,line)
        if match == None:
            outputLines.append(line)

    outputStr = "\n".join(outputLines)
    return outputStr.strip()



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

def cleanupBackups():
    #cleanup gromacs backups
    cmd = "rm \#*"
    import os
    os.system(cmd)


def sorted_nicely( l ):
    """ Sort the given iterable in the way that humans expect."""
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
    return sorted(l, key = alphanum_key)

def generateSequence(pdbFile,mutations=None):
    '''
    #given a pdb file generate a seqeunce

    #this outputs the sequence in a format suitable for scrwl4

    inputs:
        pdbFile: file
        mutations:string , a comma separated string of mutations ex. I233S,I240S
    '''

    file = open(pdbFile,"r")

    return generateOneLetterSequence(file.read(),mutations)

def generateOneLetterSequence(pdbString,mutationString=None):

    '''given a pdb string generate a seqeunce

    this outputs the sequence in a format suitable for scrwl4

    inputs:
    pdbFile: file
    mutationString:string , a comma separated string of mutations ex. I233S,I240S
'''

    mutations = dict()
    if(mutationString):
        mutations = parseMutations(mutationString)
    chains = collections.OrderedDict()
    for line in pdbString.split('\n'):
        aminoAcidThreeLetterCode = line[17:20]         #read columns 18-20 for res name, pdb column numbering starts with 1!
        if(line.startswith("ATOM") and pdb_util.isAminoAcid(aminoAcidThreeLetterCode)):
            sequenceNum = line[22:26].strip() # read columns  23-26 for sequence number, pdb column numbering starts with 1!
            chain = line[21]   #column 22 = chain , pdb column numbering starts with 1!

            if not chain in chains:
                chains[chain] = collections.OrderedDict()   #structure for this dict, sequenceNum,aminoacid

            if not sequenceNum in chains[chain]:

                if sequenceNum in mutations:
                    chains[chain][sequenceNum] = mutations[sequenceNum]
                else:
                    chains[chain][sequenceNum] = pdb_util.getAminoAcidLongToShort(aminoAcidThreeLetterCode).lower()

    str= ""
    for sequences in chains.itervalues():
        str+="".join(sequences.itervalues())

    return str


def parseMutations(mutationString):
    '''
    given a mutationstring of form I233S,I240S
    returns a list of sequenceNumbers and the corresponding mutation
    '''

    splittedString = mutationString.split(",")
    mutations = dict()
    for string in splittedString:
        sequenceNum = string[1:len(string)-1]

        mutations[sequenceNum]= string[-1]
    return mutations









