import os
import sys

out_dir = str(sys.argv[1])
from_date = int(sys.argv[2])
to_date = int(sys.argv[3])
pwd = str(sys.argv[4])

sys.path.append(pwd)
import config
variables = config.variables

import get_all_dirs_from_to
dirs = get_all_dirs_from_to.get_all_dirs_from_to(out_dir, from_date, to_date)

for var in variables:
    for dir in dirs:
        command = "cd " + dir + "; "
        command += "cdo " + var.operator + " " + var.old_variables[0] + ".nc " +  var.old_variables[1] + ".nc " + var.new_variable + ".nc; "
        command += "cdo chname," + var.old_variables[0] + "," + var.new_variable + " " + var.new_variable + ".nc " + var.new_variable + ".nc; "
        
        if var.standard_name != "":
            command += "cdo setattribute," + var.new_variable + "@standard_name=\"" + var.standard_name + "\" " + var.new_variable + ".nc " + var.new_variable + ".nc; "
            
        if var.long_name != "":
            command += "cdo setattribute," + var.new_variable + "@long_name=\"" + var.long_name + "\" " + var.new_variable + ".nc " + var.new_variable + ".nc; "
            
        os.system(command)
    