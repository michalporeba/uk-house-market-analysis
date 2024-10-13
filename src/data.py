import pandas as pd
import geopandas as gpd
import os

from src.configuration import (
  get_postcode_data_file_path,
  get_latest_hpi_file_path,
  get_latest_pp_file_path
)

def add_postcode_parts(df, postcode_column):
  df['area'] = df[postcode_column].str[:2]
  df['district'] = df[postcode_column].str[:4]
  df['district'] = df['district'].str.strip()
  df['sector'] = df[postcode_column].str[:5]
  return df


def property_type_expander(type):
  if type is None:
    return "UNKNOWN"
  return {
    "T": "TERRACED",
    "S": "SEMI-DETACHED",
    "D": "DETACHED",
    "F": "FLAT",
    "O": "OTHER"
  }.get(type, type)


def transaction_type_expander(type):
  if type is None:
    return "UNKNWON"
  return {
    "F": "FREEHOLD",
    "L": "LEASHOLD"
  }.get(type, type)


def date_to_period(date):
  if date < "2003-05":
    return "Old"
  if date < "2008-01":
    return "Bubble"
  if date < "2013-05":
    return "Crash"
  if date < "2020-10":
    return "Modern"
  if date < "2022-10":
    return "CoVID"
  return "Readjustment"


def get_all_hpi():
  hpi = pd.read_csv(get_latest_hpi_file_path())
  hpi["date"] = pd.to_datetime(hpi["Date"])
  hpi["date"] = hpi['date'].dt.strftime('%Y-%d')
  hpi["period"] = hpi["date"].apply(date_to_period)
  return hpi


def get_hpi_for(region: str):
  hpi = pd.read_csv(get_latest_hpi_file_path())
  hpi = hpi[hpi['RegionName']==region]
  hpi["date"] = pd.to_datetime(hpi["Date"])
  hpi["date"] = hpi['date'].dt.strftime('%Y-%d')
  hpi["period"] = hpi["date"].apply(date_to_period)
  return hpi


def get_prices_paid_in(postcodes):
  columns = ['id', 'price', 'ts', 'postcode', 'property_type', 'is_new_build', 'transaction_type', 'paon']
  
  sales = pd.DataFrame()
  chunk_size = 10000

  for chunk in pd.read_csv('data/pp-complete.csv', header=None, usecols=[0,1,2,3,4,5,6,7], names=columns, chunksize=chunk_size):
    if postcodes is not None:
      filtered = chunk[chunk['postcode'].isin(postcodes['postcode'])]
      sales = pd.concat([sales, filtered], ignore_index=True)
    else: 
      sales = pd.concat([sales, chunk], ignore_index=True)

  return sales


def get_all_prices_paid():
  return get_prices_paid_in(None)


def get_hsp_from(postcodes, region_name):
  sales = get_prices_paid_for(postcodes)
  sales["property_type"] = sales["property_type"].apply(property_type_expander)
  sales["transaction_type"] = sales["transaction_type"].apply(transaction_type_expander)
  sales['date'] = pd.to_datetime(sales['ts'])
  sales['date'] = sales['date'].dt.strftime('%Y-%m')
  sales['year'] = sales['date'].str[:4]
  sales["period"] = sales["date"].apply(date_to_period)

  sales = pd.merge(sales, postcodes, on='postcode', how='left')

  sales = sales.sort_values('ts')

  sales = add_indexed_house_prices(sales, region_name)
  sales = gpd.GeoDataFrame(sales, geometry = sales['geometry'])
  sales["x"] = sales.geometry.x
  sales["y"] = sales.geometry.y
  sales.crs = 'EPSG:4326'
  return sales


def add_indexed_house_prices(hsp, region):
  hpi = get_hpi(region)
  hpi = hpi.drop("period", axis=1)
  hsp['average_price'] = -1
  hsp['hpi'] = -1
  hsp = pd.merge(hsp, hpi, on="date", how="left")
  
  hsp.loc[hsp['property_type'] == 'D', 'average_price'] = hsp['DetachedPrice']
  hsp.loc[hsp['property_type'] == 'D', 'hpi'] = hsp['DetachedIndex']

  hsp.loc[hsp['property_type'] == 'S', 'average_price'] = hsp['SemiDetachedPrice']
  hsp.loc[hsp['property_type'] == 'S', 'hpi'] = hsp['SemiDetachedIndex']

  hsp.loc[hsp['property_type'] == 'T', 'average_price'] = hsp['TerracedPrice']
  hsp.loc[hsp['property_type'] == 'T', 'hpi'] = hsp['TerracedIndex']

  hsp.loc[hsp['property_type'] == 'F', 'average_price'] = hsp['FlatPrice']
  hsp.loc[hsp['property_type'] == 'F', 'hpi'] = hsp['FlatIndex']

  hsp.loc[hsp['hpi'] < 0, 'average_price'] = hsp['AveragePrice']
  hsp.loc[hsp['hpi'] < 0, 'hpi'] = hsp['Index']

  hpi_column_index = hsp.columns.get_loc('hpi')
  hsp = hsp.iloc[:, :hpi_column_index+1]

  hsp['indexed_price'] = hsp['price'] / (hsp['hpi'] / 100)
  hsp['distance_from_mean'] = 100*hsp['price']/hsp['average_price']

  return hsp


def get_postcodes():
  file = get_postcode_data_file_path()
  columns = ['postcode', 'quality', 'easting', 'northing']

  postcodes = pd.read_csv(file, header=None, usecols=[0,1,2,3], names=columns)
  postcodes.reset_index(inplace=True)
  postcodes = add_postcode_parts(postcodes, 'postcode')

  gdf = gpd.GeoDataFrame(postcodes, geometry = gpd.points_from_xy(postcodes['easting'], postcodes['northing']))
  gdf.crs = 'EPSG:27700'
  return gdf.to_crs('EPSG:4326')


def get_postcode_location(postcodes, postcode):
  match = postcodes[postcodes['postcode']==postcode.upper()]
  if match.empty:
    return None

  geometry = match['geometry'].values[0]

  return geometry

def filter_to_local(gdf, point, distance):
  gdf = gdf.to_crs('EPSG:4326')
  return gdf[gdf.distance(point)*111000 <= distance]
  