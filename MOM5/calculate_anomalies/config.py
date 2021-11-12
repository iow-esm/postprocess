# this depends on seasonal means and a processed reference
dependencies = ["seasonal_mean", "process_reference"]

seasons = ["MAM", "SON", "JJA", "DJF"]
variables = ["SST", "FI"]

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
        
        if var == "SST":
            file_pairs[var + "-" + season][1]["additional-operators"] = "-subc,273.15"
          




