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

    if not variables[var]["seasons"]:
        continue

    try:
        files = glob.glob(variables[var]["path"] + "/" + variables[var]["file"])
    except:
        try:
            files = glob.glob("../" + variables[var]["task"] + "/" + results_dir + "/" + variables[var]["file"])
        except:
            files = [dir + "/" + var + ".nc" for dir in dirs]

    if files == []:
        print("No netcdf files found for variable "+var)
        continue

    cat_file = results_dir + "/" + var + ".nc"
    if len(files) > 1:       
        files = " ".join(files)
        os.system("cdo  -cat \'" + files + "\' " + cat_file)
    else:
        os.system("cp "+files[0]+" "+cat_file)
	
    for names, numbers in variables[var]["seasons"].items():
    
        output_file = results_dir + "/" + var + "-" + names + ".nc"
        if numbers != "":
            os.system("cdo -timmean -selmon," + numbers + " " + cat_file + " " + output_file)
        else:
            os.system("cdo -timmean " + cat_file + " " + output_file)

        # add standard deviation to seasonal mean
        cmd = "for var in `cdo -showname "+output_file+"  2> /dev/null | grep -v \"showname:\"`; do "
        if numbers != "":
            cmd += "cdo -chname,$var,${var}_STD -timstd -selmon," + numbers + " " + cat_file + " " + output_file+"_STD; "
        else:
            cmd += "cdo -chname,$var,${var}_STD -timstd " + cat_file + " " + output_file+"_STD; "
        cmd += "cdo merge "+output_file+" "+output_file+"_STD tmp.nc; rm "+output_file+"_STD; mv tmp.nc "+output_file+"; done"
        os.system(cmd)

        try:
            try:
                remapping_file_path = variables[var]["remapping-file-path"]
            except:
                remapping_file_path = "../create_remapping_files/" + results_dir # default if no path is given
                
            remapped_file = output_file.split(".nc")[0] + "-remapped.nc"
            os.system("cdo -remapbil," + remapping_file_path + "/" + variables[var]["remapping-file"] + " " + output_file + " " + remapped_file)

        except:
            pass

    os.system("rm " + cat_file)