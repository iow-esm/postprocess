dependencies = ["seasonal_mean", "calculate_anomalies", "process_reference"]

import sys
sys.path.append('../../auxiliary')
from plot_config import PlotConfig

def convert_K2C(variable, units):

    variable -= 273.15
    units = "Celsius"
    
    return variable, units

cclm_template = PlotConfig("", width=7000000, height=5000000)

# templates for temperatur and rain
t2m = cclm_template.clone("T_2M_AV", contour = True, color_map = 'YlOrRd')
rain = cclm_template.clone("DAY_PREC", min_value = 0.0, max_value = 4.0, delta_value = 0.5, color_map = 'YlGnBu')
swfl = cclm_template.clone("ASWD_S", min_value = 0.0, max_value = 300.0, delta_value = 30.0, contour = True, color_map = 'inferno')
speed = cclm_template.clone("SPEED_10M_AV", min_value = 0.0, max_value = 7.0, delta_value = 0.5, contour = False, color_map = 'terrain_r')
pmsl = cclm_template.clone("PMSL_AV", min_value = 100200.0, max_value = 102200.0, delta_value = 150.0, contour = True, color_map = 'rainbow')

seasons = ["JJA", "MAM", "SON", "DJF"]

plot_configs = {}

for season in seasons:
    
    if season == "JJA":
        t2m = t2m.clone(min_value = 5.0, max_value = 25.0, delta_value = 2.5)
    elif season == "MAM" or season == "SON":
        t2m = t2m.clone(min_value = -5.0, max_value = 20.0, delta_value = 3.125)
    elif season == "DJF":
        t2m = t2m.clone(min_value = -15.0, max_value = 15.0, delta_value = 3.75)
        
    plot_configs["T_2M_AV-" + season] = [t2m.clone(task_name="seasonal_mean", file="T_2M_AV-" + season + ".nc", transform_variable = convert_K2C)]
    plot_configs["T_2M_AV-reference-" + season] = [t2m.clone(task_name="seasonal_mean", file="T_2M_AV-reference-" + season + ".nc", transform_variable = convert_K2C)]
    plot_configs["T_2M_AV-anomaly-" + season] = [t2m.clone(task_name="calculate_anomalies", file = "T_2M_AV-" + season + ".nc", min_value = -6.5, max_value = 6.5, delta_value = 1.0, color_map = 'seismic')]
    
    plot_configs["DAY_PREC-" + season] = [rain.clone(task_name="seasonal_mean", file="DAY_PREC-" + season + ".nc")]
    plot_configs["DAY_PREC-reference-" + season] = [rain.clone(task_name="seasonal_mean", file="DAY_PREC-reference-" + season + ".nc")]
    plot_configs["DAY_PREC-anomaly-" + season] = [rain.clone(task_name="calculate_anomalies", file = "DAY_PREC-" + season + ".nc", min_value = -4.5, max_value = 4.5, delta_value = 1.0, color_map = 'BrBG')]
    
    plot_configs["ASWD_S-" + season] = [swfl.clone(task_name="seasonal_mean", file="ASWD_S-" + season + ".nc")]
    plot_configs["ASWD_S-reference-" + season] = [swfl.clone(task_name="seasonal_mean", file="ASWD_S-reference-" + season + ".nc")]
    plot_configs["ASWD_S-anomaly-" + season] = [swfl.clone(task_name="calculate_anomalies", file = "ASWD_S-" + season + ".nc", min_value = -45.0, max_value = 45.0, delta_value = 10.0, color_map = 'seismic')]
    
    plot_configs["SPEED_10M_AV-" + season] = [speed.clone(task_name="seasonal_mean", file="SPEED_10M_AV-" + season + ".nc")]
    plot_configs["SPEED_10M_AV-reference-" + season] = [speed.clone(task_name="seasonal_mean", file="SPEED_10M_AV-reference-" + season + ".nc")]
    plot_configs["SPEED_10M_AV-anomaly-" + season] = [speed.clone(task_name="calculate_anomalies", file = "SPEED_10M_AV-" + season + ".nc", min_value = -5.5, max_value = 5.5, delta_value = 1.0, color_map = 'seismic')]
    
    plot_configs["PMSL_AV-" + season] = [pmsl.clone(task_name="seasonal_mean", file="PMSL_AV-" + season + ".nc")]
    plot_configs["PMSL_AV-reference-" + season] = [pmsl.clone(task_name="seasonal_mean", file="PMSL_AV-reference-" + season + ".nc")]
    plot_configs["PMSL_AV-anomaly-" + season] = [pmsl.clone(task_name="calculate_anomalies", file = "PMSL_AV-" + season + ".nc", min_value = -550.0, max_value = 550.0, delta_value = 100.0, color_map = 'seismic')]


# templates for temperatur and rain
# t2m = cclm_template.clone("T_2M", contour = True, color_map = 'YlOrRd', transform_variable = convert_K2C, task_name="seasonal_percentile")
# rain = cclm_template.clone("TOT_PREC", min_value = 0.0, max_value = 4.0, delta_value = 0.5, color_map = 'YlGnBu', task_name="seasonal_percentile")
    
# seasons = ["JJA", "DJF"]
# percentiles = ["95", "5"]

# for season in seasons:
    # for percentile in percentiles:
        
        # if season == "JJA":
            # if percentile == "95":
                # t2m = t2m.clone(min_value = 5.0, max_value = 37.0, delta_value = 4.0)
            # elif percentile == "5":
                # t2m = t2m.clone(min_value = -5.0, max_value = 27.0, delta_value = 4.0)
        # if season == "DJF":
            # if percentile == "5":
                # t2m = t2m.clone(min_value = -17.0, max_value = 10.0, delta_value = 3.0)
            # elif percentile == "95":
                # t2m = t2m.clone(min_value = -7.0, max_value = 20.0, delta_value = 3.0)
                
        # if percentile == "5":
            # rain = rain.clone(min_value = 1.0, max_value = 1.5, delta_value = 0.05)
        # elif percentile == "95":
            # rain = rain.clone(min_value = 10.0, max_value = 30.0, delta_value = 2.0) 
            
        # plot_configs[season + "-PCTL_" + percentile] = [t2m.clone(), 
                                                        # t2m.clone(task_name="process_reference", 
                                                                  # title = "T_2M-" + season + "-PCTL_" + percentile + "-reference", lon_name="longitude", lat_name="latitude"),
                                                        # rain.clone(),
                                                        # rain.clone(task_name="process_reference", 
                                                                   # title = "TOT_PREC-" + season + "-PCTL_" + percentile + "-reference", lon_name="longitude", lat_name="latitude")]
