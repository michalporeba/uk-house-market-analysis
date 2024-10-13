import marimo

__generated_with = "0.8.0"
app = marimo.App(width="medium")


@app.cell
def __():
    from configuration import get_configuration
    return get_configuration,


@app.cell
def __(get_configuration):
    get_configuration()
    return


if __name__ == "__main__":
    app.run()
