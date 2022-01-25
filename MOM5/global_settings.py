seasons = {
    "MAM" : "3,4,5",
    "JJA" : "6,7,8",
    "SON" : "9,10,11",
    "DJF" : "12,1,2",
    "year": "1,2,3,4,5,6,7,8,9,10,11,12"
}

percentiles = []

stations = { 
        "BY5" : {"lat" : "55.25", "lon" : "15.98"},
        "F9" : {"lat" : "64.71", "lon" : "22.07"},
        "SR5" : {"lat" : "61.08", "lon" : "19.58"},
        "BY31" : {"lat" : "58.58", "lon" : "18.23"}        
}

regions = {}

time_series_operators = ["-monmean", "-seasmean", "-ymonmean", "-yseasmean"]

variables = {
    "SST" : {  "reference-file-pattern" : "/scratch/usr/mvkkarst/obs/Copernicus/*-Baltic-ESACCI-L4_GHRSST-SSTdepth-OSTIA-GLOB_CDR2.0-v02.0-fv01.0.nc",
                   "reference-variable-name" : "analysed_sst",
                   "reference-additional-operators" : "-chname,lon,xt -chname,lat,yt -setattribute,analysed_sst@units=Celsius -subc,273.15",
                   "seasons" : seasons,
                   "percentiles" : percentiles, 
                   "stations" : stations,
                   "regions" : regions,
                   "time-series-operators" : time_series_operators
             },

    "FI" : {  "reference-file-pattern" : "/scratch/usr/mvkkarst/obs/Copernicus/*-Baltic-ESACCI-L4_GHRSST-SSTdepth-OSTIA-GLOB_CDR2.0-v02.0-fv01.0.nc",
                    "reference-variable-name" : "sea_ice_fraction",
                    "reference-additional-operators" : "-chname,lon,xt -chname,lat,yt",
                    "seasons" : seasons,
                    "percentiles" : percentiles,
                    "stations" : stations,
                    "regions" : regions,
                    "time-series-operators" : time_series_operators
                 },  
    "SSH" : {      "seasons" : seasons,
                   "percentiles" : percentiles,
                   "stations" : stations,
                   "regions" : regions, 
                   "time-series-operators" : time_series_operators
             },

    "SSS" : {       "seasons" : seasons,
                    "percentiles" : percentiles,
                    "stations" : stations,
                    "regions" : regions,                  
                    "time-series-operators" : time_series_operators
                 },

}
         

