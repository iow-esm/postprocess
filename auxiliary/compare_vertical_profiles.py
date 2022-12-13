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

sys.path.append(pwd)
from config import variables

script = fr"""import sys
import os

# modify the working directory if necessary
pwd = "{pwd}"

# go to working directory and import global_settings
os.chdir(pwd)
sys.path.append('../')
import global_settings
variables = global_settings.variables


sys.path.append(pwd+"/../../auxiliary")
from helpers import find_other_models, get_n_colors, process_plot_config

os.chdir(pwd+"/{results_dir}")

import matplotlib.pyplot as plt
import numpy as np
import xarray as xr

# extend this dictionary if necessary
model_directories = {{"model1" : pwd+"/../seasonal_mean/{results_dir}"}}
# change the reference directory if nercessary
ref_dir = pwd+"/../process_reference/{results_dir}"

kinds = ["stations", "regions"]

for kind in kinds:

    for var in variables.keys():

        try:
            if variables[var]['dimension'] != 4:
                continue
        except:
            continue

        try:
            variables[var]['BED-reference-file-pattern']
            bed_ref = True
        except:
            bed_ref = False
        
        try:
            variables[var]['reference-file-pattern']
            ref = True
        except:
            ref = False

        seasons = variables[var]["seasons"]

        stations = variables[var][kind]
        if len(stations) == 0:
            continue

        fig, axs = plt.subplots(len(stations), len(seasons), figsize=(3*len(seasons), 4*len(stations)), sharex=True, sharey='row', squeeze=0)

        model_dirs = {{**model_directories, **find_other_models(variables[var], "seasonal_mean", {from_date}, {to_date})}}
        models = model_dirs.keys()

        RGB_tuples = get_n_colors(len(models))  

        for i, station in enumerate(stations):
            for j, season in enumerate(seasons.keys()):
                
                if bed_ref:
                    try:
                        ds = xr.open_dataset(ref_dir+"/"+var+"-"+station+"-"+season+".nc")
                        std = np.squeeze(ds[var+"_STD"].data)
                        np.squeeze(ds[var]).plot(y=ds[var].squeeze().dims[0], ax=axs[i,j], color="grey", linewidth=3, label = "BED", marker = "o")
                        
                        axs[i,j].fill_betweenx(ds[ds[var].squeeze().dims[0]].data, ds[var].squeeze().data - 2.0*std, ds[var].squeeze().data + 2.0*std, alpha=0.3, color="grey") 
                        ds.close()
                    except:
                        print("BED reference is configured but could not find or plot data.")

                if ref:
                    try:
                        ds = xr.open_dataset(model_dirs[model]+"/"+var+"-reference-"+station+"-"+season+".nc")
                        std = np.squeeze(ds[var+"_STD"].data)
                        np.squeeze(ds[var]).plot(y=ds[var].squeeze().dims[0], ax=axs[i,j], color="black", linewidth=3, label = "reference")

                        axs[i,j].fill_betweenx(ds[ds[var].squeeze().dims[0]].data, ds[var].squeeze().data - 2.0*std, ds[var].squeeze().data + 2.0*std, alpha=0.3, color="black")    
                        ds.close()
                    except:
                        print("Reference is configured but could not find or plot data.")                    

                for k, model in enumerate(models):
                    ds = xr.open_dataset(model_dirs[model]+"/"+var+"-"+station+"-"+season+".nc")

                    if len(models) > 2:
                        std = None
                    else:
                        std = np.squeeze(ds[var+"_STD"].data)

                    np.squeeze(ds[var]).plot(y=ds[var].squeeze().dims[0], ax=axs[i,j], color=RGB_tuples[k], linewidth=3, label = model)

                    if std is not None:
                        axs[i,j].fill_betweenx(ds[ds[var].squeeze().dims[0]].data, ds[var].squeeze().data - 2.0*std, ds[var].squeeze().data + 2.0*std, alpha=0.3, color=RGB_tuples[k])

                    ds.close()

                try:
                    plot_config = variables[var]["plot-config"]
                except:
                    plot_config = None

                data_plot_cfg, _, _ = process_plot_config(plot_config, ds[var])
                axs[i,j].set_xlim(data_plot_cfg["vmin"], data_plot_cfg["vmax"])
                
                if i == 0:
                    axs[i,j].set_title(season, fontweight="bold")
                else:
                    axs[i,j].set_title("") 

                if j == 0:
                    ylabel =  axs[i,j].get_ylabel()            
                    axs[i,j].set_ylabel(r"$\bf{{"+station.replace("_","\_")+"}}$"+"\n"+ylabel)
                else:
                    axs[i,j].set_ylabel("")

                if i == (len(stations) - 1):
                    axs[i,j].set_xlabel(var+" ["+ds[var].units+"]")

                axs[i,j].invert_yaxis()
                axs[i,j].grid(linestyle='--', alpha=0.6)

        axs[0,0].legend()
        fig.tight_layout()  
        plt.subplots_adjust(wspace=0, hspace=0)
        fig.savefig(var+"-"+kind+".png", dpi=100)
"""

f = open(pwd+"/"+results_dir+"/compare_vertical_profiles.py", "w")
f.write(script)
f.close()

exec(script)

import convertpy2ipynb
convertpy2ipynb.convertpy2ipynb(pwd+"/"+results_dir+"/compare_vertical_profiles.py")