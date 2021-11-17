dependencies = ["process_raw_output"]

import sys
sys.path.append('../../auxiliary')
from arithmetics import Arithmetics

variables = [Arithmetics(operator = "add", new_variable = "ASWD_S", old_variables = ["ASWDIR_S", "ASWDIFD_S"],
                            standard_name = "averaged_total_sw_downward_radiation", long_name = "averaged total shortwave downward radiation at surface")]