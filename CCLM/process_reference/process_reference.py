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

if reference == "E-OBS":
    for var in variables.keys():
        files[var] = out_dir + "/" + variables[var] + ".nc "

for var in variables.keys():	
    for names, numbers in seasons.items():
    
        output_file = results_dir + "/" + var + "-" + names + ".nc"
        os.system("cdo -timmean -selmon," + numbers + seldate +  " -cat \'" + files[var] + "\' " + output_file)
        
        os.system("cdo timmin -selmon," + numbers + seldate + " -cat \'" + files[var] + "\' "  + results_dir + "/minfile.nc")
        os.system("cdo timmax -selmon," + numbers + seldate + " -cat \'" + files[var] + "\' "  + results_dir + "/maxfile.nc")
        
        for p in percentiles:
            output_file = results_dir + "/" + var + "-" + names + "-PCTL_" + p + ".nc"
            os.system("cdo timpctl," + p + " -selmon," + numbers + seldate + " -cat \'" + files[var] + "\' " + results_dir + "/minfile.nc " + results_dir + "/maxfile.nc " + output_file)
            
        os.system("rm " + results_dir + "/maxfile.nc " + results_dir + "/minfile.nc ")

if reference == "E-OBS":
    for var in variables.keys():
        for names, numbers in seasons.items():
            output_file = results_dir + "/" + var + "-" + names + ".nc"
            os.system("cdo chname,longitude,lon " + output_file + " tmp.nc; mv tmp.nc " + output_file)
            os.system("cdo chname,latitude,lat " + output_file + " tmp.nc; mv tmp.nc " + output_file)
            os.system("cdo chname," + variables[var].split("_")[0] + "," + var + " " + output_file + " tmp.nc; mv tmp.nc " + output_file)
            
            for p in percentiles:
                output_file = results_dir + "/" + var + "-" + names + "-PCTL_" + p + ".nc"
                os.system("cdo chname,longitude,lon " + output_file + " tmp.nc; mv tmp.nc " + output_file)
                os.system("cdo chname,latitude,lat " + output_file + " tmp.nc; mv tmp.nc " + output_file)
                os.system("cdo chname," + variables[var].split("_")[0] + "," + var + " " + output_file + " tmp.nc; mv tmp.nc " + output_file)
            