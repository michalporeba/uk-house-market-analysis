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
    import math
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
        math,
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
        "distance": mo.ui.slider(start=100, stop=3000, step=100, value=500, show_value=True),
        "leasholds": mo.ui.switch(value=False),
        "newbuilds": mo.ui.switch(value=False),
    }).form(submit_button_label="Analyse")
    parameters
    return parameters,


@app.cell
def __(
    filter_to_local,
    get_postcode_location,
    hsp,
    math,
    mo,
    parameters,
    postcodes,
):
    import numpy as np

    # convert parameters to useful local variables
    focus_postcode = parameters.value["postcode"]
    focus_distance_m = parameters.value["distance"]
    focus_point = get_postcode_location(postcodes, focus_postcode)
    include_leasholds = parameters.value["leasholds"]
    include_newbuilds = parameters.value["newbuilds"]

    # size of the point dependant on the scale of the map
    point_size = 100/(focus_distance_m/500)
    custom_category_order = ["DETACHED", "SEMI-DETACHED", "TERRACED", "FLAT", "OTHER"]

    # narrow the data from the House Sale Prices (HSP) to the local focused area
    fhsp = filter_to_local(hsp, focus_point, focus_distance_m)

    # handle removal of leasholds if requested
    leasholds_count = len(fhsp[fhsp['transaction_type'] == 'LEASHOLD'])
    if leasholds_count == 0:
        leasholds_message = "There were no leasholds sold here since 1995."
    elif not include_leasholds:
        leasholds_message = f"Excluding {leasholds_count} leasholds."
        fhsp = fhsp[fhsp["transaction_type"] != "LEASHOLD"]
    else:
        leasholds_message = f"Including {leasholds_count} leasholds."

    # handle removal of new builds if requested
    newbuilds_count = len(fhsp[fhsp['is_new_build'] == 'T'])
    if newbuilds_count == 0:
        newbuilds_message = "There were no new builds sold here since 1995."
    elif not include_newbuilds:
        newbuilds_message = f"Excluding {newbuilds_count} new builds."
        fhsp = fhsp[fhsp["is_new_build"] != "T"]
    else:
        newbuilds_message = "Including {newbuilds_count} new builds."

    newbuild_leasholds_count = len(fhsp[(fhsp['transaction_type'] == 'LEASHOLD') & (fhsp['is_new_build'] == 'T')])
    newbuild_leasholds_message = ""
    if newbuild_leasholds_count > 0:
        newbuild_leasholds_message = f"There were {newbuild_leasholds_count} newbuild leasholds here since 1995."

    # calculate jitter to show multiple sales within the same postcode
    jitter_factor = 0.0005
    fhsp['x'] = fhsp.geometry.x + np.random.uniform(-jitter_factor, jitter_factor, size=len(fhsp))
    fhsp['y'] = fhsp.geometry.y + np.random.uniform(-jitter_factor, jitter_factor, size=len(fhsp))

    months = hsp["date"].nunique()
    mean_monthly_sales = round(len(fhsp)/months,2)
    area_in_km2 = math.pi * (focus_distance_m/1000)**2

    mo.md(f"""
    Analysing **{len(fhsp)}** sales up to **{focus_distance_m}m** from **{focus_postcode}**.</br>
    {leasholds_message}</br>
    {newbuilds_message}</br>
    {newbuild_leasholds_message}\n
    On average there are **{mean_monthly_sales}** sales here per month in this area
    (**{round(mean_monthly_sales / area_in_km2, 2)}** sales per month per km2).
    """)

    return (
        area_in_km2,
        custom_category_order,
        fhsp,
        focus_distance_m,
        focus_point,
        focus_postcode,
        include_leasholds,
        include_newbuilds,
        jitter_factor,
        leasholds_count,
        leasholds_message,
        mean_monthly_sales,
        months,
        newbuild_leasholds_count,
        newbuild_leasholds_message,
        newbuilds_count,
        newbuilds_message,
        np,
        point_size,
    )


@app.cell
def __(fhsp, focus_distance_m, focus_point, get_map, point_size, sns):
    old_sales = fhsp[fhsp["period"] == "Old"]
    modern_sales = fhsp[fhsp["period"] != "Old"]

    all_sales_plot = get_map(focus_point, focus_distance_m, "All sales covered by the analysis (approximate locations)")
    all_sales_plot.scatter(old_sales.x, old_sales.y, alpha=0.2, c="grey", s=point_size)

    sns.scatterplot(data=modern_sales, ax=all_sales_plot, x='x', y='y', hue='period', s=point_size, alpha=0.5)

    #all_sales_plot
    return all_sales_plot, modern_sales, old_sales


@app.cell
def __(custom_category_order, fhsp, plt, sns):
    types_of_properties = fhsp.groupby(["property_type"]).agg({'id': 'count'}).reset_index()
    types_of_properties = types_of_properties.rename(columns={'id': 'percentage'}).reset_index()
    types_of_properties["percentage"] = round((types_of_properties["percentage"] / len(fhsp)) * 100, 10)

    ax = sns.barplot(data=types_of_properties, x='property_type', y='percentage', palette='viridis', order=custom_category_order)

    ax.set_title("Types of properties sold in the area")
    ax.set_xlabel("")
    plt.ylabel('Percentage')

    return ax, types_of_properties


@app.cell
def __(hsp, pd):
    start_date = hsp['date'].min()
    end_date = hsp['date'].max()

    date_range = pd.date_range(start=start_date, end=end_date, freq='MS').strftime('%Y-%m')
    date_range
    return date_range, end_date, start_date


@app.cell
def __(date_range, fhsp, highlight_periods, hpi, pd, plt, sns):
    sns.set_theme(rc={'figure.figsize':(11.7,7)})
    volume_of_sales = fhsp.groupby(['date', 'property_type']).agg({'period': 'max', 'id': 'count'}).reset_index()
    volume_of_sales = volume_of_sales.rename(columns={'id': 'volume'}).reset_index()

    volume_of_sales = pd.merge(pd.DataFrame({'date': date_range}), volume_of_sales, on='date', how='left')

    plt.title(f"Volume of sales")
    plt.xticks(rotation=90)
    plt.xticks(range(0, hpi['date'].nunique(), 12))
    plt.xlabel("Year and Month")
    plt.ylabel("Number of sales")

    highlight_periods(
        sns.lineplot(data=volume_of_sales, x="date", y="volume", hue="property_type"),
        volume_of_sales["date"], volume_of_sales["period"]
    )

    volume_of_sales

    return volume_of_sales,


if __name__ == "__main__":
    app.run()
