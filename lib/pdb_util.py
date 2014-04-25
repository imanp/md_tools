from lib.md_tools import *

def findAllAtomLines(pdbFile):
    '''
    Finds all lines starting with ATOM
    '''

    with open(pdbFile) as f:
        str = f.read()
        #find all lines starting with ATOM
        w = re.compile("^ATOM.*",re.MULTILINE)
        atomLines =  "\n".join(w.findall(str))

    return atomLines

def findAllAminoAcidLines(pdbFile):
#finds all Atom lines in pdbs that is an amino acid
    aminoAcids = getAminoAcidList()

    aastr = r"|".join(aminoAcids)
    regexp = r"ATOM.*(%s)"%aastr

    with open(pdbFile) as f:
        lines = f.readlines()
        #find all lines starting with ATOM
        aaLines = [line for line in lines if re.match(regexp,line)]


    return "".join(aaLines)


def findAllNonProtein(pdbFile):
    #finds all lines in pdbs that is not an amino acid
    aastr = r"|".join(getAminoAcidList())
    regexp = r"ATOM.*(%s)"%aastr

    with open(pdbFile) as f:
        lines = f.readlines()
        #find all lines starting with ATOM
        aaLines = [line for line in lines if not re.match(regexp,line) and line.startswith('ATOM')]


    return "".join(aaLines)

def findPDBBoxSize(pdbFile):
    '''
    Finds the line starting with CRYST and returns it
    '''
    with open(pdbFile,"r") as f:
        str = f.read()
        m = re.search("CRYST.*",str,re.MULTILINE)

        if m ==None:
            raise Exception("No line starting with CRYST could be found in file %s"%pdbFile)
            exit(1)

        else:
            return m.group(0)

def getAminoAcidDict():
    longToShort = { 'ARG':'R'
        ,'HIS':'H'
        ,'LYS':'K'
        ,'ASP':'D'
        ,'GLU':'E'
        ,'SER':'S'
        ,'THR':'T'
        ,'ASN':'N'
        ,'GLN':'Q'
        ,'CYS':'C'
        ,'SEC':'U'
        ,'GLY':'G'
        ,'PRO':'P'
        ,'ALA':'A'
        ,'VAL':'V'
        ,'ILE':'I'
        ,'LEU':'L'
        ,'MET':'M'
        ,'PHE':'F'
        ,'TYR':'Y'
        ,'TRP':'W'
    }

    return longToShort

def getAminoAcidList():
    return getAminoAcidDict().keys()

def getAminoAcidLongToShort(threeLetterName):
    '''
    converts the three letter name of the amino acid to the one letter name
    '''
    longToShort = getAminoAcidDict()
    return longToShort[threeLetterName]


def isAminoAcid(threeLetterName):
    longToShort = getAminoAcidDict()
    if threeLetterName in longToShort.keys():
        return True

def removeAtom(pdbFile,atomName,num):
    with open(pdbFile,"r") as f:
        lines = f.readlines()

    #NOTE not particularly effective
    regex = "ATOM\s+\d+\s+%s\s+.*"%atomName
    #find all the indices of lines having atomName X
    indices = [index for index,value in enumerate(lines) if re.match(regex,value) ]

    #give me the last num indices
    indicesToRemove = indices[-num:]
    result = [value for index,value in enumerate(lines) if index not in indicesToRemove ]

    return "\n".join(result)
