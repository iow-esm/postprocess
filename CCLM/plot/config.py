import sys
sys.path.append('../../auxiliary')
from plot_config import PlotConfig

def convert_K2C(variable, units):
    if units == "K":
        variable -= 273.15
        units = "Celsius"
    return variable, units


reference_dir = "../process_reference/results/_scratch_usr_mvkkarst_obs_E-OBS-19790901_20091130"
reference_title = "E-OBS-19790901_20091130"

cclm_template = PlotConfig("", width=7000000, height=5000000)

# templates for temperatur and rain
t2m = cclm_template.clone("T_2M", contour = True, color_map = 'YlOrRd', transform_variable = convert_K2C, task_name="seasonal_mean")
rain = cclm_template.clone("TOT_PREC", min_value = 0.0, max_value = 4.0, delta_value = 0.5, color_map = 'YlGnBu', task_name="seasonal_mean")

seasons = ["JJA", "MAM", "SON", "DJF"]

plot_configs = {}

for season in seasons:
    
    if season == "JJA":
        t2m = t2m.clone(min_value = 5.0, max_value = 25.0, delta_value = 2.5)
    elif season == "MAM" or season == "SON":
        t2m = t2m.clone(min_value = -5.0, max_value = 20.0, delta_value = 3.125)
    elif season == "DJF":
        t2m = t2m.clone(min_value = -15.0, max_value = 15.0, delta_value = 3.75)
        
    plot_configs[season] = [t2m.clone(), 
                            t2m.clone(path=reference_dir + "/T_2M-" + season + ".nc", title = "T_2M-" + season + "-" + reference_title),
                            rain.clone(),
                            rain.clone(path=reference_dir + "/TOT_PREC-" + season + ".nc", title = "TOT_PREC-" + season + "-" + reference_title)]

# templates for temperatur and rain
t2m = cclm_template.clone("T_2M", contour = True, color_map = 'YlOrRd', transform_variable = convert_K2C, task_name="seasonal_percentile")
rain = cclm_template.clone("TOT_PREC", min_value = 0.0, max_value = 4.0, delta_value = 0.5, color_map = 'YlGnBu', task_name="seasonal_percentile")
    
seasons = ["JJA", "DJF"]
percentiles = ["95", "5"]

for season in seasons:
    for percentile in percentiles:
        
        if season == "JJA":
            if percentile == "95":
                t2m = t2m.clone(min_value = 5.0, max_value = 37.0, delta_value = 4.0)
            elif percentile == "5":
                t2m = t2m.clone(min_value = -5.0, max_value = 27.0, delta_value = 4.0)
        if season == "DJF":
            if percentile == "5":
                t2m = t2m.clone(min_value = -17.0, max_value = 10.0, delta_value = 3.0)
            elif percentile == "95":
                t2m = t2m.clone(min_value = -7.0, max_value = 20.0, delta_value = 3.0)
                
        if percentile == "5":
            rain = rain.clone(min_value = 1.0, max_value = 10.0, delta_value = 1.0)
        elif percentile == "95":
            rain = rain.clone(min_value = 10.0, max_value = 20.0, delta_value = 1.0) 
            
        plot_configs[season + "-PCTL_" + percentile] = [t2m.clone(), 
                                                        t2m.clone(path=reference_dir + "/T_2M-" + season + "-PCTL_" + percentile + ".nc", 
                                                                  title = "T_2M-" + season + "-PCTL_" + percentile + "-" + reference_title),
                                                        rain.clone(),
                                                        rain.clone(path=reference_dir + "/TOT_PREC-" + season + "-PCTL_" + percentile + ".nc", 
                                                                   title = "TOT_PREC-" + season + "-PCTL_" + percentile + "-" + reference_title)]
