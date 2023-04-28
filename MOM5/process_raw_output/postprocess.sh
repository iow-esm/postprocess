#!/bin/bash

out_dir=$1
from_date=${2:--1}
to_date=${3:--1}

cd ../mppncombine/
source ./postprocess.sh "${out_dir}" ${from_date} ${to_date}
cd -

cd ../split_files/
source ./postprocess.sh "${out_dir}" ${from_date} ${to_date}
cd -