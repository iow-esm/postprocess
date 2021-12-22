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

    try:
        files = glob.glob(variables[var]["path"] + "/" + variables[var]["file"])
    except:
        try:
            files = glob.glob("../" + variables[var]["task"] + "/" + results_dir + "/" + variables[var]["file"])
        except:
            files = [dir + "/" + var + ".nc" for dir in dirs]
            
    files = " ".join(files)
    
    try:
        operators = variables[var]["operators"]
    except:
        operators = []
    
    stations = variables[var]["regions"]
    for station in stations.keys():
        lonlatbox = convert_to_decimal(stations[station]["lon-min"]) + "," + convert_to_decimal(stations[station]["lon-max"]) + "," + convert_to_decimal(stations[station]["lat-min"]) + "," + convert_to_decimal(stations[station]["lat-max"])
        command = "cdo -fldmean -sellonlatbox," + lonlatbox + " -cat \'" + files + "\' " + results_dir + "/" + var + "-" + station + ".nc"
        os.system(command)
        
        for operator in operators:
            command = "cdo " + operator + " " + results_dir + "/" + var + "-" + station + ".nc" + " " + results_dir + "/" + var + "-" + station + operator + ".nc"
            os.system(command)
            
    for station in stations.keys():
        for operator in operators:
            if operator[-4:] == "mean":
            
                std_operator = operator[:-4] + "std1"
                std_file = results_dir + "/" + var + "-" + station + operator + "_STD.nc"
                mean_file = results_dir + "/" + var + "-" + station + operator + ".nc"
                
                command = "cdo " + std_operator + " " + results_dir + "/" + var + "-" + station + ".nc" + " " + std_file   
                os.system(command)
                
                command = "for var in `cdo showname " + std_file + "`; do "
                command += "cdo chname,$var,${var}_STD " + std_file + " tmp.nc; mv tmp.nc " + std_file + "; done"
                os.system(command)
                
                command = "cdo merge " + std_file + " " + mean_file + " tmp.nc; mv tmp.nc " + mean_file    
                os.system(command)
                
                command = "rm " + std_file
                os.system(command)   
        