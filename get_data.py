import marimo

__generated_with = "0.8.0"
app = marimo.App(width="medium")


@app.cell
def __(filename, r):
    import requests
    from bs4 import BeautifulSoup
    import os
    from data import get_data_location
    from urllib.parse import urljoin


    hpi_url = "https://www.gov.uk/government/collections/uk-house-price-index-reports"


    def get_with_exceptions(url, stream=False):
        r = requests.get(url, stream=stream)
        r.raise_for_status()
        return r


    def get_soup(url):
        r = get_with_exceptions(url)
        return BeautifulSoup(r.content, "html.parser")


    def ensure_file_does_not_exist(path):
        if os.path.exists():
            raise Exception(f"File already exists: {path}!")


    def pull_from_response_stream(response, path):
        with open(path, "wb") as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)


    def download_file(url, path):
        ensure_file_does_not_exist(path)
        r = get_with_exceptions(url, stream=True)
        pull_from_response_stream(r, path)    
        print(f"Downloaded: {filename}")
        return path


    def create_predicate_for(text):
        def predicate(s):
            return s and s.startswith(text)
        return predicate


    def get_link_from(page, text):
        link = page.find("a", string=create_predicate_for(text))
        
        if link is None:
            raise Exception(f"Unable to find link{text} in {page.title}")    

        return link.get("href")

        
    def find_download_location():
        hpi_page = get_soup(hpi_url)
        download_text = "UK House Price Index: data downloads"
        download_url = urljoin(hpi_url, get_link_from(hpi_page, download_text))
        download_page = get_soup(download_url)
        return get_link_from(download_page, "UK HPI full file")


    find_download_location()

    return (
        BeautifulSoup,
        create_predicate_for,
        download_file,
        ensure_file_does_not_exist,
        find_download_location,
        get_data_location,
        get_link_from,
        get_soup,
        get_with_exceptions,
        hpi_url,
        os,
        pull_from_response_stream,
        requests,
        urljoin,
    )


if __name__ == "__main__":
    app.run()
