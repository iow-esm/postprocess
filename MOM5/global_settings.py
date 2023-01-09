name = "compare_to_era5"
#name = "compare_to_copernicus"

if name == "compare_to_era5":
    import compare_to_era5 as ref
else:
    import compare_to_copernicus as ref
    
reference = ref.reference

report_description = """
This is an example for the post-processing configuration.
"""

##########################################################################
# STEP 1: Configure what will be plotted on a map (2D time averages)     #
##########################################################################

# Define seasons for which time averages will be calculated.
# Note, the values in the dictionary must be valid input for the cdo operator "-selmon".
seasons = {
    "MAM" : "3,4,5",
    "JJA" : "6,7,8",
    "SON" : "9,10,11",
    "DJF" : "12,1,2",
    "year": "" # mean over full time interval
}

# Percentiles are not supproted currently, leave empty!
percentiles = []

##########################################################################
# STEP 2: Configure time series (1D spatial averages)                    #
##########################################################################

# Define locations of stations for which you want to have time series.
# Note, longitudes and latitudes can be in decimal format or in degrees, minutes and seconds separated by a colon.
# Leave empty if no stations are desired.
stations = { 
    "BY5" : {"lat" : "55.25", "lon" : "15.98", "alternative-names" : ["BornholmdeepBY5"]},
    "F9" : {"lat" : "64.71", "lon" : "22.07", "alternative-names" : ["BothnianBayF9"]},
    "SR5" : {"lat" : "61.08", "lon" : "19.58", "alternative-names" : ["BothnianSeaSR5"]},
    "BY31" : {"lat" : "58.58", "lon" : "18.23", "alternative-names" : ["LandsortDeepBY31"]},
    "BY15" : {"lat" : "57.3333", "lon" : "20.05", "alternative-names" : ["GotlanddeepBY15"]},
    "LL7" : {"lat" : "59.8465", "lon" : "24.8378", "alternative-names" : ["GulfFinlandLL7"]},
}

# Define regions over which a spatial average will be performed.
# Note, longitudes and latitudes can be in decimal format or in degrees, minutes and seconds separated by a colon.
# Leave empty if no regions are desired.
root = "/silod8/karsten"

regions = { 
    "BALTIC_SEA" : {"maskfile" : root+"/masks/Baltic/BALTIC_SEA.nc"},
    "BOTHNIAN_GULF" : {"maskfile" : root+"/masks/Baltic/BOTHNIAN_GULF.nc"},
    "BALTIC_PROPER" : {"maskfile" : root+"/masks/Baltic/BALTIC_PROPER.nc"},
    "BELTS" : {"maskfile" : root+"/masks/Baltic/BELTS.nc"},
    "RIGA_FINLAND" : {"maskfile" : root+"/masks/Baltic/RIGA_FINLAND.nc"},
    "test" : {"lat-min" : "55.0", "lat-max" : "56.0", "lon-min" : "19.0", "lon-max" : "20.0"}, 
}

# Define cdo operators which will be applied to the time series.
time_series_operators = ["-monmean", "-yearmean", "-ymonmean"]
#time_series_operators = ["-monmean", "-seasmean", "-ymonmean", "-yseasmean"]

other_models = {
    "uncoupled" : { 
        "root" : root+"/examples/IOW_ESM/postprocess/MOM5", 
        "output-name" : name+"_uncoupled_MOM5_MOM5_Baltic",
        #"output-dir" : root+"/examples/IOW_ESM/output/uncoupled_MOM5/MOM5_Baltic"
    },
}

#other_models = {}

##########################################################################
# STEP 4: Define the variables for which the postprocessing is performed #
##########################################################################

# The keys of the dictionary must be the names of the variables, as they are given in the NetCDF data files.
# Pass as values:
# "seasons" :                           a dictionary as given above
# "percentiles" :                       a list as given above
# "stations" :                          a dictionary as given above
# "regions" :                           a dictionary as given above
# "time-series-operators" :             a list as given above
# "plot-config" :                       a PlotConfig instance as given below (optional)

import sys
sys.path.append('../../auxiliary')
from plot_config import PlotConfig

variables = {
    "SST" : {      
        "seasons" : seasons,
        "percentiles" : percentiles, 
        "stations" : stations,
        "regions" : regions,
        "time-series-operators" : time_series_operators,
        "plot-config" : {"min_value" : 0.0, "max_value" : 15.0, "delta_value" : 1.0, "contour" : True, "color_map" : 'rainbow'},
        **reference["SST"],
        "other-models" : other_models,
        "long-name" : "sea surface temperature",
        "description" : "This parameter is the temperature of sea water near the surface measured in degrees Celsius. The corresponding model output variable is called SST."
    },
    "FI" : {        
        "seasons" : seasons,
        "percentiles" : percentiles,
        "stations" : stations,
        "regions" : regions,
        "time-series-operators" : time_series_operators,
        #"plot-config" : PlotConfig(min_value = 0.0, max_value = 1.0, delta_value = 0.1, contour = True, color_map = 'Blues_r'),
        "plot-config" : {"min_value" : 0.0, "max_value" : 1.0, "delta_value" : 0.1, "contour" : True, "color_map" : 'Blues_r'},
        **reference["FI"],
        "other-models" : other_models,
        "long-name" : "fraction of ice",
        "description" : "This parameter is the ice coverage of the grid cells, where 0 for no ice and 1 means that the cell completely covered. The corresponding model output has been calculated from a sum of sea ice concentrations (model variable `CN`) from all ice layers categorized by thickness."        
    },     
    "salt" : {     
        "seasons" : seasons,
        "percentiles" : percentiles,
        "stations" : stations,
        "regions" : regions,
        "time-series-operators" : time_series_operators,
        "dimension" : 4,
        "plot-config" : PlotConfig(min_value = 0, max_value = 24.0),
        **reference["salt"],
        "other-models" : other_models,
        "long-name" : "salinity",
        "description" : "This parameter is the four-dimensional ($x,y,z,t$) practical salinity field."
    },
    "temp" : {      
        "seasons" : seasons,
        "percentiles" : percentiles,
        "stations" : stations,
        "regions" : regions,
        "time-series-operators" : time_series_operators,
        "dimension" : 4,
        "plot-config" : {"min_value" : 0, "max_value" : 20.0},
        **reference["temp"],
        "other-models" : other_models,
        "long-name" : "Temperature",
        "description" : "This parameter is the four-dimensional ($x,y,z,t$) conservative temperature field."
    },
    "EVAP" : {        
        "seasons" : seasons,
        "percentiles" : percentiles,
        "stations" : stations,
        "regions" : regions,
        "time-series-operators" : time_series_operators,
        "plot-config" : PlotConfig(min_value = 0.0, max_value = 5.0e-5, delta_value = 0.5e-5, contour = True, color_map = 'BrBG_r'),
        **reference["EVAP"],
        "other-models" : other_models,
        "long-name" : "Evaporation",
        "description" : "This parameter is the evaporation from the ocean at the surface to the atmosphere, i.e. it is measured in positive upward direction."
    },  
    "tau_x" : {        
        "seasons" : seasons,
        "percentiles" : percentiles,
        "stations" : stations,
        "regions" : regions,
        "time-series-operators" : time_series_operators,
        "plot-config" : PlotConfig(min_value = 0.0, max_value = 0.03, delta_value = 0.003, contour = True, color_map = 'Spectral'),
        **reference["tau_x"],
        "other-models" : other_models
    },     
    "tau_y" : {
        "seasons" : seasons,
        "percentiles" : percentiles,
        "stations" : stations,
        "regions" : regions,
        "time-series-operators" : time_series_operators,
        "plot-config" : PlotConfig(min_value = -0.02, max_value = 0.02, delta_value = 0.004, contour = True, color_map = 'Spectral'),
        **reference["tau_y"],
        "other-models" : other_models
    },          
    "swdn" : {
        "seasons" : {"year" : "", "Jan" : "1", "Feb" : "2", "Mar" : "3", "Apr" : "4", "May" : "5", "Jun" : "6", "Jul" : "7", "Aug" : "8", "Sep" : "9", "Oct" : "10", "Nov" : "11", "Dec" : "12" },
        "percentiles" : percentiles,
        "stations" : stations,
        "regions" : regions,
        "time-series-operators" : time_series_operators,
        "plot-config" : PlotConfig(min_value = 0.0, max_value = 250.0, delta_value = 20.0, contour = True, color_map = 'magma'),
        **reference["swdn"],
        "other-models" : other_models
    },
    "lwdn" : {
        "seasons" : seasons,
        "percentiles" : percentiles,
        "stations" : stations,
        "regions" : regions,
        "time-series-operators" : time_series_operators,
        "plot-config" : PlotConfig(min_value = 200.0, max_value = 350.0, delta_value = 10.0, contour = True, color_map = 'magma'),
        **reference["lwdn"],
        "other-models" : other_models
         },    
    "LH" : {        
        "seasons" : seasons,
        "percentiles" : percentiles,
        "stations" : stations,
        "regions" : regions,
        "time-series-operators" : time_series_operators,
        "plot-config" : PlotConfig(min_value = 0.0, max_value = 150.0, delta_value = 15.0, contour = True, color_map = 'BrBG_r'),
        **reference["LH"],
        "other-models" : other_models
    }, 
    "SH" : {
        "seasons" : seasons,
        "percentiles" : percentiles,
        "stations" : stations,
        "regions" : regions,
        "time-series-operators" : time_series_operators,
        "plot-config" : PlotConfig(min_value = 0.0, max_value = 50.0, delta_value = 5.0, contour = True, color_map = 'Spectral'),
        **reference["SH"],
        "other-models" : other_models
    }  
}