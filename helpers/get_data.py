import os
import re
import requests
import shutil

from bs4 import BeautifulSoup
from helpers.configuration import (
  get_data_location,
  get_hpi_data_location,
  get_latest_hpi_file_path,
  get_latest_pp_file_path,
  get_postcode_data_location,
  get_postcode_zip_path,
  get_postcode_data_file_path
)
from urllib.parse import urljoin
  

def get_with_exceptions(url, stream=False, verify=True):
    r = requests.get(url, stream=stream, verify=verify)
    r.raise_for_status()
    return r


def get_soup(url):
    r = get_with_exceptions(url)
    return BeautifulSoup(r.content, "html.parser")


def ensure_file_does_not_exist(path):
    if os.path.exists(path):
        raise Exception(f"File already exists: {path}!")


def pull_from_response_stream(response, path):
    with open(path, "wb") as f:
        for chunk in response.iter_content(1024):
            f.write(chunk)


def download_file(url, path):
    ensure_file_does_not_exist(path)
    r = get_with_exceptions(url, stream=True, verify=False)
    pull_from_response_stream(r, path)    
    print(f"Downloaded: {path}")
    return path


def create_predicate_for(text):
    def predicate(s):
        return s and s.startswith(text)
    return predicate


def get_link_from(page, text):
    link = page.find("a", string=create_predicate_for(text))
    if not link:
        raise Exception(f"Unable to find link{text} in {page.title}")
    
    return link.get("href")


def get_link_to_hpi_download_page(base_url, page):
    download_text = "UK House Price Index: data downloads"
    return urljoin(base_url, get_link_from(page, download_text))


def get_link_to_hpi_file(page):
    return get_link_from(page, "UK HPI full file")


def get_link_to_pp_file(page):
    return get_link_from(page, "the complete Price Paid Transaction Data as a CSV file")


def get_link_to_pp_update_file(page):
    return get_link_from(page, "current month as a CSV file")
  
  
def find_hpi_download_location(url):
    page = get_soup(url)
    page = get_soup(get_link_to_hpi_download_page(url, page))
    return get_link_to_hpi_file(page)


def find_pp_download_location(url):
  page = get_soup(url)
  return get_link_to_pp_file(page)


def find_pp_update_location(url):
  page = get_soup(url)
  return get_link_to_pp_update_file(page)


def find_filename(url):
    match = re.search(r"([^/]+\.csv)", url)

    if not match:
        raise Exception(f"Unable to find a file name in {url}!")
  
    return match.group(1)


def get_hpi_data(hpi_url):
    url = find_hpi_download_location(hpi_url)
    filename = find_filename(url)

    path = os.path.join(get_hpi_data_location(), filename)
    if os.path.exists(path):
        return f"""
File **{path}** already exists!</br>
Remove it if you want to download it again.\n
Otherwise, the latest data is available in **{get_latest_hpi_file_path()}**.
        """

    try:
      download_file(url, path)
    except Exception as ex:
        return f"""
**Unable to download HPI data** from {url}.

{ex}
        """
    else:
      shutil.copy(path, get_latest_hpi_file_path())
  
    return f"""
Downloaded **{path}**.\n
The latest HPI data is available in **{get_latest_hpi_file_path()}**.
"""


def get_highest_ts(filename):
    max_ts = ""
    with open(filename, 'r') as f:
        for line in f:
            try:
                start = line.index(',', 41, 60)
                ts = line[start+2:start+12]
                if ts > max_ts:
                    max_ts = ts
            except:
                pass
    return ts


def get_pp_data(pp_url):
    url = find_pp_download_location(pp_url)
    filename = find_filename(url)  
    path = os.path.join(get_data_location(), filename)
    
    if os.path.exists(path):
        highest_ts = get_highest_ts(path)
        return f"""
File **{path}** already exists!</br>
The latest house sale data available is from **{highest_ts}**.\n
Remove it if you want to get a newer file.\n
        """

    else:
        try:
            download_file(url, path)
        except Exception as ex:
            return f"""
**Unable to download PP data** from {url}.

{ex}
            """
        else:
          shutil.copy(path, get_latest_pp_file_path())
    return f"""
Downloaded **{path}**.\n
    """

def combine_csv_files(source_folder, path):
    with open(path, 'w') as output:
        for filename in sorted(os.listdir(source_folder)):
            source_path = os.path.join(source_folder, filename)
            if not os.path.isdir(source_path):
                with open(source_path, 'r') as source:
                    for line in source:
                        output.write(line)


def get_postcode_data(url):
    path = get_postcode_zip_path()
    
    if os.path.exists(path):
        return f"""
File **{path}** already exists!\n
Remove it if you want to get a newer file.
        """

    try:
        download_file(url, path)
    except Exception as ex:
        return f"""
**Unable to download postcode data** from {url}.

{ex}
"""

    shutil.unpack_archive(path, get_postcode_data_location())
    csv_files_location = os.path.join(get_postcode_data_location(), 'Data/CSV')
    combine_csv_files(csv_files_location, get_postcode_data_file_path())
  
    return f"""
Downloaded **{path}**.
Postcodes are available in **{get_postcode_data_file_path()}**
    """
    