dependencies = ["process_reference", "process_raw_output"]

import sys
sys.path.append('../')
import global_settings
     
variables = {}

for var in global_settings.variables.keys():
    variables[var] = {
                "stations" : global_settings.variables[var]["stations"],
                "operators" : global_settings.variables[var]["time-series-operators"]
                }
    variables[var + "-reference"] = {
                            "stations" : global_settings.variables[var]["stations"],
                            "task" : "process_reference",
                            "file" : var + ".nc",
                            "operators" : global_settings.variables[var]["time-series-operators"]
                         }



