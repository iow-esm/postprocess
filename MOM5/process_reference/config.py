# this depends on a processed raw output
dependencies = ["create_remapping_files"]

# a dictionary with season names (left, will appear in file names) and the corresponding numbers of months (separated by commas, no spaces, ready to be used by cdo)
seasons = {
    "MAM" : "3,4,5",
    "JJA" : "6,7,8",
    "SON" : "9,10,11",
    "DJF" : "12,1,2"
}

# a list of percentiles (strings ready to be used by cdo)
percentiles = ["95", "5"]#, "25"]

reference = "Copernicus"

#sellonlatbox = "8,32,52,68"
    
if reference == "Copernicus":  
    variables = {
    # sea surface temperature
    "SST" : { "file-pattern" : "*-Baltic-ESACCI-L4_GHRSST-SSTdepth-OSTIA-GLOB_CDR2.0-v02.0-fv01.0.nc",
              "name" : "analysed_sst",
              "remapping-file" : "../create_remapping_files/results/_scratch_usr_mvkkarst_IOW_ESM_output_RUNXX_MOM5_Baltic-19810901_20091130/grid_SST.txt",
              "seasons" : seasons,
              "percentiles" : percentiles
            },
    # fraction of ice
    "FI" : { "file-pattern" : "*-Baltic-ESACCI-L4_GHRSST-SSTdepth-OSTIA-GLOB_CDR2.0-v02.0-fv01.0.nc",
             "name" : "sea_ice_fraction",
             "remapping-file" : "../create_remapping_files/results/_scratch_usr_mvkkarst_IOW_ESM_output_RUNXX_MOM5_Baltic-19810901_20091130/grid_FI.txt",
             "seasons" : seasons,
             "percentiles" : percentiles
           }              
    }
else:
    variables = {}



