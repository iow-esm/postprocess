dependencies = ["process_reference", "process_raw_output"]

import sys
sys.path.append('../')
import global_settings
     
variables = {}

for var in global_settings.variables.keys():
    variables[var] = {
                "regions" : global_settings.variables[var]["regions"],
                "operators" : global_settings.variables[var]["time-series-operators"]
                }
                
    try: 
        global_settings.variables[var]["reference-file-pattern"]
    except:
        print("No reference is given for " + var)
        continue
        
    variables[var + "-reference"] = {
                            "regions" : global_settings.variables[var]["regions"],
                            "task" : "process_reference",
                            "file" : var + ".nc",
                            "operators" : global_settings.variables[var]["time-series-operators"]
                         }



