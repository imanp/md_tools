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

def getAminoAcidList():
    return ['VAL','SER','ARG','HIS','LYS','ASP','GLU','SER' \
        ,'THR','ASN','GLN','SYS','SEC','GLY','PRO','ALA','ILE' \
        ,'LEU','MET','PHE','TYR','TRP','CYS']



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
