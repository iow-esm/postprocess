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
from helpers import convert_to_decimal, plot_coast, get_n_colors

os.chdir(pwd+"/{results_dir}")

import matplotlib.pyplot as plt
import numpy as np
import xarray as xr

hatches = ['++', '', 'xx', '', 'oo', '', 'OO', '', '..', '', '**', '']
linestyles = ['-', '--', '-', ':', '-', '-.']

for var in variables.keys():

    stations = variables[var]["stations"]
    regions = variables[var]["regions"]

    fig, ax = plt.subplots(1, 1,  figsize=(6, 4))
    
    RGB_tuples = get_n_colors(len(regions.keys())+1, cmap="Paired")  
    
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

            ax.fill(x, y, 'b', alpha=1.0, color=RGB_tuples[i], label=region, zorder=i)
            proxy.append(plt.Rectangle((0,0),1,1,fc = RGB_tuples[i], alpha=1.0))
            proxy_names.append(region)
        except:
            try:
                ds = xr.open_dataset(regions[region]["maskfile"])
                ds_var = ds["mask"]
                #np.squeeze(ds_var).plot.contourf(ax=ax, levels = [0.1, 1.1], colors=[RGB_tuples[i], RGB_tuples[i]], hatches=hatches[i%len(hatches)], alpha=0.3, add_colorbar=False, zorder=i)
                if True:
                    np.squeeze(ds_var).plot.contourf(ax=ax, levels = [0.1, 1.1], colors=[RGB_tuples[i], RGB_tuples[i]], alpha=1.0, add_colorbar=False, zorder=i)
                    proxy.append(plt.Rectangle((0,0),1,1,fc = RGB_tuples[i]))
                else:
                    borders = np.where((~ds_var.isnull()), 1.0, 0.0)
                    ds_var.values = borders
                    borders_plot_cfg = {{"levels" : [0.1], "linewidths" : [3.0], "colors" : [RGB_tuples[i]], "linestyles" : ["-"]}}
                    np.squeeze(ds_var).plot.contour(ax=ax, **borders_plot_cfg, zorder=i)
                #proxy.append(plt.Rectangle((0,0),1,1,fc = RGB_tuples[i], hatch=hatches[i%len(hatches)], alpha=0.6))
                #proxy.append(plt.Rectangle((0,0),1,1,fc = RGB_tuples[i], edgecolor=RGB_tuples[i], linestyle=linestyles[i%len(linestyles)], alpha=0.3, linewidth = 2.0*(len(regions.keys())-1-i)/(len(regions.keys())-1)))
                    proxy.append(plt.Rectangle((0,0),1,1,color = RGB_tuples[i], fill=False))
                proxy_names.append(region)
                ds.close()
            except:
                print("Configured region: "+str(regions[region])+" cannot be processed!")
                continue

    for i, station in enumerate(stations.keys()):
        try:
            x = float(convert_to_decimal(stations[station]["lon"]))
            y = float(convert_to_decimal(stations[station]["lat"]))
            ax.scatter(x, y, label=station, color=RGB_tuples[-1], zorder=200, marker="o")
            ax.text(x, y, str(i+1), zorder=200, fontweight="bold")
            proxy.append(plt.Circle((0,0), color = RGB_tuples[-1]))
            proxy_names.append(str(i+1)+": "+station)
        except:
            print("Configured station: "+str(stations[station])+" cannot be processed!")
            continue    

    plot_coast(ax)

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