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

sys.path.append('../../auxiliary')
from helpers import TaylorDiagram, get_n_colors, find_other_models, better_operator_name

sys.path.append('../')
import global_settings
variables = global_settings.variables

os.chdir(pwd+"/{results_dir}")

import matplotlib.pyplot as plt
import numpy as np
import xarray as xr

import matplotlib
from matplotlib.font_manager import FontProperties
  
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

        try:
            variables[var]["reference-file-pattern"]
        except:
            continue

        model_dirs = {{**model_directories, **find_other_models(variables[var], "extract_"+kind, {from_date}, {to_date})}}
        models = list(model_dirs.keys())

        RGB_tuples = get_n_colors(len(models))           

        operators = variables[var]["time-series-operators"]
        data = variables[var][kind]

        fig, axs = plt.subplots(len(data), len(operators), figsize=(3*len(operators), 3*len(data)), subplot_kw={{'projection': 'polar'}}, squeeze=0)

        rms = {{}}

        for i, dat in enumerate(data.keys()):
            rms[dat] = {{}}
            for j, operator in enumerate(operators):
                rms[dat][operator] = {{}}
                ref_dir = pwd+"/../extract_"+kind+"/{results_dir}"
                ds = xr.open_dataset(ref_dir+"/"+var+"-reference-"+dat+operator+".nc")
                d = np.squeeze(ds[var].data)
                units = ds[var].units
                ds.close()

                diagram = TaylorDiagram(d, axs[i,j])

                for k, model in enumerate(model_dirs.keys()):
                    ds = xr.open_dataset(model_dirs[model]+"/"+var+"-"+dat+operator+".nc")
                    dm = np.squeeze(ds[var].data)
                    ds.close()
                    
                    # Add the models to Taylor diagram
                    diagram.add_sample(dm, marker='*', ms=10, ls='', color=RGB_tuples[k], label=model)

                std, _, rms[dat][operator] = diagram.get_samples()
                for k, model in enumerate(model_dirs.keys()):
                    rms[dat][operator][model] /= std["reference"] # measure rms in standard deviation of ref

                diagram.finalize()

                if i == 0:
                    axs[i,j].set_title(better_operator_name(operator[1:]), fontweight="bold")
                if j == 0:
                    axs[i,j].set_ylabel(r"$\bf{{"+dat.replace("_","\_")+"}}$")
                if i == (len(data) - 1):
                    axs[i,j].set_xlabel("St. dev.: "+var+" ["+units+"]")
                else:
                    axs[i,j].set_xlabel("")

        axs[0,0].legend(loc="upper left")
        fig.tight_layout()  
        #plt.subplots_adjust(wspace=0, hspace=0)
        plt.subplots_adjust(top=0.95, bottom=0.05)
        fig.savefig(var+"-"+kind+".png", dpi=100)

        plt.close()
"""

f = open(pwd+"/"+results_dir+"/create_taylor_diagrams.py", "w")
f.write(script)
f.close()

exec(script)

import convertpy2ipynb
convertpy2ipynb.convertpy2ipynb(pwd+"/"+results_dir+"/create_taylor_diagrams.py")