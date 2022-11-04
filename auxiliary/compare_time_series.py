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

# which kind of time series?
kinds = ["stations", "regions"]

for kind in kinds:

    # extend this dictionary if necessary
    model_dirs = {{"model1" : pwd+"/../extract_"+kind+"/{results_dir}"}}
    models = list(model_dirs.keys())
    ref_dir = pwd+"/../extract_"+kind+"/{results_dir}"

    for var in variables.keys():

        try:
            variables[var]['reference-file-pattern']
        except:
            continue

        operators = variables[var]["time-series-operators"]
        data = variables[var][kind]

        fig, axs = plt.subplots(len(data), len(operators), figsize=(4*len(operators), 4*len(data)), sharex='col', sharey='row', squeeze=0)

        for i, dat in enumerate(data):
            for j, operator in enumerate(operators):

                for model in model_dirs.keys():
                    ds = xr.open_dataset(model_dirs[model]+"/"+var+"-"+dat+operator+".nc")
                    axs[i,j].plot(ds["time"].data, np.squeeze(ds[var].data), label=model)

                    ds.close()

                ds = xr.open_dataset(ref_dir+"/"+var+"-reference-"+dat+operator+".nc")
                axs[i,j].plot(ds["time"].data, np.squeeze(ds[var].data), label="reference")                
                
                if i == 0:
                    axs[i,j].set_title(operator[1:], fontweight="bold")
                if j == 0:
                    axs[i,j].set_ylabel(var+" ["+ds[var].units+"]")
                if j == (len(operators) - 1):
                    axs[i,j].set_ylabel(dat, fontweight="bold")
                    axs[i,j].yaxis.set_label_position("right")
                if i == (len(data) - 1):
                    axs[i,j].set_xlabel("time")

                ds.close()

        axs[0,0].legend()
        fig.tight_layout()  
        plt.subplots_adjust(wspace=0, hspace=0)
        fig.savefig(var+".png", dpi=100)
"""

f = open(pwd+"/"+results_dir+"/compare_time_series.py", "w")
f.write(script)
f.close()

exec(script)

import convertpy2ipynb
convertpy2ipynb.convertpy2ipynb(pwd+"/"+results_dir+"/compare_time_series.py")