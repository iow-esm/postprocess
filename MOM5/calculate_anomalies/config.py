# this depends on seasonal means and a processed reference
dependencies = ["seasonal_mean", "process_reference"]

data_dir = "../seasonal_mean/results/_scratch_usr_mvkkarst_IOW_ESM_output_RUNXX_MOM5_Baltic-19810901_20091130"
reference_dir = "../process_reference/results/_scratch_usr_mvkkarst_obs_Copernicus-19810901_20091130"

seasons = ["MAM", "SON", "JJA", "DJF"]
variables = ["SST", "FI"]

file_pairs = {}

for season in seasons:
    for var in variables:
        file_pairs.update({ var + "-" + season : 
            [ 
                { "path" : data_dir + "/" + var + "-" + season + ".nc"} ,
                { "path" : reference_dir + "/" + var + "-" + season + "-remapped.nc" }
            ] 
        })
        
        if var == "SST":
            file_pairs[var + "-" + season][1]["additional-operators"] = "-subc,273.15"
          




