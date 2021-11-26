seasons = {
    "MAM" : "3,4,5",
    "JJA" : "6,7,8",
    "SON" : "9,10,11",
    "DJF" : "12,1,2"
}

percentiles = []

stations = { 
    "ROSTOCK-WARNEMUNDE" : {"lat" : "54.18", "lon" : "12.08"},
    "STOCKHOLM" : {"lat" : "59.35", "lon" : "18.05"},
    "TALLINN" : {"lat" : "59:23:53", "lon" : "24:36:10"},
    "VISBY" : {"lat" : "57:40:00", "lon" : "18:19:59"},
    "SUNDSVALL" : {"lat" : "62:24:36", "lon" : "17:16:12"},
    "LULEA" : {"lat" : "65:37:12", "lon" : "22:07:48"},
    "VAASA-PALOSAARI" : {"lat" : "63:06:00", "lon" : "21:36:00"},
}

time_series_operators = ["-monmean", "-seasmean", "-ymonmean", "-yseasmean"]

variables = {
    "T_2M_AV" : {  "reference-file-pattern" : "/scratch/usr/mvkkarst/obs/E-OBS/tg_ens_mean_0.1deg_reg_v23.1e.nc",
                   "reference-variable-name" : "tg",
                   "reference-additional-operators" : "-chname,longitude,lon -chname,latitude,lat -setattribute,tg@units=Kelvin -addc,273.15",
                   "seasons" : seasons,
                   "percentiles" : percentiles, 
                   "stations" : stations,
                   "time-series-operators" : time_series_operators
             },

    "TOT_PREC" : {  "reference-file-pattern" : "/scratch/usr/mvkkarst/obs/E-OBS/rr_ens_mean_0.1deg_reg_v23.1e.nc",
                    "reference-variable-name" : "rr",
                    "reference-additional-operators" : "-chname,longitude,lon -chname,latitude,lat",
                    "seasons" : seasons,
                    "percentiles" : percentiles,
                    "stations" : stations,
                    "time-series-operators" : time_series_operators
                 },    

    "ASWD_S" : {  "reference-file-pattern" : "/scratch/usr/mvkkarst/obs/E-OBS/qq_ens_mean_0.1deg_reg_v23.1e.nc",
                  "reference-variable-name" : "qq",
                  "reference-additional-operators" : "-chname,longitude,lon -chname,latitude,lat",
                  "seasons" : seasons,
                  "percentiles" : percentiles,
                  "stations" : stations,
                  "time-series-operators" : time_series_operators
               },  
}
         

