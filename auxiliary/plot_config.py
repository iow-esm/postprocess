from copy import deepcopy

class PlotConfig:
    def __init__(self, variable, title = None, min_value = None, max_value = None, delta_value = None,
        color_map = None, contour = False, transform_variable = None, task_name = "seasonal_mean", path = None, 
        lon_name = "lon", lat_name = "lat", width = None, height = None, 
        time_name = "time", first_plot = True, last_plot = True,
        linestyle = None):
        
        args = locals()
        for arg in args.keys():
            if arg is not "self":
                setattr(self, arg, args[arg]) 
        
    def reconfigure(self, variable = None, title = None, min_value = None, max_value = None, delta_value = None, 
        color_map = None, contour = None, transform_variable = None, task_name = None, path = None, 
        lon_name = None, lat_name = None, width = None, height = None, 
        time_name = None, first_plot = None, last_plot = None,
        linestyle = None):

        args = locals()
        for arg in args.keys():
            if arg is not "self":
                if args[arg] is not None:
                    setattr(self, arg, args[arg]) 
                    
    def clone(self, variable = None, title = None, min_value = None, max_value = None, delta_value = None, 
        color_map = None, contour = None, transform_variable = None, task_name = None, path = None, 
        lon_name = None, lat_name = None, width = None, height = None, 
        time_name = None, first_plot = None, last_plot = None,
        linestyle = None, linecolor = None):
        
        c = deepcopy(self)
        c.reconfigure(variable, title, min_value, max_value, delta_value,
        color_map, contour, transform_variable, task_name, path,
        lon_name, lat_name, width, height,
        time_name, first_plot, last_plot,
        linestyle)
        
        return c