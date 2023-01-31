out_dir=$1
from_date=${2:--1}
to_date=${3:--1}

#----------------------------------------------------

cd ../analyze
./postprocess.sh ${out_dir} ${from_date} ${to_date}

#----------------------------------------------------

cd ../create_validation_report
./postprocess.sh ${out_dir} ${from_date} ${to_date}

wait
