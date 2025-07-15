# make a request with Copernicus Marine Toolbox (cmt)

import copernicusmarine
import sys
import pandas as pd

filename    = "static/cmems_mod_glo_phy_my_0.083deg_static_bathy.nc" # this works if the 
                                                                    # folders are existing!

pwd         = "Dia"

"""

copernicusmarine.subset(
  dataset_id="cmems_mod_glo_phy_my_0.083deg_static",
  dataset_part="bathy",
  variables=["deptho", "deptho_lev", "mask"],
  minimum_longitude=-21,
  maximum_longitude=20,
  minimum_latitude=26,
  maximum_latitude=64.5,
  minimum_depth=0,
  maximum_depth=6000,
  username="ibarletta1",
  password=pwd,
  output_filename=filename

)

filename    = "static/cmems_mod_glo_phy_my_0.083deg_static_coords.nc" # this works if the 
                                                                    # folders are existing!


copernicusmarine.subset(
  dataset_id="cmems_mod_glo_phy_my_0.083deg_static",
  dataset_part="coords",
  variables=["e1t", "e2t", "e3t"],
  minimum_longitude=-21,
  maximum_longitude=20,
  minimum_latitude=26,
  maximum_latitude=64.5,
  minimum_depth=0,
  maximum_depth=6000,
  username="ibarletta1",
  password=pwd,
  output_filename=filename
)
"""

filename    = "static/cmems_mod_glo_phy_my_0.083deg_static_mdt.nc" # this works if the 
                                                                    # folders are existing!

copernicusmarine.subset(
  dataset_id="cmems_mod_glo_phy_my_0.083deg_static",
  dataset_part="mdt",
  variables=["mdt"],
  minimum_longitude=-21,
  maximum_longitude=20,
  minimum_latitude=26,
  maximum_latitude=64.5,
  minimum_depth=0,
  maximum_depth=6000,
  username="ibarletta1",
  password=pwd,
  output_filename=filename
)

