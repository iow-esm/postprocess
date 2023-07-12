def get_tasks(**kwargs):

    from_date = kwargs["from_date"]
    to_date = kwargs["to_date"]

    tasks = {  
        "compare_2D_means" : {
            "name" : "Two-dimensional seasonal means",
            "text" : 
            (r"This task generates figures containing two-dimensional seasonal means $\langle \phi \rangle_S(x,y)$ for a season $s$ and a three-dimensional variable $\phi(x,y,t)$, i.e."
            r"$$ \langle \phi \rangle_S(x,y) = \frac{1}{N_S} \sum_{t\in S} \phi(x,y,t), $$"
            f"where $t$ are all time steps that are contained in season $S$. The number of these time steps is given by $N_S$, where the considered time period is from `{from_date}` to `{to_date}`."
            ),
            "caption-template" : 
            ("<b> Seasonal means for variable {var_name}. </b>"
            "The rows correspond to different models whereas the columns reflect the various seaons that are considered."
            "The $x$ and $y$ axis measure the longitudes and latitudes, respectively."
            ),
        },

        "compare_2D_anomalies" : {
            "name" : "Two-dimensional seasonal anomalies",
            "text" : 
            (r"This task generates figures containing two-dimensional seasonal anomalies $\langle \Delta \phi \rangle_S(x,y)$ for a season $s$, "
            r"a three-dimensional variable $\phi(x,y,t)$ and a three-dimensional reference field $\phi_{\mathrm{ref}}(x,y,t)$ i.e."
            r"$$ \langle \Delta \phi \rangle_S(x,y) = \frac{1}{N_S} \sum_{t\in S} \phi(x,y,t) - \phi_{\mathrm{ref}}(x,y,t) = \langle \phi \rangle_S(x,y) - \langle \phi_{\mathrm{ref}} \rangle_S(x,y) , $$"
            f"where $t$ are all time steps that are contained in season $S$. The number of these time steps is given by $N_S$, where the considered time period is from `{from_date}` to `{to_date}`."
            ),
            "caption-template" : 
            ("<b> Seasonal anomalies for variable {var_name}. </b>"
            "The rows correspond to different models whereas the columns reflect the various seaons that are considered."
            "The $x$ and $y$ axis measure the longitudes and latitudes, respectively."
            ),
        },

        "draw_stations_and_regions" : {
            "name" : "Stations and Regions",
            "text" : 
            ("This task generates an image with the configured staitons and regions for which time series data is generated."
            "For regions the time series is generated as the spatial mean over this region."
            "Whereas for stations a remapping to the nearest neighboring grid cell is performed."
            ),  
            "caption-template" : 
            ("<b> Stations and regions for variable {var_name}. </b>"
            "Colored areas depict the different regions. The dots are located at the station's coordinates."
            ),
        },

        "compare_time_series" : {
            "name" : "Time series",
            "text" : 
            ("This task generates figures of temporal means according to the configured time-series operators, "
            "e.g. if you specfied `time_series_operators = [\"-monmean\"]`, a plot with monthly means is generated."
            "Please refer to the `cdo` documentation for more information on these operators."
            "If there are more than 100 samples in the time series and it is compared to reference data, "
            "a scatter plot is generated, where the $x$ and $y$ coordinates correspond to the reference samples and the model ones, respectively."
            ),
            "caption-template" : 
            ("<b>Time series for variable {var_name}. </b>"
            r"Shaded areas depict the $\pm 2 \sigma$ vicinity (approximately the 95% confidence interval) around the mean values."
            ),      
        },

        "create_taylor_diagrams" : {
            "name" : "Taylor Diagrams",
            "text" : 
            ("Taylor diagrams graphically indicate which of several model data represents best a given reference data." 
            "In order to quantify the degree of correspondence between the modeled and observed behavior in terms of three statistics:" 
            "the Pearson correlation coefficient, the root-mean-square error (RMSE) error, and the standard deviation."
            f"Here both data, model and reference, consist of the same number of samples that correspond to a time series starting from `{from_date}` and ending at `{to_date}`."
            ),

            "caption-template" : 
            ("<b> Taylor diagrams for variable {var_name}. </b>"
            "Colored stars stand for the model result and the black circle is the reference."
            "The standard deviation of the data is measured on the radial axis whereas the correaltion to the reference is given by the angle;"
            "depicted is the arcus cosine of the angle."
            "The colormap refers to the root means square error of the model data with respect to the reference data."
            "The rows correspond to the different regions and stations whereas the columns are related to the different kind of time series."
            ),
        },

        "get_cost_function" : {
            "name" : "Cost functions",
            "text" : 
            ("The cost function $c$ as it is defined here, further summarizes the information given in a Taylor diagram."
            r"It measures the root means square error $\epsilon = \sqrt{\frac{1}{N}\sum_{t=t_1}^{t_{N}} (\phi(t)-\phi_{\mathrm{ref}}(t))^2}$ of the model data $\phi(t)$"
            r"in units of the standard deviation $\sigma_{\mathrm{ref}}$ of reference data $\phi_{\mathrm{ref}}(t)$, i.e."
            r"$$ c = \epsilon / \sigma_{\mathrm{ref}}. $$"
            r"Both data consist of $N$ samples corresponding to a time series starting from $t_1$ and ending at $t_N$."
            ),
            "caption-template" : 
            ("<b> Cost functions $c$ for variable {var_name}. </b>"
            r"The colors refer to the magnitude of the cost function: green means very good $( 0 \leq c < 1 )$,"
            r"yellow stands for satisfactory $( 1 < c < 2 )$ and red shows bad quality $( c \geq 2 )$."
            "<b>Bold</b> numbers correspond to the best performing model, whereas <i>italic</i> number refer to the worst performing model for that particular station/region and kind of time series."
            "The rows correspond to the different regions and stations whereas the columns are related to the different temporal means and models."
            ),
        },

        "compare_vertical_profiles" : {
            "name" : "Vertical profiles",
            "text" : 
            ("This task generates vertical profiles of a four-dimensional field $\phi(x, y, z, t)$ at configured stations (using remapping to nearest neighbors) "
            "accompanied by performing the configured seasonal means."
            "Vertical profiles that correspong to regions are created by an additional spatial mean over the particular region."
            ),
            "caption-template" : 
            ("<b> Vertical profiles for variable {var_name}. </b>"
            r"Shaded areas depict the 95% confidence interval around the mean values."
            ),        
        },
    }

    return tasks
