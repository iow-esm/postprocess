class PlotConfig:
    def __init__(self, variable, title = None, min_value = None, max_value = None, delta_value = None, color_map = None, contour = False, transform_variable = None, task_name = "seasonal_mean", path = None):
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