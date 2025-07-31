#!/bin/bash

ecflow_client --port=4040 --host=login210-19 --load=seaclim_ensemble.def force
ecflow_client --port=4040 --host=login210-19 --alter=change defstatus "queued" /seaclim_ensemble
ecflow_client --port=4040 --host=login210-19 --begin=/seaclim_ensemble
