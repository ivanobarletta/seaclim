#SBATCH -J %TASK%.M%MEMBER%.H%HINDCAST_YEAR%.c%CYCLE_NUMBER%.%ECF_TRYNO%
#SBATCH --output=%LOG_BASE_DIR%/M%MEMBER%/H%HINDCAST_YEAR%/C%CYCLE_NUMBER%_%CYCLE_START_DATE%/%TASK%.M%MEMBER%.hindcast_%HINDCAST_YEAR%.cycle_%CYCLE_NUMBER%.%ECF_DATE%-%TIME%.%ECF_TRYNO%.out
#SBATCH --error=%LOG_BASE_DIR%/M%MEMBER%/H%HINDCAST_YEAR%/C%CYCLE_NUMBER%_%CYCLE_START_DATE%/%TASK%.M%MEMBER%.hindcast_%HINDCAST_YEAR%.cycle_%CYCLE_NUMBER%.%ECF_DATE%-%TIME%.%ECF_TRYNO%.err
#SBATCH -N %NNODES%
#SBATCH -n %NPROCS_TOTAL%
#SBATCH --time=%run_time%
#SBATCH --mem=100G
#SBATCH --no-requeue
#SBATCH --mail-type=FAIL,END
#SBATCH --mail-user=ivano.barletta@nowsystems.eu
export JOB_ID=${SLURM_JOBID}