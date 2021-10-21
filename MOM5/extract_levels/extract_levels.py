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
        
        # loop over levels
        for i, level in enumerate(variables[var]["levels"]):
        
            level = min(levels, key=lambda x:abs(x-level))
        
            command = "cd " + dir + "; "
            output_file = variables[var]["output_names"][i] + ".nc"
            command += "cdo  -sellevel," + str(level) + " " + nc_file + " " + output_file
            os.system(command)
            
            # rename the variable
            command = "cd " + dir + "; "
            command += "cdo chname," + var + "," + variables[var]["output_names"][i] + " " + output_file + " tmp.nc; "
            command += "mv tmp.nc " + output_file
            os.system(command)
            
            
        
        
        