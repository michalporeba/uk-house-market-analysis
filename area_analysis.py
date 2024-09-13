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
    from data import (
        get_hpi,
        y_in_thousands,
        get_postcodes,
        get_postcode_location,
        filter_to_local,
        get_hsp_from
    )
    from plotting import (get_map)
    return (
        filter_to_local,
        get_hpi,
        get_hsp_from,
        get_map,
        get_postcode_location,
        get_postcodes,
        mo,
        pd,
        plt,
        sns,
        y_in_thousands,
    )


@app.cell
def __(
    filter_to_local,
    get_hpi,
    get_hsp_from,
    get_postcode_location,
    get_postcodes,
):
    # load the data for analysis
    # first load postcodes, they come in files by area
    area_distance_km = 10
    area_postcode = 'SA2 0DE'
    postcodes = get_postcodes('SA')
    # find a physical location of a specific postcode
    centre = get_postcode_location(postcodes, area_postcode)
    # filter the postcodes down to 10km around that physical location
    postcodes = filter_to_local(postcodes, centre, area_distance_km*1000)
    # get the sales data for that area
    hsp = get_hsp_from(postcodes, 'Swansea')
    hpi = get_hpi('Swansea')
    return area_distance_km, area_postcode, centre, hpi, hsp, postcodes


@app.cell
def __(area_distance_km, area_postcode, hsp, mo, postcodes):
    mo.md(f""" 
    Loaded **{len(hsp)}** sales up to **{area_distance_km}km** from **{area_postcode}**.
    The sales were in **{hsp["postcode"].nunique()}** out of **{len(postcodes)}** postcodes.
    """)
    return


@app.cell
def __(mo):
    parameters = mo.ui.dictionary({
        "postcode": mo.ui.text(),
        "distance": mo.ui.slider(start=100, stop=3000, step=100, value=500, show_value=True)
    }).form(submit_button_label="Analyse")
    parameters
    return parameters,


@app.cell
def __(
    filter_to_local,
    get_postcode_location,
    hsp,
    mo,
    parameters,
    postcodes,
):
    import numpy as np
    focus_postcode = parameters.value["postcode"]
    focus_distance_m = parameters.value["distance"]
    focus_point = get_postcode_location(postcodes, focus_postcode)
    fhsp = filter_to_local(hsp, focus_point, focus_distance_m)

    jitter_factor = 0.0005
    fhsp['x'] = fhsp.geometry.x + np.random.uniform(-jitter_factor, jitter_factor, size=len(fhsp))
    fhsp['y'] = fhsp.geometry.y + np.random.uniform(-jitter_factor, jitter_factor, size=len(fhsp))

    mo.md(f"""
    Analysing **{len(fhsp)}** sales up to **{focus_distance_m}m** from **{focus_postcode}**.
    """)
    return (
        fhsp,
        focus_distance_m,
        focus_point,
        focus_postcode,
        jitter_factor,
        np,
    )


@app.cell
def __(fhsp, focus_distance_m, focus_point, get_map):
    old_sales = fhsp[fhsp["date"] < "2012-01"]
    modern_sales = fhsp[(fhsp["date"] >= "2012-01") & (fhsp["date"] < "2020-03")]
    covid_sales = fhsp[(fhsp["date"] >= "2020-03") & (fhsp["date"] < "2023-03")]
    recent_sales = fhsp[fhsp["date"] >= "2023-03"]


    all_sales_plot = get_map(focus_point, focus_distance_m, "All sales covered by the analysis")
    #all_sales_plot.scatter(fhsp.geometry.x, fhsp.geometry.y, alpha=0.01, c="green", s=150)
    all_sales_plot.scatter(old_sales.x, old_sales.y, alpha=0.05, c="grey", s=100)
    all_sales_plot.scatter(modern_sales.x, modern_sales.y, alpha=0.1, c="green", s=100)
    all_sales_plot.scatter(covid_sales.x, covid_sales.y, alpha=0.2, c="red", s=100)
    all_sales_plot.scatter(recent_sales.x, recent_sales.y, alpha=0.2, c="yellow", s=100)

    all_sales_plot
    return (
        all_sales_plot,
        covid_sales,
        modern_sales,
        old_sales,
        recent_sales,
    )


@app.cell
def __(fhsp):
    fhsp
    return


if __name__ == "__main__":
    app.run()
