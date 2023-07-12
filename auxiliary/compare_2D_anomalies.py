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
try:
    this_model = global_settings.this_model
except:
    this_model = "model"
    
model_directories = {{this_model : pwd+"/../calculate_anomalies/{results_dir}"}}
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
    else:
        compare = False
    
    seasons = list(variables[var]["seasons"].keys())

    percentiles = [""]
    try:
       percentiles += variables[var]["percentiles"]
    except:
        pass

    for p in percentiles:    

        fig, axs = plt.subplots(len(models), len(seasons), figsize=(4*len(seasons), 4*len(models)+0.2), sharex='col', sharey='row', squeeze=0, gridspec_kw={{"width_ratios": (len(seasons)-1)*[1] + [1.25]}})

        for i, model in enumerate(models):

            for j, season in enumerate(seasons):
            
                if p == "":
                    nc_file = model_dirs[model]+"/"+var+"-"+season+".nc"
                else:
                    nc_file = model_dirs[model]+"/"+var+"-"+season+"-PCTL_"+p+".nc"
                
                ds = load_dataset(nc_file)
                ds_var = ds.data_vars[var]

                try:
                    plot_config = variables[var]["plot-config-anomaly"]
                except:
                    plot_config = None

                #if j == 0:
                data_plot_cfg, cbar_params, ctr_plot_cfg = process_plot_config(plot_config, ds_var)

                try:
                    units = ds_var.units
                except:
                    units = "a.u."               
                
                if j == len(seasons)-1:
                    cbar_pars = {{"add_colorbar" : True, **cbar_params}}
                    cbar_pars["cbar_kwargs"]["label"] = r'$\Delta$'+ds_var.name+" ["+units+"]"
                else:
                    cbar_pars = {{"add_colorbar" : False}}

                ds_var.plot(ax=axs[i,j], **cbar_pars, **data_plot_cfg)
                
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
                    axs[i,j].set_ylabel(r"$\bf{{"+model+"}}$"+"\n"+ylabel.replace("\n"," "))
                    axs[i,j].yaxis.label.set_color(RGB_tuples[i])
                    
                if i != len(models)-1:
                    axs[i,j].set_xlabel("")
                else:
                    xlabel = axs[i,j].get_xlabel()
                    axs[i,j].set_xlabel(xlabel.replace("\n"," "))                    

                axs[i,j].grid(linestyle='--', alpha=0.6)

                unload_dataset(ds)

        if p != "":
            fig.suptitle("Percentile: "+str(p), fontsize=16, fontweight='bold')

        fig.tight_layout()  
        
        if p != "":
            plt.subplots_adjust(wspace=0, hspace=0, top=1.0-0.15/len(models))
            fig.savefig(var+"-PCTL_"+str(p)+".png", dpi=100)
        else:
            plt.subplots_adjust(wspace=0, hspace=0)
            fig.savefig(var+".png", dpi=100)
        plt.close()

        if not compare:
            continue

        if p == "":
            other_model_directories = find_other_models(variables[var], "seasonal_mean", {from_date}, {to_date})  
        else:
            other_model_directories = find_other_models(variables[var], "seasonal_percentile", {from_date}, {to_date}) 

        other_models = list(other_model_directories.keys())
        
        n_comparisons = len(other_models)
        fig, axs = plt.subplots(n_comparisons, len(seasons), figsize=(4*len(seasons), 4*n_comparisons+0.2), sharex='col', sharey='row', squeeze=0, gridspec_kw={{"width_ratios": (len(seasons)-1)*[1] + [1.25]}})

        for model in model_directories.keys():
            for i, other_model in enumerate(other_models):
                for j, season in enumerate(seasons):
                    
                    if p == "":
                        model_file = model_directories[model]+"/../../../seasonal_mean/{results_dir}/"+var+"-"+season+".nc"
                        other_model_file = other_model_directories[other_model]+"/"+var+"-"+season+".nc"
                    else:
                        model_file = model_directories[model]+"/../../../seasonal_percentile/{results_dir}/"+var+"-"+season+"-PCTL_"+p+".nc"
                        other_model_file = other_model_directories[other_model]+"/"+var+"-"+season+"-PCTL_"+p+".nc"                       

                    remapped_file = "tmp-remapped.nc"
                    difference_file = "tmp-difference.nc"
                    cmd = "source ../../../../load_modules.sh; cdo remapbil,"+model_file+" "+other_model_file+" "+remapped_file+"; "
                    cmd += "cdo sub "+model_file+" "+remapped_file+" "+difference_file
                    os.system(cmd)

                    ds = load_dataset(difference_file)
                    ds_var = ds.data_vars[var]   

                    try:
                        plot_config =  variables[var]["plot-config-anomaly-inter-comparison"]
                    except:
                        try:
                            plot_config = variables[var]["plot-config-anomaly"]
                        except:
                            plot_config = None

                    #if j == 0:
                    data_plot_cfg, cbar_params, ctr_plot_cfg = process_plot_config(plot_config, ds_var)

                    try:
                        units = ds_var.units
                    except:
                        units = "a.u."               
                    
                    if j == len(seasons)-1:
                        cbar_pars = {{"add_colorbar" : True, **cbar_params}}
                        cbar_pars["cbar_kwargs"]["label"] = r'$\Delta$'+ds_var.name+" ["+units+"]"
                    else:
                        cbar_pars = {{"add_colorbar" : False}}

                    np.squeeze(ds_var).plot(ax=axs[i,j], **cbar_pars, **data_plot_cfg)
                    
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
                        axs[i,j].set_ylabel(r"$\bf{{"+model+"-"+other_model+"}}$"+"\n"+ylabel.replace("\n"," "))

                    if n_comparisons > 1:
                        axs[i,j].yaxis.label.set_color(RGB_tuples[i])                        
                        
                    if i != n_comparisons -1:
                        axs[i,j].set_xlabel("")
                    else:
                        xlabel = axs[i,j].get_xlabel()
                        axs[i,j].set_xlabel(xlabel.replace("\n"," "))                        

                    axs[i,j].grid(linestyle='--', alpha=0.6)     

                    unload_dataset(ds) 
                    cmd = "rm "+remapped_file+" "+difference_file
                    os.system(cmd)  

        title = "Model inter-comparison."
        if p != "":
            title += " Percentile: "+p
        
        fig.suptitle(title, fontsize=16, fontweight='bold')
        fig.tight_layout()  
        plt.subplots_adjust(wspace=0, hspace=0, top=1.0-0.15/n_comparisons)

        if p != "":
            fig.savefig(var+"-PCTL_"+str(p)+"-compare.png", dpi=100)
        else:
            fig.savefig(var+"-compare.png", dpi=100)                    

        plt.close()

        fig, axs = plt.subplots(n_comparisons, len(seasons), figsize=(4*len(seasons), 4*n_comparisons+0.2), sharex='col', sharey='row', squeeze=0, gridspec_kw={{"width_ratios": (len(seasons)-1)*[1] + [1.25]}})

        for model in model_directories.keys():
            for i, other_model in enumerate(other_models):
                for j, season in enumerate(seasons):
                
                    if p == "":
                        model_file = model_directories[model]+"/../../../seasonal_mean/{results_dir}/"+var+"-"+season+".nc"
                        other_model_file = other_model_directories[other_model]+"/"+var+"-"+season+".nc" 
                        model_std_file = model_file
                        other_model_std_file = other_model_file  
                    else:           
                        model_file = model_directories[model]+"/../../../seasonal_percentile/{results_dir}/"+var+"-"+season+"-PCTL_"+p+".nc"
                        other_model_file = other_model_directories[other_model]+"/"+var+"-"+season+"-PCTL_"+p+".nc"
                        model_std_file = model_directories[model]+"/../../../seasonal_mean/{results_dir}/"+var+"-"+season+".nc"
                        other_model_std_file = other_model_directories[other_model]+"/../../../seasonal_mean/{results_dir}/"+var+"-"+season+".nc"                              

                    remapped_file = "tmp-remapped.nc"
                    difference_file = "tmp-difference.nc"
                    cmd = "source ../../../../load_modules.sh; cdo remapbil,"+model_file+" "+other_model_file+" "+remapped_file+"; "
                    cmd += "cdo sub "+model_file+" "+remapped_file+" "+difference_file
                    os.system(cmd) 

                    cmd = "rm "+remapped_file
                    os.system(cmd)  
            
                    remapped_file = "tmp-remapped.nc"
                    common_file = "tmp-common.nc"
                    significance_file = "tmp-significance.nc"
                    cmd = "source ../../../../load_modules.sh; cdo remapbil,"+model_file+" "+other_model_std_file+" "+remapped_file+"; "
                    cmd += "cdo -selvar,"+var+"_STD"+" -mulc,0.5 -sqrt -add -sqr "+model_std_file+" -sqr "+remapped_file+" "+common_file+"; "
                    cmd += "cdo -div -selvar,"+var+" "+difference_file+" -selvar,"+var+"_STD "+common_file+" "+significance_file
                    os.system(cmd)

                    ds = load_dataset(significance_file)
                    ds_var = ds.data_vars[var]   

                    #if p == "":
                    #    contour = True
                    #else:
                    contour = False

                    plot_config = {{"color_map" : "seismic", "contour" : contour, "delta_value" : 0.1, "min_value" : -1.0, "max_value": 1.0}}

                    data_plot_cfg, cbar_params, ctr_plot_cfg = process_plot_config(plot_config, ds_var)

                    try:
                        units = ds_var.units
                    except:
                        units = "a.u."               
                    
                    if j == len(seasons)-1:
                        cbar_pars = {{"add_colorbar" : True, **cbar_params}}
                        cbar_pars["cbar_kwargs"]["label"] = r'$\Delta$'+ds_var.name+r'/$\bar\sigma$ [1]'
                    else:
                        cbar_pars = {{"add_colorbar" : False}}

                    np.squeeze(ds_var).plot(ax=axs[i,j], **cbar_pars, **data_plot_cfg)
                    
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
                        axs[i,j].set_ylabel(r"$\bf{{"+model+"-"+other_model+"}}$"+"\n"+ylabel.replace("\n"," "))

                    if n_comparisons > 1:
                        axs[i,j].yaxis.label.set_color(RGB_tuples[i])
                        
                    if i != n_comparisons-1:
                        axs[i,j].set_xlabel("")
                    else:
                        xlabel = axs[i,j].get_xlabel()
                        axs[i,j].set_xlabel(xlabel.replace("\n"," "))

                    axs[i,j].grid(linestyle='--', alpha=0.6)     

                    unload_dataset(ds)

                    #cmd = "cp "+common_file+" "+season+p+common_file
                    #os.system(cmd)

                    #cmd = "cp "+difference_file+" "+season+p+difference_file
                    #os.system(cmd)                    
                    
                    cmd = "rm "+remapped_file+" "+difference_file+" "+common_file+" "+significance_file
                    os.system(cmd)  

        title = "Anomaly signal-to-noise ratio."
        if p != "":
            title += " Percentile: "+p
        
        fig.suptitle(title, fontsize=16, fontweight='bold')
        fig.tight_layout()  
        plt.subplots_adjust(wspace=0, hspace=0, top=1.0-0.15/n_comparisons)

        if p != "":
            fig.savefig(var+"-PCTL_"+str(p)+"-significance.png", dpi=100)
        else:
            fig.savefig(var+"-significance.png", dpi=100)    
  

        plt.close()    
"""

f = open(pwd+"/"+results_dir+"/compare_2D_anomalies.py", "w")
f.write(script)
f.close()

exec(script)

import convertpy2ipynb
convertpy2ipynb.convertpy2ipynb(pwd+"/"+results_dir+"/compare_2D_anomalies.py")