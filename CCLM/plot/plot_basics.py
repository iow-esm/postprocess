import numpy as np
from netCDF4 import Dataset
from mpl_toolkits.basemap import Basemap

import matplotlib.pyplot as plt
        
def build_basemap(lons, lats):
    # Get some parameters for the Stereographic Projection
    lon_0 = lons.mean()
    lat_0 = lats.mean()

    m = Basemap(width=7000000,height=5000000,
                resolution='l',projection='stere',\
                lat_ts=40,lat_0=lat_0,lon_0=lon_0)

    # If lon and lat variables are 1D,
    # use meshgrid to create 2D arrays
    # Not necessary if coordinates are already in 2D arrays.
    if lons.ndim == 1 and lats.ndim == 1:
        lons, lats = np.meshgrid(lons, lats)
    xi, yi = m(lons, lats)
    
        # Add Grid Lines
    m.drawparallels(np.arange(-80., 81., 10.), labels=[1,0,0,0], fontsize=10)
    m.drawmeridians(np.arange(-180., 181., 10.), labels=[0,0,0,1], fontsize=10)

    # Add Coastlines, States, and Country Boundaries
    m.drawcoastlines()
    m.drawcountries()
    
    return m, xi, yi

def read_data(plot_config, nc_file, lon_name = 'lon', lat_name = 'lat'):
    
    fh = Dataset(nc_file, mode='r')

    lons = fh.variables[lon_name][:]
    lats = fh.variables[lat_name][:]
    variable = fh.variables[plot_config.variable][:]
    units = fh.variables[plot_config.variable].units
    
    fh.close()
    
    return lons, lats, variable, units
    
def process_config(plot_config, variable, units, add_info = ""):
    
    if plot_config.title is not None:
        title = plot_config.title
    else:
        title = plot_config.variable + " " + add_info
    
    if plot_config.transform_variable is not None:
        variable, units = plot_config.transform_variable(variable, units)
        
    if plot_config.min_value is not None:
        vmin = plot_config.min_value
    else:
        vmin = min(variable.flatten())

    if plot_config.max_value is not None:
        vmax = plot_config.max_value
    else:
        vmax = max(variable.flatten())

    if plot_config.delta_value is not None:
        delta = plot_config.delta_value
        nlevels = int((vmax-vmin)/delta)
    else:
        delta = None
        nlevels = None
        
    if plot_config.color_map is not None:
        color_map = plot_config.color_map
    else:
        color_map = 'hsv'

    if (plot_config.contour) and (delta is not None):
        contour = True
    else:
        contour = False
    
    return title, variable, units, vmin, vmax, delta, nlevels, color_map, contour


def plot_on_map(plot_configs, results_dir):
    for suffix in plot_configs.keys():
        for plot_config in plot_configs[suffix]:

            print("plotting: " + plot_config.variable + " " + suffix + "...")

            plt.figure(figsize=(12, 8), dpi=80)

            # read the data
            if plot_config.path is None:
                nc_file = '../' + plot_config.task_name + '/' + results_dir + '/' + plot_config.variable + '-' + suffix + '.nc'
            else:
                nc_file = plot_config.path

            lons, lats, variable, units = read_data(plot_config, nc_file)

            # build addtional info for title: time range if specified (last 17 characters and a minus)
            add_info = suffix
            if results_dir[-8:].isnumeric() and results_dir[-17:-9].isnumeric():
                add_info += " " + results_dir[-17:]
                
            # decode the config
            title, variable, units, vmin, vmax, delta, nlevels, color_map, contour = process_config(plot_config, variable, units, add_info = add_info)

            # build the base map
            m, xi, yi = build_basemap(lons, lats)

            # create color map
            cmap = plt.get_cmap(color_map, nlevels)

            # Plot Data
            cs = m.pcolor(xi, yi, np.squeeze(variable), cmap=cmap, vmin=vmin, vmax=vmax)

            # plot contour if wanted
            if contour:
                m.contour(xi, yi, np.squeeze(variable), np.arange(vmin, vmax, (vmax -vmin)/nlevels), colors='black', linewidths=0.4)

            # Add Colorbar
            cbar = m.colorbar(cs, location='bottom', pad="10%")
            cbar.set_label(units)

            # Add Title
            plt.title(title)

            out_file = results_dir + "/" + title.replace(" ", "-") + ".pdf"
            plt.savefig(out_file)
            plt.close()
            
            print(" plot saved in: " + out_file)
            print("...done")