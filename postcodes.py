import marimo

__generated_with = "0.8.0"
app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo
    import pandas as pd
    import matplotlib.pyplot as plt
    import geopandas as gpd
    import osmnx as ox
    from shapely import Point
    from data import get_postcodes, get_postcode_location, filter_to_local
    return (
        Point,
        filter_to_local,
        get_postcode_location,
        get_postcodes,
        gpd,
        mo,
        ox,
        pd,
        plt,
    )


@app.cell
def __(mo):
    config = mo.ui.dictionary(
        {
            "postcode": mo.ui.text(label="postcode", value="SA2 0DE"),
            "distance": mo.ui.slider(500, 2000, label="distance (m)", step=100, show_value=True, value=1000)
        }
    ).form()
    config
    return config,


@app.cell
def __(config, get_postcodes):
    postcodes = get_postcodes(config.value['postcode'])

    #postcodes
    return postcodes,


@app.cell
def __(config, filter_to_local, get_postcode_location, ox, postcodes):
    postcode = config.value['postcode']
    point = get_postcode_location(postcodes, postcode)
    location = (point.y, point.x)
    distance = config.value['distance']

    graph = ox.graph_from_point(location, dist=distance, network_type="all", truncate_by_edge=True)

    fig, ax = ox.plot_graph(graph, bgcolor="#ffffff", edge_color="#555555", node_size=0)

    local_postcodes = filter_to_local(postcodes, point, distance)

    ax.scatter(local_postcodes.geometry.x, local_postcodes.geometry.y, c='red', alpha=0.5)
    ax.scatter(point.x, point.y, c="green", s=100, alpha=0.5)
    ax.set_title(f"Postcode locations within {distance}m of {postcode}")
    ax
    return (
        ax,
        distance,
        fig,
        graph,
        local_postcodes,
        location,
        point,
        postcode,
    )


if __name__ == "__main__":
    app.run()
