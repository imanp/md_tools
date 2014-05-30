
from msmbuilder import Project
from msmbuilder import MSMLib
import mdtraj as md
from mdtraj import io
import os
import numpy as np

import lib.util

import yaml
# if CLoader/CDumper are available (i.e. user has libyaml installed)
#  then use them since they are much faster.
try:
    from yaml import CLoader as Loader
    from yaml import CDumper as Dumper
except ImportError:
    from yaml import Loader
    from yaml import Dumper

class MsmProject(Project):

    def load_frame(self, traj_index, frame_index):
        """Load one or more specified frames.

        Parameters
        ----------
        traj_index : int, [int]
            Index or indices of the trajectories to pull from
        frame_index : int, [int]
            Index or indices of the frames to pull from

        Returns  (MODIFIED BY IMAN)
        -------
        list: [(trajectory file,frame number)]
        """
        if np.isscalar(traj_index):
            traj_index = np.array([traj_index])
        if np.isscalar(frame_index):
            frame_index = np.array([frame_index])

        traj_index = np.array(traj_index)
        frame_index = np.array(frame_index)

        if not (traj_index.ndim == 1 and np.all(traj_index.shape == frame_index.shape)):
            raise ValueError('traj_index and frame_index must be 1D and have the same length')

        #get the trajectory filename
        #extract the project name and trajectory num

        # projectName = ''
        # conf = md.load(lib.util.getReferencePdb("%s/analysis/full/ref.pdb"%projectName))
        trajlist = []

        #NOTE it is only possible to get one frame per trajectory here!
        conf = self.load_conf()

        for i, j in zip(traj_index, frame_index):
            if j >= self.traj_lengths[i]:
                raise ValueError('traj %d too short (%d) to contain a frame %d' %
                                 (i, self.traj_lengths[i], j))

            trajlist.append((self.traj_originalName(i), j))



        return trajlist


    def traj_originalName(self, traj_index):
        "Get the filename of one of the trajs on disk"
        path = self._traj_converted_from[self._valid_traj_indices[traj_index]][0]
        return os.path.normpath(os.path.join(self._project_dir, path))