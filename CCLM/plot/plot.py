import glob
import os
import sys

out_dir = str(sys.argv[1])
from_date = int(sys.argv[2])
to_date = int(sys.argv[3])


import numpy as np

sys.path.append('../../auxiliary')
import create_results_dir

results_dir = create_results_dir.create_results_dir(out_dir, from_date, to_date)

import config
variables = config.variables

import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

from plot_basics import *

for suffix in variables.keys():
    for var in variables[suffix]:
        
        print(var.variable, suffix)
        
        figure(figsize=(12, 8), dpi=80)
        
        # read the data
        if var.path is None:
            nc_file = '../' + var.task_name + '/' + results_dir + '/' + var.variable + '-' + suffix + '.nc'
        else:
            nc_file = var.path
            
        lons, lats, variable, units = read_data(var, nc_file)
        
        # decode the config
        title, variable, units, vmin, vmax, delta, nlevels, color_map, contour = process_config(var, variable, units)

        # build the base map
        m, xi, yi = build_basemap(lons, lats)
        
        # create color map
        cmap = plt.get_cmap(color_map, nlevels)
        
        # Plot Data
        cs = m.pcolor(xi, yi, np.squeeze(variable), cmap=cmap, vmin=vmin, vmax=vmax)
        
        # plot contour if wanted
        if contour:
            m.contour(xi, yi, np.squeeze(variable), np.arange(vmin, vmax, delta), colors='black', linewidths=0.4)

        # Add Colorbar
        cbar = m.colorbar(cs, location='bottom', pad="10%")
        cbar.set_label(units)

        # Add Title
        plt.title(title)

plt.show()