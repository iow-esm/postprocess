# this depends on a processed raw output
dependencies = ["process_raw_output"]

seasons = {
    "MAM" : "3,4,5",
    "JJA" : "6,7,8",
    "SON" : "9,10,11",
    "DJF" : "12,1,2"
}

variables = ["SSS", "SST", "SSH", "FI"]
percentiles = ["95", "5"]