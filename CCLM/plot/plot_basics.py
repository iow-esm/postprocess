import numpy as np
from netCDF4 import Dataset
from mpl_toolkits.basemap import Basemap
        


def build_basemap(lons, lats):
    # Get some parameters for the Stereographic Projection
    lon_0 = lons.mean()
    lat_0 = lats.mean()

    m = Basemap(width=7000000,height=5000000,
                resolution='l',projection='stere',\
                lat_ts=40,lat_0=lat_0,lon_0=lon_0)

    

    # Because our lon and lat variables are 1D,
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

def read_data(var, nc_file, lon_name = 'lon', lat_name = 'lat'):
    
    fh = Dataset(nc_file, mode='r')

    lons = fh.variables[lon_name][:]
    lats = fh.variables[lat_name][:]
    variable = fh.variables[var.variable][:]
    units = fh.variables[var.variable].units
    
    fh.close()
    
    return lons, lats, variable, units
    
def process_config(var, variable, units):
    
    title = var.title
    
    if var.transform_variable is not None:
        variable, units = var.transform_variable(variable, units)
        
    if var.min_value is not None:
        vmin = var.min_value
    else:
        vmin = min(variable.flatten())

    if var.max_value is not None:
        vmax = var.max_value
    else:
        vmax = max(variable.flatten())

    if var.delta_value is not None:
        delta = var.delta_value
        nlevels = int((vmax-vmin)/delta)
    else:
        delta = None
        nlevels = None
        
    if var.color_map is not None:
        color_map = var.color_map
    else:
        color_map = 'hsv'

    if (var.contour) and (delta is not None):
        contour = True
    else:
        contour = False
    
    return title, variable, units, vmin, vmax, delta, nlevels, color_map, contour