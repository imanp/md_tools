#File and dir conventions used throughout the app
import os
import sys


class ProjectDirectories():
    MEMBED_DIR = "membed"
    EM_DIR="em"
    EQUILIBRATION_DIR="equi"
    RUN_DIR="run"
    CONF_DIR="confs"

class FileNames():
    PROJ_INFO=".proj"
    GROMPP_EM = "grompp_em.mdp"
    GROMPP_EQUI = "grompp_equi.mdp"
    GROMPP_PROD = "grompp.mdp"
    CONF = "conf.pdb"

class MDToolsDirectories():
    OTHER =  os.path.join(os.path.dirname(sys.argv[0]) ,"lib","other")
    POPC_FF_DIR = os.path.join(os.path.dirname(sys.argv[0]) ,"lib","membranes","popc288","amber99sb-ildn-berger.ff")


def getProjectName():
    return os.path.basename(os.getcwd())

def getEmProjectName():
    return "%s_em"%getProjectName()

