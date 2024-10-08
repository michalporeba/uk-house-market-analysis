import marimo

__generated_with = "0.8.0"
app = marimo.App(width="medium")


@app.cell
def __(mo):
    mo.md(r"""# Review the house sale data""")
    return


@app.cell
def __():
    import marimo as mo
    import numpy as np
    import pandas as pd
    import geopandas as gpd
    import matplotlib.pyplot as plt
    import seaborn as sns
    import osmnx as ox
    from data import (
        add_indexed_house_prices,
        get_postcodes,
        get_postcode_location,
        filter_to_local,
        get_hsp_from,
        y_in_thousands
    )
    return (
        add_indexed_house_prices,
        filter_to_local,
        get_hsp_from,
        get_postcode_location,
        get_postcodes,
        gpd,
        mo,
        np,
        ox,
        pd,
        plt,
        sns,
        y_in_thousands,
    )


@app.cell
def __(
    filter_to_local,
    get_hsp_from,
    get_postcode_location,
    get_postcodes,
):
    # load the data for analysis
    # first load postcodes, they come in files by area
    postcodes = get_postcodes('SA')
    # find a physical location of a specific postcode
    centre = get_postcode_location(postcodes, 'SA2 0DE')
    # filter the postcodes down to 10km around that physical location
    postcodes = filter_to_local(postcodes, centre, 10_000)
    # get the sales data for that area
    hsp = get_hsp_from(postcodes, 'Swansea')
    return centre, hsp, postcodes


@app.cell
def __(mo):
    mo.md(r"""Loaded {{len(hsp)}} sales records 10km around SA2 0DE""")
    return


@app.cell
def __():
    return


@app.cell
def __(
    filter_to_local,
    get_postcode_location,
    hsp,
    np,
    ox,
    postcodes,
    sns,
):
    sns.set_theme(rc={'figure.figsize':(10,10)})

    jitter_factor = 0.0005
    hsp['x'] = hsp.geometry.x + np.random.uniform(-jitter_factor, jitter_factor, size=len(hsp))
    hsp['y'] = hsp.geometry.y + np.random.uniform(-jitter_factor, jitter_factor, size=len(hsp))

    point = get_postcode_location(postcodes, 'SA2 8NA')
    distance = 2200
    local_sales = filter_to_local(hsp, point, distance)

    graph = ox.graph_from_point((point.y, point.x), dist=distance, network_type="all", truncate_by_edge=True)

    fig, ax = ox.plot_graph(graph, bgcolor="#ffffff", edge_color="#555555", node_size=0, figsize=(15,15), dpi=300)

    local_postcodes = filter_to_local(postcodes, point, distance)

    #ax.scatter(point.x, point.y, c="green", s=100, alpha=0.2)
    #sns.scatterplot(3x="x", y="y", hue="year", alpha=0.5)
    ax.scatter(local_sales.geometry.x, local_sales.geometry.y, alpha=0.01, c="red", s=150)
    ax.scatter(point.x, point.y, c="red", s=50)

    #ax.set_title(f"Postcode locations within {distance}m of {postcode}")
    print(len(local_sales))
    print(len(local_sales)/local_sales['date'].nunique())

    ax
    return (
        ax,
        distance,
        fig,
        graph,
        jitter_factor,
        local_postcodes,
        local_sales,
        point,
    )


if __name__ == "__main__":
    app.run()
