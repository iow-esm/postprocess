dependencies = ["create_remapping_files"]

seasons = {
    "MAM" : "3,4,5",
    "JJA" : "6,7,8",
    "SON" : "9,10,11",
    "DJF" : "12,1,2"
}

percentiles = []#["95", "5"]#, "25"]

     
variables = {
"T_2M_AV" : {  "file-pattern" : "/scratch/usr/mvkkarst/obs/E-OBS/tg_ens_mean_0.1deg_reg_v23.1e.nc",
            "name" : "tg",
            "remapping-file" : "grid_T_2M_AV.txt",
            "seasons" : seasons,
            "percentiles" : percentiles
         },
            
"TOT_PREC" : {  "file-pattern" : "/scratch/usr/mvkkarst/obs/E-OBS/rr_ens_mean_0.1deg_reg_v23.1e.nc",
                "name" : "rr",
                "remapping-file" : "grid_TOT_PREC.txt",
                "seasons" : seasons,
                "percentiles" : percentiles
             },    

"ASOB_S" : {  "file-pattern" : "/scratch/usr/mvkkarst/obs/E-OBS/qq_ens_mean_0.1deg_reg_v23.1e.nc",
                "name" : "qq",
                "remapping-file" : "grid_ASOB_S.txt",
                "seasons" : seasons,
                "percentiles" : percentiles
           },     
}




