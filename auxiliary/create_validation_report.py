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

import validation_tasks

tasks = validation_tasks.get_tasks(from_date = from_date, to_date = to_date)

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