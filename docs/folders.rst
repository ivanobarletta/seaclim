****************
Folders
****************

The repository folder is organized as follows


.. code-block:: bash

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

