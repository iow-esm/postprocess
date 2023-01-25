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

from helpers import convert_to_decimal

def prepare_variable(var):
    try:
        variables[var]["reference-file-pattern"]
    except:
        return False

    regions = variables[var]["regions"]

    if len(regions.keys()) == 0:
        return False

    seasons = variables[var]["seasons"]

    if len(seasons.keys()) == 0:
        return False    
    
    try:
        files = glob.glob(variables[var]["path"] + "/" + variables[var]["file"])
    except:
        try:
            files = glob.glob("../" + variables[var]["task"] + "/" + results_dir + "/" + variables[var]["file"])
        except:
            files = [dir + "/" + var + ".nc" for dir in dirs]

    if files == []:
        print("No netcdf files found for variable "+var)
        return False

    cat_file = results_dir + "/" + var + ".nc"
    if len(files) > 1:       
        files = " ".join(files)
        os.system("cdo  -cat \'" + files + "\' " + cat_file)
    else:
        os.system("cp "+files[0]+" "+cat_file)

    return True

def mask_out(var, region):

    cat_file = results_dir + "/" + var + ".nc"
    reference_file = "../process_reference/"+results_dir+"/"+var+"-remapped.nc"

    try:
        maskfile = variables[var]["regions"][region]["maskfile"]
    except:
        maskfile = None

    if maskfile is None:
        lonlatbox = convert_to_decimal(variables[var]["regions"][region]["lon-min"]) + "," + convert_to_decimal(variables[var]["regions"][region]["lon-max"]) + "," + convert_to_decimal(variables[var]["regions"][region]["lat-min"]) + "," + convert_to_decimal(variables[var]["regions"][region]["lat-max"])
        command = "cdo -sellonlatbox," + lonlatbox + " " + cat_file + " " + results_dir + "/" + var + "-" + region + ".nc"
        os.system(command)

        command = "cdo -sellonlatbox," + lonlatbox + " " + reference_file + " " + results_dir + "/" + var + "-reference-" + region + ".nc"
        os.system(command)
    else:
        command = "cp "+cat_file+" "+cat_file+"2; "
        command += "cdo -div " + cat_file + " -remapnn,"+cat_file+"2 "+maskfile + " " + results_dir + "/" + var + "-" + region + ".nc"
        command += "; rm "+cat_file+"2"
        os.system(command)

        command = "cp "+reference_file+" "+cat_file+"2; "
        command += "cdo -div " + reference_file + " -remapnn,"+cat_file+"2 "+maskfile + " " + results_dir + "/" + var + "-reference-" + region + ".nc"
        command += "; rm "+cat_file+"2"
        os.system(command)

def calculate_anommaly(var, region):
    cat_file = results_dir + "/" + var + "-" + region + ".nc"
    reference_file = results_dir + "/" + var + "-reference-" + region +  ".nc"
    command = "cdo -sub "+cat_file+" "+reference_file+" "+results_dir+"/tmp.nc; "
    command += "mv "+results_dir+"/tmp.nc "+cat_file+"; rm "+reference_file
    os.system(command)

# go over all variables from where we extract (as defined in the local config)
seasons = {}
valid_variables = []
for var in variables.keys():

    if not prepare_variable(var):
        continue

    valid_variables.append(var)

    for season in variables[var]["seasons"].keys():
        if season not in seasons.keys():
            seasons[season] = variables[var]["seasons"][season]

for var in valid_variables:

    for region in variables[var]["regions"].keys():
        mask_out(var, region)
        calculate_anommaly(var,region)

        cat_file = results_dir + "/" + var + "-" + region + ".nc"

        for season in seasons.keys():

            selmon = ""
            if seasons[season] != "":
                selmon += " -selmon,"+seasons[season]

            command = "cdo -sqrt -timsum "+selmon+" -fldsum -sqr "+cat_file+" "+results_dir+"/norm-"+ var + "-"+region+"-"+season+".nc"
            os.system(command)

for i, var_i in enumerate(valid_variables):
    for j, var_j in enumerate(valid_variables):

        if j <= i:
            continue

        for region in variables[var_j]["regions"].keys():
            if region not in variables[var_i]["regions"].keys():
                continue

            for season in seasons.keys():

                selmon = ""
                if seasons[season] != "":
                    selmon += " -selmon,"+seasons[season]
        
                cat_file_i = results_dir + "/" + var_i + "-" + region + ".nc"
                cat_file_j = results_dir + "/" + var_j + "-" + region + ".nc"
                command = "cdo -timsum "+selmon+" -fldsum -mul "+cat_file_i+" "+cat_file_j+" "+results_dir+"/tmp.nc"
                os.system(command)
                command = "cdo -div "+results_dir+"/tmp.nc "+results_dir+"/norm-"+ var_i +"-"+region+"-"+season+".nc "+results_dir+"/tmp2.nc"
                os.system(command)
                command = "cdo -div "+results_dir+"/tmp2.nc "+results_dir+"/norm-"+ var_j +"-"+region+"-"+season+".nc "+results_dir+"/"+var_i+"-"+var_j+"-"+region+"-"+season+".nc; rm "+results_dir+"/tmp*.nc"
                os.system(command)
        