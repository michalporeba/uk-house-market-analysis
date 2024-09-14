import marimo

__generated_with = "0.8.0"
app = marimo.App(width="medium")


@app.cell
def __(mo):
    mo.md(
        r"""
        # Review of House Price Index data

        Select `Region` to plot its data. (e.g. London, Wales, Swansea)
        """
    )
    return


@app.cell
def __():
    import marimo as mo
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    from data import get_hpi
    from plotting import y_in_thousands, highlight_periods
    return get_hpi, highlight_periods, mo, pd, plt, sns, y_in_thousands


@app.cell
def __(sns):
    sns.set_theme(rc={'figure.figsize':(11.7,7)})
    return


@app.cell
def __(mo):
    region = mo.ui.text(label="Region").form()
    region
    return region,


@app.cell
def __(get_hpi, highlight_periods, plt, region, sns, y_in_thousands):
    hpi = get_hpi(region.value)
    price_columns = [
        "AveragePrice",
        "DetachedPrice",
        "SemiDetachedPrice",
        "FlatPrice",
        "TerracedPrice"
    ]

    hpi_view = hpi.melt(id_vars="date", var_name="type", value_name="price",value_vars=price_columns)
    hpi_view


    plt.title(f"Avarage House Prices in {region.value}")
    plt.xticks(rotation=90)
    plt.xticks(range(0, hpi['date'].nunique(), 12))
    plt.xlabel("Year and Month")
    plt.ylabel("Average Price")

    highlight_periods(
        y_in_thousands(
            sns.lineplot(data=hpi_view, x="date", y="price", hue="type")
        ), hpi["date"], hpi["period"]
    )
    return hpi, hpi_view, price_columns


if __name__ == "__main__":
    app.run()
