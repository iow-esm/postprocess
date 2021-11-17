# this depends on a processed raw output
dependencies = ["process_raw_output", "sum_up_radiation"]

seasons = {
    "MAM" : "3,4,5",
    "JJA" : "6,7,8",
    "SON" : "9,10,11",
    "DJF" : "12,1,2"
}

variables = ["T_2M_AV", "ASWD_S", "TOT_PREC"]