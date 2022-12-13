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
from helpers import plot_coast, load_dataset, unload_dataset, get_n_colors, find_other_models, process_plot_config

os.chdir(pwd+"/{results_dir}")

import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
import math
from matplotlib.patches import Ellipse, Circle

# extend this dictionary if necessary
model_directories = {{"model1" : pwd+"/../calculate_anomalies/{results_dir}"}}
# change the reference directory if nercessary
ref_dir = pwd+"/../process_reference/{results_dir}"


for var in variables.keys():

    try:
        variables[var]['reference-file-pattern']
    except:
        continue

    try:
        if variables[var]["dimension"] != 3:
            continue
    except:
        pass    

    model_dirs = {{**model_directories, **find_other_models(variables[var], "calculate_anomalies", {from_date}, {to_date})}}

    models = list(model_dirs.keys())
    RGB_tuples = get_n_colors(len(models))
    
    if len(models) > 1:
        compare = True
        nerrors = {{}}
        perrors = {{}}
        nstds = {{}}
        pstds = {{}}
    else:
        compare = False
    
    seasons = list(variables[var]["seasons"].keys())

    fig, axs = plt.subplots(len(models), len(seasons), figsize=(4*len(seasons), 4*len(models)), sharex='col', sharey='row', squeeze=0, gridspec_kw={{"width_ratios": (len(seasons)-1)*[1] + [1.25]}})

    for i, model in enumerate(models):

        if compare:
            perrors[model] = []
            nerrors[model] = []
            pstds[model] = []
            nstds[model] = []

        for j, season in enumerate(seasons):
            
            ds = load_dataset(model_dirs[model]+"/"+var+"-"+season+".nc")
            ds_var = ds.data_vars[var]

            try:
                plot_config = variables[var]["plot-config-anomaly"]
            except:
                plot_config = None

            data_plot_cfg, cbar_params, ctr_plot_cfg = process_plot_config(plot_config, ds_var)
             
            if j == len(seasons)-1:
                cbar_params = {{"add_colorbar" : True, **cbar_params}}
                cbar_params["cbar_kwargs"]["label"] = r'$\Delta$'+ds_var.name+" ["+units+"]"
            else:
                cbar_params = {{"add_colorbar" : False}}

            try:
                units = ds_var.units
            except:
                units = "a.u."       

            ds_var.plot(ax=axs[i,j], **cbar_params, **data_plot_cfg)
            
            if ctr_plot_cfg != {{}}:
                np.squeeze(ds_var).plot.contour(ax=axs[i,j], **ctr_plot_cfg)

            plot_coast(axs[i,j])
            
            if i == 0:
                axs[i,j].set_title(season, fontweight='bold')
            else:
                axs[i,j].set_title("")

            if j != 0:
                axs[i,j].set_ylabel("")
            else:
                ylabel = axs[i,j].get_ylabel()
                axs[i,j].set_ylabel(r"$\bf{{"+model+"}}$"+"\n"+ylabel)
                axs[i,j].yaxis.label.set_color(RGB_tuples[i])
                
            if i != len(models)-1:
                axs[i,j].set_xlabel("")

            axs[i,j].grid(linestyle='--', alpha=0.6)

            if compare:
                dummy = ds_var.values
                dummy = dummy[~np.isnan(dummy)]
                dummy = dummy[(dummy>=0.0)]
                dummy = np.absolute(dummy)
                if dummy.size == 0:
                    mean = 0.0
                    std = 0.0
                else:
                    mean = np.nanmean(dummy)
                    std = np.nanstd(dummy)                
                perrors[model].append(mean)
                pstds[model].append(std)
                dummy = ds_var.values
                dummy = dummy[~np.isnan(dummy)]
                dummy = dummy[dummy<0.0]
                dummy = np.absolute(dummy)
                if dummy.size == 0:
                    mean = 0.0
                    std = 0.0
                else:
                    mean = np.nanmean(dummy)
                    std = np.nanstd(dummy)
                nerrors[model].append(mean)              
                nstds[model].append(std)
                #nerrors[model].append(np.nanmean(ds_var.values, where=(ds_var.values<0.0)))
                #nstds[model].append(np.nanstd(ds_var.values, where=(ds_var.values<0.0)))                

            unload_dataset(ds)

    fig.tight_layout()  
    plt.subplots_adjust(wspace=0, hspace=0)
    fig.savefig(var+".png", dpi=100)
    plt.close()

    if not compare:
        continue
        
    fig, axs = plt.subplots(1, len(seasons), figsize=(3*len(seasons), 3), squeeze=0, sharey=True)
    
    rmax = 0.0

    for model in models:
        for j, season in enumerate(seasons):
            #print(var, model, season, nerrors[model][j], perrors[model][j], max, rmax)
            max = np.sqrt(nerrors[model][j]**2 + perrors[model][j]**2)
            if max > rmax:
                rmax = max
    
    for j, season in enumerate(seasons):
        axs[0,j].plot(0, 0, color="black", ms=10, marker="o", ls="")
        for i, model in enumerate(models):
            x = perrors[model][j]
            y = -nerrors[model][j]
            a = pstds[model][j]
            b = nstds[model][j]
            r = np.sqrt(x**2 + y**2)
            axs[0,j].add_artist(Ellipse((x, y), a, b, fc = RGB_tuples[i], alpha=0.2)) 
            axs[0,j].add_artist(Circle((0, 0), r, fill=False, color=RGB_tuples[i], linestyle="--", linewidth=2)) 
            axs[0,j].plot(x, y, color=RGB_tuples[i], label=model, ms=10, marker="o", ls="")
            
        axs[0,j].plot([0.0, np.sqrt(2)*1.1*rmax], [0.0, -np.sqrt(2)*1.1*rmax], linestyle="--", linewidth=0.5, color="grey", alpha=0.6)
    
        axs[0,j].set_ylim([-1.1*rmax, 0.0])
        for k in axs[0,j].get_yticks():
            axs[0,j].add_artist(Circle((0, 0), -k, fill=False, color="grey", linestyle="--", linewidth=0.5, alpha=0.6))
        axs[0,j].set_xlim([0.0, 1.1*rmax])
        axs[0,j].set_aspect(1.0)

        axs[0,j].set_xlabel(r'<|$\Delta$'+var+">0|> ["+units+"]")

        axs[0,j].set_title(season, fontweight="bold")


    axs[0,0].set_ylabel(r'<|$\Delta$'+var+"<0|> ["+units+"]")
    axs[0,0].legend()
            
    fig.tight_layout()  
    plt.subplots_adjust(top=0.95, wspace=0, hspace=0)
    fig.savefig(var+"_mean_errors.png", dpi=100)
    plt.close()
"""

f = open(pwd+"/"+results_dir+"/compare_2D_anomalies.py", "w")
f.write(script)
f.close()

exec(script)

import convertpy2ipynb
convertpy2ipynb.convertpy2ipynb(pwd+"/"+results_dir+"/compare_2D_anomalies.py")