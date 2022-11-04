import re
import pygraphviz as pgv
import networkx as nx
import sys

import conventional_graph

arg = sys.argv[1]
input_file = f"data/dots/{arg}.dot"

G: nx.MultiDiGraph = conventional_graph.read(input_file)
tns = conventional_graph.get_valid_terminal_nodes(
    G,
    {
        "C1": 3,
        "C2": 1,
        "C3": 2,
    },
)
path = nx.single_source_shortest_path(G, "N1")
for n in tns:
    print(n, path[n])
    print(G.nodes[n]["grid"])
    cbs = set()
    for i in range(1, len(path[n])):
        x = path[n][i - 1]
        y = path[n][i]
        # print(x, y, G[x][y][0]["grid"].keys())
        cbs.update(set(G[x][y][0]["grid"].keys()))

    print(cbs)
