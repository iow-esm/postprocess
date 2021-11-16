dependencies = ["seasonal_mean", "process_reference"]

seasons = ["MAM", "SON", "JJA", "DJF"]
variables = ["T_2M_AV", "TOT_PREC", "ASOB_S"]

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
        
        if var == "T_2M_AV":
            file_pairs[var + "-" + season][0]["additional-operators"] = "-subc,273.15"
          




