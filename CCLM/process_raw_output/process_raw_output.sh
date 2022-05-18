if [ $# -lt 1 ]; then
	echo "Usage: `basename "$0"` <dir1> [dir2] [dir3] ..."
fi

source ./config.sh

if [ -z $max_jobs ]; then	
	max_jobs = 1
fi

dirs=("$@")

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
			for var in `cdo -showname ${o}.nc | head -n -1`; do 
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
				for var in `cdo -showname ${o}_${s}.nc | head -n -1`; do  # skip last line showing info
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
		
		# get some means and sums for comparison to observational data
		
		# sum up downward radiation to compare to reference 
		if [ -f "ASWDIR_S.nc" ] && [ -f "ASWDIFD_S.nc" ]; then
			cdo -setattribute,ASWD_S@long_name="averaged total shortwave downward radiation at surface" -setattribute,ASWD_S@standard_name="averaged_total_sw_downward_radiation" -chname,ASWDIR_S,ASWD_S -add ASWDIR_S.nc ASWDIFD_S.nc ASWD_S.nc
		fi
		
		# sum up rain 
		if [ -f "RAIN_CON.nc" ] && [ -f "RAIN_GSP.nc" ]; then
			cdo -setattribute,RAIN_TOT@long_name="total rainfall" -setattribute,RAIN_TOT@standard_name="total_rainfall_amount" -chname,RAIN_CON,RAIN_TOT -add RAIN_CON.nc RAIN_GSP.nc RAIN_TOT.nc
		fi
		
		# sum up daily precipitation amount
		if [ -f "TOT_PREC.nc" ]; then
			cdo -chname,TOT_PREC,DAY_PREC -daysum TOT_PREC.nc DAY_PREC.nc
		fi
	
		# calculate daily mean of wind speed
		if [ -f "U_10M.nc" ] && [ -f "V_10M.nc" ]; then 
			cdo -setattribute,SPEED_10M_AV@units="m/s" -daymean -expr,'SPEED_10M_AV=sqrt(U_10M*U_10M+V_10M*V_10M)' -merge U_10M.nc V_10M.nc SPEED_10M_AV.nc
		fi

		# calculate daily mean of sea level pressure
		if [ -f "PMSL.nc" ]; then 
			cdo -chname,PMSL,PMSL_AV -daymean PMSL.nc PMSL_AV.nc 
		fi

		# ... and remove the empty folder
		if [ `ls $o | wc -l` -eq 0 ]; then
			rm -r $o
		fi
	done
done
