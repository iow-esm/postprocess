root = "/silod8/karsten"

import sys
sys.path.append('../../auxiliary')
from plot_config import PlotConfig

reference = {
    "SST" : {
        "reference-file-pattern" : root+"/obs/Copernicus/monthly/*-Baltic-ESACCI-L4_GHRSST-SSTdepth-OSTIA-GLOB_CDR2.0-v02.0-fv01.0.nc",
        "reference-variable-name" : "analysed_sst",
        "reference-additional-operators" : "-chname,lon,xt -chname,lat,yt -setattribute,analysed_sst@units=Celsius -subc,273.15",
        "plot-config-anomaly" : PlotConfig("SST", min_value = -5.0, max_value = 5.0, delta_value = 0.5, contour = True, color_map = 'seismic'),
    },
    "FI" : {
        "reference-file-pattern" : root+"/obs/Copernicus/monthly/*-Baltic-ESACCI-L4_GHRSST-SSTdepth-OSTIA-GLOB_CDR2.0-v02.0-fv01.0.nc",
        "reference-variable-name" : "sea_ice_fraction",
        "reference-additional-operators" : "-chname,lon,xt -chname,lat,yt",
        "plot-config-anomaly" : PlotConfig("FI", min_value = -0.6, max_value = 0.6, delta_value = 0.1, contour = True, color_map = 'seismic'),
    },
    "EVAP" : {},
    "swdn" : {},
    "lwdn" : {},
    "LH" : {},
    "SH" : {},
    "tau_x" : {},
    "tau_y" : {},
    "temp" : {
        "BED-reference-file-pattern" : root+"/obs/BEDValidationData_1/Monthly/*TEMP*.dat",
    },
    "salt" : {
        "BED-reference-file-pattern" : root+"/obs/BEDValidationData_1/Monthly/*SALIN*.dat",
    }
}

