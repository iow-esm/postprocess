from copy import deepcopy

class PlotConfig:
    def __init__(self, variable, title = None, min_value = None, max_value = None, delta_value = None, color_map = None, contour = False, transform_variable = None, task_name = "seasonal_mean", path = None, lon_name = "lon", lat_name = "lat", width = None, height = None):
        self.variable = variable
        self.title = title
        self.min_value = min_value
        self.max_value = max_value
        self.delta_value = delta_value
        self.color_map = color_map
        self.contour = contour
        self.transform_variable = transform_variable
        self.task_name = task_name
        self.path = path
        self.lon_name = lon_name
        self.lat_name = lat_name
        self.width = width
        self.height = height
        
    def reconfigure(self, variable = None, title = None, min_value = None, max_value = None, delta_value = None, color_map = None, contour = None, transform_variable = None, task_name = None, path = None):

        args = locals()
        for arg in args.keys():
            if arg is not "self":
                if args[arg] is not None:
                    setattr(self, arg, args[arg]) 
                    
    def clone(self, variable = None, title = None, min_value = None, max_value = None, delta_value = None, color_map = None, contour = None, transform_variable = None, task_name = None, path = None):
        c = deepcopy(self)
        c.reconfigure(variable, title, min_value, max_value, delta_value, color_map, contour, transform_variable, task_name, path)
        return c