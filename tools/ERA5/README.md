usage

    1) before using the script make sure you have a conda env with 
    cdsapi (climate data store)

    https://cds.climate.copernicus.eu/

    to install it just do 

    $ pip install "cdsapi>=0.7.4"

    https://cds.climate.copernicus.eu/how-to-api

    in the link above you have some short examples
    on how to use the api

    2) the script cds_request.py assumes that you have folders like:

        year/month

    to store the output files. You have to either create the folders
    of corresponding years/months you want to download or you 
    modify the script to download all the files in the same folder.



