from typing import List, Tuple
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


def valid_terminal_nodes(G: nx.MultiDiGraph) -> List[str]:
    terminal_nodes = []
    for n in G.nodes:
        valid = True
        for consumer in G.nodes[n]["grid"]["Consumer"]:
            typ = consumer[1][0]["t"]
            if typ == "BAT":
                continue
            cap = consumer[1][0]["c"]
            power = consumer[1][1]
            if power < cap:
                valid = False
                break
        if valid:
            terminal_nodes.append(n)
    return terminal_nodes


def bfs_path(
    G: nx.MultiDiGraph, terminal_nodes: List[str]
) -> Tuple[str, List[str], int]:
    path = nx.single_source_shortest_path(G, "N1")
    min_lenth = min([len(path[n]) for n in terminal_nodes])
    for n in terminal_nodes:
        if len(path[n]) == min_lenth:
            return n, path[n], len(path[n])

    return None, [], -1


def dijkstra_path(
    G: nx.MultiDiGraph, terminal_nodes: List[str]
) -> Tuple[str, List[str], int]:
    path = nx.single_source_dijkstra_path(G, "N1")
    length = nx.single_source_dijkstra_path_length(G, "N1")
    min_lenth = min([length[n] for n in terminal_nodes])
    for n in terminal_nodes:
        if length[n] == min_lenth:
            return n, path[n], min_lenth

    return None, [], -1
