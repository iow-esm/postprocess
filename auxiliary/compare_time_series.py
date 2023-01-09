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
from helpers import get_month_names, process_time_axis,  get_n_colors, find_other_models, better_operator_name

os.chdir(pwd+"/{results_dir}")

import matplotlib.pyplot as plt
import numpy as np
import xarray as xr

# which kind of time series?
kinds = ["stations", "regions"]

markers = ["o", "s", "p", "^", "v", "D"]

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
                    t = process_time_axis(ds["time"].data, operator)
                    if len(t) < 15:
                        marker=markers[k%len(markers)]
                    elif len(t) < 100:
                        marker=None
                    else:
                        try:
                            ref_dir = pwd+"/../extract_"+kind+"/{results_dir}"
                            dsr = xr.open_dataset(ref_dir+"/"+var+"-reference-"+dat+operator+".nc")
                            dr = np.squeeze(dsr[var].data)
                            dsr.close()
                            p = axs[i,j].scatter(dr, d, label=model, marker=markers[k%len(markers)], facecolors='none', edgecolors=RGB_tuples[k], zorder=len(models)-k, alpha=0.6)
                            scatter = True
                            continue
                        except:
                            marker=None

                    scatter = False

                    p = axs[i,j].plot(t, d, color=RGB_tuples[k], label=model, linewidth=3, marker=marker, zorder=len(models)-k)

                    if len(models) < 3:
                        try:
                            std = np.squeeze(ds[var+"_STD"].data)
                            axs[i,j].fill_between(t, d - 2.0*std, d + 2.0*std, color=p[-1].get_color(), alpha=0.2)
                        except:
                            print("Could not plot standard deviation for variable "+var)

                if i == 0:
                    axs[i,j].set_title(better_operator_name(operator[1:]), fontweight="bold")
                if j == 0:
                    axs[i,j].set_ylabel(r"$\bf{{"+dat.replace("_","\_")+"}}$"+"\n"+var+" ["+ds[var].units+"]")
                if i == (len(data) - 1):
                    if not scatter:
                        axs[i,j].set_xlabel("time")
                    else:
                        axs[i,j].set_xlabel(var+" ["+ds[var].units+"]")
                

                axs[i,j].grid(linestyle='-', alpha=0.6)

                try:
                    variables[var]['reference-file-pattern']
                except:
                    continue

                if scatter:
                    xlim = axs[i,j].get_xlim()
                    p = axs[i,j].plot([xlim[0]+0.1*np.abs(xlim[1]-xlim[0]), xlim[1]-0.1*np.abs(xlim[1]-xlim[0])], [xlim[0]+0.1*np.abs(xlim[1]-xlim[0]), xlim[1]-0.1*np.abs(xlim[1]-xlim[0])], color="grey", linewidth=2, linestyle="--", zorder=0, label="reference")
                    continue
            
                try:
                    ref_dir = pwd+"/../extract_"+kind+"/{results_dir}"
                    ds = xr.open_dataset(ref_dir+"/"+var+"-reference-"+dat+operator+".nc")
                    d = np.squeeze(ds[var].data)
                    t = process_time_axis(ds["time"].data, operator)
                    if len(t) < 15:
                        marker="o"
                    else:
                        marker=None
                    p = axs[i,j].plot(t, d, label="reference", color="grey", linewidth=4, zorder=0, marker=marker) 
                    try:
                        std = np.squeeze(ds[var+"_STD"].data)
                        axs[i,j].fill_between(t, d - 2.0*std, d + 2.0*std, color=p[-1].get_color(), alpha=0.3, zorder=0)
                    except:
                        print("Could not plot standard deviation for variable "+var)
                    ds.close()
                except:
                    print("Could not plot reference for variable "+var)

                try:
                    ax2.append(axs[i,j].twinx())

                    if len(ax2) > 1:
                        ax2[-1].get_shared_y_axes().join(*ax2)

                    for k, model in enumerate(model_dirs.keys()):
                        diff_dir = model_dirs[model].replace("extract_"+kind, "calculate_anomalies")
                        ds = xr.open_dataset(diff_dir+"/"+var+"-"+dat+operator+".nc")
                        d = np.squeeze(ds[var].data)
                        t = process_time_axis(ds["time"].data, operator)
                        ax2[-1].plot(t, d, label="anomaly #"+str(k+1), color=RGB_tuples[k], linestyle="--", linewidth=2, alpha=0.6)
                        ds.close()
                except:
                    print("Could not plot anomaly for variable "+var)

            if len(ax2) > 0:
                ax2[-1].set_ylabel(r'$\Delta$'+var+" ["+ds[var].units+"]")
                ax2[-1].yaxis.label.set_color('darkred')
                
                if i == 0:
                    ax2[-1].legend()
                
                for a in ax2:
                    a.grid(linestyle='--', alpha=0.3, color="darkred")
                    a.tick_params(axis='y', colors='darkred')

            if len(ax2) > 1:
                for a in ax2[:-1]:
                    a.set_yticklabels([])

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