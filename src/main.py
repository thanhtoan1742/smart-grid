import networkx as nx
import conventional_graph
import configuration_graph
from utils import timer


INPUT_FORMAT = "data/dots/{name}.dot"


def conventional_1_bfs():
    name = "conventional_1"
    input_file = INPUT_FORMAT.format(name=name)
    G: nx.MultiDiGraph = conventional_graph.read(input_file)

    print(name)

    @timer
    def run():
        terminal_nodes = conventional_graph.valid_terminal_nodes(
            G,
            {
                "C1": 3,
                "C2": 1,
                "C3": 2,
                "Ba1": 2,
            },
        )
        print(conventional_graph.bfs_path(G, terminal_nodes))

    run()


def conventional_1_cost_dijkstra():
    name = "conventional_1"
    input_file = INPUT_FORMAT.format(name=name)
    G: nx.MultiDiGraph = conventional_graph.read(input_file)

    cost = {
        "CB1": 3,
        "CB2": 5,
    }

    for edge in G.edges:
        name = list(G.edges[edge]["grid"].keys())[0]
        if name in cost:
            G.edges[edge]["weigth"] = cost[name]
        else:
            G.edges[edge]["weigth"] = 0

    print("conventional_1_cost_dijkstra")

    @timer
    def run():
        terminal_nodes = conventional_graph.valid_terminal_nodes(
            G,
            {
                "C1": 3,
                "C2": 1,
                "C3": 2,
                "Ba1": 2,
            },
        )
        print(conventional_graph.dijkstra_path(G, terminal_nodes))

    run()


def conventional_4_bfs():
    name = "conventional_4"
    input_file = INPUT_FORMAT.format(name=name)
    G: nx.MultiDiGraph = conventional_graph.read(input_file)

    print(name)

    @timer
    def run():
        terminal_nodes = conventional_graph.valid_terminal_nodes(
            G,
            {
                "C1": 3,
                "C2": 1,
                "C3": 2,
            },
        )
        print(conventional_graph.bfs_path(G, terminal_nodes))

    run()


def conventional_4_cost_dijkstra():
    name = "conventional_4"
    input_file = INPUT_FORMAT.format(name=name)
    G: nx.MultiDiGraph = conventional_graph.read(input_file)

    cost = {
        "CB1": 3,
        "CB2": 5,
        "CB3": 2,
    }

    for edge in G.edges:
        name = list(G.edges[edge]["grid"].keys())[0]
        if name in cost:
            G.edges[edge]["weigth"] = cost[name]
        else:
            G.edges[edge]["weigth"] = 0

    print("conventional_4_cost_dijkstra")

    @timer
    def run():
        terminal_nodes = conventional_graph.valid_terminal_nodes(
            G,
            {
                "C1": 3,
                "C2": 1,
                "C3": 2,
            },
        )
        print(conventional_graph.dijkstra_path(G, terminal_nodes))

    run()


def configuration_1_bfs():
    name = "configuration_1"
    input_file = INPUT_FORMAT.format(name=name)
    G: nx.MultiDiGraph = configuration_graph.read(input_file)

    print(name)

    @timer
    def run():
        terminal_nodes = configuration_graph.valid_terminal_nodes(G)
        print(configuration_graph.bfs_path(G, terminal_nodes))

    run()


def configuration_1_cost_dijkstra():
    name = "configuration_1"
    input_file = INPUT_FORMAT.format(name=name)
    G: nx.MultiDiGraph = conventional_graph.read(input_file)

    cost = {
        1: 3 * 5,
        2: 5 * 3,
    }

    for edge in G.edges:
        name = list(G.edges[edge]["grid"].keys())[0]
        if name == "gen":
            G.edges[edge]["weight"] = cost[G.edges[edge]["grid"]["gen"]["gen"]["i"]]
        else:
            G.edges[edge]["weight"] = 0

    print("conventional_1_cost_dijkstra")

    @timer
    def run():
        terminal_nodes = configuration_graph.valid_terminal_nodes(G)
        print(configuration_graph.dijkstra_path(G, terminal_nodes))

    run()


def configuration_4_bfs():
    name = "configuration_4"
    input_file = INPUT_FORMAT.format(name=name)
    G: nx.MultiDiGraph = configuration_graph.read(input_file)

    print(name)

    @timer
    def run():
        terminal_nodes = configuration_graph.valid_terminal_nodes(G)
        print(configuration_graph.bfs_path(G, terminal_nodes))

    run()


conventional_1_bfs()
conventional_4_bfs()
# conventional_1_cost_dijkstra()
# conventional_4_cost_dijkstra()
configuration_1_bfs()
configuration_4_bfs()
# configuration_1_cost_dijkstra()