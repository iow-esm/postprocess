dependencies = ["seasonal_mean", "calculate_anomalies", "process_reference"]

import sys
sys.path.append('../../auxiliary')
from plot_config import PlotConfig

sys.path.append('../')
import global_settings

template = PlotConfig("", width=7000000, height=5000000)

plot_configs = {}

for var in global_settings.variables.keys():
    
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
        plot_configs[var + "-anomaly-" + season] = [template.clone(var, task_name="calculate_anomalies", file = var + "-" + season + ".nc", symmetric = True, color_map = 'seismic')]

