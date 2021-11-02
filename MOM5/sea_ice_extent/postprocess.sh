out_dir=$1
from_date=${2:--1}
to_date=${3:--1}

module load cdo
module load anaconda3

python3 sea_ice_extent.py "${out_dir}" ${from_date} ${to_date} "$PWD"