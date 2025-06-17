#SBATCH -J %TASK%.%ECF_TRYNO%-%MOI_expnam%-%MOI_dstop%
#SBATCH --reservation=%node_reservation%
#SBATCH -N %nodes%
#SBATCH -n %MOI_model_total_ntasks%
#SBATCH --ntasks-per-node=%procs_node%
#SBATCH --time=%run_time%
#SBATCH --mem=240G
#SBATCH --exclusive
#SBATCH --no-requeue
#SBATCH --mail-type=%mail_if:NONE%
#SBATCH --mail-user=%mail_acct:roland.aznar@nowsystems.eu%
export JOB_ID=${SLURM_JOBID}
