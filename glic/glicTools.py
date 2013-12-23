import re

from glic.protonationStates import ProtonationStates

phChoices = ['4.6','7.0']
def HIEtoHIS(infile,outfile):
    f=open(infile,'r')
    str = f.read()

    regex =re.compile('(ATOM.*)HIE(.*)')
    str = regex.sub(r'\1HIS\2',str)
    out = open(outfile,"w")
    out.write(str)
    out.close()
    f.close()



def getProtonationSelections(protein,ph):

    '''
    ph is as string of either 4.6 or 7.0
    '''

    if ph == phChoices[0] :
        #change the HIE:s to HIS
        proteinFile = "protein_temp.pdb"
        HIEtoHIS(protein,proteinFile)
        protonationSelections ="\n".join(ProtonationStates.ph46 * 5) + "\n"
        protein = proteinFile

    elif ph == phChoices[1]:
        protonationSelections = None  #the structures i provide are set to ph7 already!
        #protonationSelections ="\n".join(ProtonationStates.ph7 * 5) + "\n"

    return protein,protonationSelections