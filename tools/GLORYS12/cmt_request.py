# make a request with Copernicus Marine Toolbox (cmt)

import copernicusmarine
import sys
import pandas as pd

if len(sys.argv) < 4:
    print("Error! you must provide:")
    print("1) year")
    print("2) month")
    print("3) day")
    sys.exit(1)

year    = int(sys.argv[1])
month   = int(sys.argv[2])
day     = int(sys.argv[3])

date    = pd.Timestamp(year=year,month=month,day=day)

date_str    = date.strftime("%Y-%m-%dT%H:%M:%S")
date_str2   = date.strftime("%Y%m%d")

year_str    = str(year)
month_str   = str(month).zfill(2)

filename_root   = "%s/%s/cmems_mod_glo_phy_my_0.083deg_P1D-m_multi-vars_%s" # this works if the 
                                                                            # folders are existing!

filename        = filename_root % (year_str,month_str,date_str2)

pwd             = "Di"

copernicusmarine.subset(
  dataset_id="cmems_mod_glo_phy_my_0.083deg_P1D-m",
  variables=["so", "thetao", "zos", "vo", "uo"],
  minimum_longitude=-21,
  maximum_longitude=20,
  minimum_latitude=26,
  maximum_latitude=64.5,
  start_datetime=date_str,
  end_datetime=date_str,
  minimum_depth=0,
  maximum_depth=6000,
  username="ibarletta1",
  password=pwd,
  output_filename=filename
)
