from plot_config import PlotConfig

def convert_K2C(variable, units):
    if units == "K":
        variable -= 273.15
        units = "Celsius"
    return variable, units

variables = {}
variables["JJA"] = [PlotConfig("T_2M", min_value = 5.0, max_value = 25.0, delta_value = 2.5, contour = True, color_map = 'YlOrRd', transform_variable = convert_K2C, task_name="seasonal_mean"), 
                    PlotConfig("RAIN_TOT", min_value = 0.0, max_value = 4.0, delta_value = 0.5, color_map = 'YlGnBu', task_name="seasonal_mean"),
                    PlotConfig("T_2M", min_value = 5.0, max_value = 25.0, delta_value = 2.5, contour = True, color_map = 'YlOrRd', transform_variable = convert_K2C, path="../process_reference/results/_scratch_usr_mvkkarst_obs_E-OBS-19790901_19891130/T_2M-JJA.nc")]
variables["DJF"] = [PlotConfig("T_2M", min_value = -15.0, max_value = 15.0, delta_value = 3.75, contour = True, color_map = 'YlOrRd', transform_variable = convert_K2C, task_name="seasonal_mean"), 
                    PlotConfig("RAIN_TOT", min_value = 0.0, max_value = 4.0, delta_value = 0.5, color_map = 'YlGnBu', task_name="seasonal_mean")]
variables["JJA-PCTL_95"] = [PlotConfig("T_2M", min_value = 5.0, max_value = 37.0, delta_value = 4.0, contour = True, color_map = 'YlOrRd', transform_variable = convert_K2C, task_name="seasonal_percentile")]
variables["DJF-PCTL_95"] = [PlotConfig("T_2M", task_name="seasonal_percentile")]
