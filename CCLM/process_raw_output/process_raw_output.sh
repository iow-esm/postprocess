if [ $# -lt 1 ]; then
	echo "Usage: `basename "$0"` <dir1> [dir2] [dir3] ..."
fi

source ./config.sh

if [ -z $max_jobs ]; then	
	max_jobs = 1
fi

dirs=("$@")

module load cdo

for d in ${dirs[@]}; do
	
	cd $d
	echo $PWD
	
	# check if there is something to do
	if [ `ls -d * | grep "out[0-9][0-9]" | wc -l` -eq 0 ]; then
		continue
	fi
	
	for o in out??; do
		cd $o
		
		echo $PWD
		
		# merge all output files wrt time
		if [ `find ./ -type f -or -type l -name 'lffd*[0-9].nc' | wc -l` -gt 0 ]; then
			cdo mergetime 'lffd*[0-9].nc' ${o}.nc && rm lffd*.nc
		fi
		# create individual files for the variables
		if [ -f ${o}.nc ]; then
			for var in `cdo -showname ${o}.nc`; do 
				while [ `jobs | wc -l` -ge ${max_jobs} ]; do sleep 1; done
				cdo -selname,$var ${o}.nc $var.nc &
			done
			wait
			rm ${o}.nc
		fi
		
		# treat files with suffixes
		suffixes=("p" "z")
		for s in  ${suffixes[@]}; do
			if [ `ls lffd*${s}.nc | wc -l` -gt 0 ]; then
				cdo mergetime lffd*${s}.nc ${o}_${s}.nc && rm lffd*${s}.nc
			fi
			if [ -f ${o}_${s}.nc ]; then
				for var in `cdo -showname ${o}_${s}.nc`; do 
					while [ `jobs | wc -l` -ge ${max_jobs} ]; do sleep 1; done
					cdo -selname,$var ${o}_${s}.nc ${var}_${s}.nc &
				done
				wait
				rm ${o}_${s}.nc
			fi
		done
		
		# if everything is done, move files up...
		if [ `ls ${o}*.nc | wc -l` -eq 0 ] && [ `ls lffd*.nc | wc -l` -eq 0 ]; then
			mv *.nc ../
		fi
		
		cd ..
		
		# ... and remove the empty folder
		if [ `ls $o | wc -l` -eq 0 ]; then
			rm -r $o
		fi
	done
done