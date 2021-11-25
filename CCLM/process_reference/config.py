dependencies = ["create_remapping_files"]

import sys
sys.path.append('../')
import global_settings

seasons = global_settings.seasons

percentiles = global_settings.percentiles

variables = {}
for var in global_settings.variables.keys():     
    variables[var] =  {    "file-pattern" : global_settings.variables[var]["reference-file-pattern"],
                            "name" : global_settings.variables[var]["reference-variable-name"],
                            "remapping-file" : "grid_" + var + ".txt",
                            "seasons" : seasons,
                            "percentiles" : percentiles
                       } 
    try:
        variables[var]["additional-operators"] = global_settings.variables[var]["reference-additional-operators"]
    except:
        pass




