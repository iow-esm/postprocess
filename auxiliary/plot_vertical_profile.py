def plot_vertical_profile(ax,
                          data,
                          depths,
                          std = None,
                          samples = None,
                          label = "",
                          smooth = False,
                          linestyle = "-",
                          linewidth=3,
                          color = None,
                          marker = None
                          ):
            
    import matplotlib.pyplot as plt
    from scipy.interpolate import make_interp_spline, BSpline
    import numpy as np
        
    ax.grid(axis='x', linestyle='--')

    if smooth: 
        p = ax.plot(data, -depths, marker = marker, linestyle="", label=label, color=color)
    else:
        p = ax.plot(data, -depths, marker = marker, linestyle=linestyle, linewidth=linewidth, label=label, color=color)
        
    if smooth:    
        spl = make_interp_spline(depths, data, k=3)  # type: BSpline
        xnew = np.linspace(depths.min(), depths.max(), depths.size*10) 
        smoothed_curve = spl(xnew)
        ax.plot(smoothed_curve, -xnew, color=color)#, label="spline")

    if samples is not None:
        try:
            for i, y in enumerate(-depths):
                ax.text(data[i] + 0.1, y, samples[i] + 10)
        except:
            print("No sample numbers to show!")

    if std is not None:
        try:
            ax.fill_betweenx(-depths, data - 0.5*std, data + 0.5*std, alpha=0.3, color=color)#, label=label+" std")
            #plt.plot(data["values"] - 0.5*data["std"], -data["depths"], linestyle="--", color=p[-1].get_color())
            #plt.plot(data["values"] + 0.5*data["std"], -data["depths"], linestyle="--", color=p[-1].get_color())
        except:
            pass

    ax.grid(axis='y', linestyle='--')