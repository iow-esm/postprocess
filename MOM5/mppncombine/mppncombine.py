import glob
import os
import sys

# decode the input arguments
out_dir = str(sys.argv[1])
from_date = int(sys.argv[2])
to_date = int(sys.argv[3])

# read the local config
from config import files_to_process, path_to_mppn, station_pattern

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
    
    # if there is no out_raw, there is nothing left to do
    if glob.glob(dir + "/out_raw") == []:
        continue
    
    print(dir)
    
    # bash array for files to be processed
    files_array = "("
    
    # go over all file types that should be processed
    for f in files_to_process:
        
        # construct the pattern for all files that should be processed
        files_pattern = f + "*.nc.????"
        
        # if there is no file left of this type, go on with the next type
        if glob.glob(dir + "/out_raw/" + files_pattern) == []:
            continue
            
        files_array += f + " "
        
        print(f)

    files_array = files_array[:-1] + ")"
        
    # since path_to_mppn is defined relative to the local one, we have to know the local one
    pwd = os.getcwd()

    # execute mppnccombine and combine all files of this type
    shellscript_name = dir + "/mppnccombine.sh"
    shellscript = open(shellscript_name, 'w')
    shellscript.writelines("files_to_process=" + files_array + "\n")
    shellscript.writelines("cd " + dir + "/out_raw/" + "\n")
    shellscript.writelines("for f in ${files_to_process[@]}; do " + "\n")
    shellscript.writelines("    while [ `jobs | wc -l` -ge " + max_jobs + " ]; do sleep 1; done " + "\n")
    shellscript.writelines("    " + pwd + "/" + path_to_mppn + "/mppnccombine -r -n4 -m -k 0 ${f}.nc ${f}*.nc.???? &" + "\n")
    shellscript.writelines("done " + "\n")
    shellscript.writelines("wait " + "\n")
    shellscript.close()
    
    command = "chmod u+x " + shellscript_name + "; " + shellscript_name
    print("execute: " + command, flush=True)
    os.system(command)
    
    os.system("rm " + shellscript_name)

    for f in files_to_process:
        
        # construct the pattern for all files that should be processed
        files_pattern = f + "*.nc.????"
    
        # check if the outputfile has been created
        output_file = f + "*.nc"
        # if not, try the next file type
        if glob.glob(dir + "/out_raw/" + output_file) == []:
            print("Error: " + output_file + " could not be found.")
            continue
        
        # move the output file one level up (out_raw should be removed when everything is done)
        os.system("mv " + dir + "/out_raw/" + output_file + " " + dir + "/" + f + ".nc")
        
    
    # save station data
    os.system("mv " + dir + "/out_raw/" + station_pattern + " " + dir + "/")
    
    # check if any real files (no links) are left in raw output, if not remove
    os.system("if [ `find " + dir + "/out_raw/ -mindepth 1 ! -type l | wc -l` -eq 0 ]; then  rm -r " + dir + "/out_raw; fi")