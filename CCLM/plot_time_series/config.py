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

    # check the dimensionality of the variable (only station/region data of 3D (2 spatial + time) variable can be plotted as time series)
    try:
        dimension = global_settings.variables[var]["dimension"]
    except:
        dimension = 3

    if dimension != 3:
        continue        
    
    if var == "T_2M_AV":
        transform_variable = convert_K2C
    else:
        transform_variable = None
        
    for operator in global_settings.variables[var]["time-series-operators"]:

        if operator == "-monmean":
            trend = True
            std = False
        else:
            trend = False
            std = True          
    
        temp = PlotConfig(var, task_name="extract_stations")
        
        for station in global_settings.variables[var]["stations"]:

            plot_configs[var + "-" + station + operator] = [temp.clone(file=var + "-" + station + operator + ".nc", title="model", trend=trend, std_deviation=std, transform_variable = transform_variable)]
            
            try: 
                global_settings.variables[var]["reference-file-pattern"]
                plot_configs[var + "-" + station + operator] += [temp.clone(file=var + "-reference-" + station + operator + ".nc", linestyle="r.-", title="reference", trend=trend, std_deviation=std, transform_variable = transform_variable)]
                if var != "PMSL_AV":
                    plot_configs[var + "-" + station + operator] += [temp.clone(task_name="calculate_anomalies", file=var + "-" + station + operator + ".nc", title="anomaly", trend=False, std_deviation=False)]  
            except:
                print("No reference is given for " + var)
                pass

        plot_configs[var + "-ensmean" + operator] = [temp.clone(file=var + "-ensmean" + operator + ".nc", title="model", trend=trend, std_deviation=std, transform_variable = transform_variable)]        
        try: 
            global_settings.variables[var]["reference-file-pattern"]
            plot_configs[var + "-ensmean" + operator] += [temp.clone(file=var + "-reference-ensmean" + operator + ".nc", linestyle="r.-", title="reference", trend=trend, std_deviation=std, transform_variable = transform_variable)]
            if var != "PMSL_AV":
                plot_configs[var + "-ensmean" + operator] += [temp.clone(task_name="calculate_anomalies", file= var + "-ensmean" + operator + ".nc", title="anomaly", trend=False, std_deviation=False)]                                                                               
        except:
            print("No reference is given for " + var)
            pass
            
        temp = PlotConfig(var, task_name="extract_regions")
        
        for station in global_settings.variables[var]["regions"]:

            plot_configs[var + "-" + station + operator] = [temp.clone(file=var + "-" + station + operator + ".nc", title="model", trend=trend, std_deviation=std, transform_variable = transform_variable)]
            
            try: 
                global_settings.variables[var]["reference-file-pattern"]
                plot_configs[var + "-" + station + operator] += [temp.clone(file=var + "-reference-" + station + operator + ".nc", linestyle="r.-", title="reference", trend=trend, std_deviation=std, transform_variable = transform_variable)]
                if var != "PMSL_AV":
                    plot_configs[var + "-" + station + operator] += [temp.clone(task_name="calculate_anomalies", file=var + "-" + station + operator + ".nc", title="anomaly", trend=False, std_deviation=False)]  
            except:
                print("No reference is given for " + var)
                pass            
    

