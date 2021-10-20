import glob
import os
import sys

out_dir = str(sys.argv[1])
from_date = int(sys.argv[2])
to_date = int(sys.argv[3])

import config
variables = config.variables

sys.path.append('../../auxiliary')
import get_all_dirs_from_to

dirs = get_all_dirs_from_to.get_all_dirs_from_to(out_dir, from_date, to_date)

import create_results_dir
results_dir = create_results_dir.create_results_dir(out_dir, from_date, to_date)

from netCDF4 import Dataset

for dir in dirs:
    for var in variables.keys():
        nc_file = dir + "/" + var + ".nc"
        fh = Dataset(nc_file, mode='r')
        levels = fh.variables[variables[var]["level_name"]][:]
        fh.close()
        
        #TODO loop over levels
        
        level = min(levels, key=lambda x:abs(x-variables[var]["levels"][0]))
        
        command = "cd " + dir + "; "
        command += "cdo  -sellevel," + str(level) + " " + nc_file + " " + variables[var]["output_names"][0] + ".nc"
        #TODO rename the variable
        os.system(command)
        
        
        