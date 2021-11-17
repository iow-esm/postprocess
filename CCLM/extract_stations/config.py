dependencies = ["process_reference", "process_raw_output"]

stations = { 
    "ROSTOCK-WARNEMUNDE" : {"lat" : "54.18", "lon" : "12.08"},
    "HELSINKI-KAISANIEMI" : {"lat" : "60.18", "lon" : "24.95"},
    "STOCKHOLM" : {"lat" : "59.35", "lon" : "18.05"},
    "TALLINN" : {"lat" : "59:23:53", "lon" : "24:36:10"},
    "VISBY" : {"lat" : "57:40:00", "lon" : "18:19:59"},
    "SUNDSVALL" : {"lat" : "62:24:36", "lon" : "17:16:12"},
    "LULEA" : {"lat" : "65:37:12", "lon" : "22:07:48"},
    "VAASA-PALOSAARI" : {"lat" : "63:06:00", "lon" : "21:36:00"},
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
                         },
    "ASWD_S" : {
                "stations" : stations,
                "operators" : operators,
                },   
    "ASWD_S-reference" : {
                            "stations" : stations,
                            "task" : "process_reference",
                            "file" : "ASWD_S.nc",
                            "operators" : operators,
                         }
}




