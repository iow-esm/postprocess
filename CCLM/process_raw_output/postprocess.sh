out_dir=$1
from=$2
to=$3


dependencies=()

source ../../auxiliary/get_all_dirs_from_to.sh ${out_dir} $from $to
echo "$dirs"

./process_raw_output.sh "${dirs}"


