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
model_dirs = {{"model1" : pwd+"/../seasonal_mean/{results_dir}"}}
# change the reference directory if nercessary
ref_dir = pwd+"/../process_reference/{results_dir}"

for var in variables.keys():

    try:
        variables[var]['BED-reference-file-pattern']
    except:
        continue

    seasons = variables[var]["seasons"]
    stations = variables[var]["stations"]

    fig, axs = plt.subplots(len(stations), len(seasons), figsize=(3*len(seasons), 5*len(stations)), sharex=True, sharey='row', squeeze=0)

    for i, station in enumerate(stations):
        for j, season in enumerate(seasons.keys()):
            
            ds = xr.open_dataset(ref_dir+"/"+var+"-"+station+"-"+season+".nc")
            plot_vertical_profile.plot_vertical_profile(axs[i,j], ds[var].data, ds.depth.data, ds[var+"_STD"].data, smooth=True, label = "reference", color="grey")

            for model in model_dirs.keys():
                ds = xr.open_dataset(model_dirs[model]+"/"+var+"-"+station+"-"+season+".nc")
                plot_vertical_profile.plot_vertical_profile(axs[i,j], np.squeeze(ds[var].data), ds[variables[var]["plot-config"].vert_name].data, np.squeeze(ds[var+"_STD"].data), label = model)

            axs[i,j].set_xlim([variables[var]["plot-config"].min_value, variables[var]["plot-config"].max_value])
            
            if i == 0:
                axs[i,j].set_title(season, fontweight="bold")
            if j == 0:
                axs[i,j].set_ylabel(variables[var]["plot-config"].vert_name+" ["+ds[variables[var]["plot-config"].vert_name].units+"]")
            if j == (len(seasons) - 1):
                axs[i,j].set_ylabel(station, fontweight="bold")
                axs[i,j].yaxis.set_label_position("right")
            if i == (len(stations) - 1):
                axs[i,j].set_xlabel(var+" ["+ds[var].units+"]")

    axs[0,0].legend()
    fig.tight_layout()  
    plt.subplots_adjust(wspace=0, hspace=0)
    fig.savefig(var+".png", dpi=100)
"""

f = open(pwd+"/"+results_dir+"/compare_vertical_profiles.py", "w")
f.write(script)
f.close()

exec(script)

import convertpy2ipynb
convertpy2ipynb.convertpy2ipynb(pwd+"/"+results_dir+"/compare_vertical_profiles.py")