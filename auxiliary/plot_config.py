from copy import deepcopy

class PlotConfig:
    def __init__(self, variable = None, title = None, min_value = None, max_value = None, delta_value = None,
        color_map = "ocean", contour = True, transform_variable = None, task_name = None, path = None, file = None,
        lon_name = "lon", lat_name = "lat", vert_name = "z", width = None, height = None, 
        time_name = "time", trend=False, std_deviation=True,
        linestyle = None, symmetric = False):
        
        args = locals()
        for arg in args.keys():
            if arg is not "self":
                setattr(self, arg, args[arg]) 
        
    def reconfigure(self, variable = None, title = None, min_value = None, max_value = None, delta_value = None, 
        color_map = None, contour = None, transform_variable = None, task_name = None, path = None, file = None, 
        lon_name = None, lat_name = None, vert_name = None, width = None, height = None, 
        time_name = None, trend=None, std_deviation=None,
        linestyle = None, symmetric = None):

        args = locals()
        for arg in args.keys():
            if arg is not "self":
                if args[arg] is not None:
                    setattr(self, arg, args[arg]) 
                    
    def clone(self, variable = None, title = None, min_value = None, max_value = None, delta_value = None, 
        color_map = None, contour = None, transform_variable = None, task_name = None, path = None, file = None, 
        lon_name = None, lat_name = None, vert_name = None, width = None, height = None, 
        time_name = None, trend=None, std_deviation=None,
        linestyle = None, symmetric = None):
        
        c = deepcopy(self)
        c.reconfigure(variable, title, min_value, max_value, delta_value,
        color_map, contour, transform_variable, task_name, path, file,
        lon_name, lat_name, vert_name, width, height,
        time_name, trend, std_deviation,
        linestyle, symmetric)
        
        return c

    def __str__(self):
        s = ""
        for a in dir(self):
            if a.startswith("__") or callable(getattr(self, a)):
                continue
            s += a+": "+str(getattr(self, a))+", "

        return s[:-2]

