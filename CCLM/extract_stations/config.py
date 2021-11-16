dependencies = ["process_reference", "process_raw_output"]

stations = { 
    "ROSTOCK-WARNEMUNDE" : {"lat" : "54.18", "lon" : "12.08"}                                
}

operators = ["-monmean", "-seasmean", "-ymonmean", "-yseasmean"]
     
variables = {
    "T_2M_AV" : {
                "stations" : stations,
                "operators" : operators,
                },   
    "T_2M_AV-reference" : {
                            "stations" : stations,
                            "task" : "process_reference",
                            "file" : "T_2M_AV.nc",
                            "operators" : operators,
                         },
    "TOT_PREC" : {
                "stations" : stations,
                "operators" : operators,
                },   
    "TOT_PREC-reference" : {
                            "stations" : stations,
                            "task" : "process_reference",
                            "file" : "TOT_PREC.nc",
                            "operators" : operators,
                         }
}




