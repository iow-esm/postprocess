import glob
import os
import sys

from netCDF4 import Dataset
import numpy as np

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
        variables[var]["reference-file-pattern"]
    except:
        print("No reference is given for " + var)
        continue

    operator = "-monmean"
    if not operator in variables[var]["time-series-operators"]:
        continue

    for station in variables[var]["stations"]:
        # get standard deviation of reference time mean
        command = "cdo chname,"+var+"_STD,"+var+" -selvar,"+var+"_STD ../extract_stations/"+results_dir+"/"+var+"-reference-"+station+operator+".nc "+results_dir+"/"+var+"_STD-"+station+".nc"
        os.system(command)
        # get the difference between varaible and reference time mean
        command = "cdo selvar,"+var+" ../calculate_anomalies/"+results_dir+"/"+var+"-"+station+operator+".nc "+results_dir+"/"+var+"-"+station+".nc"
        os.system(command)

        # divide diference by standard deviation and the absolute value
        command = "cdo -timmean -abs -div "+results_dir+"/"+var+"-"+station+".nc "+results_dir+"/"+var+"_STD-"+station+".nc "+results_dir+"/"+var+"_C-"+station+".nc"
        os.system(command)

        command = "cdo -timmean "+results_dir+"/"+var+"_C-"+station+".nc "+results_dir+"/"+var+"-"+station+"-cost.nc"
        os.system(command)

        fh = Dataset(results_dir+"/"+var+"-"+station+"-cost.nc", mode='r')
        cost =  np.squeeze(fh.variables[var][:])
        fh.close()

        print(var, station, cost)
