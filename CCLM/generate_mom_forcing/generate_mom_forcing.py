import glob
import os
import sys

out_dir = str(sys.argv[1])
from_date = int(sys.argv[2])
to_date = int(sys.argv[3])
pwd = str(sys.argv[4])

sys.path.append(pwd)
import config

try:
    max_jobs=config.max_jobs
except:
    max_jobs = 1

remapping_file_path = None
remapping = None

try:
    remapping_file_path = config.remapping_file_path
except:
    try: 
        remapping = config.remapping
    except:
        print("No remapping is specified! Created files might not work for MOM5 model.")

sys.path.append('../../auxiliary')
import get_all_dirs_from_to

dirs = get_all_dirs_from_to.get_all_dirs_from_to(out_dir, from_date, to_date)

import create_results_dir
results_dir = create_results_dir.create_results_dir(out_dir, from_date, to_date)

if (remapping_file_path is None) and (remapping is not None):
    remapping_file_path = results_dir + "/remapping.txt"
    f = open(remapping_file_path, "w")
    f.write(remapping)
    f.close()
    do_remapping = "-remapbil," + remapping_file_path
else:
    do_remapping = ""

# input variables from CCLM that are used
variables = ["T_2M", "U_10M", "V_10M", "PMSL", "CLCT", "QV_2M", "TOT_PREC", "ASWD_S", "ALWD_S"]

# store original directories
original_dirs = dirs[:]

# check if input is compressed
for i, dir in enumerate(dirs):

    # take only tar.gz archives into
    if dir[-7:] != ".tar.gz":
        continue

    # take directory name without ending
    dir = dir[:-7]
    
    # create output directory with date
    output_dir = results_dir + "/" + dir.split("/")[-1]
    os.system("mkdir -p " + output_dir)

    # get list of files that should be extracted
    extract = ""
    cmd = "cd "+output_dir+"\n"
    for j, var in enumerate(variables):
        cmd += "tar -zxvf "+dir+".tar.gz "+dir.split("/")[-1]+"/"+var+".nc"
        
        if ((j+1) % config.max_jobs == 0) or (j == len(variables)-1):
            cmd += "\n wait \n"
            os.system(cmd)
            cmd = "cd "+output_dir+"\n"
        else:
            cmd += " & \n"

    # extract them into the results dir
    #os.system("cd "+output_dir+"; tar -zxvf "+dir+".tar.gz "+extract)

    # replace original directory with the new one
    dirs[i] = output_dir+"/"+dir.split("/")[-1]

for i, dir in enumerate(dirs):        

    # make output directory according to time slice of input directory
    output_dir = results_dir + "/" + dir.split("/")[-1]
    os.system("mkdir -p " + output_dir)
    
    # preprocess output: get possibly missing time step from next output of next time slice
    for var in variables:
        # start with empty seldate operator for cdo
        seldate = ""
        # current time slice is always an input
        inputs = dir + "/" + var + ".nc "
        
        # if there is a next output
        if (i < (len(dirs) - 1)): 
            # directory of next time slice is also part of input
            dir_p1 = dirs[i + 1]
            inputs += dir_p1 + "/" + var + ".nc"
            
            # transform date format from YYYYMMDD to YYYY-MM-DD for cdo
            # next time slice
            tp1 = dir_p1.split("/")[-1]
            tp1 = tp1[0:4] + "-" + tp1[4:6] + "-" + tp1[6:8]
            # current time slice
            t = dir.split("/")[-1]
            t = t[0:4] + "-" + t[4:6] + "-" + t[6:8]
            
            # assemble seldate operator
            seldate = "-seldate," + t + "T00:00:00," + tp1 + "T00:00:00"
        
        # perform preprocessing, store output in output_dir
        cmd = "cdo " + seldate + " -cat " + inputs + " " + output_dir + "/" + var + ".nc"
        os.system(cmd)
        
    # perform transformation for this time slice
    
    ##### temperature T_2M -> tairK
    cmd = "cdo "
    cmd += "-L -chname,T_2M,tairK "+do_remapping 
    cmd += " " + output_dir + "/T_2M.nc " + output_dir + "/tairK.mom.dta.nc"
    os.system(cmd)
    
    cmd = "ncatted -a cartesian_axis,lon,o,c,X -a cartesian_axis,lat,o,c,Y  " + output_dir + "/tairK.mom.dta.nc"
    os.system(cmd)
    
    cmd = "ncatted -a cartesian_axis,time,o,c,T -a calendar,time,o,c,julian " + output_dir + "/tairK.mom.dta.nc"
    os.system(cmd)
    
    
    ##### wind stress U_10M,V_10m -> windx, windy
    cmd = "cdo "
    cmd += "merge " + output_dir + "/U_10M.nc " + output_dir + "/V_10M.nc " + output_dir + "/UV10.nc"
    os.system(cmd)
    
    cmd = "export IGNORE_ATT_COORDINATES=1; cdo "
    cmd += "-L -chname,U_10M,windx,V_10M,windy "+do_remapping + " -rotuvb,U_10M,V_10M"
    cmd += " " + output_dir + "/UV10.nc " + output_dir + "/windxy.nc"
    os.system(cmd)
    
    cmd = "cdo "
    cmd += "selvar,windx " + output_dir + "/windxy.nc " + output_dir + "/windx.mom.dta.nc "
    os.system(cmd)
    
    cmd = "ncatted -a cartesian_axis,lon,o,c,X -a cartesian_axis,lat,o,c,Y  " + output_dir + "/windx.mom.dta.nc"
    os.system(cmd)
    
    cmd = "ncatted -a cartesian_axis,time,o,c,T -a calendar,time,o,c,julian " + output_dir + "/windx.mom.dta.nc"
    os.system(cmd)
    
    cmd = "cdo "
    cmd += "selvar,windy " + output_dir + "/windxy.nc " + output_dir + "/windy.mom.dta.nc "
    os.system(cmd)
    
    cmd = "ncatted -a cartesian_axis,lon,o,c,X -a cartesian_axis,lat,o,c,Y  " + output_dir + "/windy.mom.dta.nc"
    os.system(cmd)

    cmd = "ncatted -a cartesian_axis,time,o,c,T -a calendar,time,o,c,julian " + output_dir + "/windy.mom.dta.nc"
    os.system(cmd)
    
    cmd = "rm " + output_dir + "/UV10.nc " + output_dir + "/windxy.nc"
    os.system(cmd)

    ##### pressure PMSL -> pair
    cmd = "cdo "
    cmd += "-L -chname,PMSL,pair -mulc,0.01 "+do_remapping 
    cmd += " " + output_dir + "/PMSL.nc " + output_dir + "/pair.mom.dta.nc"
    os.system(cmd)
    
    cmd = "ncatted -a units,pair,o,c,hPa " + output_dir + "/pair.mom.dta.nc"
    os.system(cmd)
    
    cmd = "ncatted -a cartesian_axis,lon,o,c,X -a cartesian_axis,lat,o,c,Y " + output_dir + "/pair.mom.dta.nc"
    os.system(cmd)
    
    cmd = "ncatted -a cartesian_axis,time,o,c,T -a calendar,time,o,c,julian " + output_dir + "/pair.mom.dta.nc"
    os.system(cmd)
    
    ##### cloud cover CLCT -> clour
    cmd = "cdo "
    cmd += "-L -chname,CLCT,clour "+do_remapping 
    cmd += " " + output_dir + "/CLCT.nc " + output_dir + "/clour.mom.dta.nc"
    os.system(cmd)
    
    cmd = "ncatted -a cartesian_axis,lon,o,c,X -a cartesian_axis,lat,o,c,Y " + output_dir + "/clour.mom.dta.nc"
    os.system(cmd)
 
    cmd = "ncatted -a cartesian_axis,time,o,c,T -a calendar,time,o,c,julian " + output_dir + "/clour.mom.dta.nc"
    os.system(cmd)
    
    ##### specific humidity QV_2M -> shumi
    cmd = "cdo "
    cmd += "-L -chname,QV_2M,shumi "+do_remapping 
    cmd += " " + output_dir + "/QV_2M.nc " + output_dir + "/shumi.mom.dta.nc"
    os.system(cmd)
    
    cmd = "ncatted -a cartesian_axis,lon,o,c,X -a cartesian_axis,lat,o,c,Y " + output_dir + "/shumi.mom.dta.nc"
    os.system(cmd)
    
    cmd = "ncatted -a cartesian_axis,time,o,c,T -a calendar,time,o,c,julian " + output_dir + "/shumi.mom.dta.nc"
    os.system(cmd)
    
    ##### precipitation TOT_PREC -> rain, snow
    cmd = "cdo "
    cmd += "-L -chname,TOT_PREC,prec -divc,3600.0 "+do_remapping 
    cmd += " " + output_dir + "/TOT_PREC.nc " + output_dir + "/prec.mom.dta.nc"
    os.system(cmd)
    
    cmd = "ncatted -a units,prec,o,c,\"kg m-2 s-1\" " + output_dir + "/prec.mom.dta.nc"
    os.system(cmd)
    
    cmd = "ncatted -a cartesian_axis,lon,o,c,X -a cartesian_axis,lat,o,c,Y " + output_dir + "/prec.mom.dta.nc"
    os.system(cmd)
    
    cmd = "ncatted -a cartesian_axis,time,o,c,T -a calendar,time,o,c,julian " + output_dir + "/prec.mom.dta.nc"
    os.system(cmd)
    
    f = open(output_dir + "/rain.nco", "w")
    f.write("rain = prec;\n")
    f.write("where(tairK < 273.15){\n")
    f.write("   rain = 0.0;\n")
    f.write("}\n")
    f.close()
    
    f = open(output_dir + "/snow.nco", "w")
    f.write("snow = prec;\n")
    f.write("where(tairK >= 273.15){\n")
    f.write("   snow = 0.0;\n")
    f.write("}\n")
    f.close()
    
    cmd = "cp " + output_dir + "/prec.mom.dta.nc " + output_dir + "/rain_snow.tmp1.nc; "
    cmd += "ncks -A " + output_dir + "/tairK.mom.dta.nc " + output_dir + "/rain_snow.tmp1.nc"
    os.system(cmd)
    
    cmd = "ncap2 -O -v -S " + output_dir + "/rain.nco " + output_dir + "/rain_snow.tmp1.nc " + output_dir + "/rain.mom.dta.nc"
    os.system(cmd)
    
    cmd = "ncap2 -O -v -S " + output_dir + "/snow.nco " + output_dir + "/rain_snow.tmp1.nc " + output_dir + "/snow.mom.dta.nc"
    os.system(cmd)
    
    cmd = "rm " + output_dir + "/rain_snow.tmp1.nc"
    os.system(cmd)
    
    ##### shortwave radiation ASOB_S -> swdn
    cmd = "cdo "
    cmd += "-L -chname,ASWD_S,swdn "+do_remapping 
    cmd += " " + output_dir + "/ASWD_S.nc " + output_dir + "/swdn.mom.dta.nc"
    os.system(cmd)
    
    cmd = "ncatted -a cartesian_axis,lon,o,c,X -a cartesian_axis,lat,o,c,Y " + output_dir + "/swdn.mom.dta.nc"
    os.system(cmd)  

    cmd = "ncatted -a cartesian_axis,time,o,c,T -a calendar,time,o,c,julian " + output_dir + "/swdn.mom.dta.nc"
    os.system(cmd)      
    
    ##### longwave radiation ALWD_S -> lwdn
    cmd = "cdo "
    cmd += "-L -chname,ALWD_S,lwdn "+do_remapping 
    cmd += " " + output_dir + "/ALWD_S.nc " + output_dir + "/lwdn.mom.dta.nc"
    os.system(cmd)
    
    cmd = "ncatted -a cartesian_axis,lon,o,c,X -a cartesian_axis,lat,o,c,Y " + output_dir + "/lwdn.mom.dta.nc"
    os.system(cmd)   
    
    cmd = "ncatted -a cartesian_axis,time,o,c,T -a calendar,time,o,c,julian " + output_dir + "/lwdn.mom.dta.nc"
    os.system(cmd)  
    
    # remove preprocessed inputs
    for var in variables:
        cmd = "rm " + output_dir + "/" + var + ".nc"
        os.system(cmd)   

# check if orignal input was compressed
for i, dir in enumerate(original_dirs):

    # take only tar.gz archives into
    if dir[-7:] != ".tar.gz":
        continue

    # if yes, remove the extracted temporary files
    os.system("rm -r "+dirs[i])      