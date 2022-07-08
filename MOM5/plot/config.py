# this depends on a processed raw output
dependencies = ["seasonal_mean", "calculate_anomalies", "process_reference"]

import sys
sys.path.append('../../auxiliary')
from plot_config import PlotConfig

sys.path.append('../')
import global_settings

template = PlotConfig("", lon_name = "xt", lat_name = "yt", width = 1500000, height = 1800000)

plot_configs = {}

for var in global_settings.variables.keys():

    # check the dimensionality of the variable (only 3D (2 spatial + time) can be plotted on map)
    try:
        dimension = global_settings.variables[var]["dimension"]
    except:
        dimension = 3

    if dimension != 3:
        continue
    
    try:
        config = global_settings.variables[var]["plot-config"].clone()
    except:
        config = template.clone()

    seasons = global_settings.variables[var]["seasons"].keys()

    for season in seasons:
        plot_configs[var + "-" + season] = [config.clone(var, task_name="seasonal_mean", file=var + "-" + season + ".nc")]
         
        try: 
            global_settings.variables[var]["reference-file-pattern"]
        except:
            print("No reference is given for " + var)
            continue
        
        plot_configs[var + "-reference-" + season] = [config.clone(var, task_name="seasonal_mean", file=var + "-reference-" + season + ".nc")]
        
        try:
                anomaly_config = global_settings.variables[var]["plot-config-anomaly"].clone()
        except:
                anomaly_config = template.clone(symmetric = True, color_map = 'seismic')
        plot_configs[var + "-anomaly-" + season] = [anomaly_config.clone(var, task_name="calculate_anomalies", file = var + "-" + season + ".nc")]

