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

sys.path.append('../../auxiliary')
from helpers import plot_coast, load_dataset, unload_dataset

os.chdir(pwd+"/{results_dir}")

import matplotlib.pyplot as plt
import numpy as np
import xarray as xr

# extend this dictionary if necessary
model_dirs = {{"model1" : pwd+"/../calculate_anomalies/{results_dir}"}}
# change the reference directory if nercessary
ref_dir = pwd+"/../process_reference/{results_dir}"

models = list(model_dirs.keys())
if len(models) > 1:
    compare = True
    errors = {{}}
    stds = {{}}
    import colorsys
    HSV_tuples = [(x*1.0/(len(models)), 0.5, 0.7) for x in range(len(models))]
    RGB_tuples = list(map(lambda x: colorsys.hsv_to_rgb(*x), HSV_tuples))    
else:
    compare = False

for var in variables.keys():

    try:
        variables[var]['reference-file-pattern']
    except:
        continue

    seasons = list(variables[var]["seasons"].keys())

    vmin = variables[var]["plot-config-anomaly"].min_value
    vmax = variables[var]["plot-config-anomaly"].max_value

    if variables[var]["plot-config-anomaly"].delta_value is not None:
        d = variables[var]["plot-config-anomaly"].delta_value
        levels = np.arange(vmin,vmax+d,d)
        levels = levels[np.abs(levels)>1.0e-15].tolist()
        s = len(levels)//14 + 1
        ticks = list(set(sorted(levels[::s]+[0])))
    else:
        levels = np.linspace(vmin,vmax,13).tolist()
        ticks = list(set(sorted(levels+[0])))

    ctr_plot_cfg = {{"levels" : levels, "linewidths" : 0.75, "colors" : "black",  "linestyles" : "-"}}
    data_plot_cfg = {{"cmap" : variables[var]["plot-config-anomaly"].color_map, "levels" : levels}}

    fig, axs = plt.subplots(len(models), len(seasons), figsize=(4*len(seasons), 4*len(models)), sharex='col', sharey='row', squeeze=0, gridspec_kw={{"width_ratios": (len(seasons)-1)*[1] + [1.25]}})

    for i, model in enumerate(models):

        if compare:
            errors[model] = []
            stds[model] = []

        for j, season in enumerate(seasons):
            
            ds = load_dataset(model_dirs[model]+"/"+var+"-"+season+".nc")
            ds_var = ds.data_vars[var]

            try:
                units = ds_var.units
            except:
                units = "a.u."

            if j == len(seasons)-1:
                cbar_params = {{"add_colorbar" : True, "cbar_kwargs" : {{"label" : var+" ["+units+"]", "ticks" : ticks}}}}
            else:
                cbar_params = {{"add_colorbar" : False}}

            ds_var.plot(ax=axs[i,j], **cbar_params, **data_plot_cfg)
            
            if variables[var]["plot-config-anomaly"].contour:
                np.squeeze(ds_var).plot.contour(ax=axs[i,j], **ctr_plot_cfg)

            plot_coast(axs[i,j])
            
            if i == 0:
                axs[i,j].set_title(season, fontweight='bold')
            else:
                axs[i,j].set_title("")

            if j != 0:
                axs[i,j].set_ylabel("")
                
            if i != len(models)-1:
                axs[i,j].set_xlabel("")

            axs[i,j].grid(linestyle='--', alpha=0.6)

            if compare:
                dummy = ds_var.values.ravel()
                dummy = np.abs(dummy[~np.isnan(dummy)])
                errors[model].append(np.mean(dummy))
                stds[model].append(np.std(dummy))

            unload_dataset(ds)

    fig.tight_layout()  
    plt.subplots_adjust(wspace=0, hspace=0)
    fig.savefig(var+".png", dpi=100)

    if not compare:
        continue
        
    fig, axs = plt.subplots(1, len(seasons), figsize=(4*len(seasons), 4), sharey='row', squeeze=0)
    
    for j, season in enumerate(seasons):
        for i, model in enumerate(models):
            axs[0,j].bar(model, errors[model][j], yerr=stds[model][j], color=RGB_tuples[i], ecolor=RGB_tuples[i], label=model)
            axs[0,j].plot([i,len(models)-1+0.4],[errors[model][j],errors[model][j]], color=RGB_tuples[i], alpha=0.5, linestyle="--")
            
    fig.tight_layout()  
    plt.subplots_adjust(wspace=0, hspace=0)
    fig.savefig(var+"2.png", dpi=100)
"""

f = open(pwd+"/"+results_dir+"/compare_2D_anomalies.py", "w")
f.write(script)
f.close()

exec(script)

import convertpy2ipynb
convertpy2ipynb.convertpy2ipynb(pwd+"/"+results_dir+"/compare_2D_anomalies.py")