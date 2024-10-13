import os


class Configuration:
  def __init__(self, data):
    self.data = data

  def __getattr__(self, key):
    if key in self.data:
      return self.data[key]
    raise AttributeError(f"Confiugration has no '{key}' value")

  def __getattr__(self, key):
    if key in self.data:
      return self.data[key]
    raise AttributeError(f"Confiugration has no '{key}' value")

  def __setattr__(self, key, value):
    self.data[key] = value

def ensure_location_exists(path):
  os.makedirs(path, exist_ok=True)
  return path

  
def get_configuration():
  data_configuration = Configuration({
    "location": ensure_location_exists("data")
  })

  hpi_configuration = Configuration({
    "location": ensure_location_exists("data/hpi"),
    "latest_file_path": "data/hpi.csv"
  })

  pp_configuration = Configuration({
    "location": ensure_location_exists("data/pp"),
    "latest_file_path": "data/pp.csv"
  })

  postcodes_configuration = Configuration({
    "location": ensure_location("data/postcodes"),
    "latest_file_path": "data/postcodes.csv"  
  })

  data_configuration.hpi = hpi_configuration
  data_configuration.pp = pp_configuration
  data_configuration.postcodes = postcodes_configuration
  
  return Configuration({
    "data": data_configuration
  })

  

def get_hpi_data_location():
  location = os.path.join(get_data_location(), "hpi")
  os.makedirs(location, exist_ok=True)
  return location


def get_latest_hpi_file_path():
  location = get_data_location()
  return os.path.join(location, "hpi.csv")


def get_pp_data_location():
    return get_data_location()


def get_latest_pp_file_path():
  location = get_pp_data_location()
  return os.path.join(location, "pp.csv")


def get_postcode_data_location():
  location = os.path.join(get_data_location(), "postcodes")
  os.makedirs(location, exist_ok=True)
  return location


def get_postcode_zip_path():
  location = get_postcode_data_location()
  return os.path.join(location, "postcodes.zip")


def get_postcode_data_file_path():
  location = get_data_location()
  return os.path.join(location, "postcodes.csv")
