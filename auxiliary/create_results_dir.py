import os
import glob

def create_results_dir(out_dir, from_date, to_date):

    import sys
    pwd = os.getcwd()
    sys.path.append(pwd+"/../")
    try:
        from global_settings import name
        prefix = name+"_"
    except:
        prefix = ""

    # relate results uniquely to path to data (replace slashes by underscores)
    output_folder = out_dir.split("/output/")[-1]
    results_dir = "results/" + prefix + output_folder.replace("/","_")
    
    # if limits are given, add them to the name 
    if from_date > 0 and to_date > 0:
        results_dir += "-" + str(from_date) + "_" + str(to_date)
        
    # if directory already exists, remove old one
    if glob.glob(results_dir):
        os.system("rm -r " + results_dir)

    # create directory
    os.system("mkdir -p " + results_dir)

    # return the path
    return results_dir

