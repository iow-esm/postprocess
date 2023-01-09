import glob
import os
import sys

out_dir = str(sys.argv[1])
from_date = int(sys.argv[2])
to_date = int(sys.argv[3])
pwd = str(sys.argv[4])

sys.path.append(pwd)
import config
variables = config.variables

import create_results_dir
results_dir = create_results_dir.create_results_dir(out_dir, from_date, to_date)

if from_date > 0 and to_date > 0:
    seldate = " -seldate," + str(from_date)[0:4] + "-" + str(from_date)[4:6] + "-" + str(from_date)[6:8] + "," + str(to_date)[0:4] + "-" + str(to_date)[4:6] + "-" + str(to_date)[6:8]
else:
    seldate = ""
    
try:
    sellonlatbox = " -sellonlatbox," + config.sellonlatbox
except:
    sellonlatbox = ""

for var in variables.keys():	

    try: 
        variables[var]["reference-file-pattern"]
    except:
        print("No reference is given for " + var)
        continue

    files = sorted(glob.glob(variables[var]["reference-file-pattern"]))
    files = " ".join(files)
    
    merge_file = results_dir + "/" + var + ".nc"
    
    try:
        additional_operators = variables[var]["reference-additional-operators"]
    except:
        additional_operators = ""
        
    os.system("cdo " +  additional_operators + " -selvar," + variables[var]["reference-variable-name"] + sellonlatbox + seldate +  " -mergetime " + files + " " + merge_file)
    
    if variables[var]["reference-variable-name"] != var:
        os.system("cdo chname," + variables[var]["reference-variable-name"] + "," + var + " " + merge_file + " " + results_dir +"/tmp.nc; mv " + results_dir +"/tmp.nc " + merge_file)

    try: 
        try:
            remapping_file_path = variables[var]["remapping-file-path"]
        except:
            remapping_file_path = "../create_remapping_files/" + results_dir # default if no path is given
            
        remapped_file = merge_file.split(".nc")[0] + "-remapped.nc"
        remapping_file = "grid_" + var + ".txt"

        os.system("cdo -remapbil," + remapping_file_path + "/" + remapping_file + " " + merge_file + " " + remapped_file)
    except:
        pass

import process_BED
process_BED.process_BED(variables, results_dir, from_date, to_date)