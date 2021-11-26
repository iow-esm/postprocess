dependencies = ["extract_stations", "calculate_anomalies"]

import sys
sys.path.append('../../auxiliary')
from plot_config import PlotConfig

sys.path.append('../')
import global_settings

def convert_K2C(variable, units):
    variable -= 273.15
    units = "Celsius"
    return variable, units

plot_configs = {}

for var in global_settings.variables.keys():
    
    temp = PlotConfig(var, task_name="extract_stations")
    if var == "T_2M_AV":
        transform_variable = convert_K2C
    else:
        transform_variable = None
        
    for operator in global_settings.variables[var]["time-series-operators"]:
        for station in global_settings.variables[var]["stations"]:
        
            if operator == "monmean":
                trend = True
                std = False
            else:
                trend = False
                std = True   

            plot_configs[var + "-" + station + operator] = [ temp.clone(file=var + "-" + station + operator + ".nc", transform_variable = transform_variable, title="model", trend=trend, std_deviation=std), 
                                                                   temp.clone(file=var + "-reference-" + station + operator + ".nc", transform_variable = transform_variable, linestyle="r.-", title="reference", trend=trend, std_deviation=std),
                                                                   temp.clone(task_name="calculate_anomalies", file=var + "-" + station + operator + ".nc", title="anomaly", trend=False, std_deviation=False)]  
                

        plot_configs[var + "-ensmean" + operator] = [temp.clone(file=var + "-ensmean" + operator + ".nc", transform_variable = transform_variable, title="model", trend=trend, std_deviation=std), 
                                                      temp.clone(file=var + "-reference-ensmean" + operator + ".nc", transform_variable = transform_variable, linestyle="r.-", title="reference", trend=trend, std_deviation=std),
                                                      temp.clone(task_name="calculate_anomalies", file= var + "-ensmean" + operator + ".nc", title="anomaly", trend=False, std_deviation=False)]                                                                                

    

