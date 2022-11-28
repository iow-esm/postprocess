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
from helpers import TaylorDiagram, get_n_colors, find_other_models

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
    model_directories = {{"model1" : pwd+"/../extract_"+kind+"/{results_dir}"}}

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
                    axs[i,j].set_title(operator[1:], fontweight="bold")
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

        fig, axs = plt.subplots(1, 1, figsize=(1*len(operators)*len(models)+2, 1*len(data)+2))
        fig.patch.set_visible(False)
        axs.axis('off')
        axs.axis('tight')
        
        f = 1.0 / (len(data.keys())+2)

        table = axs.table(cellText=[['']*len(operators)],
                colLabels=operators,
                loc='center',
                bbox=[0, 1.0-2*f, 1.0, 2*f]
                )

        for (row, col), cell in table.get_celld().items():
            if (row == 0):
                cell.set_text_props(fontproperties=FontProperties(weight='bold'))

        from  matplotlib.colors import LinearSegmentedColormap
        c = ["darkgreen", "green", "limegreen", "greenyellow", "yellow", "orange", "orangered", "red", "darkred"]
        v = np.linspace(0, 1, num=9, endpoint=True)
        l = list(zip(v,c))
        colors = LinearSegmentedColormap.from_list('rg',l, N=256) 
        #colors = matplotlib.cm.get_cmap("RdYlGn_r")
        cell_colors = []
        cell_text = []
        for dat in data.keys():
            r = []
            c = []
            for operator in operators:
                tmp = {{**rms[dat][operator]}}
                tmp.pop("reference")
                mini = min(tmp, key=tmp.get)
                maxi = max(tmp, key=tmp.get)
                norm = plt.Normalize(0.0, 2.0)
                for model in models:
                    v = rms[dat][operator][model]
                    if v < 0.01 or v > 99.9:
                        fmt = "{{:.2e}}"
                    else:
                        fmt = "{{:.2f}}"

                    if model == mini:
                        r.append("*"+fmt.format(v))
                    elif model == maxi:
                        r.append("_"+fmt.format(v))
                    else:
                        r.append(fmt.format(v))
                    color = colors(norm(v), alpha=0.6)
                    c.append(color)
            cell_colors.append(c)
            cell_text.append(r)



        table = axs.table(cellText=cell_text,
                      rowLabels=list(data.keys()),
                      colLabels=len(operators)*models,
                      colColours=len(operators)*RGB_tuples,
                      cellColours = cell_colors,
                      loc='center',
                      bbox=[0.0, 0, 1.0, 1.0-f]
                      )

        for (row, col), cell in table.get_celld().items():
            #print(row, col, cell.get_text().get_text())
            if (row == 0):
                cell.set_text_props(fontproperties=FontProperties(weight='bold'))
            
            if (col == -1):
                cell.set_text_props(fontproperties=FontProperties(weight='bold'))

            text = cell.get_text().get_text()
            if text.startswith("_"):
                cell.get_text().set_text(text[1:])
                cell.set_text_props(fontproperties=FontProperties(style='italic'))

            if text.startswith("*"):
                cell.get_text().set_text(text[1:])
                cell.set_text_props(fontproperties=FontProperties(weight='bold'))         

        #table.set_fontsize(14)
        #table.scale(1.5, 1.5) 

        #img = axs.imshow([np.linspace(0.0, 2.0, num=10) for _ in range(10)], cmap=colors)
        #fig.colorbar(img, ax=axs, ticks = [0.0, 1.0, 2.0], orientation="horizontal", pad=0.01)
        #img.set_visible(False)

        table.auto_set_font_size(False)

        axs.set_title("Cost function (RMSE/$\sigma_{{ref}}$ [1]) for variable "+var, fontweight="bold")
        fig.tight_layout()  
        #plt.subplots_adjust(wspace=0, hspace=0)
        plt.subplots_adjust(top=0.9, bottom=0.05)

        fig.savefig(var+"-"+kind+"-table.png", dpi=100)

        plt.close()
        
"""

f = open(pwd+"/"+results_dir+"/create_taylor_diagrams.py", "w")
f.write(script)
f.close()

exec(script)

import convertpy2ipynb
convertpy2ipynb.convertpy2ipynb(pwd+"/"+results_dir+"/create_taylor_diagrams.py")