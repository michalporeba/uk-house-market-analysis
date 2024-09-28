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

    from helpers.get_data import (
        get_hpi_data,
        get_pp_data,
        get_postcode_data
    )

    from helpers.data import get_postcodes


    # House Price Index website
    hpi_url = "https://www.gov.uk/government/collections/uk-house-price-index-reports"

    # Price Paid Data website
    pp_url = "https://www.gov.uk/government/statistical-data-sets/price-paid-data-downloads"

    # Postcode page
    postcode_url = "https://api.os.uk/downloads/v1/products/CodePointOpen/downloads?area=GB&format=CSV&redirect"
    return (
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
    mo.md(r"""## House Price Index""")
    return


@app.cell
def __(get_hpi_data, hpi_url, mo):
    mo.md(
        get_hpi_data(hpi_url)
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
def __(mo):
    mo.md(r"""## Postcodes""")
    return


@app.cell
def __(get_postcode_data, mo, postcode_url):
    mo.md(
        get_postcode_data(postcode_url)
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ---
        Unique values in the `get_postcodes()` output:
        """
    )
    return


@app.cell
def __(get_postcodes):
    postcodes = get_postcodes()
    postcodes.nunique()

    return postcodes,


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


if __name__ == "__main__":
    app.run()
