#SBATCH -J %TASK%
#SBATCH --output=%LOG_BASE_DIR%/create_log/%TASK%.%ECF_TRYNO%.out
#SBATCH --error=%LOG_BASE_DIR%/create_log/%TASK%.%ECF_TRYNO%.err
#SBATCH -N 1
#SBATCH --ntasks-per-node=1
#SBATCH --time=%run_time%
#SBATCH --mem=1G
#SBATCH --no-requeue
#SBATCH --mail-type=FAIL,END
#SBATCH --mail-user=ivano.barletta@nowsystems.eu
export JOB_ID=${SLURM_JOBID}
