out_dir=$1
from_date=${2:--1}
to_date=${3:--1}

#----------------------------------------------------

cd ../create_remapping_files
./postprocess.sh ${out_dir} ${from_date} ${to_date}

#----------------------------------------------------

cd ../process_reference
./postprocess.sh ${out_dir} ${from_date} ${to_date}
#----------------------------------------------------

cd ../extract_regions
./postprocess.sh ${out_dir} ${from_date} ${to_date} &

cd ../extract_stations
./postprocess.sh ${out_dir} ${from_date} ${to_date}
wait

#----------------------------------------------------

cd ../seasonal_mean
./postprocess.sh ${out_dir} ${from_date} ${to_date}

#----------------------------------------------------

cd ../calculate_anomalies
./postprocess.sh ${out_dir} ${from_date} ${to_date}
#----------------------------------------------------

