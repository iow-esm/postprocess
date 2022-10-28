import sys
import pandas as pd
import glob
import xarray as xr
import numpy as np

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

sys.path.append(pwd+"/../../auxiliary")
import plot_vertical_profile

os.chdir(pwd+"/{results_dir}")

import matplotlib.pyplot as plt
import numpy as np
import xarray as xr

# extend this dictionary if necessary
model_dirs = {{"model1" : pwd+"/../calculate_anomalies/{results_dir}"}}
# change the reference directory if nercessary
ref_dir = pwd+"/../process_reference/{results_dir}"

models = list(model_dirs.keys())

for var in variables.keys():

    try:
        variables[var]['reference-file-pattern']
    except:
        continue

    seasons = list(variables[var]["seasons"].keys())

    vmin = variables[var]["plot-config-anomaly"].min_value
    vmax = variables[var]["plot-config-anomaly"].max_value

    if variables[var]["plot-config-anomaly"].delta_value is not None:
        nlevels = int((vmax - vmin)/variables[var]["plot-config-anomaly"].delta_value)
    else:
        nlevels = 13

    cmap = plt.get_cmap(variables[var]["plot-config-anomaly"].color_map, nlevels)

    ctr_plot_cfg = {{"vmin" : vmin, "vmax" : vmax, "levels" : np.linspace(vmin,vmax,nlevels+1), "linewidths" : 0.75, "colors" : "black",  "linestyles" : "-"}}
    coast_plot_cfg = {{"levels" : [0.1], "linewidths" : 1.5, "colors" : "black"}}
    data_plot_cfg = {{"vmin" : vmin, "vmax" : vmax, "cmap" : cmap}}

    fig, axs = plt.subplots(len(models), len(seasons), figsize=(4*len(seasons), 4*len(models)), sharex='col', sharey='row', squeeze=0, gridspec_kw={{"width_ratios": (len(seasons)-1)*[1] + [1.25]}})

    for i, model in enumerate(models):
        for j, season in enumerate(seasons):
            
            ds = xr.open_dataset(model_dirs[model]+"/"+var+"-"+season+".nc")
            ds_var = ds.data_vars[var]

            try:
                units = ds_var.units
            except:
                units = "a.u."

            if j == len(seasons)-1:
                cbar_params = {{"add_colorbar" : True, "cbar_kwargs" : {{"label" : ""}}}}
            else:
                cbar_params = {{"add_colorbar" : False}}

            ds_var.plot(ax=axs[i,j], **cbar_params, **data_plot_cfg)
            
            if variables[var]["plot-config-anomaly"].contour:
                axs[i,j].contour(ds_var.coords[variables[var]["plot-config-anomaly"].lon_name], ds_var.coords[variables[var]["plot-config-anomaly"].lat_name], np.squeeze(ds_var.data), **ctr_plot_cfg)
            
            coast = np.where((~ds_var.isnull()), 1.0, 0.0)
            axs[i,j].contour(ds_var.coords[variables[var]["plot-config-anomaly"].lon_name], ds_var.coords[variables[var]["plot-config-anomaly"].lat_name], np.squeeze(coast.data), **coast_plot_cfg)
            
            if i == 0:
                axs[i,j].set_title(season, fontweight='bold')
            else:
                axs[i,j].set_title("")

            if j != 0:
                axs[i,j].set_ylabel("")
                
            if i != len(models)-1:
                axs[i,j].set_xlabel("")

            axs[i,j].grid(linestyle='--', alpha=0.6)

    fig.tight_layout()  
    plt.subplots_adjust(wspace=0, hspace=0)
    fig.savefig(var+".png", dpi=100)
"""

f = open(pwd+"/"+results_dir+"/compare_2D_anomalies.py", "w")
f.write(script)
f.close()

exec(script)

import convertpy2ipynb
convertpy2ipynb.convertpy2ipynb(pwd+"/"+results_dir+"/compare_2D_anomalies.py")