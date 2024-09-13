import osmnx as ox

def get_map(point, distance, title=None):
  graph = ox.graph_from_point((point.y, point.x), dist=distance, network_type="all", truncate_by_edge=True)
  fix, ax = ox.plot_graph(graph, bgcolor="#ffffff", edge_color="#555555", node_size=0, figsize=(15,15), dpi=300)
  if title is not None:
    ax.set_title(title)
    
  return ax