# this depends on a processed raw output
dependencies = ["process_raw_output"]

import sys
sys.path.append('../')
import global_settings

seasons = global_settings.seasons

variables = global_settings.variables.keys()