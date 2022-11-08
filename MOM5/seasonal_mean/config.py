# this depends on a processed raw output
dependencies = ["process_raw_output", "process_reference", "extract_stations"]

import sys
sys.path.append('../')
import global_settings

variables = {}

for var in global_settings.variables.keys():
    variables[var] = {
                "seasons" : global_settings.variables[var]["seasons"],
                }
                
    for station in global_settings.variables[var]["stations"].keys():
        variables[var + "-" + station] = {
                        "seasons" : global_settings.variables[var]["seasons"],
                        "task" : "extract_stations",
                        "file" : var + "-" + station + ".nc"
                        }    

    for region in global_settings.variables[var]["regions"].keys():
        variables[var + "-" + region] = {
                        "seasons" : global_settings.variables[var]["seasons"],
                        "task" : "extract_regions",
                        "file" : var + "-" + region + ".nc"
                        }                                     
                
    try: 
        global_settings.variables[var]["reference-file-pattern"]
    except:
        print("No reference is given for " + var)
        continue
    
        
    variables[var + "-reference"] = {
                            "seasons" : global_settings.variables[var]["seasons"],
                            "task" : "process_reference",
                            "file" : var + ".nc",
                            "remapping-file" : "grid_" + var + ".txt",
                         }

    for station in global_settings.variables[var]["stations"].keys():
        variables[var + "-reference-" + station] = {
                        "seasons" : global_settings.variables[var]["seasons"],
                        "task" : "extract_stations",
                        "file" : var + "-reference-" + station + ".nc"
                        }                           

    for region in global_settings.variables[var]["regions"].keys():
        variables[var + "-reference-" + region] = {
                        "seasons" : global_settings.variables[var]["seasons"],
                        "task" : "extract_regions",
                        "file" : var + "-reference-" + region + ".nc"
                        }                          