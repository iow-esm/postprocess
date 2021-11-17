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
        plot_configs["SST-" + station + "-" + operator] = [sst.clone(file="SST-" + station + "-" + operator + ".nc", title="model"),
                                                           sst.clone(file="SST-reference-" + station + "-" + operator + ".nc", linestyle="ro", transform_variable = convert_K2C, title="reference") ]       

    

