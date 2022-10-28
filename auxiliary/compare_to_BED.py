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

def get_mean_vertical_profile_from_BED(csv_files, varname, season, min_date = None, max_date = None, delimiter = " "):

    import pandas as pd
    import glob
    import xarray as xr
    import numpy as np

    depths = []
    nsamples = []
    stds = []
    values = []
        
    for csvf in csv_files:

        # read in the csv file
        if delimiter == " ":
            df = pd.read_csv(csvf, delim_whitespace=True)
        else:
            df = pd.read_csv(csvf, delimiter=delimiter)
        
        samples = []
        
        for i, dnr in enumerate(df["Dnr"]): 
        
            date = int(str(df["Year"][i])+str("{month:02d}").format(month = df["Month"][i])+str("{day:02d}").format(day = df["Day"][i]))
            
            #print(date)        
            if min_date is not None and date < min_date:
                continue
                
            if max_date is not None and date > max_date:
                continue
                
            if (season != "") and (str(df["Month"][i]) not in season.replace(" ","").split(",")):
                continue
            
            samples.append(df["Average"][i])

        samples = np.array(samples)
        nsamples.append(samples.size)
        stds.append(samples.std())
        values.append(samples.mean())
        depths.append(float(csvf.split(".")[-2][-3:]))
        
    if not depths:
        return None
    
    ds = xr.Dataset({varname : (("depth"), values),
                     varname+"_STD" : (("depth"), stds),
                     "nsamples" : (("depth"), nsamples)
                    },
                    coords = {"depth" : depths})
    
    return ds


for var in variables.keys():
    
    try:
        ref_file_pattern = variables[var]["BED-reference-file-pattern"]
    except:
        print("No BED reference given for variable "+var)
        continue

    seasons = variables[var]["seasons"]
    stations = variables[var]["stations"]

    ref_files = glob.glob(ref_file_pattern)

    for station in stations:

        try:
            from config import station_names
            for name in station_names.keys():
                if station in station_names[name]:
                    station_name = name
                    break
        except:
             station_name = station
                
        station_ref_files = [s for s in ref_files if station_name in s]

        if not station_ref_files:
            print("No reference files found for variable "+var+" and station "+station)
            continue

        for season in seasons.keys():
            bed_data = get_mean_vertical_profile_from_BED(station_ref_files, var, min_date=from_date, max_date=to_date, season=seasons[season])
            if bed_data is None:
                continue
                
            bed_data.to_netcdf(results_dir+"/"+var+"-"+station+"-"+season+".nc")


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
model_dirs = {{"model1" : "../../../seasonal_mean/{results_dir}"}}

for var in variables.keys():

    try:
        variables[var]['BED-reference-file-pattern']
    except:
        continue

    seasons = variables[var]["seasons"]
    stations = variables[var]["stations"]

    fig, axs = plt.subplots(len(stations), len(seasons), figsize=(3*len(seasons), 5*len(stations)), sharex=True, sharey='row')

    for i, station in enumerate(stations):
        for j, season in enumerate(seasons.keys()):
            
            ds = xr.open_dataset(var+"-"+station+"-"+season+".nc")
            plot_vertical_profile.plot_vertical_profile(axs[i,j], ds[var].data, ds.depth.data, ds[var+"_STD"].data, smooth=True, label = "BED", color="grey")

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

f = open(results_dir+"/compare_to_BED.py", "w")
f.write(script)
f.close()

import convertpy2ipynb
convertpy2ipynb.convertpy2ipynb(results_dir+"/compare_to_BED.py")