import shlex
from lib.md_tools import executeCommand
import os
from lib.util import MDToolsDirectories


class CpcUtil():
    @staticmethod
    def buildMDWorkflow(projectName,gromppPath,filePathList,maxCores=24,maxFiles=None):
        '''
        creates a workflow for md simulation using grompp and mdrun function blocks
        '''

        cmd = "cpcc start %s"%projectName
        executeCommand(shlex.split(cmd))


        cmd="cpcc import gromacs"
        executeCommand(shlex.split(cmd))
        cmd="cpcc instance gromacs::grompp_multi grompp"
        executeCommand(shlex.split(cmd))
        cmd="cpcc instance gromacs::mdrun_multi mdrun"
        executeCommand(shlex.split(cmd))


        cmd ="cpcc transact"
        executeCommand(shlex.split(cmd))
        cmd="cpcc connect grompp:out.tpr mdrun:in.tpr"
        executeCommand(shlex.split(cmd))


        #maximum number of cores to user per simulation. if not set simulations will be tuned
        cmd="cpcc set mdrun.in.resources[0].max.cores 24"
        executeCommand(shlex.split(cmd))

        cmd="cpcc setf grompp.in.top[+] topol.top"
        executeCommand(shlex.split(cmd))
        cmd ="cpcc setf grompp.in.mdp[+] %s"%gromppPath
        executeCommand(shlex.split(cmd))

        #this is a 2d array
        cmd ="cpcc setf grompp.in.include[0][0] topol_Protein_chain_A.itp"


        #needed for equilibrations
        #cmd ="cpcc setf grompp.in.include[+][+] posre_Protein_chain_A.itp"
        executeCommand(shlex.split(cmd))

        cmd ="cpcc setf grompp.in.include[0][1] %s"%os.path.join(MDToolsDirectories.OTHER,"ffnonbonded.itp")
        executeCommand(shlex.split(cmd))

        cmd ="cpcc setf grompp.in.include[0][2] %s"%os.path.join(MDToolsDirectories.OTHER,"ffbonded.itp")
        executeCommand(shlex.split(cmd))


        cmd ="cpcc setf grompp.in.include[0][3] %s"%os.path.join(MDToolsDirectories.POPC_FF_DIR,"popc.itp")
        executeCommand(shlex.split(cmd))

        gros = filePathList

        count = 0
        for gro in gros:
            cmd="cpcc setf grompp.in.conf[+] %s"%gro
            executeCommand(shlex.split(cmd))
            count+=1
            #if we want to limit the number of files to submit in an easy way
            if maxFiles and count==max:
                break

        cmd="cpcc commit"
        executeCommand(shlex.split(cmd))

        cmd="cpcc activate"
        executeCommand(shlex.split(cmd))