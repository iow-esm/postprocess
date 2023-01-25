out_dir=$1
from_date=${2:--1}
to_date=${3:--1}

cd ../compare_2D_means
./postprocess.sh ${out_dir} ${from_date} ${to_date} &

cd ../compare_2D_anomalies
./postprocess.sh ${out_dir} ${from_date} ${to_date} &

cd ../compare_time_series
./postprocess.sh ${out_dir} ${from_date} ${to_date} &

cd ../create_taylor_diagrams
./postprocess.sh ${out_dir} ${from_date} ${to_date} &

cd ../get_cost_function
./postprocess.sh ${out_dir} ${from_date} ${to_date} &

cd ../draw_stations_and_regions
./postprocess.sh ${out_dir} ${from_date} ${to_date} &

cd ../compare_vertical_profiles
./postprocess.sh ${out_dir} ${from_date} ${to_date} &
wait

cd ../create_validation_report
python3 ../../auxiliary/create_validation_report.py "${out_dir}" ${from_date} ${to_date} "$PWD"
