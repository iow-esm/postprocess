dependencies = ["process_raw_output"]

import sys
sys.path.append('../')
import global_settings

seasons = global_settings.seasons

variables = global_settings.variables.keys()
percentiles = global_settings.percentiles

ranges = { "TOT_PREC" : "1,10000" }