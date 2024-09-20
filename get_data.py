import marimo

__generated_with = "0.8.0"
app = marimo.App(width="medium")


@app.cell
def __(filename):
    import requests
    from bs4 import BeautifulSoup
    import os
    from data import get_data_location

    hpi_url = "https://www.gov.uk/government/collections/uk-house-price-index-reports"


    def get_soup(url):
        r = requests.get(url)
        r.raise_for_status()
        return BeautifulSoup(r.content, "html.parser")
        

    def download_file(url, path):
        if os.path.exists():
            print(f"File already exists: {path}!")
            return

        r = requests.get(url, stream=True)
        r.raise_for_status()

        with open(path, "wb") as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)

        print(f"Downloaded: {filename}")

        return path


    get_soup(hpi_url)

    return (
        BeautifulSoup,
        download_file,
        get_data_location,
        get_soup,
        hpi_url,
        os,
        requests,
    )


app._unparsable_cell(
    r"""
    import requests
    from bs4 import BeautifulSoup
    import os

    # Define the base URL and target data folder
    base_url = 
    data_folder = \"data\"

    # Ensure data folder exists
    os.makedirs(data_folder, exist_ok=True)




    def download_file(url, filename):
      \"\"\"Downloads a file from the given URL and saves it with the specified filename.\"\"\"
      response = requests.get(url, stream=True)
      response.raise_for_status()

      filepath = os.path.join(data_folder, filename)
      if not os.path.exists(filepath):
        with open(filepath, \"wb\") as f:
          for chunk in response.iter_content(1024):
            f.write(chunk)
        print(f\"Downloaded: {filename}\")
      else:
        print(f\"File already exists: {filename}\")

    # Get the HTML content
    response = requests.get(base_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, \"html.parser\")

    # Find the first link with \"UK House Price Index: data downloads\"
    download_link = soup.find(\"a\", text=lambda text: text and text.startswith(\"UK House Price Index: data downloads\"))

    if download_link:
      # Extract the link URL
      download_url = download_link.get(\"href\")
      
      # Follow the link to find the data download page
      download_response = requests.get(download_url)
      download_response.raise_for_status()
      download_soup = BeautifulSoup(download_response.content, \"html.parser\")
      
      # Find the link with \"UK HPI full file\" description
      hpi_file_link = download_soup.find(\"a\", text=lambda text: text and text == \"UK HPI full file\")
      
      if hpi_file_link:
        # Extract the HPI data download URL
        hpi_file_url = hpi_file_link.get(\"href\")
        filename = os.path.basename(hpi_file_url)  # Extract filename from URL
        
        # Download the HPI data file
        download_file(hpi_file_url, filename)
        
        # Copy the downloaded file to uk-hpi-lates.csv
        copy_path = os.path.join(os.getcwd(), \"uk-hpi-lates.csv\")
        os.replace(os.path.join(data_folder, filename), copy_path)
        print(f\"Copied {filename} to uk-hpi-lates.csv\")
      else:
        print(\"Couldn't find 'UK HPI full file' link.\")
    else:
      print(\"Couldn't find 'UK House Price Index: data downloads' link.\")
    """,
    name="__"
)


if __name__ == "__main__":
    app.run()
