import glob
import os
import sys

out_dir = str(sys.argv[1])
from_date = int(sys.argv[2])
to_date = int(sys.argv[3])

import config
variables = config.variables
seasons = config.seasons
percentiles = config.percentiles
reference = config.reference

sys.path.append('../../auxiliary')
import create_results_dir

results_dir = create_results_dir.create_results_dir(out_dir, from_date, to_date)

if from_date > 0 and to_date > 0:
    seldate = " -seldate," + str(from_date)[0:4] + "-" + str(from_date)[4:6] + "-" + str(from_date)[6:8] + "," + str(to_date)[0:4] + "-" + str(to_date)[4:6] + "-" + str(to_date)[6:8]
else:
    seldate = ""
    
files={}

try:
    sellonlatbox = " -sellonlatbox," + config.sellonlatbox
except:
    sellonlatbox = ""

if reference == "Copernicus":
    for var in variables.keys():
        all_files = sorted(glob.glob(out_dir + "/" + variables[var]["pattern"]))
        files[var] = ""
        for file in all_files:
            files[var] += file + " " 

for var in variables.keys():	
    merge_file = results_dir + "/" + var + ".nc"
    os.system("cdo -selvar," + variables[var]["name"] + sellonlatbox + seldate +  " -mergetime " + files[var] + " " + merge_file)
    
    for names, numbers in seasons.items():
    
        output_file = results_dir + "/" + var + "-" + names + ".nc"
        os.system("cdo -timmean " + " -selmon," + numbers +  " " + merge_file + " " + output_file)
        
        os.system("cdo timmin " + " -selmon," + numbers + " " + merge_file + " "  + results_dir + "/minfile.nc")
        os.system("cdo timmax " + " -selmon," + numbers + " " + merge_file + " "  + results_dir + "/maxfile.nc")
        
        for p in percentiles:
            output_file = results_dir + "/" + var + "-" + names + "-PCTL_" + p + ".nc"
            os.system("cdo timpctl," + p + " -selmon," + numbers + seldate + " " + merge_file + " " + results_dir + "/minfile.nc " + results_dir + "/maxfile.nc " + output_file)
            
        os.system("rm " + results_dir + "/maxfile.nc " + results_dir + "/minfile.nc ")

if reference == "Copernicus":
    for var in variables.keys():
        for names, numbers in seasons.items():
            output_file = results_dir + "/" + var + "-" + names + ".nc"
            os.system("cdo chname,lon,xt_ocean " + output_file + " tmp.nc; mv tmp.nc " + output_file)
            os.system("cdo chname,lat,yt_ocean " + output_file + " tmp.nc; mv tmp.nc " + output_file)
            os.system("cdo chname," + variables[var]["name"] + "," + var + " " + output_file + " tmp.nc; mv tmp.nc " + output_file)
            
            for p in percentiles:
                output_file = results_dir + "/" + var + "-" + names + "-PCTL_" + p + ".nc"
                os.system("cdo chname,lon,xt_ocean " + output_file + " tmp.nc; mv tmp.nc " + output_file)
                os.system("cdo chname,lat,yt_ocean " + output_file + " tmp.nc; mv tmp.nc " + output_file)
                os.system("cdo chname," + variables[var]["name"] + "," + var + " " + output_file + " tmp.nc; mv tmp.nc " + output_file)
            