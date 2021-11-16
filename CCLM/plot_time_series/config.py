dependencies = ["extract_stations"]

import sys
sys.path.append('../../auxiliary')
from plot_config import PlotConfig

stations = ["ROSTOCK-WARNEMUNDE"]
operators = ["monmean", "ymonmean"]

def convert_K2C(variable, units):
    variable -= 273.15
    units = "Celsius"
    return variable, units

t2m = PlotConfig("T_2M_AV", task_name="extract_stations")
rain = PlotConfig("TOT_PREC", task_name="extract_stations")

plot_configs = {}

for station in stations:
    for operator in operators:
        
        plot_configs[station + "-" + operator] = [t2m.clone(transform_variable = convert_K2C, first_plot = True, last_plot = False)]   
        plot_configs["reference-" + station + "-" + operator] = [t2m.clone(linestyle="ro", first_plot = False, last_plot = True)]     
        plot_configs[station + "-" + operator] = [rain.clone(first_plot = True, last_plot = False)]   
        plot_configs["reference-" + station + "-" + operator] = [rain.clone(linestyle="r-", first_plot = False, last_plot = True)]     

    

