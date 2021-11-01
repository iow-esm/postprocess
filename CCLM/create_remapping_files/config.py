seasons = {
    "MAM" : "3,4,5",
    "JJA" : "6,7,8",
    "SON" : "9,10,11",
    "DJF" : "12,1,2"
}

percentiles = ["95", "5", "25"]

reference = "E-OBS"

if reference == "E-OBS":  
    variables = {"T_2M" : "tg_ens_mean_0.1deg_reg_v23.1e",
                 #"RAIN_TOT" : "rr_ens_mean_0.1deg_reg_v23.1e",
                 "TOT_PREC" : "rr_ens_mean_0.1deg_reg_v23.1e"}
                 
    variables = {
    "T_2M" : {  "file-pattern" : "tg_ens_mean_0.1deg_reg_v23.1e.nc",
                "name" : "tg",
                "remap_file" : "../create_remapping_files/results/T_2M-remapping.txt"},
    "TOT_PREC" : {  "file-pattern" : "rr_ens_mean_0.1deg_reg_v23.1e.nc",
                    "name" : "rr" }      
    }
else:
    variables = {}



