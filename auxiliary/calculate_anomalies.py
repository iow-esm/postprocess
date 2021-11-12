import os
import sys

out_dir = str(sys.argv[1])
from_date = int(sys.argv[2])
to_date = int(sys.argv[3])
pwd = str(sys.argv[4])

import create_results_dir

results_dir = create_results_dir.create_results_dir(out_dir, from_date, to_date)

sys.path.append(pwd)
from config import file_pairs

for var in file_pairs.keys():
    command = "cdo -sub "
    
    try:
        command += file_pairs[var][0]["additional-operators"] + " "
    except:
        pass
        
    try:
        command += file_pairs[var][0]["path"] + "/" + file_pairs[var][0]["file"] + " "
    except:
        try:
            command += "../" + file_pairs[var][0]["task"] + "/" + results_dir + "/" + file_pairs[var][0]["file"] + " "
        except:
            command += "../" + file_pairs[var][0]["task"] + "/" + results_dir + "/" + var + ".nc "
            
    
    try:
        command += file_pairs[var][1]["additional-operators"] + " "
    except:
        pass
        
    try:
        command += file_pairs[var][1]["path"] + "/" + file_pairs[var][1]["file"] + " "
    except:
        try:
            command += "../" + file_pairs[var][1]["task"] + "/" + results_dir + "/" + file_pairs[var][1]["file"] + " "
        except:
            command += "../" + file_pairs[var][1]["task"] + "/" + results_dir + "/" + var + ".nc "
    
    command += results_dir + "/" + var + ".nc"
    
    os.system(command)