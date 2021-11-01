import glob
import os
import sys

out_dir = str(sys.argv[1])
from_date = int(sys.argv[2])
to_date = int(sys.argv[3])

import config
variables = config.variables


sys.path.append('../../auxiliary')
import create_results_dir

results_dir = create_results_dir.create_results_dir(out_dir, from_date, to_date)

