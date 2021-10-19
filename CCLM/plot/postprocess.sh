out_dir=$1
from_date=${2:--1}
to_date=${3:--1}

dependencies=("seasonal_mean" "seasonal_percentile" "process_reference")

module load cdo
module load anaconda3

python3 plot.py "${out_dir}" ${from_date} ${to_date}