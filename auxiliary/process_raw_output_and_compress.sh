out_dir=$1
from=$2
to=$3

local="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

source ${local}/get_all_dirs_from_to.sh ${out_dir} $from $to

if [ -z ${max_jobs} ]; then	
	max_jobs=1
fi

process_dir () {
    dir=$1
    # split path into array of strings
    IFS='/' read -r -a array <<< "$dir"
    new_dir=""
    for i in ${!array[@]}; do 
        if [ "${array[$i]}" == "" ]; then 
            continue
        fi 
        new_dir=$new_dir"/"${array[$i]}
        if [ $i == $((${#array[@]}-3)) ]; then 
            new_dir=${new_dir}"_monthly"
        fi 
    done
    mkdir -p "${new_dir}"
    cd ${dir}
    for f in *.nc; do
        cdo monmean $f "${new_dir}"/$f
    done
    cd -

    tar cfvz ${dir}.tar.gz ${dir} && rm -r ${dir}
}

dirs=("${dirs}")
for dir in ${dirs[@]}; do
    while [ `jobs | wc -l` -ge ${max_jobs} ]; do sleep 1; done
    process_dir $dir &
done
wait
    
    

    