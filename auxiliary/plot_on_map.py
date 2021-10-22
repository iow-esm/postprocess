import glob
import os
import sys

out_dir = str(sys.argv[1])
from_date = int(sys.argv[2])
to_date = int(sys.argv[3])
pwd = str(sys.argv[4])

import numpy as np

import create_results_dir
from plot_basics import *

results_dir = create_results_dir.create_results_dir(out_dir, from_date, to_date)

sys.path.append(pwd)
import config
plot_configs = config.plot_configs
    
plot_on_map(plot_configs, results_dir)