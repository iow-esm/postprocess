import glob
import os
import sys

out_dir = str(sys.argv[1])
from_date = int(sys.argv[2])
to_date = int(sys.argv[3])

from config import files_to_process, path_to_mppn

sys.path.append('../../auxiliary')
import get_all_dirs_from_to

dirs = get_all_dirs_from_to.get_all_dirs_from_to(out_dir, from_date, to_date)

for dir in dirs:
    
    if glob.glob(dir + "/out_raw") == []:
        continue
    
    print(dir)
    
    for f in files_to_process:
        
        year = dir.split("/")[-1][0:4]
        month = dir.split("/")[-1][4:6]
        
        files_pattern = f + "_" + year + "_" + month + ".nc.????"
        
        if glob.glob(dir + "/out_raw/" + files_pattern) == []:
            continue
        
        print(f)
        
        pwd = os.getcwd()
    
        command = "cd " + dir + "/out_raw/; "
        command += pwd + "/" + path_to_mppn + "/mppnccombine -n4 -d 3 -m -k 11 -r " + files_pattern
        os.system(command)
        
        output_file = f + "_" + year + "_" + month + ".nc"
        
        if glob.glob(dir + "/out_raw/" + output_file) == []:
            print("Error: " + output_file + " could not be found.")
            continue
        
        os.system("mv " + dir + "/out_raw/" + output_file + " " + dir + "/" + output_file)
        os.system("rm " + dir + "/out_raw/" + files_pattern)
        
        command = "cd " + dir + "/; "
        command += "for var in `cdo -showname " +  output_file +" 2> /dev/null`; do "
        command += "cdo -selname,$var " + output_file + " $var.nc 2> /dev/null; done; "
        command += "rm " + output_file
        os.system(command)
     
    # save station data
    os.system("mv " + dir + "/out_raw/" + "rregion_* " + dir + "/")
    
    # check if any real files (no links) are left in raw output, if not remove
    os.system("if [ `find " + dir + "/out_raw/ -mindepth 1 ! -type l | wc -l` -eq 0 ]; then  rm -r " + dir + "/out_raw; fi")


