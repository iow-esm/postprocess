# assign your station names (left, as they appear in the output files) to the validator names (right, see , see https://openresearchsoftware.metajnl.com/articles/10.5334/jors.259/ and https://github.com/hagenradtke/validator)
station_names = {
    "AnholtE"           : "anholte",
    "ArkonaBY2"         : "by2",
    "BornholmDeepBY5"   : "by5",
    "BothnianBayF9"     : "f9",
    "BothnianSeaSR5"    : "sr5",
    "BothnianSeaUS3"    : "us3",
    "FehmarnBelt"       : "fehnmarn",
    "GdanskDeep"        : "gdansk",
    "GotlandDeepBY15"   : "by15",
    "GreatBelt"         : "greatbelt",
    "GulfFinlandLL7"    : "ll7",
    "GulfofFinlandF1"   : "f1",
    "GulfofRiga"        : "gulfofriga",
    "LandskronaW"       : "landskron",
    "LandsortDeepBY31"  : "by31",
    "SEGotlandBasin"    : "segotlandbasin"
    }

# assign your variable names to the validator variable names
variable_names     = {
    "salt" : "MODEL_SALIN",
    "temp" : "MODEL_TEMP"
    }

# how is the vertical axis called in your output (regular expressions are possible)
depth_pattern = "st_ocean_*"

# how are station files called in output/<model>/<run>/<date>/
data_pattern = "rregion_*.nc*"

# how to extract the station name (defined in the above dictionary) from the file name
# return value has to be one of the keys in station_names
def extract_station_name(file_name):
    return file_name.split("rregion_")[1].split(".nc.")[0].split("_")[0]