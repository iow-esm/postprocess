import numpy as np
from netCDF4 import Dataset, num2date, date2num
from mpl_toolkits.basemap import Basemap

import matplotlib.pyplot as plt
import os
        
def build_basemap(lons, lats, width = None, height = None):
    # Get some parameters for the Stereographic Projection
    lon_0 = lons.mean()
    lat_0 = lats.mean()
    
    # If lon and lat variables are 1D,
    # use meshgrid to create 2D arrays
    # Not necessary if coordinates are already in 2D arrays.
    if lons.ndim == 1 and lats.ndim == 1:
        lons, lats = np.meshgrid(lons, lats)
      
    if width is None and height is None:

        llcrnrlon = lons[0][0]
        urcrnrlon = lons[-1][-1]
        llcrnrlat = lats[0][0]
        urcrnrlat = lats[-1][-1]
    
        m = Basemap(llcrnrlon = llcrnrlon, urcrnrlon = urcrnrlon, llcrnrlat = llcrnrlat, urcrnrlat = urcrnrlat, 
                    resolution='l',projection='stere', lat_0=lat_0, lon_0=lon_0)
        
    else:
        m = Basemap(width=width, height=height, resolution='l',projection='stere', 
                    lat_0=lat_0, lon_0=lon_0)
        
    xi, yi = m(lons, lats)
    
        # Add Grid Lines
    m.drawparallels(np.arange(-80., 81., 10.), labels=[1,0,0,0], fontsize=10)
    m.drawmeridians(np.arange(-180., 181., 10.), labels=[0,0,0,1], fontsize=10)

    # Add Coastlines, States, and Country Boundaries
    m.drawcoastlines()
    m.drawcountries()
    
    return m, xi, yi

def read_data(plot_config, nc_file):
    
    fh = Dataset(nc_file, mode='r')
    
    lon_name = plot_config.lon_name
    lat_name = plot_config.lat_name
    
    lons = fh.variables[lon_name][:]
    lats = fh.variables[lat_name][:]
    variable = fh.variables[plot_config.variable][:]
    units = fh.variables[plot_config.variable].units
    
    fh.close()
    
    return lons, lats, variable, units
    
def read_time_series(plot_config, nc_file):
    
    fh = Dataset(nc_file, mode='r')
    
    time_name = plot_config.time_name
    
    time = fh.variables[time_name]
    time_units = time.units
    time = num2date(np.squeeze(time[:]),time.units)
    
    variable = np.squeeze(fh.variables[plot_config.variable][:])
    
    # sort variable according to the time
    szl = sorted(zip(time, variable))
    time = np.array([element for element,_ in szl])
    variable = np.array([element for _, element in szl])
    
    units = fh.variables[plot_config.variable].units
    
    try:
        std = np.squeeze(fh.variables[plot_config.variable + "_STD"][:])
    except:
        std = None
        
    fh.close()
    
    return time, variable, units, std, time_units
    
def process_config(plot_config, variable, units):
    
    if plot_config.transform_variable is not None:
        variable, units = plot_config.transform_variable(variable, units)
        
    if plot_config.min_value is not None:
        vmin = plot_config.min_value
    else:
        vmin = variable.min()

    if plot_config.max_value is not None:
        vmax = plot_config.max_value
    else:
        vmax = variable.max()
        
    if plot_config.symmetric:
        vmax = max(abs(vmax), abs(vmin))
        vmin = -vmax

    if plot_config.delta_value is not None:
        delta = plot_config.delta_value
        nlevels = int((vmax-vmin)/delta)
    else:
        delta = None
        nlevels = None
        
        if plot_config.symmetric:
            delta = (vmax-vmin)/9.0
            nlevels = 9
        
    if plot_config.color_map is not None:
        color_map = plot_config.color_map
    else:
        color_map = 'hsv'

    if (plot_config.contour) and (delta is not None):
        contour = True
    else:
        contour = False
    
    return variable, units, vmin, vmax, delta, nlevels, color_map, contour


def plot_on_map(plot_configs, results_dir):
    for title in plot_configs.keys():
    
        print("plotting: " + title + "...")
        plt.figure(figsize=(12, 8), dpi=80)
            
        for plot_config in plot_configs[title]:

            # read the data
            if plot_config.path is not None:
                nc_file = plot_config.path + "/" + plot_config.file
            elif plot_config.file is not None:
                nc_file = '../' + plot_config.task_name + '/' + results_dir + '/' + plot_config.file
            else:
                nc_file = '../' + plot_config.task_name + '/' + results_dir + '/' + plot_config.variable + ".nc"

            lons, lats, variable, units = read_data(plot_config, nc_file)
                
            # decode the config
            variable, units, vmin, vmax, delta, nlevels, color_map, contour = process_config(plot_config, variable, units)

            # build the base map
            m, xi, yi = build_basemap(lons = lons, lats = lats, width = plot_config.width, height = plot_config.height)

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
            
        # build addtional info for title: time range if specified (last 17 characters and a minus)
        if results_dir[-8:].isnumeric() and results_dir[-17:-9].isnumeric():
            title += " " + results_dir[-17:]
            
        # Add Title
        plt.title(title)

        out_file = results_dir + "/" + title.replace(" ", "-") + ".pdf"
        plt.savefig(out_file)
        plt.close()
        
        print(" plot saved in: " + out_file)
        
        os.system("pdfcrop " + out_file + " " + out_file)
        
        print("...done")
            
def plot_time_series(plot_configs, results_dir):
    for title in plot_configs.keys():

        print("plotting: " + title + "...")
        plt.figure(figsize=(12, 8), dpi=80)
        
        for plot_config in plot_configs[title]:

            # read the data
            if plot_config.path is not None:
                nc_file = plot_config.path + "/" + plot_config.file
            elif plot_config.file is not None:
                nc_file = '../' + plot_config.task_name + '/' + results_dir + '/' + plot_config.file
            else:
                nc_file = '../' + plot_config.task_name + '/' + results_dir + '/' + plot_config.variable + ".nc"

            time, variable, units, std, time_units = read_time_series(plot_config, nc_file)

            # decode the config
            variable, units, vmin, vmax, delta, nlevels, color_map, contour = process_config(plot_config, variable, units)

            plt.grid(linestyle='--')
          
            # Plot Data
            if plot_config.linestyle is not None:
                p = plt.plot(time, variable, plot_config.linestyle, label=plot_config.title)
            else:
                p = plt.plot(time, variable, label=plot_config.title)
                
            if std is not None and plot_config.std_deviation:
                if plot_config.linestyle is not None:
                    plt.plot(time, variable + 0.5*std, plot_config.linestyle, linestyle="--", marker="", linewidth=0.1)
                    plt.plot(time, variable - 0.5*std, plot_config.linestyle, linestyle="--", marker="", linewidth=0.1)    
                else:
                    plt.plot(time, variable + 0.5*std, color=p[-1].get_color(), linestyle="--", marker="", linewidth=0.1)
                    plt.plot(time, variable - 0.5*std, color=p[-1].get_color(), linestyle="--", marker="", linewidth=0.1)        
                    
                plt.fill_between(time, variable - 0.5*std, variable + 0.5*std, color=p[-1].get_color(), alpha=0.1)

            if plot_config.trend:
                try:
                    x = date2num(time, time_units)
                    z = np.polyfit(x, variable, 1)
                    z = np.poly1d(z)
                    plt.plot(time, z(x), color=p[-1].get_color(), linestyle="dotted")
                except Exception as e:
                    print("Could not calculate trend due to exception:", e)
                
            plt.legend(loc="upper left")
            
        # build addtional info for title: time range if specified (last 17 characters and a minus)
        if results_dir[-8:].isnumeric() and results_dir[-17:-9].isnumeric():
            title += " " + results_dir[-17:]
            
        # Add Title
        plt.title(title)
        plt.ylabel(plot_config.variable + " [" + units + "]")
        plt.xlabel(plot_config.time_name)

        out_file = results_dir + "/" + title.replace(" ", "-") + ".pdf"
        plt.savefig(out_file)
        plt.close()
    
        print(" plot saved in: " + out_file)
        
        os.system("pdfcrop " + out_file + " " + out_file)
        
        print("...done")