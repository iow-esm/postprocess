dependencies = ["extract_stations"]

import sys
sys.path.append('../../auxiliary')
from plot_config import PlotConfig

stations = ["BY5"]
operators = ["monmean", "ymonmean"]

def convert_K2C(variable, units):
    variable -= 273.15
    units = "Celsius"
    return variable, units

sst = PlotConfig("SST", task_name="extract_stations")

plot_configs = {}

for station in stations:
    for operator in operators:
        
        plot_configs[station + "-" + operator] = [sst.clone(first_plot = True, last_plot = False)]   
        plot_configs["reference-" + station + "-" + operator] = [sst.clone(linestyle="ro", transform_variable = convert_K2C, first_plot = False, last_plot = True)]     

    

