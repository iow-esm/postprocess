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

os.chdir(pwd+"/{results_dir}")

import matplotlib.pyplot as plt
import numpy as np
import xarray as xr

def get_month_names(numbers):
    month_names = {{ 1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun", 7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"}}

    names = []
    for n in numbers:
        names.append(month_names[n])
    
    return np.array(names)

def process_time_axis(time, operator):
    years = time.astype('datetime64[Y]').astype(int) + 1970
    months = time.astype('datetime64[M]').astype(int) % 12 + 1
    days = time - time.astype('datetime64[M]') + 1

    if operator == "-ymonmean":
        t = get_month_names(months)
    else:
        t = time

    return t

# which kind of time series?
kinds = ["stations", "regions"]

for kind in kinds:

    # extend this dictionary if necessary
    model_dirs = {{"model1" : pwd+"/../extract_"+kind+"/{results_dir}"}}
    models = list(model_dirs.keys())

    for var in variables.keys():

        try:
            if variables[var]["dimension"] > 3:
                continue
        except:
            pass

        operators = variables[var]["time-series-operators"]
        data = variables[var][kind]

        fig, axs = plt.subplots(len(data), len(operators), figsize=(5*len(operators), 2*len(data)), sharex='col', sharey='row', squeeze=0)

        for i, dat in enumerate(data):
            ax2 = []
            for j, operator in enumerate(operators):

                for model in model_dirs.keys():
                    ds = xr.open_dataset(model_dirs[model]+"/"+var+"-"+dat+operator+".nc")
                    d = np.squeeze(ds[var].data)
                    t = process_time_axis(ds["time"].data, operator)
                    p = axs[i,j].plot(t, d, label=model)
                    try:
                        std = np.squeeze(ds[var+"_STD"].data)
                        axs[i,j].fill_between(t, d - 0.5*std, d + 0.5*std, color=p[-1].get_color(), alpha=0.3)
                    except:
                        print("Could not plot standard deviation for variable "+var)


                if i == 0:
                    axs[i,j].set_title(operator[1:], fontweight="bold")
                if j == 0:
                    axs[i,j].set_ylabel(r"$\\bf{{"+dat.replace("_","\_")+"}}$"+"\\n"+var+" ["+ds[var].units+"]")
                if i == (len(data) - 1):
                    axs[i,j].set_xlabel("time")

                ds.close()

                axs[i,j].grid(linestyle='--', alpha=0.6)

                try:
                    variables[var]['reference-file-pattern']
                except:
                    continue
            
                try:
                    ref_dir = pwd+"/../extract_"+kind+"/{results_dir}"
                    ds = xr.open_dataset(ref_dir+"/"+var+"-reference-"+dat+operator+".nc")
                    d = np.squeeze(ds[var].data)
                    t = process_time_axis(ds["time"].data, operator)
                    p = axs[i,j].plot(t, d, label="reference", color="grey", linewidth=3, zorder=0) 
                    try:
                        std = np.squeeze(ds[var+"_STD"].data)
                        axs[i,j].fill_between(t, d - 0.5*std, d + 0.5*std, color=p[-1].get_color(), alpha=0.3)
                    except:
                        print("Could not plot standard deviation for variable "+var)
                    ds.close()
                except:
                    print("Could not plot reference for variable "+var)

                try:
                    diff_dir = pwd+"/../calculate_anomalies/{results_dir}"
                    ds = xr.open_dataset(diff_dir+"/"+var+"-"+dat+operator+".nc")
                    d = np.squeeze(ds[var].data)
                    t = process_time_axis(ds["time"].data, operator)
                    ax2.append(axs[i,j].twinx())
                    ax2[-1].plot(t, d, label="anomaly", color="red", linestyle="--", linewidth=1, alpha=0.6)
                    ds.close()
                except:
                    print("Could not plot anomaly for variable "+var)

            if len(ax2) > 0:
                ax2[-1].set_ylabel(r'$\Delta$'+var+" ["+ds[var].units+"]")
                ax2[0].get_shared_y_axes().join(*ax2)
                if i == 0:
                    ax2[-1].legend()
                for a in ax2:
                    a.grid(linestyle='--', alpha=0.3, color="red")
                    
            if len(ax2) > 1:
                for a in ax2[:-1]:
                    a.set_yticklabels([])

        axs[0,0].legend()
        fig.tight_layout()  
        plt.subplots_adjust(wspace=0, hspace=0)
        fig.savefig(var+"-"+kind+".png", dpi=100)
"""

f = open(pwd+"/"+results_dir+"/compare_time_series.py", "w")
f.write(script)
f.close()

exec(script)

import convertpy2ipynb
convertpy2ipynb.convertpy2ipynb(pwd+"/"+results_dir+"/compare_time_series.py")