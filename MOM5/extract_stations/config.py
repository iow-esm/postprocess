dependencies = ["process_reference", "process_raw_output"]

stations = { 
        "BY5" : {"lat" : "55.25", "lon" : "15.98"},
        "F9" : {"lat" : "64.71", "lon" : "22.07"},
        "SR5" : {"lat" : "61.08", "lon" : "19.58"},
        "BY31" : {"lat" : "58.58", "lon" : "18.23"}        
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
                         },
    "FI" : {
                "stations" : stations,
                "operators" : operators,
                },   
    "FI-reference" : {
                            "stations" : stations,
                            "task" : "process_reference",
                            "file" : "FI.nc",
                            "operators" : operators,
                         }                         
}




