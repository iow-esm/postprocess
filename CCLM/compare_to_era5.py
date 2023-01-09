# To customize the plotting you can import the PlotConfig class, see below for usage examples.
# If you leave that out, the plots will have gneric color maps and values ranges.
import sys
sys.path.append('../../auxiliary')
from plot_config import PlotConfig

root = "/silod8/karsten"

reference = {
    "T_2M_AV" : {  
        "reference-file-pattern" : root+"/era5/Eurocordex/reanalysis-era5-single-levels-monthly-means_2m_temperature_*.nc",
        "reference-additional-operators" : "-b F32",
        "reference-variable-name" : "t2m",
        "plot-config-anomaly" : PlotConfig("T_2M_AV", min_value = -3.0, max_value = 3.0, delta_value = 0.5, color_map = 'seismic'),
    },

    "DAY_PREC" : {  "reference-file-pattern" : root+"/era5/Eurocordex/reanalysis-era5-single-levels-monthly-means_total_precipitation_*.nc",
                  "reference-additional-operators" : "-b F32 -mulc,1000.0 -setattribute,tp@units=\"kg/m^2\"",
                    "reference-variable-name" : "tp",
                    "plot-config-anomaly" : PlotConfig("DAY_PREC", min_value = -1.0, max_value = 1.0, delta_value = 0.2, color_map = 'BrBG')
                 },    

    "ASWD_S" : {  "reference-file-pattern" : root+"/era5/Eurocordex/reanalysis-era5-single-levels-monthly-means_mean_surface_downward_short_wave_radiation_flux_*.nc",
                "reference-additional-operators" : "-b F32",
                  "reference-variable-name" : "msdwswrf",
                  "plot-config-anomaly" : PlotConfig("ASWD_S", min_value = -40.0, max_value = 40.0, delta_value = 10.0, contour = True, color_map = 'seismic')
               },  
    
    "ALWD_S" : {  "reference-file-pattern" : root+"/era5/Eurocordex/reanalysis-era5-single-levels-monthly-means_mean_surface_downward_long_wave_radiation_flux_*.nc",
                "reference-additional-operators" : "-b F32",
                  "reference-variable-name" : "msdwlwrf",
                  "plot-config-anomaly" : PlotConfig("ALWD_S", min_value = -40.0, max_value = 40.0, delta_value = 10.0, contour = True, color_map = 'seismic')
               },     
               
    "SPEED_10M_AV" : {  "reference-file-pattern" : root+"/era5/Eurocordex/reanalysis-era5-single-levels-monthly-means_10m_wind_speed_*.nc",
                      "reference-additional-operators" : "-b F32",
                  "reference-variable-name" : "si10",
                  "plot-config-anomaly" : PlotConfig("SPEED_10M_AV", min_value = -2.0, max_value = 2.0, delta_value = 0.5, color_map = 'seismic')
               }, 
               
    "PMSL_AV" : {  "reference-file-pattern" : root+"/era5/Eurocordex/reanalysis-era5-single-levels-monthly-means_mean_sea_level_pressure_*.nc",
                 "reference-additional-operators" : "-b F32",
                  "reference-variable-name" : "msl",
                  "plot-config-anomaly" : PlotConfig("PMSL_AV", min_value = -300.0, max_value = 300.0, delta_value = 50.0, contour = True, color_map = 'seismic')
               }, 
    
    "AEVAP_S" : {  "reference-file-pattern" : root+"/era5/Eurocordex/reanalysis-era5-single-levels-monthly-means_mean_evaporation_rate_*.nc",
                  "reference-additional-operators" : "-b F32 -mulc,86400.0 -setattribute,mer@units=\"kg/m^2\"",
                  "reference-variable-name" : "mer",
                  "plot-config-anomaly" : PlotConfig("AEVAP_S", min_value = -1.0, max_value = 1.0, delta_value = 0.2, color_map = 'seismic')
               },    
    
    "ALHFL_S" : {
                    "reference-file-pattern" : root+"/era5/Eurocordex/reanalysis-era5-single-levels-monthly-means_mean_surface_latent_heat_flux*.nc",
                    "reference-variable-name" : "mslhf",
                    "reference-additional-operators" : "-b F32",
                    "plot-config-anomaly" : PlotConfig("ALHFL_S", min_value = -20.0, max_value = 20.0, delta_value = 2.0, color_map = 'seismic'),
            },

    "ASHFL_S" : {
                    "reference-file-pattern" : root+"/era5/Eurocordex/reanalysis-era5-single-levels-monthly-means_mean_surface_sensible_heat_flux*.nc",
                    "reference-variable-name" : "msshf",
                    "reference-additional-operators" : "-b F32",
                    "plot-config-anomaly" : PlotConfig("ASHFL_S", min_value = -20.0, max_value = 20.0, delta_value = 2.0, color_map = 'seismic'),
            },
    "CLCT" : {
                    "reference-file-pattern" : root+"/era5/Eurocordex/reanalysis-era5-single-levels-monthly-means_total_cloud_cover*.nc",
                    "reference-variable-name" : "tcc",
                    "reference-additional-operators" : "-b F32",
                    "plot-config-anomaly" : PlotConfig("CLCT", min_value = -0.3, max_value = 0.3, delta_value = 0.05, contour = True, color_map = 'seismic'),
            },
    
    "AUMFL_S" : {
                    "reference-file-pattern" : root+"/era5/Eurocordex/reanalysis-era5-single-levels-monthly-means_mean_eastward_turbulent_surface_stress_*.nc",
                    "reference-variable-name" : "metss",
                    "reference-additional-operators" : "-b F32",
                    "plot-config-anomaly" : PlotConfig("AUMFL_S",  min_value = -0.03, max_value = 0.03, delta_value = 0.005, contour = True, color_map = 'seismic'),
            },  
    
    "AVMFL_S" : {
                    "reference-file-pattern" : root+"/era5/Eurocordex/reanalysis-era5-single-levels-monthly-means_mean_northward_turbulent_surface_stress_*.nc",
                    "reference-variable-name" : "mntss",
                    "reference-additional-operators" : "-b F32",
                    "plot-config-anomaly" : PlotConfig("AVMFL_S",  min_value = -0.03, max_value = 0.03, delta_value = 0.005, contour = True, color_map = 'seismic'),
            },    
    
    "T" : {},
    
    "RELHUM_2M" : {}
}
         

