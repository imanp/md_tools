from md_tools import *

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


def findAllNonAminoAcidLines(pdbFile):
    #finds all lines in pdbs that is not an amino acid
    aminoAcids = getAminoAcidList()

    aastr = r"|".join(aminoAcids)
    regexp = r"ATOM.*(%s)"%aastr


    with open(pdbFile) as f:
        lines = f.readlines()
        #find all lines starting with ATOM
        aaLines = [line for line in lines if not re.match(regexp,line)]


    return "".join(aaLines)

def getAminoAcidList():
    return ['VAL','SER','ARG','HIS','LYS','ASP','GLU','SER' \
        ,'THR','ASN','GLN','SYS','SEC','GLY','PRO','ALA','ILE' \
        ,'LEU','MET','PHE','TYR','TRP','CYS']


