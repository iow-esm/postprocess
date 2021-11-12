import glob
import os
import sys

# decode the input arguments
out_dir = str(sys.argv[1])
from_date = int(sys.argv[2])
to_date = int(sys.argv[3])

# read the local config
try:
    from config import sellonlatbox
    sellonlatbox = " -sellonlatbox," + sellonlatbox
except:
    sellonlatbox = ""

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

try:
    from config import operators
except:
    operators = [""]
    
for operator in operators:
    command = "cdo " + operator
    command += " -fldmean " + sellonlatbox + " -cat \'" + files + "\' " + results_dir + "/FI" + operator + ".nc"
    os.system(command)

try:
    from config import additional_files
except:
    exit()
    
for f in additional_files.keys():

    try:
        files = sorted(glob.glob(additional_files[f]["path"]))
    except:
        try:
           files = sorted(glob.glob("../" + additional_files[f]["task"] + "/" + results_dir + "/" + additional_files[f]["file"])) 
        except:
           files = sorted(glob.glob("../" + additional_files[f]["task"] + "/" + results_dir + "/FI.nc"))
           
    files = " ".join(files)

    if from_date > 0 and to_date > 0:
        seldate = " -seldate," + str(from_date)[0:4] + "-" + str(from_date)[4:6] + "-" + str(from_date)[6:8] + "," + str(to_date)[0:4] + "-" + str(to_date)[4:6] + "-" + str(to_date)[6:8]
    else:
        seldate = ""
        
    for operator in operators:
        command = "cdo " + operator
        command += " -fldmean " + sellonlatbox + " " + seldate + " -cat \'" + files + "\' " + results_dir + "/" + f + operator + ".nc"
        os.system(command)
