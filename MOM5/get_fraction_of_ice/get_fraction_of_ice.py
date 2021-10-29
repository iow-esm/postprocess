import glob
import os
import sys

# decode the input arguments
out_dir = str(sys.argv[1])
from_date = int(sys.argv[2])
to_date = int(sys.argv[3])

# get all dirs to be processed
sys.path.append('../../auxiliary')
import get_all_dirs_from_to

dirs = get_all_dirs_from_to.get_all_dirs_from_to(out_dir, from_date, to_date)

# go over all desired directories
for dir in dirs:

    # if ice concentration is available get the fraction of ice as a vertical sum over thickness
    if glob.glob(dir + "/CN.nc") == []:
        print("No CN.nc found in " + dir)
        continue
        
    command = "cd " + dir + "/; "
    command += "cdo vertsum CN.nc FI.nc; "
    command += "cdo chname,CN,FI FI.nc tmp.nc && mv tmp.nc FI.nc; "
    command += "cdo setattribute,FI@long_name=\"fraction of ice\" FI.nc tmp.nc && mv tmp.nc FI.nc; "
    os.system(command)
   
