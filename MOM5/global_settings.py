##########################################################################
# STEP 1: Configure what will be plotted on a map (2D time averages)     #
##########################################################################

# Define seasons for which time averages will be calculated.
# Note, the values in the dictionary must be valid input for the cdo operator "-selmon".
seasons = {
 #   "MAM" : "3,4,5",
 #   "JJA" : "6,7,8",
 #   "SON" : "9,10,11",
 #   "DJF" : "12,1,2",
    "mean": "" # mean over full time interval
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
        "BY5" : {"lat" : "55.25", "lon" : "15.98"},
        "F9" : {"lat" : "64.71", "lon" : "22.07"},
        "SR5" : {"lat" : "61.08", "lon" : "19.58"},
        "BY31" : {"lat" : "58.58", "lon" : "18.23"}        
}

# Define regions over which a spatial average will be performed.
# Note, longitudes and latitudes can be in decimal format or in degrees, minutes and seconds separated by a colon.
# Leave empty if no regions are desired.
regions = { 
    "BALTIC_SEA" : {"lat-min" : "52.0", "lat-max" : "67.0", "lon-min" : "8.0", "lon-max" : "32.0"},
    "BOTHNIAN_GULF" : {"lat-min" : "60.6", "lat-max" : "66.0", "lon-min" : "16.0", "lon-max" : "26.0"},
    "BALTIC_PROPER" : {"lat-min" : "53.0", "lat-max" : "60.6", "lon-min" : "14.0", "lon-max" : "23.0"},
    "BELTS" : {"lat-min" : "53.0", "lat-max" : "60.6", "lon-min" : "8.0", "lon-max" : "14.0"},
    "RIGA_FINLAND" : {"lat-min" : "56.5", "lat-max" : "60.6", "lon-min" : "23.0", "lon-max" : "31.5"},
	}

# Define cdo operators which will be applied to the time series.
time_series_operators = [""]
#time_series_operators = ["-monmean", "-seasmean", "-ymonmean", "-yseasmean"]


##########################################################################
# STEP 3: Auxiliary steps (optional)                                     #
##########################################################################

# To customize the plotting you can import the PlotConfig class, see below for usage examples.
# If you leave that out, the plots will have gneric color maps and values ranges.
import sys
sys.path.append('../auxiliary')
from plot_config import PlotConfig

    
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

variables = {
    "SST" : {      "seasons" : seasons,
                   "percentiles" : percentiles, 
                   "stations" : stations,
                   "regions" : regions,
                   "time-series-operators" : time_series_operators,
                   "plot-config" : PlotConfig("SST", lon_name = "xt", lat_name = "yt", width = 1500000, height = 1800000, min_value = 0.0, max_value = 15.0, delta_value = 1.0, contour = True, color_map = 'YlOrRd'),
                   #"reference-file-pattern" : "/scratch/usr/mvkkarst/obs/Copernicus/*-Baltic-ESACCI-L4_GHRSST-SSTdepth-OSTIA-GLOB_CDR2.0-v02.0-fv01.0.nc",
                   #"reference-variable-name" : "analysed_sst",
                   #"reference-additional-operators" : "-chname,lon,xt -chname,lat,yt -setattribute,analysed_sst@units=Celsius -subc,273.15",
                   #"plot-config-anomaly" : PlotConfig("SST", lon_name = "xt", lat_name = "yt", width = 1500000, height = 1800000, min_value = -6.5, max_value = 6.5, delta_value = 1.0, contour = True, color_map = 'seismic'),
             },
    "FI" : {        "seasons" : seasons,
                    "percentiles" : percentiles,
                    "stations" : stations,
                    "regions" : regions,
                    "time-series-operators" : time_series_operators,
                    "plot-config" : PlotConfig("FI", lon_name = "xt", lat_name = "yt", width = 1500000, height = 1800000, min_value = 0.0, max_value = 1.0, delta_value = 0.1, contour = True, color_map = 'Blues_r'),
                 },  
    "SSH" : {      "seasons" : seasons,
                   "percentiles" : percentiles,
                   "stations" : stations,
                   "regions" : regions, 
                   "time-series-operators" : time_series_operators,
                   "plot-config" : PlotConfig("SSH", lon_name = "xt", lat_name = "yt", width = 1500000, height = 1800000, min_value = -0.6, max_value = 0.6, delta_value = 0.05, contour = True, color_map = 'PiYG'),
             },
    "SSS" : {       "seasons" : seasons,
                    "percentiles" : percentiles,
                    "stations" : stations,
                    "regions" : regions,                  
                    "time-series-operators" : time_series_operators,
                    "plot-config" : PlotConfig("SSS", lon_name = "xt", lat_name = "yt", width = 1500000, height = 1800000, min_value = 0.0, max_value = 10.0, delta_value = 1.25, contour = True, color_map = 'RdPu'),
                 },

}
         

