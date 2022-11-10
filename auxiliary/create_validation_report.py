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
    "compare_vertical_profiles" : {"name" : "Vertical profiles"},
}



sys.path.append("../")
import global_settings
variables = global_settings.variables

script = f"""# Validation report

## General information

|||
|---|---|
|Created at                     |`{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}`|
|Created for output directory:  |`{out_dir}`|
|Start date:                    |`{from_date}`|
|End date:                      |`{to_date}`|
|Author:                        |`{os.getlogin()}`|


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