# this task does not depend on any other task
dependencies = ["mppncombine"]

# prefixes of raw files that should be processed
files_to_process = ["ocean_day2d", "ocean_day3d", "ice_day", "ocean_trps", "ergom_flux3d", "ergom_flux_surf", "ergom_flux_sed", "atmos_day", "gridinfo"]

max_jobs = 96