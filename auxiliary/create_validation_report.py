import sys

out_dir = str(sys.argv[1])
from_date = int(sys.argv[2])
to_date = int(sys.argv[3])
pwd = str(sys.argv[4])

import create_results_dir

results_dir = create_results_dir.create_results_dir(out_dir, from_date, to_date)

from datetime import datetime
import glob
import os

from helpers import get_n_colors

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




sys.path.append("../")
import global_settings
variables = global_settings.variables

try:
    name = f"|**Name:** | **`{global_settings.name}`**|"
except:
    name = "|||"

try:
    user = os.getlogin()
except:
    try:
        user = os.environ.get("USER")
    except:
        user = "unknown"

out_dir_parts = [""]
max_column_length = 45
if len(out_dir) > max_column_length:
    parts = out_dir.split("/")
    for part in parts:
        if part == "":
            continue
        if len(out_dir_parts[-1]+"/"+part) < max_column_length:
            out_dir_parts[-1] += "/"+part
        else:
            if len(part) > max_column_length:
                sub_parts = part.split("_")
                try:
                    sub_parts.remove("")
                except:
                    pass
            else:
                sub_parts = [part]
            
            out_dir_parts.append("/")
            for i, sub in enumerate(sub_parts):
                if len(out_dir_parts[-1]+sub) < max_column_length:
                    out_dir_parts[-1] += sub
                else:
                    out_dir_parts.append(sub)
                if i != len(sub_parts)-1:
                    out_dir_parts[-1] += "_"
else:
    out_dir_parts = [out_dir]

model_name = out_dir_parts[-1].split("/")[-1]
script = f"""# Validation report for '`{model_name}`'

## General information

|||
|---|---|
{name}
|Created at:                    |`{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}`|
|Created for output directory:  |`{out_dir_parts[0]}`|
"""

for i in range(1, len(out_dir_parts)):
    script += f"|                               |`{out_dir_parts[i]}`|\n"

script += f"""|Start date:                    |`{from_date}`|
|End date:                      |`{to_date}`|
|User:                          |`{user}`|


"""

try: 
    script += f"""
    
### Report description

{global_settings.report_description}

    """
except:
    pass

float_colors = get_n_colors(1)[0]
int_colors = []
for i in range(3):
    int_colors.append(int(255*float_colors[i]))
int_colors.append(0.5*float_colors[3])
int_colors = tuple(int_colors)

try:
    this_model = global_settings.this_model
    
    script += fr"""

### Model description

<hr style="border:1px solid gray">

<h4 style="background-color: rgba{int_colors};"><b>`{this_model}`</b></h4>

"""
except:
    script += fr"""

### Model description

<hr style="border:1px solid gray">

<h4 style="background-color: rgba{int_colors};"><b>`model1`</b></h4>

"""

try:
    description = global_settings.this_model_description
    script += f"""

{description}

    """
except:
    pass

script += """

### Performed tasks

<hr style="border:1px solid gray">


"""

for task in tasks.keys():
    script += "#### **"+tasks[task]["name"]+"**\n\n" 
    try:
        script += tasks[task]["text"]+"\n\n\n" 
    except:
        pass

script += """

## Results

"""

fig_counter = 0
for i, var in enumerate(variables.keys()):
    try:
        var_name = variables[var]["long-name"]+" ("+var+")"
    except:
        var_name = var

    if "(" in var_name: # if it is a long name ensure that starts with capital letter
        section = var_name[0].upper()+var_name[1:]
    else:
        section = var_name

    script += f"""

### {section}   

<hr style="border:2px solid gray">

<details>
<summary><b><i>Analysis</i></b></summary>

    """
    
    try:
        description = "#### **Description**\n\n"
        description += variables[var]["description"]
    except:
        description = ""

    try:
        variables[var]["reference-description"]
        description += "\n\n#### **Reference description**\n\n"
        description += variables[var]["reference-description"]
    except:
        pass

    try:
        other_models = variables[var]["other-models"]
        if other_models != {}:
            description += "\n\n#### **Comparison to other models**\n\n  $\\vphantom{M}$ \n\n"
            RGB_tuples = get_n_colors(len(other_models.keys())+1)
            for i, om in enumerate(other_models.keys()):
                float_colors = RGB_tuples[i+1]
                int_colors = []
                for i in range(3):
                    int_colors.append(int(255*float_colors[i]))
                int_colors.append(0.5*float_colors[3])
                int_colors = tuple(int_colors)
                description += f"""\n<h5 style="background-color: rgba{int_colors};"><b>`{om}`</b></h5>\n\n"""
                try:
                    description += other_models[om]["description"]+"\n"
                except:
                    description += "\n"
    except:
        pass

    script += f"""

{description}

"""

    script += f"""

<details>
<summary><i> Postprocess settings for variable {var_name} </i></summary>

[**Go to settings ->**](../../../global_settings.py)

    """
    script += "\n"
    for a in variables[var].keys():
        script += "##### "+a+"\n"
        script += "`"+str(variables[var][a])+"`\n"
        script += "\n"+r'<hr style="border:1px solid gray">'+"\n\n"
    script += "\n"

    script += """

</details>

    """
    for task in tasks.keys():
    
        figure_patterns = ["../"+task+"/"+results_dir+"/"+var+".png", "../"+task+"/"+results_dir+"/"+var+"-*.png"]

        figures = ""

        os.system("mkdir -p "+results_dir+"/figures/"+task)

        for pattern in figure_patterns:

            for fig in glob.glob(pattern):
                fig_counter += 1
                try:
                    caption = tasks[task]["caption-template"].format(var_name=var_name)
                except:
                    caption = "<b>"+tasks[task]["name"]+".</b> Plots for variable "+var_name+"."

                os.system("ln -s `realpath "+fig+"` "+results_dir+"/figures/"+task+"/")

                figures += f"""

 $\\vphantom{{M}}$

![](./figures/{task}/{fig.split("/")[-1]})
<figure>
    <figcaption align = "center"> <b> Fig. {fig_counter}: </b> {caption} </figcaption>
</figure>  

"""   
        # if there a figures we create a subsection for this task
        if figures != "":

            script += f"""
#### **{tasks[task]["name"]}**

<hr style="border:1px solid gray">

<details>
<summary><b><i>Figures</b></i></summary>

[**Go to notebook ->**](../../../{task}/{results_dir}/{task}.ipynb)

{figures}

</details>

"""

    script += """

</details>

"""
f = open(pwd+"/"+results_dir+"/validation_report.md", "w")
f.write(script)
f.close()

import convertpy2ipynb
convertpy2ipynb.convertpy2ipynb(pwd+"/"+results_dir+"/validation_report.md", cell_type="markdown")