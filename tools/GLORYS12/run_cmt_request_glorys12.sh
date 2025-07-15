#!/bin/bash
##################################################
#SBATCH -J cmtrequest
#SBATCH -o LOGS/cdsreq.out.%j
#SBATCH -e LOGS/cdsreq.err.%j
#SBATCH --time=01:00:00
#SBATCH -N 1
#SBATCH -n 1
#SBATCH --mem=10G
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=ivano.barletta@nowsystems.eu
##################################################

module load miniconda3

conda activate cmt_1.0

isleap() { 
   year=$1
   (( !(year % 4) && ( year % 100 || !(year % 400) ) )) &&
      echo "true" || echo "false"
}

get_nb_days_month() {
    year=$1
    month=$2

    # Convert the input string to an integer, removing any leading zeros.
    # This ensures that "01" is treated as 1, and "10" as 10 for arithmetic.

    month_int=$(echo "$month" | sed 's/^0*//')

    #      1  2  3  4  5  6  7  8  9  10 11 12
    ndays=(31 28 31 30 31 30 31 31 30 31 30 31)         
    
    # 0 based indexing
    value=${ndays[$((month_int-1))]}

    if [ $(isleap ${year}) == "true" ] && [ ${month_int} -eq 2 ]; then
        value=$((value+1)) # 28->29
    fi 

    echo ${value}
}



year=$1
month=$2
month2=$(printf "%02d" ${month})    # make sure that 1 is 01,2 is 02...

ndays=$(get_nb_days_month ${year} ${month})

mkdir -p ${year}/${month2}

for day in $(seq -f "%02g" 1 ${ndays}); do 
    python cmt_request.py ${year} ${month} ${day}
done
