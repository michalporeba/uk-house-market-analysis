import marimo

__generated_with = "0.8.0"
app = marimo.App(width="medium")


@app.cell
def __(mo):
    mo.md(r"""# Scripts to get or update data""")
    return


@app.cell
def __():
    import marimo as mo
    import pandas as pd

    from src.get_data import (
        get_hpi_data,
        get_pp_data,
        get_postcode_data
    )

    from helpers.data import (
        get_postcodes,
        get_all_hpi,
        get_all_prices_paid
    )


    # House Price Index website
    hpi_url = "https://www.gov.uk/government/collections/uk-house-price-index-reports"

    # Price Paid Data website
    pp_url = "https://www.gov.uk/government/statistical-data-sets/price-paid-data-downloads"

    # Postcode page
    postcode_url = "https://api.os.uk/downloads/v1/products/CodePointOpen/downloads?area=GB&format=CSV&redirect"
    return (
        get_all_hpi,
        get_all_prices_paid,
        get_hpi_data,
        get_postcode_data,
        get_postcodes,
        get_pp_data,
        hpi_url,
        mo,
        pd,
        postcode_url,
        pp_url,
    )


@app.cell
def __(mo):
    mo.md(r"""## Postcodes""")
    return


@app.cell
def __(get_postcode_data, get_postcodes, mo, postcode_url):
    postcodes_message = mo.md(
        get_postcode_data(postcode_url)
    )
    postcodes = get_postcodes()
    postcodes_message
    return postcodes, postcodes_message


@app.cell
def __(postcodes):
    postcodes.describe()
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ---
        The head of the postcodes dataframe:
        """
    )
    return


@app.cell
def __(postcodes):
    postcodes.head()
    return


@app.cell
def __(mo):
    mo.md(r"""## House Price Index""")
    return


@app.cell
def __(get_all_hpi, get_hpi_data, hpi_url, mo):
    hpi_message = mo.md(
        get_hpi_data(hpi_url)
    )
    hpi = get_all_hpi()
    hpi_message
    return hpi, hpi_message


@app.cell
def __(hpi):
    hpi.describe()
    return


@app.cell
def __(hpi, mo):
    mo.md(
        f"""
    ## Below are House Price Index regions. You will need to select one of the regions for analysis.\n
        {", ".join(hpi["RegionName"].unique())}
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Prices Paid

        The data file is over 5GB and may take a few moments (15+ minutes) to download. If the file already exists, then monthly files can be used to update the data.
        """
    )
    return


@app.cell
def __(get_pp_data, mo, pp_url):
    mo.md(
        get_pp_data(pp_url)
    )
    return


@app.cell
def __():
    #get_all_prices_paid().describe()
    return


if __name__ == "__main__":
    app.run()
