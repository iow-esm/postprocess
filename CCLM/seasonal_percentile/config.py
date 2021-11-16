dependencies = ["process_raw_output"]

seasons = {
    "MAM" : "3,4,5",
    "JJA" : "6,7,8",
    "SON" : "9,10,11",
    "DJF" : "12,1,2"
}

variables = ["T_2M_AV", "TOT_PREC"]
percentiles = ["95", "5", "25"]

ranges = { "TOT_PREC" : "1,10000" }