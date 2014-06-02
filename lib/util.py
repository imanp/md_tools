#File and dir conventions used throughout the app
import os
import sys


class ProjectDirectories():
    MEMBED_DIR = "membed"
    EM_DIR="em"
    EQUILIBRATION_DIR="equi"
    RUN_DIR="run"
    CONF_DIR="confs"
    TPR_DIR="tprs"
    TRAJ_DIR="trajectories"
    ANALYSIS_DIR="analysis"
    ANALYSIS_FULL_DIR="%s/%s"%(ANALYSIS_DIR,"full")
    ANALYSIS_TMD_DIR="%s/%s"%(ANALYSIS_DIR,"tmd")
    ANALYSIS_M2_DIR="%s/%s"%(ANALYSIS_DIR,"m2")
    ANALYSIS_PROTEIN_DIR="%s/%s"%(ANALYSIS_DIR,"protein")
    ANALYSIS_TMD_BACKBONE_DIR="%s/%s"%(ANALYSIS_DIR,"tmd_backbone")
    ANALYSIS_M2_BACKBONE_DIR="%s/%s"%(ANALYSIS_DIR,"m2_backbone")
    ANALYSIS_PORE_DIMENSION_DIR="%s/%s"%(ANALYSIS_DIR,"pore_dimensions")
    ANALYSIS_WATER_COUNT_DIR="%s/%s"%(ANALYSIS_DIR,"water_counts")

class FileNames():
    PROJ_INFO=".proj"
    GROMPP_EM = "grompp_em.mdp"
    GROMPP_EQUI = "grompp_equi.mdp"
    GROMPP_PROD = "grompp.mdp"
    CONF = "conf.pdb"
    FIRST_CONF="conf*0.pdb"

class MDToolsDirectories():
    OTHER =  os.path.join(os.path.dirname(sys.argv[0]) ,"lib","other")
    POPC_FF_DIR = os.path.join(os.path.dirname(sys.argv[0]) ,"lib","membranes","popc288","amber99sb-ildn-berger.ff")


def getProjectName():
    return os.path.basename(os.getcwd())

def getEmProjectName():
    return "%s_em"%getProjectName()

def getEmProjectName():
    return "%s_em"%getProjectName()

def getReferencePdb(dir):
    return "%s/ref.pdb"%dir

