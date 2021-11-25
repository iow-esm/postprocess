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

import get_all_dirs_from_to

dirs = get_all_dirs_from_to.get_all_dirs_from_to(out_dir, from_date, to_date)

import create_results_dir
results_dir = create_results_dir.create_results_dir(out_dir, from_date, to_date)

for var in variables.keys():

    try:
        files = glob.glob(variables[var]["path"] + "/" + variables[var]["file"])
    except:
        try:
            files = glob.glob("../" + variables[var]["task"] + "/" + results_dir + "/" + variables[var]["file"])
        except:
            files = [dir + "/" + var + ".nc" for dir in dirs]
            
    files = " ".join(files)
	
    for names, numbers in variables[var]["seasons"].items():
    
        output_file = results_dir + "/" + var + "-" + names + ".nc"
        os.system("cdo -timmean -selmon," + numbers + " -cat \'" + files + "\' " + output_file)
        
        try:
            try:
                remapping_file_path = variables[var]["remapping-file-path"]
            except:
                remapping_file_path = "../create_remapping_files/" + results_dir # default if no path is given
                
            remapped_file = output_file.split(".nc")[0] + "-remapped.nc"
            os.system("cdo -remapbil," + remapping_file_path + "/" + variables[var]["remapping-file"] + " " + output_file + " " + remapped_file)

        except:
            pass