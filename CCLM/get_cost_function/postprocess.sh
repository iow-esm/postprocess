out_dir=$1
from_date=${2:--1}
to_date=${3:--1}

python3 ../../auxiliary/get_cost_function.py "${out_dir}" ${from_date} ${to_date} "$PWD"