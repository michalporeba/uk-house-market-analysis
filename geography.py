import marimo

__generated_with = "0.8.0"
app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo
    import pandas as pd
    import os
    import matplotlib.pyplot as plt
    import seaborn as sns
    from shapely.geometry import Point, LineString, Polygon
    return LineString, Point, Polygon, mo, os, pd, plt, sns


@app.cell
def __(pd, sns):
    file = 'data/postcodes/sa.csv'
    postcode_columns = ['postcode', 'quality', 'easting', 'northing']

    postcodes = pd.read_csv(file, header=None, usecols=[0,1,2,3], names=postcode_columns)
    postcodes.reset_index(inplace=True)
    postcodes['area'] = postcodes['postcode'].str[:2]
    postcodes['district'] = postcodes['postcode'].str[:4]
    postcodes['district'] = postcodes['district'].str.strip()
    postcodes['sector'] = postcodes['postcode'].str[:5]

    local_postcodes = postcodes[postcodes['district'].isin(['SA1', 'SA2', 'SA3', 'SA4', 'SA5', 'SA6'])]
    sns.set_theme(rc={'figure.figsize':(11.7,8.27)})
    sns.scatterplot(data=local_postcodes, x="easting", y="northing", hue="district")
    return file, local_postcodes, postcode_columns, postcodes


@app.cell
def __(pd):
    hpi = pd.read_csv('data/UK-HPI-full-file-2024-06.csv')
    hpi = hpi[hpi['RegionName']=='Swansea']
    hpi["date"] = pd.to_datetime(hpi["Date"])
    hpi['date'] = hpi['date'].dt.strftime('%Y-%d')
    hpi
    return hpi,


@app.cell
def __(mo):
    mo.md(
        """
        ## Load the property prices

        chunk it and filter to only local postcodes
        """
    )
    return


@app.cell
def __(local_postcodes, pd):
    prices_columns = ['id', 'price', 'ts', 'postcode', 'property_type', 'is_new_build', 'transaction_type', 'paon']

    local_sales = pd.DataFrame()
    chunk_size = 10000

    for chunk in pd.read_csv('data/pp-complete.csv', header=None, usecols=[0,1,2,3,4,5,6,7], names=prices_columns, chunksize=chunk_size):
        filtered = chunk[chunk['postcode'].isin(local_postcodes['postcode'])]
        local_sales = pd.concat([local_sales, filtered], ignore_index=True)

    local_sales = local_sales.sort_values('ts')
    return chunk, chunk_size, filtered, local_sales, prices_columns


@app.cell
def __(local_sales, pd):
    local_sales['area'] = local_sales['postcode'].str[:2]
    local_sales['district'] = local_sales['postcode'].str[:4]
    local_sales['district'] = local_sales['district'].str.strip()
    local_sales['sector'] = local_sales['postcode'].str[:5]

    local_sales['date'] = pd.to_datetime(local_sales['ts'])
    local_sales['date'] = local_sales['date'].dt.strftime('%Y-%m')
    local_sales['year'] = local_sales['date'].str[:4]
    local_sales['average_price'] = -1
    local_sales['hpi'] = -1

    local_sales
    return


@app.cell
def __(hpi, local_sales, pd):
    indexed_sales = pd.merge(local_sales, hpi, on="date", how="left")

    indexed_sales.loc[indexed_sales['property_type'] == 'D', 'average_price'] = indexed_sales['DetachedPrice']
    indexed_sales.loc[indexed_sales['property_type'] == 'D', 'hpi'] = indexed_sales['DetachedIndex']

    indexed_sales.loc[indexed_sales['property_type'] == 'S', 'average_price'] = indexed_sales['SemiDetachedPrice']
    indexed_sales.loc[indexed_sales['property_type'] == 'S', 'hpi'] = indexed_sales['SemiDetachedIndex']

    indexed_sales.loc[indexed_sales['property_type'] == 'T', 'average_price'] = indexed_sales['TerracedPrice']
    indexed_sales.loc[indexed_sales['property_type'] == 'T', 'hpi'] = indexed_sales['TerracedIndex']

    indexed_sales.loc[indexed_sales['property_type'] == 'F', 'average_price'] = indexed_sales['FlatPrice']
    indexed_sales.loc[indexed_sales['property_type'] == 'F', 'hpi'] = indexed_sales['FlatIndex']

    indexed_sales.loc[indexed_sales['hpi'] < 0, 'average_price'] = indexed_sales['AveragePrice']
    indexed_sales.loc[indexed_sales['hpi'] < 0, 'hpi'] = indexed_sales['Index']

    hpi_column_index = indexed_sales.columns.get_loc('hpi')
    indexed_sales = indexed_sales.iloc[:, :hpi_column_index+1]

    indexed_sales['indexed_price'] = indexed_sales['price'] / (indexed_sales['hpi'] / 100)
    indexed_sales['distance_from_mean'] = 100*indexed_sales['price']/indexed_sales['average_price']

    #indexed_sales[(indexed_sales['postcode'] == 'SA2 0DE') & (indexed_sales['paon'] == '7')]
    #indexed_sales[indexed_sales['district'] == 'SA2']
    indexed_sales
    return hpi_column_index, indexed_sales


@app.cell
def __():
    ## price change over time by postcode district
    return


@app.cell
def __(indexed_sales, plt, sns):
    prices_over_time = indexed_sales.groupby(['year', 'district'])['indexed_price'].agg(['mean'])

    plt.xticks(rotation=90)
    sns.lineplot(data=prices_over_time, x="year", y="mean", hue="district")
    return prices_over_time,


@app.cell
def __(indexed_sales, plt, sns):
    sa2only = indexed_sales[indexed_sales['district'] == 'SA2']
    prices_over_time_in_sa2 = sa2only.groupby(['year', 'sector'])['indexed_price'].agg(['mean'])

    plt.xticks(rotation=90)
    sns.lineplot(data=prices_over_time_in_sa2, x="year", y="mean", hue="sector")
    return prices_over_time_in_sa2, sa2only


@app.cell
def __(plt, sa2only, sns):
    plt.xticks(rotation=90)
    plt.xticks(range(0, sa2only['date'].nunique(), 6))
    sns.scatterplot(data=sa2only, x="date", y="hpi", hue="sector")
    return


@app.cell
def __(plt, sa2only, sns):
    plt.xticks(rotation=90)
    plt.xticks(range(0, sa2only['date'].nunique(), 6))
    recent_only = sa2only[sa2only['year'] > '2020']
    sns.scatterplot(data=recent_only, x="date", y="hpi", hue="property_type")
    return recent_only,


@app.cell
def __(plt, sa2only, sns):
    plt.xticks(rotation=90)
    plt.xticks(range(0, sa2only['date'].nunique(), 6))
    plt.ylim(10, 500)
    sns.scatterplot(data=sa2only, x="date", y="distance_from_mean", hue="sector")
    return


if __name__ == "__main__":
    app.run()
