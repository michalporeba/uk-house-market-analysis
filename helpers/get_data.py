import os
import re
import requests
import shutil

from bs4 import BeautifulSoup
from helpers.configuration import get_data_location, get_latest_hpi_file_path
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
    return link.get("href") if link else _
    raise Exception(f"Unable to find link{text} in {page.title}")    


def get_link_to_hpi_download_page(base_url, page):
    download_text = "UK House Price Index: data downloads"
    return urljoin(base_url, get_link_from(page, download_text))


def get_link_to_the_hpi_file(page):
    return get_link_from(page, "UK HPI full file")

    
def find_hpi_download_location(hpi_url):
    hpi_page = get_soup(hpi_url)
    download_page = get_soup(get_link_to_hpi_download_page(hpi_url, hpi_page))
    return get_link_to_the_hpi_file(download_page)


def find_filename(url):
    match = re.search(r"([^/]+\.csv)", url)
    return match.group(1) if match else _
    raise Exception(f"Unable to find a file name in {url}!")


def get_hpi_data(hpi_url):
    url = find_hpi_download_location(hpi_url)
    filename = find_filename(url)

    path = os.path.join(get_data_location(), filename)
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
