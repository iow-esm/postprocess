dependencies = ["process_reference", "process_raw_output"]

import sys
sys.path.append('../')
import global_settings

stations = global_settings.stations

operators = global_settings.time_series_operators
     
variables = {}

for var in global_settings.variables.keys():
    variables[var] = {
                "stations" : stations,
                "operators" : operators,
                }
    variables[var + "-reference"] = {
                            "stations" : stations,
                            "task" : "process_reference",
                            "file" : var + ".nc",
                            "operators" : operators,
                         }



