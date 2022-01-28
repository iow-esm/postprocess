seasons = {
    "MAM" : "3,4,5",
    "JJA" : "6,7,8",
    "SON" : "9,10,11",
    "DJF" : "12,1,2",
    "year": "1,2,3,4,5,6,7,8,9,10,11,12"
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

regions = { 
    "BALTIC_SEA" : {"lat-min" : "52.0", "lat-max" : "67.0", "lon-min" : "8.0", "lon-max" : "32.0"},
}

time_series_operators = ["-monmean", "-seasmean", "-ymonmean", "-yseasmean"]

variables = {
    "T_2M_AV" : {  "seasons" : seasons,
                   "percentiles" : percentiles, 
                   "stations" : stations,
                   "regions" : regions,
                   "time-series-operators" : time_series_operators
             },

    "DAY_PREC" : {  "seasons" : seasons,
                    "percentiles" : percentiles,
                    "stations" : stations,
                    "regions" : regions,
                    "time-series-operators" : time_series_operators
                 },    

    "ASWD_S" : {  "seasons" : seasons,
                  "percentiles" : percentiles,
                  "stations" : stations,
                  "regions" : regions,
                  "time-series-operators" : time_series_operators
               },  
               
    "SPEED_10M_AV" : {  "seasons" : seasons,
                  "percentiles" : percentiles,
                  "stations" : stations,
                  "regions" : regions,
                  "time-series-operators" : time_series_operators
               }, 
               
    "PMSL_AV" : {  
                  "seasons" : seasons,
                  "percentiles" : percentiles,
                  "stations" : stations,
                  "regions" : regions,
                  "time-series-operators" : time_series_operators,
                  #"reference-file-pattern" : "/scratch/usr/mvkkarst/obs/E-OBS/pp_ens_mean_0.1deg_reg_v23.1e.nc",
                  #"reference-variable-name" : "pp",
                  #"reference-additional-operators" : "-b f32 -chname,longitude,lon -chname,latitude,lat -setattribute,pp@units=Pa -mulc,100.0",
               }, 
}
         

