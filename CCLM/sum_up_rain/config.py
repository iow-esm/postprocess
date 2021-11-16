dependencies = ["process_raw_output"]

import sys
sys.path.append('../../auxiliary')
from arithmetics import Arithmetics

variables = [Arithmetics(operator = "add", new_variable = "RAIN_TOT", old_variables = ["RAIN_CON", "RAIN_GSP"],
                            standard_name = "total_rainfall_amount", long_name = "total rainfall")]