import cdsapi
import sys

var     = sys.argv[1]
year    = sys.argv[2]
month   = sys.argv[3]
day     = sys.argv[4]

year    = str(year) 
month   = str(month).zfill(2)
day     = str(day).zfill(2)

var2    = "NONE"

if var == "BULKTAIR":
    var2 = "2m_temperature"
if var == "BULKHUMI":
    var2 = "specific_humidity"
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


dataset = "reanalysis-era5-single-levels"
if var == "BULKHUMI":
    dataset = "reanalysis-era5-pressure-levels"
    
request = {
    "product_type": ["reanalysis"],
    "variable": [var2],
    "year": [year],
    "month": [month],
    "day": [
        day,
    ],
    "time": [
        "00:00", "01:00", "02:00",
        "03:00", "04:00", "05:00",
        "06:00", "07:00", "08:00",
        "09:00", "10:00", "11:00",
        "12:00", "13:00", "14:00",
        "15:00", "16:00", "17:00",
        "18:00", "19:00", "20:00",
        "21:00", "22:00", "23:00"
    ],
    "pressure_level": ["1000"],
    "data_format": "netcdf",
    "download_format": "unarchived"
}

file_string = "{year}/{month}/ERA5_{var}_1H_y{year}m{month}d{day}.nc"
target = file_string.format(var=var,year=year,month=month,day=day)

#target = "ERA5_BULKTAIR_1H_y1993m11d01.nc"

client = cdsapi.Client()
client.retrieve(dataset, request,target)

