import sys
sys.path.append('../../auxiliary')
from plot_config import PlotConfig

# templates for temperatur and rain
mom_temp = PlotConfig("", task_name="seasonal_mean", lon_name = "xt_ocean", lat_name = "yt_ocean", width = 1500000, height = 1800000)

sst = mom_temp.clone("sst", contour = True, color_map = 'YlOrRd')
eta = mom_temp.clone("eta_t", min_value = -0.6, max_value = 0.6, delta_value = 0.05, contour = True, color_map = 'coolwarm')
sss = mom_temp.clone("sss", min_value = 0.0, max_value = 10.0, delta_value = 1.25, contour = True, color_map = 'RdPu')

seasons = ["JJA", "MAM", "SON", "DJF"]

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
        
    plot_configs[season] = [sst.clone(), eta.clone(), sss.clone()]

    

