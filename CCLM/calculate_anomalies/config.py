data_dir = "../seasonal_mean/results/_scratch_usr_mvkkarst_IOW_ESM_output_RUNXX_CCLM_Eurocordex-19790901_20091130"
reference_dir = "../process_reference/results/_scratch_usr_mvkkarst_obs_E-OBS-19790901_20091130"

seasons = ["MAM", "SON", "JJA", "DJF"]
variables = ["T_2M", "TOT_PREC"]

file_pairs = {}

for season in seasons:
    for var in variables:
        file_pairs.update({ var + "-" + season : 
            [ 
                { "path" : data_dir + "/" + var + "-" + season + ".nc"} ,
                { "path" : reference_dir + "/" + var + "-" + season + "-remapped.nc" }
            ] 
        })
        
        if var == "T_2M":
            file_pairs[var + "-" + season][0]["additional-operators"] = "-subc,273.15"
          




