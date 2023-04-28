import glob
import os
import sys

out_dir = str(sys.argv[1])
from_date = int(sys.argv[2])
to_date = int(sys.argv[3])
pwd = str(sys.argv[4])

variables = {}
def prepare_variables():

    sys.path.append(pwd)
    import config

    for var in config.variables.keys():
        variables[var] = {
                    "seasons" : config.variables[var]["seasons"],
                    }
                    
        for station in config.variables[var]["stations"].keys():
            variables[var + "-" + station] = {
                            "seasons" : config.variables[var]["seasons"],
                            "task" : "extract_stations",
                            "file" : var + "-" + station + ".nc"
                            }    

        for region in config.variables[var]["regions"].keys():
            variables[var + "-" + region] = {
                            "seasons" : config.variables[var]["seasons"],
                            "task" : "extract_regions",
                            "file" : var + "-" + region + ".nc"
                            }                                     
                    
        try: 
            config.variables[var]["reference-file-pattern"]
        except:
            print("No reference is given for " + var)
            continue
        
            
        variables[var + "-reference"] = {
                                "seasons" : config.variables[var]["seasons"],
                                "task" : "process_reference",
                                "file" : var + ".nc",
                                "remapping-file" : "grid_" + var + ".txt",
                            }

        for station in config.variables[var]["stations"].keys():
            variables[var + "-reference-" + station] = {
                            "seasons" : config.variables[var]["seasons"],
                            "task" : "extract_stations",
                            "file" : var + "-reference-" + station + ".nc"
                            }                           

        for region in config.variables[var]["regions"].keys():
            variables[var + "-reference-" + region] = {
                            "seasons" : config.variables[var]["seasons"],
                            "task" : "extract_regions",
                            "file" : var + "-reference-" + region + ".nc"
                            }                          

import get_all_dirs_from_to

dirs = get_all_dirs_from_to.get_all_dirs_from_to(out_dir, from_date, to_date)

import create_results_dir
results_dir = create_results_dir.create_results_dir(out_dir, from_date, to_date)

prepare_variables()

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
            os.system("cdo -L -timmean -selmon,"+numbers+" -ymonsub "+cat_file+" -ymonmean "+cat_file+" "+output_file)
        else:
            os.system("cdo -L -timmean -ymonsub "+cat_file+" -ymonmean "+cat_file+" "+output_file)

        # add standard deviation to seasonal mean
        cmd = "for var in `cdo -showname "+output_file+"  2> /dev/null | grep -v \"showname:\"`; do "
        if numbers != "":
            cmd += "cdo -L -chname,$var,${var}_STD -timstd -selmon," + numbers +" -ymonsub "+cat_file+" -ymonmean "+cat_file+" "+output_file+"_STD; "
        else:
            cmd += "cdo -L -chname,$var,${var}_STD -timstd -ymonsub "+cat_file+" -ymonmean "+cat_file+" "+output_file+"_STD; "
        cmd += "cdo merge "+output_file+" "+output_file+"_STD "+results_dir+"/tmp.nc; rm "+output_file+"_STD; mv "+results_dir+"/tmp.nc "+output_file+"; done"
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