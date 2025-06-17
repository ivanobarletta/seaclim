#SBATCH -J %TASK%.%ECF_TRYNO%-%MOI_expnam%-%MOI_dstop%
#SBATCH -N %nodes%
#SBATCH -n %MOI_obsopr_ntasks_modelgrid%
#SBATCH --ntasks-per-node=%MOI_obsopr_procs_node%
#SBATCH --time=%run_time%
#SBATCH --mem=%mem%
#SBATCH --no-requeue
#SBATCH --mail-type=%mail_if:NONE%
#SBATCH --mail-user=%mail_acct:roland.aznar@nowsystems.eu%
export JOB_ID=${SLURM_JOBID}
