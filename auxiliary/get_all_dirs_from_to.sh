out_dir=$1
from=$2
to=$3

dirs=""

for d in `ls ${out_dir} | grep '^[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]$'`; do

	if [ -z $to ]; then
		:	# this does nothing, thus go on
	elif [ $d -gt $to ]; then
		continue # skipt that date
	fi

	if [ -z $from ]; then
		:	# this does nothing, thus go on
	elif [ $d -lt $from ]; then
		continue # skipt that date
	fi
	
	dirs="$dirs "${out_dir}"/$d"
done