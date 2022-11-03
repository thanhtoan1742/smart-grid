import re
import pygraphviz as pgv
import networkx as nx
import functools

INPUT_FILE = "data/dots/conventional_1.dot"


def count_terminal_node_from_raw_input(text: str) -> int:
    matches = re.findall(r"N\d+ \[label", text)
    # print('\n'.join(matches[:min(len(matches), 20)]))
    return len(matches)


with open(INPUT_FILE) as f:
    fc = f.read()
print("terminal nodes:", count_terminal_node_from_raw_input(fc))


G: nx.DiGraph = nx.nx_agraph.from_agraph(pgv.AGraph(INPUT_FILE))
print(len(G.nodes))
terminal_nodes = [n for n, d in G.out_degree() if d == 0]
print(len(terminal_nodes))
print(nx.is_weighted(G))
path = nx.single_source_shortest_path(G, "N1")
res, _ = min(
    [(n, path[n]) for n in terminal_nodes],
    key=lambda np: len(np[1]),
)
print(res, path[res], G.nodes[res]["label"], len(path[res]), sep="\n" + "-" * 30 + "\n")
