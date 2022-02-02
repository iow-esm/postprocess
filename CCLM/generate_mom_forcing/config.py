# this depends on a processed raw output
dependencies = ["process_raw_output"]

# Important: the following CCLM variables are used 
# "T_2M", "U_10M", "V_10M", "PMSL", "CLCT", "QV_2M", "TOT_PREC", "ASOB_S", "ALWD_S"
# to generate the forcing, thus they should have been printed out with a reasonable time resolution!

# you can either specify a path to a remapping file (compatible to the remapbil operator of cdo)
#remapping_file_path = "/scratch/usr/mvkkarst/test/grid_MOM5_Baltic.txt"

# or you can specify the remapping directly here (also compatible to the remapbil operator of cdo)
remapping = """
gridtype  = lonlat
xsize     = 91
ysize     = 102
xfirst    = 8.12
xinc      = 0.24
yfirst    = 53.64
yinc      = 0.119999999999999
"""