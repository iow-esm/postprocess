import os
aux_path = os.path.abspath(os.path.dirname(__file__))

def convert_to_decimal(value):
    if ":" not in value:
        return value
    
    tmp = value.split(":")
    decimal_value = float(tmp[0]) + float(tmp[1])/60.0 + float(tmp[2])/3600.0
    
    return str(decimal_value)



def plot_coast(ax):

    import xarray as xr
    import numpy as np
    import os

    print(aux_path)

    xlim = ax.get_xlim()
    ylim = ax.get_ylim()

    ds = xr.open_dataset(aux_path+"/coast.nc")

    ds_var = ds["mask"]
    coast = np.where((~ds_var.isnull()), 1.0, 0.0)
    ds_var.values = coast
    coast_plot_cfg = {"levels" : [0.1], "linewidths" : 1.5, "colors" : "grey"}
    np.squeeze(ds_var).plot.contour(ax=ax, **coast_plot_cfg, zorder=100)
    ds.close()
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)

def load_dataset(nc_file):
    import xarray as xr

    ds = xr.open_dataset(nc_file)

    if hasattr(ds, "rotated_pole"):

        remapped_file = "tmp-remapped.nc"
        cmd = "cdo remapbil,"+aux_path+"/coast_grid.txt"+" "+nc_file+" "+remapped_file
        print(cmd)
        os.system(cmd)
        ds.close()
        ds = xr.open_dataset(remapped_file)

    return ds

def unload_dataset(ds):

    ds.close()

    import glob
    remapped_file = "tmp-remapped.nc"
    if glob.glob(remapped_file) != []:
        os.system("rm "+remapped_file)