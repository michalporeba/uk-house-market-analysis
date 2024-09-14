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
        get_postcodes,
        get_postcode_location,
        filter_to_local,
        get_hsp_from
    )
    from plotting import (get_map, y_in_thousands, highlight_periods)
    return (
        filter_to_local,
        get_hpi,
        get_hsp_from,
        get_map,
        get_postcode_location,
        get_postcodes,
        highlight_periods,
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
    point_size = 100/(focus_distance_m/500)
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
        point_size,
    )


@app.cell
def __(fhsp, focus_distance_m, focus_point, get_map, point_size, sns):
    old_sales = fhsp[fhsp["period"] == "Old"]
    modern_sales = fhsp[fhsp["period"] != "Old"]

    all_sales_plot = get_map(focus_point, focus_distance_m, "All sales covered by the analysis")
    all_sales_plot.scatter(old_sales.x, old_sales.y, alpha=0.2, c="grey", s=point_size)

    sns.scatterplot(data=modern_sales, ax=all_sales_plot, x='x', y='y', hue='period', s=point_size, alpha=0.5)

    #all_sales_plot
    return all_sales_plot, modern_sales, old_sales


@app.cell
def __():
    return


if __name__ == "__main__":
    app.run()
