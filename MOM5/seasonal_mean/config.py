# this depends on a processed raw output
dependencies = ["process_raw_output", "process_reference"]

import sys
sys.path.append('../')
import global_settings

variables = {}

for var in global_settings.variables.keys():
    variables[var] = {
                "seasons" : global_settings.variables[var]["seasons"],
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