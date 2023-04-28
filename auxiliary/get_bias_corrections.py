#!/usr/bin/env python
# coding: utf-8

import glob
import os
import sys
import xarray as xr
import numpy as np


# decode the input arguments
#out_dir = "/silod8/karsten/work/IOW_ESM_3nm_ERA5/output/era5_reference_run_monthly/MOM5_Baltic"
out_dir = "/silod8/karsten/work/IOW_ESM_3nm_ERA5_bias_correction/output/coupled-MOM5_Baltic_3nm-CCLM_Eurocordex_0.22deg_ERA5_bias_correction_monthly/MOM5_Baltic"
from_date = 19600101
to_date = 19881231
#to_date = 20191231
pwd = "/silod8/karsten/work/IOW_ESM_3nm_ERA5/postprocess/MOM5/get_bias_corrections"

os.chdir(pwd)

# import the local config 
sys.path.append(pwd)
import config
variables = config.variables

# get directories from where we extract
import get_all_dirs_from_to
dirs = get_all_dirs_from_to.get_all_dirs_from_to(out_dir, from_date, to_date)

# construct proper result directory
import create_results_dir
results_dir = create_results_dir.create_results_dir(out_dir, from_date, to_date)

from helpers import convert_to_decimal

def prepare_variable(var):
    
    cat_file = results_dir + "/" + var + ".nc"
    if glob.glob(cat_file) != []:
        return True
    
    try:
        variables[var]["reference-file-pattern"]
    except:
        return False

    seasons = variables[var]["seasons"]

    if len(seasons.keys()) == 0:
        return False    
    
    try:
        files = glob.glob(variables[var]["path"] + "/" + variables[var]["file"])
    except:
        try:
            files = glob.glob("../" + variables[var]["task"] + "/" + results_dir + "/" + variables[var]["file"])
        except:
            files = [dir + "/" + var + ".nc" for dir in dirs]

    if files == []:
        print("No netcdf files found for variable "+var)
        return False

    #cat_file = results_dir + "/" + var + ".nc"
    if len(files) > 1:       
        files = " ".join(files)
        #print("cdo  -cat \'" + files + "\' " + cat_file)
        os.system("module load cdo; cdo  -cat \'" + files + "\' " + cat_file)
    else:
        os.system("cp "+files[0]+" "+cat_file)

    return True
    
def calculate_anommaly(var):
    cat_file = results_dir + "/" + var + ".nc"
    reference_file = "../process_reference/"+results_dir+"/"+var+"-remapped.nc"
    command = "module load cdo; cdo -sub "+cat_file+" "+reference_file+" "+results_dir+"/"+var+"-anomaly.nc; "
    os.system(command)
    
def remap(var, map_var):
    cat_file = results_dir + "/" + var + "-anomaly.nc"
    map_file = results_dir + "/" + map_var + "-anomaly.nc"
    command = "module load cdo; cdo -remapbil,"+map_file+" "+cat_file+" "+results_dir+"/tmp.nc; mv "+results_dir+"/tmp.nc "+cat_file
    os.system(command)


# go over all variables from where we extract (as defined in the local config)
seasons = {}
valid_variables = []
for var in variables.keys():

    if not prepare_variable(var):
        continue

    valid_variables.append(var)

    for season in variables[var]["seasons"].keys():
        if season not in seasons.keys():
            seasons[season] = variables[var]["seasons"][season]
            
print(valid_variables)
print(seasons)

N = len(valid_variables) 
    
for var in valid_variables:
    
    calculate_anommaly(var)
    
    if var != valid_variables[0]:
        remap(var, valid_variables[0])
    
    anomaly_file = results_dir+"/"+var+"-anomaly.nc"
    
    for season in seasons.keys():
        
        seasonal_anomaly_file = results_dir+"/"+var+"-anomaly-"+season+".nc"
        
        if seasons[season] == "":
            os.system("cp "+anomaly_file+" "+seasonal_anomaly_file)
            continue
        
        selmon = " -selmon,"+seasons[season]
        
        #command = "cdo -sqrt -timmean "+selmon+" -sqr "+cat_file+" "+results_dir+"/norm-"+ var+"-"+season+".nc"
        command = "module load cdo; cdo "+selmon+" "+anomaly_file+" "+seasonal_anomaly_file
        os.system(command)


import matplotlib.pyplot as plt
norm = {}

for var in valid_variables:
    norm[var] = {}
    for season in seasons.keys():
        norm[var][season] = None

for var in valid_variables:
    for season in seasons.keys():
        
        fig = plt.figure(figsize=(6, 3.2))
        
        seasonal_anomaly_file = results_dir+"/"+var+"-anomaly-"+season+".nc"
        
        ds = xr.open_dataset(seasonal_anomaly_file)
        ds_var = ds[var]
        tmp = np.sqrt(np.nanmean(np.square(ds_var), axis=0))
        if var == valid_variables[0] and season == list(seasons.keys())[0]:
            indices = np.argwhere(~np.isnan(ds_var.data[0]))
            shape = ds_var.data[0].shape
            dims = ds_var.dims

            coordinates = {}
            for dim in dims:
                if dim == "time":
                    continue
                coordinates[dim] = ds_var[dim].data
        norm[var][season] = np.ndarray((len(indices)))
        for x, index in enumerate(indices):
            norm[var][season][x] = tmp.data[index[0], index[1]]
            
        print(var, season)
        plt.plot(norm[var][season])
        plt.show()
        ds.close()

S = {}

for i, var_i in enumerate(valid_variables):
    
    S[var_i] = {}
    for j, var_j in enumerate(valid_variables):
        if j <= i:
            continue
            
        S[var_i][var_j] = {}
        for season in seasons.keys():
            S[var_i][var_j][season] = 0
    
for season in seasons.keys():
    
    for i, var_i in enumerate(valid_variables):
    
        seasonal_anomaly_file_i = results_dir+"/"+var_i+"-anomaly-"+season+".nc"
        ds_i = xr.open_dataset(seasonal_anomaly_file_i)
        ds_var_i = ds_i[var_i]
    
        for j, var_j in enumerate(valid_variables):

            if j <= i:
                continue

            fig = plt.figure(figsize=(6, 3.2))
            
            print(season, var_i, var_j)

            seasonal_anomaly_file_j = results_dir+"/"+var_j+"-anomaly-"+season+".nc"

            ds_j = xr.open_dataset(seasonal_anomaly_file_j)
            ds_var_j = ds_j[var_j]
            
            if ds_var_i.dims != ds_var_j.dims:
                ds_var_j = ds_var_j.rename(dict(zip(ds_var_j.dims, ds_var_i.dims)))
                
            tmp = np.nanmean((ds_var_i * ds_var_j), axis=0)
            
            S[var_i][var_j][season] = np.ndarray((len(indices)))
            for x, index in enumerate(indices):
                n = (norm[var_i][season][x] * norm[var_j][season][x])
                if n > 0.0:
                    S[var_i][var_j][season][x] = tmp.data[index[0], index[1]] / n
                else:
                    S[var_i][var_j][season][x] = 0.0
                    
            plt.plot(S[var_i][var_j][season])
            #S[var_i][var_j][season][:] = np.nan_to_num(S[var_i][var_j][season][:])
            
            #S[var_i][var_j][season].plot()
            plt.show()
        
            ds_j.close()
            
        ds_i.close()


T = len(seasons.keys())
N = len(valid_variables)
X = len(indices)

A = np.zeros((N-1, N-1))
b = np.zeros((N-1))

coeff = {}

from helpers import process_plot_config, plot_coast

for t, season in enumerate(seasons.keys()):
    coeff[season] = {}
    for i, var_i in enumerate(valid_variables):
        coeff[season][var_i] = []
        list_without_i = [w for w in valid_variables if w != var_i]
        for x in range(X):
            for j, var_j in enumerate(list_without_i):
                try:
                    b[j] = S[var_i][var_j][season][x]
                except:
                    b[j] = S[var_j][var_i][season][x]
                    
                for k, var_k in enumerate(list_without_i):
                    if k >= j:
                        continue
                    try:
                        A[j][k] = S[var_j][var_k][season][x]
                        A[k][j] = A[j][k]
                    except:
                        A[j][k] = S[var_k][var_j][season][x] 
                        A[k][j] = A[j][k]

                A[j][j] = 1.0
                
            coeff[season][var_i].append(np.linalg.solve(A, b))

C = np.empty((T, N, N-1, *shape))
C.fill(np.nan)

N = np.empty((T, N, *shape))
N.fill(np.nan)

print(shape)


for t, season in enumerate(seasons.keys()):
    for i, var_i in enumerate(valid_variables):
        list_without_i = [w for w in valid_variables if w != var_i]
        for x, index in enumerate(indices):
            for j, var_j in enumerate(list_without_i):
                C[t][i][j][index[0]][index[1]] = coeff[season][var_i][x][j]
                N[t][i][index[0]][index[1]] = norm[var_i][season][x]
                
for t, season in enumerate(seasons.keys()):
    for i, var_i in enumerate(valid_variables):
        N[t][i] = xr.DataArray(N[t][i], dims=coordinates.keys(), coords=coordinates)
        list_without_i = [w for w in valid_variables if w != var_i]
        for j, var_j in enumerate(list_without_i): 
            C[t][i][j] = xr.DataArray(C[t][i][j], dims=coordinates.keys(), coords=coordinates)

#fig = plt.figure(figsize=(6, 3.2))

for t, season in enumerate(seasons.keys()):
    #for i, var_i in enumerate(valid_variables):
    for i, var_i in [(0, "SST")]:
        print(season, var_i)
        
                
        seasonal_anomaly_file_i = results_dir+"/"+var_i+"-anomaly-"+season+".nc"
        ds_i = xr.open_dataset(seasonal_anomaly_file_i)
        ds_var_i = ds_i.data_vars[var_i]
        units = ds_var_i.attrs["units"]
        ds_var_i = xr.DataArray(np.nanmean(ds_var_i.data, axis=0), dims=coordinates.keys(), coords=coordinates, name=var_i)
        ds_var_i.attrs["units"] = units
        data_plot_cfg, cbar_params, ctr_plot_cfg = process_plot_config(variables[var_i]["plot-config-anomaly"], ds_var_i)
        ds_i.close()
        
        list_without_i = [w for w in valid_variables if w != var_i]
        
        fig, axs = plt.subplots(1, len(list_without_i)+3, figsize=(4*(len(list_without_i)+3), 4), sharex='col', sharey='row', squeeze=0, gridspec_kw={"width_ratios": (len(list_without_i)+2)*[1] + [1.25]})
        
        test = xr.DataArray(np.zeros(C[t][i][0].shape))
        for j, var_j in enumerate(list_without_i):
            print("Contribution from "+var_j)

            seasonal_anomaly_file_j = results_dir+"/"+var_j+"-anomaly-"+season+".nc"

            ds_j = xr.open_dataset(seasonal_anomaly_file_j)
            ds_var_j = ds_j[var_j]
            
            ori_j = valid_variables.index(var_j)
            tmp = xr.DataArray(N[t][i]/N[t][ori_j] * C[t][i][j] * np.nanmean(ds_var_j.data, axis=0), dims=coordinates.keys(), coords=coordinates)
              
            tmp.plot(ax=axs[0,j], **{"add_colorbar" : False}, **data_plot_cfg)
            
            plot_coast(axs[0,j])
            
            if ctr_plot_cfg != {}:
                np.squeeze(tmp).plot.contour(ax=axs[0,j], **ctr_plot_cfg)
            
            axs[0,j].set_title("Contribution from "+var_j)

            test.data = test.data + tmp.data             
            ds_j.close()
            
            if j != 0:
                axs[0,j].set_ylabel("")
            else:
                ylabel = axs[0,j].get_ylabel()
                axs[0,j].set_ylabel(ylabel)

            axs[0,j].grid(linestyle='--', alpha=0.6)
            
        #print("Reconstruction")
        test = xr.DataArray(test.data, dims=coordinates.keys(), coords=coordinates)
        test.plot(ax=axs[0,-3], **{"add_colorbar" : False}, **data_plot_cfg)
        plot_coast(axs[0,-3])
        if ctr_plot_cfg != {}:
            np.squeeze(test).plot.contour(ax=axs[0,-3], **ctr_plot_cfg)
        axs[0,-3].set_title("Reconstruction")
        axs[0,-3].set_ylabel("")
        axs[0,-3].grid(linestyle='--', alpha=0.6)


        #print("Original")
        ds_var_i.plot(ax=axs[0,-2], **{"add_colorbar" : False}, **data_plot_cfg)
        plot_coast(axs[0,-2])
        if ctr_plot_cfg != {}:
            np.squeeze(ds_var_i).plot.contour(ax=axs[0,-2], **ctr_plot_cfg)        
        axs[0,-2].set_title("Original")
        axs[0,-2].set_ylabel("")
        axs[0,-2].grid(linestyle='--', alpha=0.6)
        ds_i.close()
        
        #print("Original-Reconstruction")
        (ds_var_i-test).plot(ax=axs[0,-1], **cbar_params, **data_plot_cfg)
        plot_coast(axs[0,-1])
        if ctr_plot_cfg != {}:
            np.squeeze(ds_var_i-test).plot.contour(ax=axs[0,-1], **ctr_plot_cfg)        
        axs[0,-1].set_title("Original-Reconstruction")
        axs[0,-1].set_ylabel("")
        axs[0,-1].grid(linestyle='--', alpha=0.6)
        fig.tight_layout() 
        plt.subplots_adjust(wspace=0, hspace=0)
        var_list = ("-").join(list_without_i)
        fig.savefig(var_i+"-"+season+"___"+var_list+".png", dpi=100)        
        plt.show()
            