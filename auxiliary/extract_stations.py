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

def convert_to_decimal(value):
    if ":" not in value:
        return value
    
    tmp = value.split(":")
    decimal_value = float(tmp[0]) + float(tmp[1])/60.0 + float(tmp[2])/3600.0
    
    return str(decimal_value)

# go over all variables from where we extract (as defined in the local config)
for var in variables.keys():

    stations = variables[var]["stations"]

    if not stations:
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
    
    try:
        operators = variables[var]["operators"]
    except:
        operators = []

    # go over stations
    for station in stations.keys():
        # extract the station's time series via the remapnn (nearest neighbor) operator from cdo
        command = "cdo -remapnn,lon=" + convert_to_decimal(stations[station]["lon"]) + "/lat=" + convert_to_decimal(stations[station]["lat"]) + " " + cat_file + " " + results_dir + "/" + var + "-" + station + ".nc"
        os.system(command)
        
        # apply operators to the station time series
        for operator in operators:
            if operator == "":
                continue
            command = "cdo " + operator + " " + results_dir + "/" + var + "-" + station + ".nc" + " " + results_dir + "/" + var + "-" + station + operator + ".nc"
            os.system(command)

    os.system("rm " + cat_file)

    # add standard deviation for mean operators
    for station in stations.keys():
        for operator in operators:
            if operator[-4:] == "mean":
            
                std_operator = operator[:-4] + "std1"
                std_file = results_dir + "/" + var + "-" + station + operator + "_STD.nc"
                mean_file = results_dir + "/" + var + "-" + station + operator + ".nc"
                
                command = "cdo " + std_operator + " " + results_dir + "/" + var + "-" + station + ".nc" + " " + std_file   
                os.system(command)
                
                command = "for var in `cdo showname " + std_file + " 2> /dev/null | grep -v \"showname:\"`; do "
                command += "cdo chname,$var,${var}_STD " + std_file + " tmp.nc; mv tmp.nc " + std_file + "; done"
                os.system(command)
                
                command = "cdo merge " + std_file + " " + mean_file + " tmp.nc; mv tmp.nc " + mean_file    
                os.system(command)
                
                command = "rm " + std_file
                os.system(command)   
      
    # add a mean over all station time series (ensmean) and add the standard deviation to that mean         
    files = ""        
    for station in stations.keys():
        files += results_dir + "/" + var + "-" + station + ".nc "
        
    command = "cdo ensmean " + files + " " + results_dir + "/" + var + "-ensmean.nc"   
    os.system(command)
    
    command = "cdo ensstd1 " + files + " " + results_dir + "/" + var + "_STD.nc"   
    os.system(command)
    
    command = "for var in `cdo showname " + results_dir + "/" + var + "_STD.nc 2> /dev/null | grep -v \"showname:\"`; do "
    command += "cdo chname,$var,${var}_STD " + results_dir + "/" + var + "_STD.nc tmp.nc; mv tmp.nc " + results_dir + "/" + var + "_STD.nc; done"
    os.system(command)
    
    command = "cdo merge " + results_dir + "/" + var + "_STD.nc " + results_dir + "/" + var + "-ensmean.nc tmp.nc; mv tmp.nc " + results_dir + "/" + var + "-ensmean.nc"    
    os.system(command)
    
    command = "rm " + results_dir + "/" + var + "_STD.nc"
    os.system(command)
    
    # apply operators also to mean over stations
    for operator in operators:
        if operator == "":
            continue
        command = "cdo " + operator + " " + results_dir + "/" + var + "-ensmean.nc" + " " + results_dir + "/" + var + "-ensmean" + operator + ".nc"
        os.system(command)
        