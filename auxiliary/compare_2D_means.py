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

script = fr"""import sys
import os

# modify the working directory if necessary
pwd = "{pwd}"

# go to working directory and import global_settings
os.chdir(pwd)
sys.path.append('../')
import global_settings
variables = global_settings.variables

sys.path.append('../../auxiliary')
from helpers import plot_coast, load_dataset, unload_dataset, find_other_models, get_n_colors, process_plot_config

os.chdir(pwd+"/{results_dir}")

import matplotlib.pyplot as plt
import numpy as np
import xarray as xr

# extend this dictionary if necessary

model_directories = {{"model1" : pwd+"/../seasonal_mean/{results_dir}"}}

for var in variables.keys():

    try:
        if variables[var]["dimension"] != 3:
            continue
    except:
        pass

    model_dirs = {{**model_directories, **find_other_models(variables[var], "seasonal_mean", {from_date}, {to_date})}}

    try:
        variables[var]['reference-file-pattern']
        model_dirs["reference"] = pwd+"/../seasonal_mean/{results_dir}"
    except:
        try:
            del model_dirs["reference"]
        except:
            pass

    models = list(model_dirs.keys())

    RGB_tuples = get_n_colors(len(models))   

    seasons = list(variables[var]["seasons"].keys())

    fig, axs = plt.subplots(len(models), len(seasons), figsize=(4*len(seasons), 4*len(models)), sharex='col', sharey='row', squeeze=0, gridspec_kw={{"width_ratios": (len(seasons)-1)*[1] + [1.25]}})

    for i, model in enumerate(models):

        for j, season in enumerate(seasons):

            if model == "reference":
                nc_file = model_dirs[model]+"/"+var+"-reference-"+season+"-remapped.nc"
                color = "black"
            else:
                nc_file = model_dirs[model]+"/"+var+"-"+season+".nc"
                color = RGB_tuples[i]
                
            ds = load_dataset(nc_file)

            ds_var = ds.data_vars[var]
            
            try:
                plot_config = variables[var]["plot-config"]
            except:
                plot_config = None

            data_plot_cfg, cbar_params, ctr_plot_cfg = process_plot_config(plot_config, ds_var)
             
            if j == len(seasons)-1:
                cbar_params = {{"add_colorbar" : True, **cbar_params}}
            else:
                cbar_params = {{"add_colorbar" : False}}                

            plot_coast(axs[i,j])

            ds_var.plot(ax=axs[i,j], **cbar_params, **data_plot_cfg)
            
            if ctr_plot_cfg != {{}}:
                np.squeeze(ds_var).plot.contour(ax=axs[i,j], **ctr_plot_cfg)

            if i == 0:
                axs[i,j].set_title(season, fontweight='bold')
            else:
                axs[i,j].set_title("")

            if j != 0:
                axs[i,j].set_ylabel("")
            else:
                ylabel = axs[i,j].get_ylabel()
                axs[i,j].set_ylabel(r"$\bf{{"+model+"}}$"+"\n"+ylabel)
                axs[i,j].yaxis.label.set_color(color)
                
            if i != len(models)-1:
                axs[i,j].set_xlabel("")

            axs[i,j].grid(linestyle='--', alpha=0.6)

            unload_dataset(ds)

    fig.tight_layout()  
    plt.subplots_adjust(wspace=0, hspace=0)
    fig.savefig(var+".png", dpi=100)


"""

f = open(pwd+"/"+results_dir+"/compare_2D_means.py", "w")
f.write(script)
f.close()

exec(script)

import convertpy2ipynb
convertpy2ipynb.convertpy2ipynb(pwd+"/"+results_dir+"/compare_2D_means.py")