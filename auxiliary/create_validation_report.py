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

tasks = {  
    "compare_2D_means" : {"name" : "2D means"},
    "compare_2D_anomalies" : {"name" : "2D anomalies"},
    "draw_stations_and_regions" : {"name" : "Stations and Regions"},
    "compare_time_series" : {"name" : "Time series"},
    "create_taylor_diagrams" : {
        "name" : "Taylor Diagrams",
        "text" : r"""
Taylor diagrams are mathematical diagrams designed to graphically indicate which of several approximate representations (or models) of a system, 
process, or phenomenon is most realistic. 
This diagram, invented by Karl E. Taylor in 1994 ([published in 2001](doi:10.1029/2000JD900719)) facilitates the comparative assessment of different models. 
It is used to quantify the degree of correspondence between the modeled and observed behavior in terms of three statistics: 
the Pearson correlation coefficient, the root-mean-square error (RMSE) error, and the standard deviation. 

(__Text taken from: [https://en.wikipedia.org/wiki/Taylor_diagram](https://en.wikipedia.org/wiki/Taylor_diagram)__)

The tables depicted below the taylor diagrams show the **cost function** $c$, which is here defined as
$$ c = \textrm{RMSE} / \sigma_{ref}, $$
where $\textrm{RMSE}$ is the root mean square error of each model and $\sigma_{ref}$ is the standard deviation of the reference data.
"""
        },
    "compare_vertical_profiles" : {"name" : "Vertical profiles"},
}



sys.path.append("../")
import global_settings
variables = global_settings.variables

try:
    name = f"|**Name:** | **`{global_settings.name}`**|"
except:
    name = "|||"

script = f"""# Validation report 

## General information

|||
|---|---|
{name}
|Created at:                     |`{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}`|
|Created for output directory:  |`{out_dir}`|
|Start date:                    |`{from_date}`|
|End date:                      |`{to_date}`|
|Author:                        |`{os.getlogin()}`|


### Performed tasks

"""

for task in tasks.keys():
    script += "#### "+tasks[task]["name"]+"\n\n" 
    try:
        script += tasks[task]["text"]+"\n\n\n" 
    except:
        pass

script += """

## Analyzed variables

"""

for i, var in enumerate(variables.keys()):
    script += f"""
[**{i+1}. {var} ->**](#{var})
"""

script += f"""


## Results

"""

for var in variables.keys():
    script += f"""


### {var}

<hr style="border:2px solid gray">

<details>

#### Postprocess settings

[**Go to settings ->**](../../../global_settings.py)

    """
    script += "\n"
    for a in variables[var].keys():
        script += "##### "+a+"\n"
        script += "`"+str(variables[var][a])+"`\n"
        script += "\n---\n"
    script += "\n"

    script += """

</details>

    """
    for task in tasks.keys():
    
        script += f"""
### {tasks[task]["name"]}

***
 
[**Go to notebook ->**](../../../{task}/{results_dir}/{task}.ipynb)

        """

        for fig in glob.glob("../"+task+"/"+results_dir+"/"+var+"*.png"):
            script += f"""
![{fig.split("/")[-4:]}](../../{fig})  

        """

f = open(pwd+"/"+results_dir+"/validation_report.md", "w")
f.write(script)
f.close()

import convertpy2ipynb
convertpy2ipynb.convertpy2ipynb(pwd+"/"+results_dir+"/validation_report.md", cell_type="markdown")