import glob
import os
import sys

# decode the input arguments
out_dir = str(sys.argv[1])
from_date = int(sys.argv[2])
to_date = int(sys.argv[3])

# read the local config
from config import files_to_process, path_to_mppn

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
    
    # go over all file types that should be processed
    for f in files_to_process:
        
        # extract the year and month from the directory's name
        year = dir.split("/")[-1][0:4]
        month = dir.split("/")[-1][4:6]
        
        # construct the pattern for all files that should be processed
        files_pattern = f + "_" + year + "_" + month + ".nc.????"
        
        # if there is no file left of this type, go on with the next type
        if glob.glob(dir + "/out_raw/" + files_pattern) == []:
            continue
        
        print(f)
        
        # since path_to_mppn is defined relative to the local one, we have to know the local one
        pwd = os.getcwd()
    
        # execute mppnccombine and combine all files of this type
        command = "cd " + dir + "/out_raw/; "
        command += pwd + "/" + path_to_mppn + "/mppnccombine -n4 -d 3 -m -k 11 -r " + files_pattern
        os.system(command)
        
        # check if the outputfile has been created
        output_file = f + "_" + year + "_" + month + ".nc"
        # if not, try the next file type
        if glob.glob(dir + "/out_raw/" + output_file) == []:
            print("Error: " + output_file + " could not be found.")
            continue
        
        # move the output file one level up (out_raw should be removed when everything is done)
        os.system("mv " + dir + "/out_raw/" + output_file + " " + dir + "/" + output_file)
        os.system("rm " + dir + "/out_raw/" + files_pattern)
        
        # from combined file extract variable-specific files, and remove combined file afterwards
        command = "cd " + dir + "/; "
        command += "for var in `cdo -showname " +  output_file +" 2> /dev/null`; do "
        command += "cdo -selname,$var " + output_file + " $var.nc 2> /dev/null; done; "
        command += "rm " + output_file
        os.system(command)
     
    # save station data
    os.system("mv " + dir + "/out_raw/" + "rregion_* " + dir + "/")
    
    # check if any real files (no links) are left in raw output, if not remove
    os.system("if [ `find " + dir + "/out_raw/ -mindepth 1 ! -type l | wc -l` -eq 0 ]; then  rm -r " + dir + "/out_raw; fi")


