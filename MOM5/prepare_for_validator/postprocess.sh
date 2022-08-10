out_dir=$1
from_date=${2:--1}
to_date=${3:--1}

# get the most current validator_peparator from IOW's git server
if [ -d "./validator_peparator/.git" ]; then
	cd "./validator_peparator"
	git pull
	cd ..
else
	git clone https://git.io-warnemuende.de/phy_drcs/validator_preparator.git ./validator_preparator
fi
	
# do the preparation
python3 ../../auxiliary/prepare_for_validator.py "${out_dir}" ${from_date} ${to_date} "$PWD"