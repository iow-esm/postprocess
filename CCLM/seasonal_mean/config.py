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
    variables[var + "-reference"] = {
                            "seasons" : global_settings.variables[var]["seasons"],
                            "task" : "process_reference",
                            "file" : var + ".nc",
                            "remapping-file" : "grid_" + var + ".txt",
                         }