import sys
sys.path.append('../../auxiliary')
from plot_config import PlotConfig

# templates for temperatur and rain
mom_temp = PlotConfig("", task_name="seasonal_mean", lon_name = "xt", lat_name = "yt", width = 1500000, height = 1800000)

sst = mom_temp.clone("SST", contour = True, color_map = 'YlOrRd')
eta = mom_temp.clone("SSH", min_value = -0.6, max_value = 0.6, delta_value = 0.05, contour = True, color_map = 'PiYG')
sss = mom_temp.clone("SSS", min_value = 0.0, max_value = 10.0, delta_value = 1.25, contour = True, color_map = 'RdPu')
fi = mom_temp.clone("FI", min_value = 0.0, max_value = 1.0, delta_value = 0.1, contour = True, color_map = 'Blues_r')

seasons = ["MAM", "SON", "JJA", "DJF"]

reference_dir = "../process_reference/results/_scratch_usr_mvkkarst_obs_Copernicus-19810901_20091130"
reference_title = "Copernicus-19810901_20091130"

def convert_K2C(variable, units):
    variable -= 273.15
    units = "Celsius"
    return variable, units

plot_configs = {}

for season in seasons:
    
    if season == "JJA":
        sst = sst.clone(min_value = 8.0, max_value = 18.0, delta_value = 1.0,)
    elif season == "MAM":
        sst = sst.clone(min_value = 0.0, max_value = 10.0, delta_value = 1.0)
    elif season == "SON":
        sst = sst.clone(min_value = 5.0, max_value = 15.0, delta_value = 1.0)
    elif season == "DJF":
        sst = sst.clone(min_value = -2.0, max_value = 8.0, delta_value = 1.0)
        
    plot_configs[season] = [sst.clone(),
                            sst.clone(path=reference_dir + "/SST-" + season + ".nc", title = "SST-" + season + "-" + reference_title, transform_variable = convert_K2C, lon_name = "lon", lat_name = "lat"),
                            sst.clone(task_name="calculate_anomalies", min_value = -4.5, max_value = 4.5, delta_value = 1.0, title = "SST-" + season + "-anomaly-" + reference_title, color_map = 'seismic'),
                            eta.clone(), 
                            sss.clone(),
                            fi.clone(),
                            fi.clone(path=reference_dir + "/FI-" + season + ".nc", title = "FI-" + season + "-" + reference_title, lon_name = "lon", lat_name = "lat"),
                            fi.clone(task_name="calculate_anomalies", min_value = -0.45, max_value = 0.45, delta_value = 0.1, title = "FI-" + season + "-anomaly-" + reference_title, color_map = 'seismic_r')]
    
# percentiles = ["95", "5"]
# mom_temp = PlotConfig("", task_name="seasonal_percentile", lon_name = "xt_ocean", lat_name = "yt_ocean", width = 1500000, height = 1800000)

# sst = mom_temp.clone("SST", contour = True, delta_value = 1.0, color_map = 'YlOrRd')
# eta = mom_temp.clone("SSH", delta_value = 0.05, contour = True, color_map = 'coolwarm')
# sss = mom_temp.clone("SSH", delta_value = 1.25, contour = True, color_map = 'RdPu')
# for season in seasons:
    # for percentile in percentiles:
        # if season == "JJA":
            # if percentile == "95":
                # sst = sst.clone(min_value = 10.0, max_value = 24.0, delta_value = 2.0,)
            # elif percentile == "5":
                # sst = sst.clone(min_value = 2.0, max_value = 15.0, delta_value = 2.0)
        # elif season == "DJF":
            # if percentile == "95":
                # sst = sst.clone(min_value = 2.0, max_value = 7.0, delta_value = 0.5,)
            # elif percentile == "5":
                # sst = sst.clone(min_value = -2.0, max_value = 3.0, delta_value = 0.5)
                
        # plot_configs[season + "-PCTL_" + percentile] = [sst.clone(), 
                                                        # sst.clone(path=reference_dir + "/SST-" + season + ".nc", title = "SST-" + season + "-PCTL_" + percentile + "-" + reference_title, transform_variable = convert_K2C),
                                                        # eta.clone(), sss.clone()]

    

