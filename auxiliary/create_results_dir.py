import os

def create_results_dir(out_dir, from_date, to_date):

    # relate results uniquely to path to data (replace slashes by underscores)
    results_dir = "results/" + out_dir.replace("/","_")
    
    # if limits are given, add them to the name 
    if from_date > 0 and to_date > 0:
        results_dir += "-" + str(from_date) + "_" + str(to_date)
        
    # create directory
    os.system("mkdir -p " + results_dir)

    # return the path
    return results_dir

