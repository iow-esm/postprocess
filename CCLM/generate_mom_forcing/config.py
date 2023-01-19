# this depends on a processed raw output
dependencies = ["process_raw_output"]

max_jobs = 4

# Important: the following CCLM variables are used 
# "T_2M", "U_10M", "V_10M", "PMSL", "CLCT", "QV_2M", "TOT_PREC", "ASWD_S", "ALWD_S"
# to generate the forcing, thus they should have been printed out with a reasonable time resolution!

# you can either specify a path to a remapping file (compatible to the remapbil operator of cdo)
#remapping_file_path = "/scratch/usr/mvkkarst/test/grid_MOM5_Baltic.txt"

# or you can specify the remapping directly here (also compatible to the remapbil operator of cdo)
remapping = """
gridtype  = lonlat
xsize     = 224
ysize     = 242
xfirst    = 8.28
xinc      = 0.1
yfirst    = 53.85
yinc      = 0.05
"""

