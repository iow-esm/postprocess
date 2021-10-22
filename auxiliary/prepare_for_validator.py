# import necessary python modules
import glob
import sys

# decode input arguments
out_dir = str(sys.argv[1])
from_date = int(sys.argv[2])
to_date = int(sys.argv[3])
pwd = str(sys.argv[4])

# import validator preparator modules:
# base classes
sys.path.append(pwd + "/validator_preparator")
print(pwd + "/validator_preparator")
import validator_preparator

# prepare parameters for the preparator
parameters = validator_preparator.ValidatorParameters()

# get all dirs with results
import get_all_dirs_from_to
dirs = get_all_dirs_from_to.get_all_dirs_from_to(out_dir, from_date, to_date)

# construct proper results_dir
import create_results_dir
results_dir = create_results_dir.create_results_dir(out_dir, from_date, to_date)

# import config
sys.path.append(pwd)
import config

# build up list of files (use absolute paths, with read permissions!)
parameters.paths_to_data = []
for dir in dirs:
    parameters.paths_to_data += glob.glob(dir + "/" + config.data_pattern)
    
# where should the output be stored (you need write permissions there)
parameters.path_to_output = results_dir

# create an instance of a vaildator preparator
# instantiate it with the parameters
preparator = validator_preparator.ValidatorPreparator(parameters=parameters, 
                                                      variable_names=config.variable_names, 
                                                      station_names=config.station_names, 
                                                      depth_pattern=config.depth_pattern,
                                                      extract_station_name_function=config.extract_station_name)
# do the preparation
preparator.prepare_for_validation()

# have a look into output path, 
# copy files to a place where the validator can handle it (/silod5)
# be sure that all have read permissions for this location