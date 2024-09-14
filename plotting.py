import osmnx as ox
import matplotlib.pyplot as plt

def format_in_thousands(value):
    return f"£{int(value / 1000):,}K"


def y_in_thousands(plot):
  ylabels = [format_in_thousands(x) for x in plot.get_yticks()]
  plot.set_yticks(plot.get_yticks())
  plot.set_yticklabels(ylabels)
  return plot


def highlight_periods(plot, dates, periods):
  max_y = plt.gca().get_ylim()[1]
  bubble = (periods == "Bubble") | (periods == "CoVID")
  crash = (periods == "Crash") | (periods == "Readjustment")
  
  plot.fill_between(dates, 0, max_y, where=bubble, color="orange", alpha=0.2, step="pre")
  plot.fill_between(dates, 0, max_y, where=crash, color="red", alpha=0.2, step="pre")
  return plot


  
def get_map(point, distance, title=None):
  graph = ox.graph_from_point((point.y, point.x), dist=distance, network_type="all", truncate_by_edge=True)
  fix, ax = ox.plot_graph(graph, bgcolor="#ffffff", edge_color="#555555", node_size=0, figsize=(15,15), dpi=300)
  if title is not None:
    ax.set_title(title)
    
  return ax