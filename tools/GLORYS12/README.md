some scripts to request GLORYS12 (global reanalysis) from cmems

NOTE! 
    1) You must have a conda environment with copernicus marine toolbox
    https://help.marine.copernicus.eu/en/collections/9080063-copernicus-marine-toolbox

    here the conda environment is called cmt_1.0 (but is actually a newer version)

    check this out to install a new conda env with copernicusmarine 

    https://help.marine.copernicus.eu/en/articles/7970514-copernicus-marine-toolbox-installation

    2) the Script cmt_request.py assumes the existence of folders of year/month

    you can either create the folders in advance

    mkdir yyyy/mm 

    or modify the script to save all the files in the same folder

    2a) Don't forget to set your cmems account username & password in the script!

    2b) the same applies for the script to get the static files (cmt_request_static.py)    
