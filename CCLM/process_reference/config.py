seasons = {
    "MAM" : "3,4,5",
    "JJA" : "6,7,8",
    "SON" : "9,10,11",
    "DJF" : "12,1,2"
}

percentiles = ["95", "5", "25"]

reference = "E-OBS"

if reference == "E-OBS":       
    variables = {
    "T_2M" : {  "file-pattern" : "tg_ens_mean_0.1deg_reg_v23.1e.nc",
                "name" : "tg",
                "remapping-file" : "../create_remapping_files/results/_scratch_usr_mvkkarst_IOW_ESM_output_RUNXX_CCLM_Eurocordex-19790901_20091130/grid_T_2M.txt",
                "seasons" : seasons,
                "percentiles" : percentiles},
                
    "TOT_PREC" : {  "file-pattern" : "rr_ens_mean_0.1deg_reg_v23.1e.nc",
                    "name" : "rr",
                    "remapping-file" : "../create_remapping_files/results/_scratch_usr_mvkkarst_IOW_ESM_output_RUNXX_CCLM_Eurocordex-19790901_20091130/grid_TOT_PREC.txt",
                    "seasons" : seasons,
                    "percentiles" : percentiles}      
    }
else:
    variables = {}



