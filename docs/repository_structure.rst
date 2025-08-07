****************
Repository Structure 
****************


The repository folder is organized as follows


.. code-block:: bash
    create_suite.py

    docs/               # folders containing this documentation
    src/                # folder with .ecf files
    include/            # include files
        header/
        scheduler/
        seaclim_common.h 
    inputs/             # base directory of inputs
        atm/
        bdy/
    outputs/            # base directory of simulations outputs (populated at runtime)
    restarts/           # base directory of restarts (populated at runtime)
    static/             # static files    
        atm/            # weights for IOF interpolation    
        nml/            # namelist templates
        ocean/          # static files of ocean (load tides)
    runs/               # base directory of calc directories (populated at runtime)
    tools/              # some tools to download ERA5 or GLORYS12 files
    logs/               # base directory of tasks logs

The script create_suite.py creates the suite to be loaded by ecflow server. 
The first part of the script can be adjusted depending on preferences. 

.. code-block:: python 

    nMembers        = 1         # number of members 000,001,002...
    hindcastYear1   = 1993      # 1993
    hindcastYear2   = 1993      # 2019

    hindcast_month_periods = 6  # should be 62

    start_month_day = "0101"    # "1101"

    model_dt = pd.Timedelta(seconds = 900)  # 900 sec

    nNodes      = 4             # number of HPC nodes
    nProcsNEMO  = 252           # number of NEMO MPI processes     
    nProcsXIOS  = 4             # number of XIOS MPI processes
    nProcsTOTAL = nProcsNEMO + nProcsXIOS
    nProcsMerge = 64            # MPI processes to merge 

    defs = Defs()   

    suite = defs.add_suite("seaclim_ensemble")  # name of suite

    suite.add_variable("ECF_JOB_CMD"    , "sbatch %ECF_JOB% 2>&1")

    main_dir = "/mnt/lustre/scratch/nlsas/home/empresa/now/iba/seaclim" # base directory