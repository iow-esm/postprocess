import os
import sys

out_dir = str(sys.argv[1])
from_date = int(sys.argv[2])
to_date = int(sys.argv[3])
pwd = str(sys.argv[4])

import create_results_dir

results_dir = create_results_dir.create_results_dir(out_dir, from_date, to_date)

sys.path.append(pwd)
from config import variables

file_pairs = {}

for var in variables.keys():

    try: 
        variables[var]["reference-file-pattern"]
    except:
        print("No reference is given for " + var)
        continue
        
    for season in variables[var]["seasons"]:
        file_pairs.update({ var + "-" + season : 
            [ 
                { "task" : "seasonal_mean" } ,
                { "task" : "seasonal_mean",
                  "file" : var + "-reference-" + season + "-remapped.nc" }
            ] 
        })

        try:
            percentiles = variables[var]["percentiles"]
        except:
            percentiles = []

        for p in percentiles:
            file_pairs.update({ var + "-" + season + "-PCTL_"+p : 
                [ 
                    { "task" : "seasonal_percentile" } ,
                    { "task" : "seasonal_percentile",
                    "file" : var+"-reference-"+season+"-PCTL_"+p+"-remapped.nc" }
                ] 
            })            
          

    for station in variables[var]["stations"].keys():
        file_pairs.update({ var + "-" + station : 
            [ 
                { "task" : "extract_stations" } ,
                { "task" : "extract_stations",
                  "file" : var + "-reference-" + station + ".nc" }
            ] 
        })


    for station in variables[var]["stations"].keys():
        for operator in variables[var]["time-series-operators"]:

            file_pairs.update({ var + "-" + station + operator : 
                [ 
                    { "task" : "extract_stations" } ,
                    { "task" : "extract_stations",
                      "file" : var + "-reference-" + station + operator + ".nc" }
                ] 
            })
                

            file_pairs.update({ var + "-ensmean" + operator : 
                [ 
                    { "task" : "extract_stations" } ,
                    { "task" : "extract_stations",
                      "file" : var + "-reference-ensmean" + operator + ".nc" }
                ] 
            })
            
            
            
                  
    for station in variables[var]["regions"].keys():
        file_pairs.update({ var + "-" + station : 
            [ 
                { "task" : "extract_regions" } ,
                { "task" : "extract_regions",
                  "file" : var + "-reference-" + station + ".nc" }
            ] 
        })

    for station in variables[var]["regions"].keys():
        for operator in variables[var]["time-series-operators"]:

            file_pairs.update({ var + "-" + station + operator : 
                [ 
                    { "task" : "extract_regions" } ,
                    { "task" : "extract_regions",
                      "file" : var + "-reference-" + station + operator + ".nc" }
                ] 
            })

for var in file_pairs.keys():
    command = "cdo -sub "
    
    try:
        command += file_pairs[var][0]["additional-operators"] + " "
    except:
        pass
        
    try:
        command += file_pairs[var][0]["path"] + "/" + file_pairs[var][0]["file"] + " "
    except:
        try:
            command += "../" + file_pairs[var][0]["task"] + "/" + results_dir + "/" + file_pairs[var][0]["file"] + " "
        except:
            command += "../" + file_pairs[var][0]["task"] + "/" + results_dir + "/" + var + ".nc "
            
    
    try:
        command += file_pairs[var][1]["additional-operators"] + " "
    except:
        pass
        
    try:
        command += file_pairs[var][1]["path"] + "/" + file_pairs[var][1]["file"] + " "
    except:
        try:
            command += "../" + file_pairs[var][1]["task"] + "/" + results_dir + "/" + file_pairs[var][1]["file"] + " "
        except:
            command += "../" + file_pairs[var][1]["task"] + "/" + results_dir + "/" + var + ".nc "
    
    command += results_dir + "/" + var + ".nc"
    
    os.system(command)