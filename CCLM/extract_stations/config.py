dependencies = ["process_reference", "process_raw_output"]

stations = { 
    "ROSTOCK-WARNEMUNDE" : {"lat" : "54.18", "lon" : "12.08"}                               
}

operators = ["-monmean", "-seasmean", "-ymonmean", "-yseasmean"]
     
variables = {
    "ASOB_S" : {
                "stations" : stations,
                "operators" : operators,
                },   
    "ASOB_S-reference" : {
                            "stations" : stations,
                            "task" : "process_reference",
                            "file" : "ASOB_S.nc",
                            "operators" : operators,
                         }
}




