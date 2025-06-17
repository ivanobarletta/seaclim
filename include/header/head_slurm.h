#!/bin/bash
set -e # stop the shell on first error
set -u # fail when using an undefined variable
set -x # echo script lines as they are executed
 
 
# Defines the variables that are needed for any communication with ECF
export ECF_PORT=%ECF_PORT%    # The server port number
export ECF_HOST=%ECF_HOST%    # The name of ecf host that issued this task
export ECF_NAME=%ECF_NAME%    # The name of this current task
export ECF_PASS=%ECF_PASS%    # A unique password
export ECF_TRYNO=%ECF_TRYNO%  # Current try number of the task
export ECF_RID=${JOB_ID}             # record the process id. Also used for zombie detection
 
# Define the path where to find ecflow_client
# make sure client and server use the *same* version.
# Important when there are multiple versions of ecFlow

export MOI_ECF_HOST=${ECF_HOST}

remote_ecflow_client () 
{
	set +e
	_args=$*
	ssh_status=666
	while [ $ssh_status -gt 0 ]; do
	ssh  -o LogLevel=%MOI_openssh_LogLevel:VERBOSE% -o ConnectionAttempts=300  -o ConnectTimeout=300 -o BatchMode=yes -o StrictHostKeyChecking=no -o PreferredAuthentications=publickey ${SLURM_SUBMIT_HOST} \
	"export ECF_PORT=$ECF_PORT ECF_HOST=$ECF_HOST ECF_NAME=$ECF_NAME ECF_PASS=$ECF_PASS ECF_TRYNO=$ECF_TRYNO ECF_RID=$ECF_RID PATH=$PATH; ecflow_client ${_args}"
        ssh_status=$?
	done     	
	set -e
}

# Tell ecFlow we have started
remote_ecflow_client --init=$ECF_RID
 
# Define a error handler
ERROR() {
   set +e                      # Clear -e flag, so we dont fail
   # check if tmp dir was created
   #if [[ "${WORK_DIR:-}" ||  -d "${WORK_DIR:-}" ]]; then
   #    rm -rf "${WORK_DIR:-}"
   #fi
   remote_ecflow_client --abort=trap
   trap 0                      # Remove the trap
   exit 0                      # End the script
}
 
MSG() {
    echo "$(date): $*"
}

# Trap any calls to exit and errors caught by the -e flag
trap ERROR 0
  
# Trap any signal that may cause the script to fail
trap '{ echo "Killed by a signal"; ERROR ; }' 1 2 3 4 5 6 7 8 10 12 13

MSG "START JOB"
