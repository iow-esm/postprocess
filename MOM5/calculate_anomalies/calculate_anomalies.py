
data_dir = "../seasonal_mean/results/_scratch_usr_mvkkarst_IOW_ESM_output_RUNXX_MOM5_Baltic-19810901_20091130"
reference_dir = "../process_reference/results/_scratch_usr_mvkkarst_obs_Copernicus-19810901_20091130"

seasons = ["MAM", "SON", "JJA", "DJF"]
variables = ["SST", "FI"]

import os
import sys

out_dir = str(sys.argv[1])
from_date = int(sys.argv[2])
to_date = int(sys.argv[3])

sys.path.append("../../auxiliary")
import create_results_dir

results_dir = create_results_dir.create_results_dir(out_dir, from_date, to_date)

files = {}
for season in seasons:
    for var in variables:
        command = "cdo -sub " + data_dir + "/" + var + "-" + season + ".nc "
        if var == "SST":
            command += "-subc,273.15 "
        command += reference_dir + "/" + var + "-" + season + "-remapped.nc "
        command += results_dir + "/" + var + "-" + season + ".nc "
        os.system(command)