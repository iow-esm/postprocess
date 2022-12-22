
root = "/silod8/karsten"

import sys
sys.path.append('../../auxiliary')
from plot_config import PlotConfig

# "reference-file-pattern" :            a string containing the path pattern to reference files (optional), see commented examples below
# "reference-variable-name" :           a string containing the name of the variable in the refrence files, this variable will be renamed to the key of the dictionary entry 
#                                       (if "reference-file-pattern" is set this must be set as well)
# "reference-additional-operators" :    a string containing additional cdo operators applied to the reference files, e.g. commented examples below
#                                       (if "reference-file-pattern" is set this must be set as well)
# "plot-config-anomaly" :               a PlotConfig instance for plotting the difference between data and reference as given below (optional)

reference = { 
    "SST" : {
        "reference-file-pattern" : root+"/era5/Baltic/reanalysis-era5-single-levels-monthly-means_sea_surface_temperature*.nc",
        "reference-variable-name" : "sst",
        "reference-additional-operators" : "-b F32 -setattribute,sst@units=Celsius -subc,273.15",
        "reference-description" : "Reference is taken from https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-single-levels-monthly-means. Search for \"Sea surface temperature\"",
        "plot-config-anomaly" : {"min_value" : -5.0, "max_value" : 5.0, "delta_value" : 1.0, "contour" : True, "color_map" : 'seismic'},
    },
    "FI" :  {
        "reference-file-pattern" : root+"/era5/Baltic/reanalysis-era5-single-levels-monthly-means_sea_ice_cover*.nc",
        "reference-variable-name" : "siconc",
        "reference-additional-operators" : "-b F32",
        "plot-config-anomaly" : PlotConfig(min_value = -0.6, max_value = 0.6, delta_value = 0.1, contour = True, color_map = 'seismic'),
    },
    "EVAP": {
        "reference-file-pattern" : root+"/era5/Baltic/reanalysis-era5-single-levels-monthly-means_mean_evaporation_rate*.nc",
        "reference-variable-name" : "mer",
        "reference-additional-operators" : "-b F32 -mulc,-1.0",
        "plot-config-anomaly" : PlotConfig(min_value = -2.0e-5, max_value = 2.0e-5, delta_value = 0.5e-5, contour = True, color_map = 'seismic'),
    },
    "swdn" :  {
        "reference-file-pattern" : root+"/era5/Baltic/reanalysis-era5-single-levels-monthly-means_mean_surface_downward_short_wave_radiation_flux_*.nc",
        "reference-variable-name" : "msdwswrf",
        "reference-additional-operators" : "-b F32",
        "plot-config-anomaly" : PlotConfig(min_value = -30.0, max_value = 30.0, delta_value = 5.0, contour = True, color_map = 'seismic'),
    },
    "lwdn" : {
        "reference-file-pattern" : root+"/era5/Baltic/reanalysis-era5-single-levels-monthly-means_mean_surface_downward_long_wave_radiation_flux_*.nc",
        "reference-variable-name" : "msdwlwrf",
        "reference-additional-operators" : "-b F32",
        "plot-config-anomaly" : PlotConfig(min_value = -10.0, max_value = 10.0, delta_value = 2.0, contour = True, color_map = 'seismic'),
    },
    "LH" : {
        "reference-file-pattern" : root+"/era5/Baltic/reanalysis-era5-single-levels-monthly-means_mean_surface_latent_heat_flux*.nc",
        "reference-variable-name" : "mslhf",
        "reference-additional-operators" : "-b F32 -mulc,-1.0",
        "plot-config-anomaly" : PlotConfig(min_value = -30.0, max_value = 30.0, delta_value = 6.0, contour = True, color_map = 'seismic'),
    },
    "SH" : {
        "reference-file-pattern" : root+"/era5/Baltic/reanalysis-era5-single-levels-monthly-means_mean_surface_sensible_heat_flux*.nc",
        "reference-variable-name" : "msshf",
        "reference-additional-operators" : "-b F32 -mulc,-1.0",
        "plot-config-anomaly" : PlotConfig(min_value = -20.0, max_value = 20.0, delta_value = 4.0, contour = True, color_map = 'seismic'),
    },
    "tau_x" : {
        "reference-file-pattern" : root+"/era5/Baltic/reanalysis-era5-single-levels-monthly-means_mean_eastward_turbulent_surface_stress_*.nc",
        "reference-variable-name" : "metss",
        "reference-additional-operators" : "-b F32",
        "plot-config-anomaly" : PlotConfig(min_value = -0.03, max_value = 0.03, delta_value = 0.005, contour = True, color_map = 'seismic'),
    },
    "tau_y" : {
        "reference-file-pattern" : root+"/era5/Baltic/reanalysis-era5-single-levels-monthly-means_mean_northward_turbulent_surface_stress_*.nc",
        "reference-variable-name" : "mntss",
        "reference-additional-operators" : "-b F32",
        "plot-config-anomaly" : PlotConfig(min_value = -0.03, max_value = 0.03, delta_value = 0.005, contour = True, color_map = 'seismic'),
    },
    "temp" : {
        "BED-reference-file-pattern" : root+"/obs/BEDValidationData_1/Monthly/*TEMP*.dat",
    },
    "salt" : {
        "BED-reference-file-pattern" : root+"/obs/BEDValidationData_1/Monthly/*SALIN*.dat",
    }
}

