dependencies = ["extract_stations"]

import sys
sys.path.append('../../auxiliary')
from plot_config import PlotConfig

stations = ["ROSTOCK-WARNEMUNDE", "HELSINKI-KAISANIEMI", "STOCKHOLM", "TALLINN", "VISBY", "SUNDSVALL", "LULEA", "VAASA-PALOSAARI"]

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
        plot_configs["T_2M_AV-" + station + "-" + operator] = [ t2m.clone(file="T_2M_AV-" + station + "-" + operator + ".nc", transform_variable = convert_K2C), 
                                                                t2m.clone(file="T_2M_AV-reference-" + station + "-" + operator + ".nc", linestyle="ro")]   
        plot_configs["TOT_PREC-" + station + "-" + operator] = [ rain.clone(file="TOT_PREC-" + station + "-" + operator + ".nc"), 
                                                                rain.clone(file="TOT_PREC-reference-" + station + "-" + operator + ".nc", linestyle="ro-")]     

    

