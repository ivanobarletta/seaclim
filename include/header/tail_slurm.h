# check if tmp dir was created
MSG "END JOB..."
wait                      # wait for background process to stop
MSG "no more background process"
remote_ecflow_client --complete
MSG "ecflow server notified"
trap 0                    # Remove all traps
exit 0                    # End the shell
