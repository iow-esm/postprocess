# dictionary for level extraction
# keys: name of variable from which we extraction
# values: dictionary with
#               - name of the vertical coordinate ("level_name")
#               - list of level values ("levels"), floats in units of vertical coordinate, closest possible value will be extracted
#               - list of variable names ("output_names") that correspond to the "levels" list, resulting output file will also have this name 
variables = { "temp" : {"level_name" : "st_ocean",
                        "levels" : [0.0],
                        "output_names" : ["sst"]},
             "salt" : {"level_name" : "st_ocean",
                        "levels" : [0.0],
                        "output_names" : ["sss"]}
             }