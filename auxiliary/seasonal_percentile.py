import glob
import os
import sys

out_dir = str(sys.argv[1])
from_date = int(sys.argv[2])
to_date = int(sys.argv[3])
pwd = str(sys.argv[4])

sys.path.append(pwd)

import config

variables = {}

for var in config.variables.keys():

    variables[var] = {}

    try:
        variables[var]["percentiles"] = config.variables[var]["percentiles"]
    except:
        continue

    try:
        variables[var]["seasons"] = config.variables[var]["seasons"]
    except:
        continue     

    try: 
        stations = config.variables[var]["stations"].keys()
    except:
        stations = []

    for station in stations:
        variables[var + "-" + station] = {
                        "seasons" : config.variables[var]["seasons"],
                        "percentiles" : config.variables[var]["percentiles"],
                        "task" : "extract_stations",
                        "file" : var + "-" + station + ".nc"
                        }    

    try: 
        regions = config.variables[var]["regions"].keys()
    except:
        regions = []

    for region in regions:
        variables[var + "-" + region] = {
                        "seasons" : config.variables[var]["seasons"],
                        "percentiles" : config.variables[var]["percentiles"],
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
                            "percentiles" : config.variables[var]["percentiles"],
                            "task" : "process_reference",
                            "file" : var + ".nc",
                            "remapping-file" : "grid_" + var + ".txt",
                         }                    

    for station in stations:
        variables[var + "-reference-" + station] = {
                        "seasons" : config.variables[var]["seasons"],
                        "percentiles" : config.variables[var]["percentiles"],
                        "task" : "extract_stations",
                        "file" : var + "-reference-" + station + ".nc"
                        }                           

    for region in regions:
        variables[var + "-reference-" + region] = {
                        "seasons" : config.variables[var]["seasons"],
                        "percentiles" : config.variables[var]["percentiles"],
                        "task" : "extract_regions",
                        "file" : var + "-reference-" + region + ".nc"
                        }        

import get_all_dirs_from_to
dirs = get_all_dirs_from_to.get_all_dirs_from_to(out_dir, from_date, to_date)

import create_results_dir
results_dir = create_results_dir.create_results_dir(out_dir, from_date, to_date)

for var in variables:

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

        if numbers != "":
            selmon = "-selmon,"+numbers
        else:
            selmon = ""
    
        os.system("cdo timmin  "+selmon+" "+cat_file+" "+results_dir+"/minfile.nc")
        os.system("cdo timmax  "+selmon+" "+cat_file+" "+results_dir+"/maxfile.nc")
        
        for p in variables[var]["percentiles"]:
            output_file = results_dir+"/"+var+"-"+names+"-PCTL_"+p+".nc"
            os.system("cdo timpctl,"+p+" "+selmon+" "+cat_file+" "+results_dir+"/minfile.nc "+results_dir+"/maxfile.nc "+output_file)

            try:
                try:
                    remapping_file_path = variables[var]["remapping-file-path"]
                except:
                    remapping_file_path = "../create_remapping_files/" + results_dir # default if no path is given
                    
                remapped_file = output_file.split(".nc")[0] + "-remapped.nc"
                os.system("cdo -remapbil," + remapping_file_path + "/" + variables[var]["remapping-file"] + " " + output_file + " " + remapped_file)

            except:
                pass
        
        os.system("rm "+results_dir+"/maxfile.nc "+results_dir+"/minfile.nc ")

    os.system("rm " + cat_file)