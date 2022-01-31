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
    "year": "1,2,3,4,5,6,7,8,9,10,11,12"
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
regions = { 
    "BALTIC_SEA" : {"lat-min" : "52.0", "lat-max" : "67.0", "lon-min" : "8.0", "lon-max" : "32.0"},
}

# Define cdo operators which will be applied to the time series.
time_series_operators = ["-monmean", "-seasmean", "-ymonmean", "-yseasmean"]


##########################################################################
# STEP 3: Auxiliary steps (optional)                                     #
##########################################################################

# To customize the plotting you can import the PlotConfig class, see below for usage examples.
# If you leave that out, the plots will have gneric color maps and values ranges.
import sys
sys.path.append('../auxiliary')
from plot_config import PlotConfig

# You can also pass transformation functions to the PlotConfig. The arguments must be variable in units.
def convert_K2C(variable, units):

    variable -= 273.15
    units = "Celsius"
    
    return variable, units
    
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

variables = {
    "T_2M_AV" : {  "seasons" : seasons,
                   "percentiles" : percentiles, 
                   "stations" : stations,
                   "regions" : regions,
                   "time-series-operators" : time_series_operators,
                   "plot-config" : PlotConfig("T_2M_AV", width=7000000, height=5000000, min_value = -5.0, max_value = 25.0, delta_value = 2.0, contour = True, color_map = 'YlOrRd', transform_variable = convert_K2C),
                   #"reference-file-pattern" : "/scratch/usr/mvkkarst/obs/E-OBS/tg_ens_mean_0.1deg_reg_v23.1e.nc",
                   #"reference-variable-name" : "tg",
                   #"reference-additional-operators" : "-chname,longitude,lon -chname,latitude,lat -setattribute,tg@units=Kelvin -addc,273.15",
             },

    "DAY_PREC" : {  "seasons" : seasons,
                    "percentiles" : percentiles,
                    "stations" : stations,
                    "regions" : regions,
                    "time-series-operators" : time_series_operators,
                    "plot-config" : PlotConfig("DAY_PREC", width=7000000, height=5000000, min_value = 0.0, max_value = 6.0, delta_value = 1.0, contour = True, color_map = 'YlGnBu')
                 },    

    "ASWD_S" : {  "seasons" : seasons,
                  "percentiles" : percentiles,
                  "stations" : stations,
                  "regions" : regions,
                  "time-series-operators" : time_series_operators,
                  "plot-config" : PlotConfig("ASWD_S", width=7000000, height=5000000, min_value = 0.0, max_value = 300.0, delta_value = 30.0, contour = True, color_map = 'inferno')
                  
               },  
               
    "SPEED_10M_AV" : {  "seasons" : seasons,
                  "percentiles" : percentiles,
                  "stations" : stations,
                  "regions" : regions,
                  "time-series-operators" : time_series_operators,
                  "plot-config" : PlotConfig("SPEED_10M_AV", width=7000000, height=5000000, min_value = 0.0, max_value = 7.0, delta_value = 0.5, contour = False, color_map = 'terrain_r')
               }, 
               
    "PMSL_AV" : {  
                  "seasons" : seasons,
                  "percentiles" : percentiles,
                  "stations" : stations,
                  "regions" : regions,
                  "time-series-operators" : time_series_operators,
                  "plot-config" : PlotConfig("PMSL_AV", width=7000000, height=5000000, min_value = 100200.0, max_value = 102200.0, delta_value = 150.0, contour = True, color_map = 'rainbow')
                  #"reference-file-pattern" : "/scratch/usr/mvkkarst/obs/E-OBS/pp_ens_mean_0.1deg_reg_v23.1e.nc",
                  #"reference-variable-name" : "pp",
                  #"reference-additional-operators" : "-b f32 -chname,longitude,lon -chname,latitude,lat -setattribute,pp@units=Pa -mulc,100.0",
               }, 
}
         

