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


def get_latest_pp_file_path():
  location = get_data_location()
  return os.path.join(location, "pp.csv")