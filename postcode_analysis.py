import marimo

__generated_with = "0.8.0"
app = marimo.App(width="medium")


@app.cell
def __(mo):
    mo.md(r"""# House prices around a specific postcode""")
    return


@app.cell
def __():
    import marimo as mo
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    from data import get_hpi, y_in_thousands
    return get_hpi, mo, pd, plt, sns, y_in_thousands


if __name__ == "__main__":
    app.run()
