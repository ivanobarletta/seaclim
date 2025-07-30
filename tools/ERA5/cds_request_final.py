# make a request to climate data store
# https://cds.climate.copernicus.eu/how-to-api
#
import cdsapi
import sys
from os.path import isfile
import pandas as pd
import xarray as xr

client = cdsapi.Client()

year    = sys.argv[1]
month   = sys.argv[2]

year    = str(year) 
month   = str(month).zfill(2)

nDays   = pd.Period(f"{year}-{month}-01").days_in_month

days    = [str(d).zfill(2) for d in range(1,nDays+1)]

var2    = "NONE"

varnames    = ["BULKTAIR","BULKHUMI","BULKU10","BULKV10","FLUXPRE","FLUXSSRD","FLUXSTRD","MSLP"]

for var in varnames:

    print("Processing: ", var)

    dataset = "reanalysis-era5-single-levels"

    if var == "BULKTAIR":
        var2 = "2m_temperature"
    if var == "BULKHUMI":
        var2 = "specific_humidity"
        dataset = "reanalysis-era5-pressure-levels"
    if var == "BULKU10":    
        var2 = "10m_u_component_of_wind"
    if var == "BULKV10":    
        var2 = "10m_v_component_of_wind"
    if var == "FLUXPRE":    
        var2 = "total_precipitation"
    if var == "FLUXSSRD":
        var2 = "surface_solar_radiation_downwards"
    if var == "FLUXSTRD":    
        var2 = "surface_thermal_radiation_downwards"
    if var == "MSLP":
        var2 = "mean_sea_level_pressure"
    
    if var2 == "NONE":
        raise Exception("Error! Check name of var you provided!")
        
    request = {
        "product_type": ["reanalysis"],
        "variable": [var2],
        "year": [year],
        "month": [month],
        "day": days,
        "time": [
            "00:00", 
            "03:00", 
            "06:00", 
            "09:00", 
            "12:00", 
            "15:00", 
            "18:00", 
            "21:00", 
        ],
        "pressure_level": ["1000"],
        "data_format": "netcdf",
        "download_format": "unarchived",
        "area": [65, -21, 25, 23]
    }
    
    file_string_temp    = "{year}/{month}/temp_ERA5_{var}_3H_y{year}m{month}.nc"
    file_string_final   = "{year}/{month}/ERA5_{var}_3H_y{year}m{month}.nc"
    target = file_string_temp.format(var=var,year=year,month=month)

    client.retrieve(dataset, request,target)    

    outfile = file_string_final.format(var=var,year=year,month=month)

    # load ds     
    ds = xr.open_dataset(target)

    ds = ds.rename({"valid_time":"time"})   # do this in any case

    if var == "BULKHUMI":  
        print("Renaming q -> q2m")
        ds = ds.rename({"q":"q2m"}).isel(pressure_level=0)

    if var == "FLUXSSRD":
        print("Rescaling ssrd")
        ds["ssrd"] = ds["ssrd"] / 3600
        ds["ssrd"] = ds["ssrd"].assign_attrs({"units":"W m**-2"})

    if var == "FLUXSTRD":
        print("Rescaling strd")
        ds["strd"] = ds["strd"] / 3600
        ds["strd"] = ds["strd"].assign_attrs({"units":"W m**-2"})

    print("Saving file:",outfile)
    ds.to_netcdf(outfile,encoding={"time" : {"dtype": "i4"} },unlimited_dims=["time"])  # I want time int (not int64) and UNLIMITED 
    ds.close()
    
