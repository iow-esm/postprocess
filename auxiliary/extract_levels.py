import glob
import os
import sys

# decode the input arguments
out_dir = str(sys.argv[1])
from_date = int(sys.argv[2])
to_date = int(sys.argv[3])
pwd = str(sys.argv[4])

# import the local config 
sys.path.append(pwd)
import config
variables = config.variables

# get directories from where we extract
import get_all_dirs_from_to
dirs = get_all_dirs_from_to.get_all_dirs_from_to(out_dir, from_date, to_date)

# construct proper result directory
import create_results_dir
results_dir = create_results_dir.create_results_dir(out_dir, from_date, to_date)

# we need netCDF4 to read in the file and find the closest level
from netCDF4 import Dataset

# go over all directories
for dir in dirs:
    # go over all variables from where we extract (as defined in the local config)
    for var in variables.keys():
        # read the vertical levels from the source file
        nc_file = dir + "/" + var + ".nc"
        fh = Dataset(nc_file, mode='r')
        levels = fh.variables[variables[var]["level_name"]][:]
        fh.close()
        
        # loop over levels that should be extracted
        for i, level in enumerate(variables[var]["levels"]):
        
            # find the closest available level
            level = min(levels, key=lambda x:abs(x-level))
        
            # use cdo's sellevel and write result to new file (name specified in local config)
            command = "cd " + dir + "; "
            output_file = variables[var]["output_names"][i] + ".nc"
            command += "cdo  -sellevel," + str(level) + " " + nc_file + " " + output_file
            os.system(command)
            
            # rename the variable
            command = "cd " + dir + "; "
            command += "cdo chname," + var + "," + variables[var]["output_names"][i] + " " + output_file + " tmp.nc; "
            command += "mv tmp.nc " + output_file
            os.system(command)
            
            
        
        
        