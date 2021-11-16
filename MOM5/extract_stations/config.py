dependencies = ["process_reference", "process_raw_output"]

stations = { 
        "BY5" : {"lat" : "55.25", "lon" : "15.98"}                               
}

operators = ["-monmean", "-seasmean", "-ymonmean", "-yseasmean"]
     
variables = {
    "SST" : {
                "stations" : stations,
                "operators" : operators,
                },   
    "SST-reference" : {
                            "stations" : stations,
                            "task" : "process_reference",
                            "file" : "SST.nc",
                            "operators" : operators,
                         }
}




