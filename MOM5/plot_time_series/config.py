dependencies = ["extract_stations"]

import sys
sys.path.append('../../auxiliary')
from plot_config import PlotConfig

stations = ["BY5", "F9", "SR5", "BY31"]
    
operators = ["monmean", "ymonmean"]

def convert_K2C(variable, units):
    variable -= 273.15
    units = "Celsius"
    return variable, units

sst = PlotConfig("SST", task_name="extract_stations")
fi = PlotConfig("FI", task_name="extract_stations")

plot_configs = {}

for station in stations:
    for operator in operators:
    
        if operator == "monmean":
            trend = True
            std = False
        else:
            trend = False
            std = True   
            
        plot_configs["SST-" + station + "-" + operator] = [sst.clone(file="SST-" + station + "-" + operator + ".nc", title="model", trend=trend, std_deviation=std),
                                                           sst.clone(file="SST-reference-" + station + "-" + operator + ".nc", linestyle="r.-", transform_variable = convert_K2C, title="reference", trend=trend, std_deviation=std) ]      
        plot_configs["FI-" + station + "-" + operator] = [fi.clone(file="FI-" + station + "-" + operator + ".nc", title="model", trend=trend, std_deviation=std),
                                                           fi.clone(file="FI-reference-" + station + "-" + operator + ".nc", linestyle="r.-", title="reference", trend=trend, std_deviation=std) ]                                                           

    

