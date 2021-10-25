out_dir=$1
from_date=${2:--1}
to_date=${3:--1}

dependencies=("process_raw_output" "extract_levels")

module load cdo
module load anaconda3

python3 ../../auxiliary/seasonal_mean.py "${out_dir}" ${from_date} ${to_date} "$PWD"