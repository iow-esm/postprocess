import sys

out_dir = str(sys.argv[1])
from_date = int(sys.argv[2])
to_date = int(sys.argv[3])
pwd = str(sys.argv[4])

import create_results_dir

results_dir = create_results_dir.create_results_dir(out_dir, from_date, to_date)

script = f"""import sys
import os

# modify the working directory if necessary
pwd = "{pwd}"
# go to working directory and import global_settings
os.chdir(pwd)
sys.path.append('../')
import global_settings
variables = global_settings.variables

sys.path.append('../../auxiliary')
from helpers import convert_to_decimal

os.chdir(pwd+"/{results_dir}")

import matplotlib.pyplot as plt
import numpy as np
import xarray as xr

import colorsys
  

for var in variables.keys():

    stations = variables[var]["stations"]
    regions = variables[var]["regions"]

    fig, ax = plt.subplots(1, 1,  figsize=(10, 6))
    
    nregions = len(regions.keys())
    HSV_tuples = [(x*1.0/nregions, 0.5, 0.7) for x in range(nregions)]
    RGB_tuples = list(map(lambda x: colorsys.hsv_to_rgb(*x), HSV_tuples))  
    
    proxy = []
    proxy_names = []

    for i, region in enumerate(regions.keys()):
        
        
        try:
            corners = {{}}
            for c in regions[region].keys():
                
                if not "lat-" in c and not "lon-" in c:
                    continue

                corners[c] = float(convert_to_decimal(regions[region][c]))
                
            x = [corners["lon-min"], corners["lon-max"], corners["lon-max"], corners["lon-min"], corners["lon-min"]]
            y = [corners["lat-min"], corners["lat-min"], corners["lat-max"], corners["lat-max"], corners["lat-min"]]

            ax.fill(x, y, 'b', alpha=0.6, color=RGB_tuples[i], label=region, zorder=i)
            proxy.append(plt.Rectangle((0,0),1,1,fc = RGB_tuples[i], alpha=0.6))
            proxy_names.append(region)
        except:
            try:
                ds = xr.open_dataset(regions[region]["maskfile"])
                ds_var = ds.data_vars["mask"]
                np.squeeze(ds_var).plot.contourf(ax=ax, levels = [0.1, 1.1], colors=[RGB_tuples[i], RGB_tuples[i]], alpha=0.6, add_colorbar=False, zorder=i)
                proxy.append(plt.Rectangle((0,0),1,1,fc = RGB_tuples[i], alpha=0.6))
                proxy_names.append(region)
            except:
                print("Configured region: "+str(regions[regions])+" cannot be processed!")
                continue

    for station in stations.keys():
        try:
            x = float(convert_to_decimal(stations[station]["lon"]))
            y = float(convert_to_decimal(stations[station]["lat"]))
            ax.scatter(x, y, label=station, color="red", zorder=nregions+1)
            ax.text(x, y, station, zorder=nregions+1)
        except:
            print("Configured station: "+str(station[stations])+" cannot be processed!")
            continue    

    ax.set_title("Stations and regions for variable "+var)
    ax.legend(proxy, proxy_names, loc='center left', bbox_to_anchor=(1, 0.5))
    ax.grid(linestyle='--', alpha=0.6)
    plt.subplots_adjust(right=0.6)
    fig.savefig(var+".png", dpi=100)
"""



f = open(pwd+"/"+results_dir+"/draw_stations_and_regions.py", "w")
f.write(script)
f.close()

exec(script)

import convertpy2ipynb
convertpy2ipynb.convertpy2ipynb(pwd+"/"+results_dir+"/draw_stations_and_regions.py")