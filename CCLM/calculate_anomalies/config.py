dependencies = ["seasonal_mean", "process_reference", "extract_stations"]

import sys
sys.path.append('../')
import global_settings

variables = global_settings.variables

file_pairs = {}


for var in variables.keys():
    for season in variables[var]["seasons"]:
        file_pairs.update({ var + "-" + season : 
            [ 
                { "task" : "seasonal_mean" } ,
                { "task" : "seasonal_mean",
                  "file" : var + "-reference-" + season + "-remapped.nc" }
            ] 
        })
          

for var in variables.keys():
    for station in variables[var]["stations"].keys():
        file_pairs.update({ var + "-" + station : 
            [ 
                { "task" : "extract_stations" } ,
                { "task" : "extract_stations",
                  "file" : var + "-reference-" + station + ".nc" }
            ] 
        })


for var in variables.keys():
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
                  

