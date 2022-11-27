import functools
import sys
from queue import PriorityQueue

import networkx as nx

import configuration_graph

INPUT_FORMAT = "../data/dots/{name}.dot"
OUTPUT_FORMAT = "../data/path/{name}.txt"
MAX_VALUE = 2147483647


class Graph:
    def __init__(self, G, adj_edges):
        self.G: nx.MultiDiGraph = G
        self.adj_edges = adj_edges

    def get_nodes(self):
        return self.G.nodes

    def get_detail(self, node):
        return self.G.nodes[node]["grid"]

    def get_consumer_power_list(self, node):
        detail = self.get_detail(node)
        return [cons[1][1] for cons in detail["Consumer"]]

    def get_edges(self, node):
        if node not in self.adj_edges.keys():
            return []
        return self.adj_edges[node]


@functools.total_ordering
class Heu_element:
    request_state: list

    def __init__(self, cons_power_list, generated, cost, node):
        self.cons_power_list = cons_power_list
        self.generated = generated
        self.node = node
        self.cost = cost
        # self.priority = self.get_priority()
        self.priority = self.get_rever_priority()

    def get_rever_priority(self):
        priority = self.get_priority()
        if priority == 0:
            return 0
        return 1 / priority

    def get_priority(self):
        return self.h1()
        # return self.h2()
        # return 0

    def h1(self):
        priority = 0
        for i in range(len(Heu_element.request_state)):
            temp = (
                Heu_element.request_state[i] - self.cons_power_list[i]
            ) / Heu_element.request_state[i]
            if temp > 0:
                priority += temp
        return priority

    def h2(self):
        priority = 0
        for i in range(len(Heu_element.request_state)):
            temp = (
                Heu_element.request_state[i] - self.cons_power_list[i]
            ) / Heu_element.request_state[i]
            if temp > 0:
                priority += temp

        sumlst = sum(Heu_element.request_state) - sum(self.cons_power_list)
        if self.generated <= sumlst:
            priority += sumlst - self.generated
        return priority

    def __lt__(self, other):
        return self.cost + self.priority < other.cost + other.priority

    def __eq__(self, other):
        return self.cost + self.priority == other.cost + other.priority


def checkTerminal(detail):
    if detail["Generator"] == None and detail["Generated"][0][1] == 0:
        return True
    # for cons in detail["Consumer"]:
    #     c = cons[1][0]['c']
    #     p = cons[1][1]
    #     if c > p:
    #         return False
    # return True
    return False


def isFinal(request_list, detail):
    isTerminal = checkTerminal(detail)
    if not isTerminal:
        return False
    power_list = [cons[1][1] for cons in detail["Consumer"]]
    flag = True
    for i in range(len(power_list)):
        flag = flag and (request_list[i] <= power_list[i])
    return flag


def PrintResult(u, cost, trace, searched_nodes):
    lst = []
    while trace[u]:
        lst.append(u)
        u = trace[u]

    lst.append(u)
    lst.reverse()

    name = "case3_1"
    heuristic = "h1_rever"
    output_file = OUTPUT_FORMAT.format(name=name + "_" + heuristic)
    with open(output_file, "w") as f:
        sys.stdout = f  # Change the standard output to the file we created.
        print("Final node:", lst[-1])
        print("Cost:", cost)
        print("Path length: ", len(lst))
        print("Path:", lst)
        print("Length searched nodes:", len(searched_nodes))
        print("Searched nodes:", searched_nodes)
        # print(u, cost, len(searched_nodes))
        # print(lst)
        # print(searched_nodes)
        sys.stdout = sys.stdout  #


def astar(graph: Graph, request_state):
    Q = PriorityQueue()
    f = {}
    in_path = {}
    trace = {}
    searched_nodes = []
    for node in graph.get_nodes():
        f[node] = MAX_VALUE
        in_path[node] = False
        trace[node] = None
    start = "N1"
    f[start] = 0

    Heu_element.request_state = request_state
    Q.put(
        Heu_element(
            graph.get_consumer_power_list(start),
            graph.get_detail(start)["Generated"][0][1],
            0,
            start,
        )
    )

    while not Q.empty():
        u: Heu_element = Q.get()
        if in_path[u.node]:
            continue
        if isFinal(request_state, graph.get_detail(u.node)):
            searched_nodes.append(u.node)
            PrintResult(u.node, f[u.node], trace, searched_nodes)
            return

        in_path[u.node] = True
        searched_nodes.append(u.node)
        for edge in graph.get_edges(u.node):
            v = edge["to"]
            new_cost = f[u.node] + 1
            if (not in_path[v]) and new_cost < f[v]:
                f[v] = new_cost
                Q.put(
                    Heu_element(
                        graph.get_consumer_power_list(v),
                        graph.get_detail(v)["Generated"][0][1],
                        f[v],
                        v,
                    )
                )
                trace[v] = u.node


def configuration_4_astar():
    name = "example_2"
    input_file = INPUT_FORMAT.format(name=name)
    G: nx.MultiDiGraph = configuration_graph.read(input_file)

    print("Finish Parser")

    adj_edges = {}
    for edge in G.edges:
        u = edge[0]
        if u not in adj_edges:
            adj_edges[u] = []
        adj_edges[u] = adj_edges[u] + [{"to": edge[1], "info": G.edges[edge]["grid"]}]

    # request_state = [150, 100, 90, 250]
    # request_state = [1, 1]
    request_state = [1, 3, 1, 2]

    # terminal_nodes = []
    # for n in G.nodes:
    #     valid = True
    #     ls = []
    #     for consumer in G.nodes[n]["grid"]["Consumer"]:
    #         # cap = consumer[1][0]["c"]
    #         power = consumer[1][1]
    #         # if power < cap:
    #         #     valid = False
    #         #     break
    #         ls.append(power)
    #     for i in range(len(ls)):
    #         if ls[i] < request_state[i]:
    #             valid = False
    #             break
    #     if valid:
    #         terminal_nodes.append(n)

    # print(terminal_nodes)
    graph = Graph(G, adj_edges)
    # detail = graph.get_detail('N1655')
    # print(detail["Consumer"])
    astar(graph, request_state)


configuration_4_astar()
