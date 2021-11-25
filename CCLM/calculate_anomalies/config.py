dependencies = ["seasonal_mean", "process_reference", "extract_stations"]

import sys
sys.path.append('../')
import global_settings

seasons = global_settings.seasons
variables = global_settings.variables.keys()

stations = global_settings.stations
operators = global_settings.time_series_operators

file_pairs = {}

for season in seasons:
    for var in variables:
        file_pairs.update({ var + "-" + season : 
            [ 
                { "task" : "seasonal_mean" } ,
                { "task" : "process_reference",
                  "file" : var + "-" + season + "-remapped.nc" }
            ] 
        })
          
for station in stations.keys():
    for var in variables:
        file_pairs.update({ var + "-" + station : 
            [ 
                { "task" : "extract_stations" } ,
                { "task" : "extract_stations",
                  "file" : var + "-reference-" + station + ".nc" }
            ] 
        })


for operator in operators:
    for station in stations.keys():
        for var in variables:
            file_pairs.update({ var + "-" + station + operator : 
                [ 
                    { "task" : "extract_stations" } ,
                    { "task" : "extract_stations",
                      "file" : var + "-reference-" + station + operator + ".nc" }
                ] 
            })
                
    for var in variables:
        file_pairs.update({ var + "-ensmean" + operator : 
            [ 
                { "task" : "extract_stations" } ,
                { "task" : "extract_stations",
                  "file" : var + "-reference-ensmean" + operator + ".nc" }
            ] 
        })
                  

