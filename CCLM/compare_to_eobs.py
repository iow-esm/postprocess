# To customize the plotting you can import the PlotConfig class, see below for usage examples.
# If you leave that out, the plots will have gneric color maps and values ranges.
import sys
sys.path.append('../../auxiliary')
from plot_config import PlotConfig


root = "/silod8/karsten"

reference = {
    "T_2M_AV" : {  "reference-file-pattern" : root+"/obs/E-OBS/monthly/tg_ens_mean_0.1deg_reg_v23.1e.nc",
                   "reference-variable-name" : "tg",
                   "reference-additional-operators" : "-setattribute,tg@units=Kelvin -addc,273.15",
                   "plot-config-anomaly" : PlotConfig(min_value = -5.0, max_value = 5.0, delta_value = 0.5, color_map = 'seismic'),
                   "reference-description" : "E-OBS data taken from https://knmi-ecad-assets-prd.s3.amazonaws.com/ensembles/data/Grid_0.1deg_reg_ensemble/tg_ens_mean_0.1deg_reg_v23.1e.nc"
             },

    "DAY_PREC" : {  "reference-file-pattern" : root+"/obs/E-OBS/monthly/rr_ens_mean_0.1deg_reg_v23.1e.nc",
                    "reference-variable-name" : "rr",
                    "plot-config-anomaly" : PlotConfig(min_value = -4.5, max_value = 4.5, delta_value = 1.0, color_map = 'BrBG')
                 },    

    "ASWD_S" : {  "reference-file-pattern" : root+"/obs/E-OBS/monthly/qq_ens_mean_0.1deg_reg_v23.1e.nc",
                  "reference-variable-name" : "qq",
                  "plot-config-anomaly" : PlotConfig(min_value = -45.0, max_value = 45.0, delta_value = 10.0, color_map = 'seismic'),
                   "reference-description" : "E-OBS data taken from https://knmi-ecad-assets-prd.s3.amazonaws.com/ensembles/data/Grid_0.1deg_reg_ensemble/qq_ens_mean_0.1deg_reg_v23.1e.nc"
               },  
    
    "ALWD_S" : {},
    
    "SPEED_10M_AV" : {  "reference-file-pattern" : root+"/obs/E-OBS/monthly/fg_ens_mean_0.1deg_reg_v23.1e.nc",
                  "reference-variable-name" : "fg",
                  "reference-additional-operators" : "-setattribute,fg@missing_value=-9999s", # change missing value from string to number, otherwise problems with plotting
                  "plot-config-anomaly" : PlotConfig(min_value = -5.5, max_value = 5.5, delta_value = 1.0, color_map = 'seismic')
               }, 
               
    "PMSL_AV" : {  "reference-file-pattern" : root+"/obs/E-OBS/monthly/pp_ens_mean_0.1deg_reg_v23.1e.nc",
                  "reference-variable-name" : "pp",
                  "reference-additional-operators" : "-b f32 -setattribute,pp@units=Pa -mulc,100.0",
                  "plot-config-anomaly" : PlotConfig( min_value = -550.0, max_value = 550.0, delta_value = 100.0, color_map = 'seismic')
               }, 
    
    "RELHUM_2M" : {  "reference-file-pattern" : root+"/obs/E-OBS/monthly/hu_ens_mean_0.1deg_reg_v23.1e.nc",
                  "reference-variable-name" : "hu",
                  "reference-additional-operators" : "-b f32",
                  "plot-config-anomaly" : PlotConfig( min_value = -20.0, max_value = 20.0, delta_value = 5.0, color_map = 'seismic')
               },    
    
    "AEVAP_S" : {},    
    "ALHFL_S" : {},
    "ASHFL_S" : {},
    "CLCT" : {},
    "AUMFL_S" : {},  
    "AVMFL_S" : {},    
    "T" : {},  
}
         

