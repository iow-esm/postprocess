#name = "compare_to_uncoupled"
#name = "compare_to_era5"
name = "compare_to_era5"

if name == "compare_to_eobs":
    import compare_to_eobs as ref
elif name == "compare_to_era5":
    import compare_to_era5 as ref
else:
    import compare_to_uncoupled as ref

reference = ref.reference


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
    "mean": ""
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
    "ROSTOCK-WARNEMUNDE" : {"lat" : "54.18", "lon" : "12.08"},
    "STOCKHOLM" : {"lat" : "59.35", "lon" : "18.05"},
    "TALLINN" : {"lat" : "59:23:53", "lon" : "24:36:10"},
    "VISBY" : {"lat" : "57:40:00", "lon" : "18:19:59"},
    "SUNDSVALL" : {"lat" : "62:24:36", "lon" : "17:16:12"},
    "LULEA" : {"lat" : "65:37:12", "lon" : "22:07:48"},
    "VAASA-PALOSAARI" : {"lat" : "63:06:00", "lon" : "21:36:00"},
}

# Define regions over which a spatial average will be performed.
# Note, longitudes and latitudes can be in decimal format or in degrees, minutes and seconds separated by a colon.
# Leave empty if no regions are desired.
root = "/silod8/karsten"

regions = { 
    "VALID_DOMAIN" : {"lat-min" : "35.0", "lat-max" : "70.0", "lon-min" : "-10.0", "lon-max" : "35.0"},
    "NORTHERN_LANDS" : {"maskfile" : root+"/masks/Eurocordex/NORTHERN_LANDS.nc"},
    "BALTIC_CATCHMENT" : {"maskfile" : root+"/masks/Eurocordex/BALTIC_CATCHMENT.nc"},
    "NORTHERN_WATERS" : {"maskfile" : root+"/masks/Eurocordex/NORTHERN_WATERS.nc"},
    "BALTIC_SEA" : {"maskfile" : root+"/masks/Baltic/BALTIC_SEA.nc"},
    "BOTHNIAN_GULF" : {"maskfile" : root+"/masks/Baltic/BOTHNIAN_GULF.nc"},
    "BALTIC_PROPER" : {"maskfile" : root+"/masks/Baltic/BALTIC_PROPER.nc"},
    "BELTS" : {"maskfile" : root+"/masks/Baltic/BELTS.nc"},
    "RIGA_FINLAND" : {"maskfile" : root+"/masks/Baltic/RIGA_FINLAND.nc"}, 
    "NORTH_SEA" : {"maskfile" : root+"/masks/Eurocordex/NORTH_SEA.nc"},
}

# Define cdo operators which will be applied to the time series.
time_series_operators = ["-monmean", "-yearmean", "-ymonmean"]
#time_series_operators = ["-monmean", "-seasmean", "-ymonmean", "-yseasmean"]

    
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

# "reference-file-pattern" :            a string containing the path pattern to reference files (optional), see commented examples below
# "reference-variable-name" :           a string containing the name of the variable in the refrence files, this variable will be renamed to the key of the dictionary entry 
#                                       (if "reference-file-pattern" is set this must be set as well)
# "reference-additional-operators" :    a string containing additional cdo operators applied to the reference files, e.g. commented examples below
#                                       (if "reference-file-pattern" is set this must be set as well)
# "plot-config-anomaly" :               a PlotConfig instance for plotting the difference between data and reference as given below (optional)

this_model = "coupled"
this_model_description = """
This is an example for the coupled model.
"""

other_models = {
    "uncoupled" : { 
        "root" : root+"/examples/IOW_ESM/postprocess/CCLM", 
        "output-name" : name+"_uncoupled_CCLM_CCLM_Eurocordex",
        "description" : "Uncoupled CCLM model run with the same setup as the coupled model."
    },
}

other_models = {}

import sys
sys.path.append('../../auxiliary')
from plot_config import PlotConfig

if name == "compare_to_eobs":
    regions = {"BALTIC_CATCHMENT" : regions["BALTIC_CATCHMENT"]}

variables = {
    "T_2M_AV" : {  
        "seasons" : seasons,
        "percentiles" : percentiles, 
        "stations" : stations,
        "regions" : regions,
        "time-series-operators" : time_series_operators,
        "plot-config" : PlotConfig(min_value = 273.15 - 5.0, max_value = 273.15 + 25.0, delta_value = 2.0, contour = True, color_map = 'rainbow'),
        **reference["T_2M_AV"],
        "other-models" : other_models,
        "long-name" : "averaged 2 meter air temperature",
        "description" : "This parameter is the 2 meter air temperature that is averaged over output period, e.g. for daily output it is the daily average."
    },

    "DAY_PREC" : {  
        "seasons" : seasons,
        "percentiles" : percentiles,
        "stations" : stations,
        "regions" : regions,
        "time-series-operators" : time_series_operators,
        "plot-config" : PlotConfig(min_value = 0.0, max_value = 6.0, delta_value = 1.0, contour = True, color_map = 'YlGnBu'),
        **reference["DAY_PREC"],
        "other-models" : other_models
    },    

    "ASWD_S" : {  
        "seasons" : seasons,
        "percentiles" : percentiles,
        "stations" : stations,
        "regions" : regions,
        "time-series-operators" : time_series_operators,
        "plot-config" : PlotConfig(min_value = 0.0, max_value = 300.0, delta_value = 30.0, contour = True, color_map = 'inferno'),
        **reference["ASWD_S"],
        "other-models" : other_models
    },   
    
    "ALWD_S" : {  
        "seasons" : seasons,
        "percentiles" : percentiles,
        "stations" : stations,
        "regions" : regions,
        "time-series-operators" : time_series_operators,
        "plot-config" : PlotConfig(min_value = 200.0, max_value = 500.0, delta_value = 30.0, contour = True, color_map = 'rainbow'),
        **reference["ALWD_S"],
        "other-models" : other_models
    },     
               
    "SPEED_10M_AV" : {  
        "seasons" : seasons,
        "percentiles" : percentiles,
        "stations" : stations,
        "regions" : regions,
        "time-series-operators" : time_series_operators,
        "plot-config" : PlotConfig(min_value = 0.0, max_value = 7.0, delta_value = 0.5, contour = False, color_map = 'terrain_r'),
        **reference["SPEED_10M_AV"],
        "other-models" : other_models
    }, 
               
    "PMSL_AV" : {        
        "seasons" : seasons,
        "percentiles" : percentiles,
        "stations" : stations,
        "regions" : regions,
        "time-series-operators" : time_series_operators,
        "plot-config" : PlotConfig(min_value = 100200.0, max_value = 102200.0, delta_value = 150.0, contour = True, color_map = 'RdYlBu_r'),
        **reference["PMSL_AV"],
        "other-models" : other_models
    }, 
    
    "AEVAP_S" : {  
        "seasons" : seasons,
        "percentiles" : percentiles,
        "stations" : stations,
        "regions" : regions,
        "time-series-operators" : time_series_operators,
        "plot-config" : PlotConfig(min_value = -3.0, max_value = 0.0, delta_value = 0.3, contour = True, color_map = 'BrBG_r'),
        **reference["AEVAP_S"],
        "other-models" : other_models
    }, 
    
    "ALHFL_S" : {  
        "seasons" : seasons,
        "percentiles" : percentiles,
        "stations" : stations,
        "regions" : regions,
        "time-series-operators" : time_series_operators,
        "plot-config" : PlotConfig(min_value = -150.0, max_value = 0.0, delta_value = 15.0, contour = True, color_map = 'BrBG_r'),
        **reference["ALHFL_S"],
        "other-models" : other_models
    },   
         
    "ASHFL_S" : {  
        "seasons" : seasons,
        "percentiles" : percentiles,
        "stations" : stations,
        "regions" : regions,
        "time-series-operators" : time_series_operators,
        "plot-config" : PlotConfig(min_value = -100.0, max_value = 0.0, delta_value = 10.0, contour = True, color_map = 'Spectral'),
        **reference["ASHFL_S"],
        "other-models" : other_models
    },   
    
    "CLCT" :{  
        "seasons" : seasons,
        "percentiles" : percentiles,
        "stations" : stations,
        "regions" : regions,
        "time-series-operators" : time_series_operators,
        "plot-config" : PlotConfig(min_value = 0.0, max_value = 1.0, delta_value = 0.1, contour = True, color_map = 'Blues'),
        **reference["CLCT"],
        "other-models" : other_models
    },      
    
    "AUMFL_S" : {  
        "seasons" : seasons,
        "percentiles" : percentiles,
        "stations" : stations,
        "regions" : regions,
        "time-series-operators" : time_series_operators,
        "plot-config" : PlotConfig(min_value = 0.0, max_value = 0.03, delta_value = 0.003, contour = True, color_map = 'Spectral'),
        **reference["AUMFL_S"],
        "other-models" : other_models
    },    
    
    "AVMFL_S" : {  
        "seasons" : seasons,
        "percentiles" : percentiles,
        "stations" : stations,
        "regions" : regions,
        "time-series-operators" : time_series_operators,
        "plot-config" : PlotConfig(min_value = -0.02, max_value = 0.02, delta_value = 0.004, contour = True, color_map = 'Spectral'),
        **reference["AVMFL_S"],
        "other-models" : other_models
    },    
    
    "RELHUM_2M" : {  
        "seasons" : seasons,
        "percentiles" : percentiles,
        "stations" : stations,
        "regions" : regions,
        "time-series-operators" : time_series_operators,
        "plot-config" : PlotConfig(min_value = 0.0, max_value = 100.0, delta_value = 10.0, contour = True, color_map = 'gist_earth_r'),
        **reference["RELHUM_2M"],
        "other-models" : other_models
    },     

    "T" : {  
        "seasons" : seasons,
        "percentiles" : percentiles,
        "stations" : stations,
        "regions" : regions,
        "dimension" : 4,
        "time-series-operators" : time_series_operators,
        "plot-config" : PlotConfig(min_value = 273.15 - 100.0, max_value = 273.15 + 25.0),
        **reference["T"],
        "other-models" : other_models
    }
}