import warnings
warnings.filterwarnings("ignore")

import geopandas as gpd
import pandas as pd

# input parameters
mode_prefix = "W"

# =============================================================================
# merge link_tons
# =============================================================================
# link_tons_gdf = gpd.read_file('../../__INPUT__/Water/USACE_linktons/2017/linkton17.shp')
link_tons_gdf = gpd.read_file('../../__INPUT__/Water/BTS_Water_Network_Input/link_tons/Link_tonnages.shp')

# =============================================================================
# convert CRS
target_CRS = 'EPSG:5070'
link_tons_gdf = link_tons_gdf.to_crs(target_CRS)
link_tons_gdf.to_file('output/01/link_tons.shp')
