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
    from helpers.get_data import get_hpi_data

    hpi_url = "https://www.gov.uk/government/collections/uk-house-price-index-reports"
    return get_hpi_data, hpi_url, mo


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
    mo.md(r""" """)
    return


if __name__ == "__main__":
    app.run()
