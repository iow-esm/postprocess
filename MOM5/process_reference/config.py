seasons = {
    "MAM" : "3,4,5",
    "JJA" : "6,7,8",
    "SON" : "9,10,11",
    "DJF" : "12,1,2"
}

percentiles = ["95", "5"]#, "25"]

reference = "Copernicus"

#sellonlatbox = "8,32,52,68"
    
if reference == "Copernicus":  
    variables = {
    "sst" : { "pattern" : "*-Baltic-ESACCI-L4_GHRSST-SSTdepth-OSTIA-GLOB_CDR2.0-v02.0-fv01.0.nc",
              "name" : "analysed_sst" }
    }
else:
    variables = {}



