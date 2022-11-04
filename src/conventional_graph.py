from typing import List
import networkx as nx
import pygraphviz

from parser import parse


def read(filename: str) -> nx.MultiDiGraph:
    G: nx.MultiDiGraph = nx.nx_agraph.from_agraph(pygraphviz.AGraph(filename=filename))
    GNodes: nx.Graph = nx.nx_agraph.from_agraph(
        pygraphviz.AGraph(filename=filename[:-4] + ".nodes.dot")
    )
    for node in G.nodes:
        G.nodes[node]["grid"] = parse(GNodes.nodes[node]["label"], start="node_label")
    for edge in G.edges:
        G.edges[edge]["grid"] = parse(G.edges[edge]["label"], start="edge_label")
    return G


def get_valid_terminal_nodes(G: nx.MultiDiGraph, config) -> List[str]:
    res = []

    for node in G.nodes():
        state = G.nodes[node]["grid"]
        valid = True
        for k in config:
            if k not in state or not state[k] or state[k][0][0] < config[k]:
                valid = False
                break
        if valid:
            res.append(node)
    return res
