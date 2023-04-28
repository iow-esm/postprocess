import sys

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
from helpers import get_month_names,  get_n_colors, find_other_models, better_operator_name

os.chdir(pwd+"/{results_dir}")

import matplotlib.pyplot as plt
import numpy as np
import xarray as xr

import scipy.stats as st

# which kind of time series?
kinds = ["stations", "regions"]

for kind in kinds:

    # extend this dictionary if necessary

    try:
        this_model = global_settings.this_model
    except:
        this_model = "model"
        
    model_directories = {{this_model : pwd+"/../extract_"+kind+"/{results_dir}"}}

    for var in variables.keys():

        try:
            if variables[var]["dimension"] > 3:
                continue
        except:
            pass

        operators = variables[var]["time-series-operators"]
        if len(operators) == 0:
            continue

        data = variables[var][kind]
        if len(data) == 0:
            continue

        model_dirs = {{**model_directories, **find_other_models(variables[var], "extract_"+kind, {from_date}, {to_date})}}
        models = list(model_dirs.keys())

        RGB_tuples = get_n_colors(len(models))         

        fig, axs = plt.subplots(len(data), len(operators), figsize=(5*len(operators), 3*len(data)), sharex='col', sharey='row', squeeze=0)

        for i, dat in enumerate(data):

            ax2 = []
            for j, operator in enumerate(operators):

                for k, model in enumerate(models):
                    ds = xr.open_dataset(model_dirs[model]+"/"+var+"-"+dat+operator+".nc")
                    d = np.squeeze(ds[var].data)
                    mean = np.mean(d)
                    axs[i,j].axvline(x = mean, color=RGB_tuples[k], zorder=len(models)-k, linestyle="--")

                    nbins = 10
                    hist, bin_edges = np.histogram(d, bins = 10, density=True)

                    if len(models) < 3:
                        axs[i,j].bar(0.5*(bin_edges[:-1]+bin_edges[1:]), hist/max(hist), width=bin_edges[1:]-bin_edges[:-1], color=RGB_tuples[k], zorder=len(models)-k, alpha=0.3)

                    if len(hist) > 5:
                        from scipy.signal import savgol_filter
                        yhat = savgol_filter(hist/max(hist), 7, 3)
                        axs[i,j].plot(0.5*(bin_edges[:-1]+bin_edges[1:]), yhat, color=RGB_tuples[k], label=model, zorder=len(models)-k, linewidth=3)

                if i == 0:
                    axs[i,j].set_title(better_operator_name(operator[1:]), fontweight="bold")
                if j == 0:
                    axs[i,j].set_ylabel(r"$\bf{{"+dat.replace("_","\_")+"}}$"+"\n"+"norm. density [1]")
                if i == (len(data) - 1):
                    axs[i,j].set_xlabel(var+" ["+ds[var].units+"]")
                
                axs[i,j].grid(linestyle='-', alpha=0.6)

                try:
                    variables[var]['reference-file-pattern']
                except:
                    continue
            
                ref_dir = pwd+"/../extract_"+kind+"/{results_dir}"
                dsr = xr.open_dataset(ref_dir+"/"+var+"-reference-"+dat+operator+".nc")
                dr = np.squeeze(dsr[var].data)

                mean = np.mean(dr)
                axs[i,j].axvline(x = mean,  color="grey", zorder=0, linestyle="--")

                nbins = 10
                hist, bin_edges = np.histogram(dr, bins=nbins, density=True)
                axs[i,j].bar(0.5*(bin_edges[:-1]+bin_edges[1:]), hist/max(hist), width=bin_edges[1:]-bin_edges[:-1], color="grey", zorder=0, alpha=0.4)

                if len(hist) > 5:
                    from scipy.signal import savgol_filter
                    yhat = savgol_filter(hist/max(hist), 7, 3)
                    axs[i,j].plot(0.5*(bin_edges[:-1]+bin_edges[1:]), yhat, label="reference", color="grey", zorder=0, linewidth=5)
                
                dsr.close()

        axs[0,0].legend()
        fig.tight_layout()  
        plt.subplots_adjust(wspace=0, hspace=0)
        fig.savefig(var+"-"+kind+".png", dpi=100)
        plt.close()
"""

f = open(pwd+"/"+results_dir+"/compare_time_series.py", "w")
f.write(script)
f.close()

exec(script)

import convertpy2ipynb
convertpy2ipynb.convertpy2ipynb(pwd+"/"+results_dir+"/compare_time_series.py")