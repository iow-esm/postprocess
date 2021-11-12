# this depends on 
dependencies = ["process_raw_output", "process_reference"]

additional_files = { "FI-reference" : 
                        { "task" : "process_reference",
                          "file" : "FI-remapped.nc" }
                   }

operators = ["", "-yearmax", "-monmean", "-seasmean", "-monmax", "-yseasmean", "-ymonmean"]

sellonlatbox = "13,32,52,68"