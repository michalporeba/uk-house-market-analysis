import pandas as pd
import geopandas as gpd

def format_in_thousands(value):
    return f"£{int(value / 1000):,}K"


def y_in_thousands(plot):
  ylabels = [format_in_thousands(x) for x in plot.get_yticks()]
  plot.set_yticks(plot.get_yticks())
  plot.set_yticklabels(ylabels)
  return plot


def get_hpi(region: str):
  hpi = pd.read_csv('data/UK-HPI-full-file-2024-06.csv')
  hpi = hpi[hpi['RegionName']==region]
  hpi["date"] = pd.to_datetime(hpi["Date"])
  hpi['date'] = hpi['date'].dt.strftime('%Y-%d')
  return hpi


def get_hsp(postcodes):
  pass


def get_postcodes(area: str):
  file = f"data/postcodes/{area[:2].lower()}.csv"
  columns = ['postcode', 'quality', 'easting', 'northing']

  postcodes = pd.read_csv(file, header=None, usecols=[0,1,2,3], names=columns)
  postcodes.reset_index(inplace=True)
  postcodes['area'] = postcodes['postcode'].str[:2]
  postcodes['district'] = postcodes['postcode'].str[:4]
  postcodes['district'] = postcodes['district'].str.strip()
  postcodes['sector'] = postcodes['postcode'].str[:5]

  gdf = gpd.GeoDataFrame(postcodes, geometry = gpd.points_from_xy(postcodes['easting'], postcodes['northing']))
  gdf.crs = 'EPSG:27700'
  return gdf.to_crs('EPSG:4326')


def get_postcode_location(postcodes, postcode):
  match = postcodes[postcodes['postcode']==postcode.upper()]
  if match.empty:
    return None

  geometry = match['geometry'].values[0]

  return geometry

def filter_to_local(postcodes, point, distance):
  return postcodes[postcodes.distance(point)*111000 <= distance]
  