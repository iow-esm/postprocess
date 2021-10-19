import glob
import os
import sys

out_dir = str(sys.argv[1])
from_date = int(sys.argv[2])
to_date = int(sys.argv[3])

import config
variables = config.variables
seasons = config.seasons

sys.path.append('../../auxiliary')
import get_all_dirs_from_to

dirs = get_all_dirs_from_to.get_all_dirs_from_to(out_dir, from_date, to_date)

import create_results_dir
results_dir = create_results_dir.create_results_dir(out_dir, from_date, to_date)

for var in variables:
    files=""
    for dir in dirs:
        files += dir + "/" + var + ".nc "
	
    for names, numbers in seasons.items():
        os.system("cdo -timmean -selmon," + numbers + " -cat \'" + files + "\' " + results_dir + "/" + var + "-" + names + ".nc")