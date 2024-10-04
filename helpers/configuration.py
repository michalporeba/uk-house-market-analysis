import os


def get_data_location():
  location = "data"
  os.makedirs(location, exist_ok=True)
  return location


def get_hpi_data_location():
  location = os.path.join(get_data_location(), "hpi")
  os.makedirs(location, exist_ok=True)
  return location


def get_latest_hpi_file_path():
  location = get_data_location()
  return os.path.join(location, "hpi.csv")


def get_pp_data_location():
  location = os.path.join(get_data_location(), "pp")
  os.makedirs(location, exist_ok=True)
  return location


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
