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
        cmd = "source "+aux_path+"/../load_modules.sh; cdo remapbil,"+aux_path+"/coast_grid.txt"+" "+nc_file+" "+remapped_file
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


def get_month_names(numbers):
    import numpy as np
    month_names = { 1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun", 7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"}

    names = []
    for n in numbers:
        names.append(month_names[n])
    
    return np.array(names)

def process_time_axis(time, operator):
    years = time.astype('datetime64[Y]').astype(int) + 1970
    months = time.astype('datetime64[M]').astype(int) % 12 + 1
    days = time - time.astype('datetime64[M]') + 1

    if operator == "-ymonmean":
        t = get_month_names(months)
    else:
        t = time

    return t

def find_other_models(var, task, from_date, to_date):
    model_dirs = {}
    try:
        other_models = var['other-models']
        for om in other_models.keys():
            model_dirs[om] = other_models[om]["root"]+"/"+task+"/results/"+other_models[om]["output_name"]
            if {from_date} != -1 and {to_date} != -1:
                model_dirs[om] += "-"+str(from_date)+"_"+str(to_date)
    except:
        pass    

    return model_dirs

def get_n_colors(n, cmap="tab10"):
    import numpy as np
    import matplotlib

    if cmap == "tab10":
        colors = matplotlib.cm.get_cmap(cmap)
        colors = colors(np.linspace(0.0, 1.1, 11, endpoint=False))
        c = []
        for i in range(n):
            c.append(colors[i%10])
        return c

    if cmap == "hsv":
        import colorsys
        HSV_tuples = [(x*1.0/n, 0.5, 0.7) for x in range(n)]
        return list(map(lambda x: colorsys.hsv_to_rgb(*x), HSV_tuples))  
    
    colors = matplotlib.cm.get_cmap(cmap)
    return colors(np.linspace(0.0, 1.0, n, endpoint=True))     

def process_plot_config(plot_config, data_array):
    from matplotlib import cm
    from matplotlib.colors import ListedColormap
    import numpy as np

    import plot_config as pc

    if plot_config is None:
        plot_config = pc.PlotConfig()
    else:
        if not isinstance(plot_config, pc.PlotConfig):
            plot_config = pc.PlotConfig(**plot_config)

    if plot_config.min_value is not None:
        vmin = plot_config.min_value
    else:
        vmin = np.amin(np.squeeze(data_array))

    if plot_config.max_value is not None:
        vmax = plot_config.max_value
    else:
        vmax = np.amax(np.squeeze(data_array))

    if plot_config.symmetric:
        vmin = min(vmin, -vmax)
        vmax = max(-vmin, vmax)

    try:
        units = data_array.units
    except:
        units = "a.u."

    if plot_config.delta_value is None:
        data_plot_cfg = {"cmap" : plot_config.color_map, "vmin" : vmin, "vmax" : vmax}
        cbar_cfg = {"cbar_kwargs" : {"label" : data_array.name+" ["+units+"]"}} 
        ctr_plot_cfg = {}

    else:
        d = plot_config.delta_value
        levels = np.arange(vmin,vmax+d,d)
        levels = levels[np.abs(levels)>1.0e-15].tolist()
        s = len(levels)//14 + 1
        ticks = list(set(sorted(levels[::s]+[0])))
        cmap = cm.get_cmap(plot_config.color_map, 256)
        color_values = ((np.array(levels)-min(levels))/(max(levels)-min(levels))).tolist()
        
        if np.amax(np.squeeze(data_array)) > vmax:
            color_values += [1.1]
        if np.amin(np.squeeze(data_array)) < vmin:
            color_values += [-0.1]
            
        color_values = sorted(color_values + [0.5])
        newcolors = cmap(color_values)
        cmap = ListedColormap(newcolors)

        data_plot_cfg = {"levels" : levels, "cmap" : cmap, "vmin" : vmin, "vmax" : vmax}
        cbar_cfg = {"cbar_kwargs" : {"ticks" : ticks, "label" : data_array.name+" ["+units+"]"}}

        if plot_config.contour:
            ctr_plot_cfg = {"levels" : levels, "linewidths" : 0.75, "colors" : "black",  "linestyles" : "-"}
        else:
            ctr_plot_cfg = {}

    return data_plot_cfg, cbar_cfg, ctr_plot_cfg 


import numpy as np
import matplotlib.pyplot as plt


class TaylorDiagram(object):
    """
    Taylor diagram.

    Plot model standard deviation and correlation to reference (data)
    sample in a single-quadrant polar plot, with r=stddev and
    theta=arccos(correlation).
    """

    def __init__(self, refdata, ax,  *args, **kwargs):

        # memorize reference data
        self.refdata = refdata
        self.ax = ax

        refstd = refdata.std(ddof=1) 
        rlim = [0.0, 1.2*refstd]
        thetalim = [0.0, 0.5*np.pi]

        if ax != None:

            # Add reference point and stddev contour
            try:
                kwargs["marker"]
            except:
                kwargs["marker"] = 'o'
            try:
                kwargs["color"]
            except:
                kwargs["color"] = "black"
            try:
                kwargs["ms"]
            except:
                kwargs["ms"] = 10     
            try:
                kwargs["label"]
            except:
                kwargs["label"] = "reference"                     

            ax.plot([0], refstd, *args, ls='', zorder=0, **kwargs)
            ax.grid(True, linestyle="--")
            
            ax.set_xlabel("St. dev.")
            ax.xaxis.set_label_coords(0.5, -0.1)

            ax.set_xlim(thetalim)
            ax.set_ylim(rlim)

            self.rlim = rlim
            self.thetalim = thetalim

        self.model_std = {"reference" : refstd}
        self.corrcoef = {"reference" : 1.0}
        self.rms = {"reference" : 0.0}

    def add_sample(self, model_data, *args, **kwargs):
        """
        Add sample to the Taylor
        diagram. *args* and *kwargs* are directly propagated to the
        `Figure.plot` command.
        """

        model_std = model_data.std(ddof=1)
        corrcoef = np.corrcoef(model_data, self.refdata)[0, 1]
        rms = np.sqrt(self.model_std["reference"]**2 + model_std**2 - 2.0*self.model_std["reference"]*model_std*np.cos(np.arccos(corrcoef)))

        try:
            label = kwargs["label"]
        except:
            label = "model"+str(len(self.model_std.keys())) 

        if self.ax != None:

            self.ax.plot(np.arccos(corrcoef), model_std,
                            *args, **kwargs)  # (theta, radius)

            if model_std > self.rlim[1]:
                self.rlim = [0, 1.2 * model_std]
                self.ax.set_ylim(*self.rlim)

            if np.arccos(corrcoef) > self.thetalim[1]:
                self.thetalim[1] = 1.2 * np.arccos(corrcoef)
                self.ax.set_xlim(*self.thetalim)                       

        self.model_std[label] = model_std
        self.corrcoef[label] = corrcoef
        self.rms[label] = rms
        #self.ax.set_ylim(rlim) 


    def get_samples(self):
        return self.model_std, self.corrcoef, self.rms

    def finalize(self):
        
        if self.ax is None:
            return 

        self.ax.text(0.5*(self.thetalim[1]-self.thetalim[0]), (1.0+0.03*(self.thetalim[1]-self.thetalim[0])**2)*self.rlim[1],"Correlation", rotation=0.5*(self.thetalim[1]-self.thetalim[0])*180.0/np.pi-90.0)

        rs, ts = np.meshgrid(np.linspace(*self.rlim), np.linspace(*self.thetalim))

        rms = np.sqrt(self.model_std["reference"]**2 + rs**2 - 2.0*self.model_std["reference"]*rs*np.cos(ts))

        self.ax.contourf(ts, rs, rms, 9, alpha=0.3, cmap="RdYlGn_r")
        contours = self.ax.contour(ts, rs, rms, 9, linestyles="--", linewidths=1, alpha=0.5, colors="grey")

        if self.model_std["reference"] > 100.0 or self.model_std["reference"] < 0.1:
            fmt = '%3.2e'
        else:
            fmt = '%3.2f'

        self.ax.clabel(contours, inline=False, fmt=fmt, colors="black")

        t = np.linspace(*self.thetalim)
        r = np.zeros_like(t) + self.model_std["reference"]
        self.ax.plot(t, r, 'k--', label='_')

        xticks = [1.0, 0.99, 0.95, 0.9, 0.8, 0.7, 0.6, 0.4, 0.2, 0.0]

        if self.thetalim[1] > 0.5*np.pi:
            for x in [-0.2, -0.4, -0.6, -0.8, -0.9, -0.95, -0.99 -1.0]:

                if np.arccos(x) > self.thetalim[1]:
                    break

                xticks += [x]

        self.ax.set_xticks(np.arccos(xticks))
        self.ax.set_xticklabels(xticks)

def better_operator_name(operator):

    better_names = {
        "monmean" : "monthly means",
        "ymonmean" : "annual cycle",
        "yearmean" : "annual means", 
        "daymean" : "daily means",
        "" : "time series"
    }

    try:
        return better_names[operator]
    except:
        return operator