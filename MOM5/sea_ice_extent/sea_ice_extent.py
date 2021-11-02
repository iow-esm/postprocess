import glob
import os
import sys

# decode the input arguments
out_dir = str(sys.argv[1])
from_date = int(sys.argv[2])
to_date = int(sys.argv[3])

# read the local config
#from config import files_to_process, path_to_mppn, station_pattern

# get all dirs to be processed
sys.path.append('../../auxiliary')
import get_all_dirs_from_to

dirs = get_all_dirs_from_to.get_all_dirs_from_to(out_dir, from_date, to_date)

import create_results_dir
results_dir = create_results_dir.create_results_dir(out_dir, from_date, to_date)

# go over all desired directories
files = ""
for dir in dirs:
    files += dir + "/FI.nc "

command = "cdo -yearmax "
command += "-divc,`cdo -s -infov " + files.split(" ")[0] + " | awk '{if(NR==2){print $6-$7}}'`"
command += " -fldsum -cat \'" + files + "\' " + results_dir + "/FI.nc"

os.system(command)

try:
    from config import reference_file_pattern
    files = sorted(glob.glob(reference_file_pattern))
    files = " ".join(files)

    if from_date > 0 and to_date > 0:
        seldate = " -seldate," + str(from_date)[0:4] + "-" + str(from_date)[4:6] + "-" + str(from_date)[6:8] + "," + str(to_date)[0:4] + "-" + str(to_date)[4:6] + "-" + str(to_date)[6:8]
    else:
        seldate = ""

    command = "cdo -yearmax "
    command += "-divc,`cdo -s -infov " + files.split(" ")[0] + " | awk '{if(NR==2){print $6-$7}}'`"
    command += " -fldsum " + seldate + " -cat \'" + files + "\' " + results_dir + "/FI-reference.nc"

    os.system(command)
 
except:
    pass

#cdo -yearmax -divc,`cdo ngridpoints /scratch/usr/mvkkarst/IOW_ESM/postprocess/MOM5/process_reference/results/_scratch_usr_mvkkarst_obs_Copernicus-19810901_20091130/FI-remapped.nc` -fldsum /scratch/usr/mvkkarst/IOW_ESM/postprocess/MOM5/process_reference/results/_scratch_usr_mvkkarst_obs_Copernicus-19810901_20091130/FI-remapped.nc test_obs.nc
    


