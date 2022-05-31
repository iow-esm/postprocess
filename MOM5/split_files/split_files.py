import glob
import os
import sys

# decode the input arguments
out_dir = str(sys.argv[1])
from_date = int(sys.argv[2])
to_date = int(sys.argv[3])

from config import files_to_process

try:
    from config import max_jobs
    max_jobs = str(max_jobs)
except:
    max_jobs = str(len(files_to_process))

# get all dirs to be processed
sys.path.append('../../auxiliary')
import get_all_dirs_from_to

dirs = get_all_dirs_from_to.get_all_dirs_from_to(out_dir, from_date, to_date)

# go over all desired directories
for dir in dirs:
    
    print(dir)
    
    # bash array for files to be processed
    files_array = "( "
    
    # go over all file types that should be processed
    for f in files_to_process:
        
        # construct the pattern for all files that should be processed
        files_pattern = f + ".nc"
        
        # if there is no file left of this type, go on with the next type
        if glob.glob(dir + "/" + files_pattern) == []:
            continue
            
        files_array += f + ".nc" + " "
        
        print(f)

    files_array = files_array[:-1] + ")"
    
    # extract all variables from the files
    shellscript_name = dir + "/extract_vars.sh"
    shellscript = open(shellscript_name, 'w')
    shellscript.writelines("files_to_process=" + files_array + "\n")
    shellscript.writelines("cd " + dir + "/ " + "\n")
    shellscript.writelines("for f in ${files_to_process[@]}; do " + "\n")
    shellscript.writelines("    for var in `cdo -showname ${f}  2> /dev/null | grep -v \"showname:\"`; do " + "\n") # skip last line showing info
    shellscript.writelines("        while [ `jobs | wc -l` -ge " + max_jobs + " ]; do sleep 1; done " + "\n")
    shellscript.writelines("        cdo -selname,$var ${f} $var.nc &" + "\n")
    shellscript.writelines("    done " + "\n")
    shellscript.writelines("done " + "\n")
    shellscript.writelines("wait " + "\n")
    shellscript.writelines("for f in ${files_to_process[@]}; do " + "\n")
    shellscript.writelines("    rm ${f}" + "\n")
    shellscript.writelines("done " + "\n")
    shellscript.close()
    
    command = "chmod u+x " + shellscript_name + "; source " + shellscript_name
    print("execute: " + command, flush=True)
    os.system(command)
    
    os.system("rm " + shellscript_name)
     
    # if ice concentration is available get the fraction of ice as a vertical sum over thickness
    if glob.glob(dir + "/CN.nc") != []:
        command = "cd " + dir + "/; "
        command += "cdo vertsum CN.nc FI.nc; "
        command += "cdo chname,CN,FI FI.nc tmp.nc && mv tmp.nc FI.nc; "
        command += "cdo setattribute,FI@long_name=\"fraction of ice\" FI.nc tmp.nc && mv tmp.nc FI.nc; "
        os.system(command)
     


