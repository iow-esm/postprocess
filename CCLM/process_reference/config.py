seasons = {
    "MAM" : "3,4,5",
    "JJA" : "6,7,8",
    "SON" : "9,10,11",
    "DJF" : "12,1,2"
}

percentiles = ["95", "5"]

reference = "E-OBS"


if reference == "E-OBS":
    variables = {"T_2M" : "tg_ens_mean_0.1deg_reg_v23.1e"}
else:
    variables = {}


