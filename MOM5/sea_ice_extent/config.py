# this depends on 
dependencies = ["process_raw_output", "process_reference"]

reference_file_pattern = "/scratch/usr/mvkkarst/IOW_ESM_MOM5_uncoupled_test/postprocess/MOM5/process_reference/results/_scratch_usr_mvkkarst_obs_Copernicus-19810901_20091130/FI-remapped.nc"

operators = ["", "-yearmax", "-monmean", "-seasmean", "-monmax", "-yseasmean", "-ymonmean"]

sellonlatbox = "13,32,52,68"