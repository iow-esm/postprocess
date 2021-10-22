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

variable_names     = {
    "salt" : "MODEL_SALIN",
    "temp" : "MODEL_TEMP"
    }

depth_pattern = "st_ocean_*"

data_pattern = "rregion_*.nc*"

# return value has to be one of the keys in self.station_names
def extract_station_name(file_name):
    return file_name.split("rregion_")[1].split(".nc.")[0].split("_")[0]