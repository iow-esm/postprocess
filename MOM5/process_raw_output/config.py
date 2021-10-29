# prefixes of raw files that should be processed
files_to_process = ["ocean_day2d", "ocean_day3d", "ice_day", "ocean_trps", "ergom_flux3d", "ergom_flux_surf", "ergom_flux_sed"]

station_pattern = "rregion_*"

# path to the MOM tool for combination of raw output 
path_to_mppn = "../../../components/MOM5/src/postprocessing/mppnccombine" # relative to this directory 