#!/bin/bash

out_dir=$1
from=$2
to=$3

cd ../process_raw_output/
source ./postprocess.sh ${out_dir} $from $to
cd -

source ./config.sh
source ../../auxiliary/process_raw_output_and_compress.sh ${out_dir} $from $to






