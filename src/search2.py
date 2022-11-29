from queue import PriorityQueue
import networkx as nx
import configuration_graph
import functools
import json
from enum import Enum

INPUT_FORMAT = "../data/dots/{name}.dot"
OUTPUT_FORMAT = "../data/path/{name}.json"
MAX_VALUE = 2147483647

DOTFILE_NAME = 'case3_1'
HEURISTIC_NAME = 'h2'

class EdgeType(Enum):
    GEN = 1
    TRANS = 2


class Node:
    def __init__(self, id, grid):
        self.id = id
        self.info = self.parse_from_grid(grid)

    def parse_from_grid(self, grid):
        info = {}
        info['Generated'] = grid['Generated'][0][1]

        lst = []
        if grid['Generator'] is not None:
            for u in grid['Generator']:
                lst.append({
                    'config': u[1][0],
                    'power': u[1][1]
                })
        info['Generator'] = lst

        lst = []
        if grid['Consumer'] is not None:
            for u in grid['Consumer']:
                lst.append({
                    'config': u[1][0],
                    'power': u[1][1]
                })
        info['Consumer'] = lst
        return info

    def __str__(self) -> str:
        return f"""('id': {self.id}, 'info': {self.info}"""
        # return self.id

class Edge:
    def __init__(self, from_id, to_id, grid):
        self.from_id = from_id
        self.to_id = to_id
        self.type, self.info = self.parse_from_grid(grid)
        self.cost = self.cal_cost()

    def parse_from_grid(self, grid: dict):
        edge_type = EdgeType.GEN if 'gen' in grid.keys() else EdgeType.TRANS
        info = {}
        if edge_type == EdgeType.GEN:
            info = grid['gen']
        else:
            info = grid['trans']
        return edge_type, info
    
    def cal_cost(self):
        if self.type != EdgeType.GEN: 
            return 1
        if ('rcb_gen' in self.info.keys()) and (self.info['rcb_gen']) == 'OFF': 
            return 0
        return self.info['p1']

@functools.total_ordering
class HeuristicElement:
    request_state: list

    def __init__(self, id, cost, node: Node):
        self.id = id
        self.cost = cost
        self.node = node
        self.priority = self.get_priority()
        # print(id, self.priority)
        # self.priority = self.get_rever_priority()

    # def get_rever_priority(self):
    #     priority = self.get_priority()
    #     if priority == 0:
    #         return 0
    #     return 1 / priority
    def get_rever(self, value):
        if value == 0:
            return 0
        return 1 / value

    def get_priority(self):
        if HEURISTIC_NAME == self.h1.__name__:
            return self.h1()
        elif HEURISTIC_NAME == self.h2.__name__:
            return self.h2()
        elif HEURISTIC_NAME == self.h1.__name__ + '_rever':
            return self.get_rever(self.h1())
        elif HEURISTIC_NAME == self.h2.__name__ + '_rever':
            return self.get_rever(self.h1())
        return 0

    def h1(self):
        priority = 0
        for i in range(len(HeuristicElement.request_state)):
            temp = (
                HeuristicElement.request_state[i] - self.node.info['Consumer'][i]['power']
            ) / HeuristicElement.request_state[i]
            # print(temp, HeuristicElement.request_state[i] , self.node.info['Consumer'][i]['power'])
            if temp > 0:
                priority += temp
        return priority

    def h2(self):
        priority = self.h1()
        sumlst = sum(HeuristicElement.request_state) - sum([consumer['power'] for consumer in self.node.info['Consumer']])
        if self.node.info['Generated'] <= sumlst:
            priority += sumlst - self.node.info['Generated']
        
        return priority

    def __lt__(self, other):
        return self.cost + self.priority < other.cost + other.priority

    def __eq__(self, other):
        return self.cost + self.priority == other.cost + other.priority


def PrintResult(u, cost, trace, searched_nodes):
    lst = []
    while trace[u]:
        lst.append(u)
        u = trace[u]

    lst.append(u)
    lst.reverse()

    searched_edges = []
    for u in searched_nodes:
        if trace[u]:
            searched_edges.append(trace[u] + "-" + u)


    output = {
        "final_node": lst[-1],
        "cost": cost,
        "path_length": len(lst),
        "path": lst,
        "searched_nodes_length": len(searched_nodes),
        "searched_nodes": searched_nodes,
        "searched_edges": searched_edges,
    }

    output_file = OUTPUT_FORMAT.format(name=DOTFILE_NAME + "_" + HEURISTIC_NAME)
    print(output_file)
    json_object = json.dumps(output, indent=4)

    # Writing to sample.json
    with open(output_file, "w") as outfile:
        outfile.write(json_object)


class Graph:
    def __init__(self, G: nx.MultiDiGraph):
        self.nodes, self.adj_edges = self.read_from_dot_graph(G)
        self.request_state = []

    def read_from_dot_graph(self, G: nx.MultiDiGraph):
        nodes = {}
        for node in G.nodes:
            if node not in nodes:
                nodes[node] = []
            new_node = Node(node, G.nodes[node]["grid"])
            nodes[node] = new_node

        adj_edges = {}
        for edge in G.edges:
            u = edge[0]
            if u not in adj_edges:
                adj_edges[u] = []
            new_edge = Edge(u, edge[1], G.edges[edge]["grid"])
            adj_edges[u].append(new_edge)
        return nodes, adj_edges

    def set_request(self, request_state):
        self.request_state = request_state

    def get_edges(self, id):
        if id not in self.adj_edges.keys():
            return []
        return self.adj_edges[id]

    def checkTerminal(self, node: Node):
        if node.info["Generator"] == [] and node.info["Generated"] == 0:
            return True
        # for cons in detail["Consumer"]:
        #     c = cons[1][0]['c']
        #     p = cons[1][1]
        #     if c > p:
        #         return False
        # return True
        return False

    def isFinal(self, node: Node):
        isTerminal = self.checkTerminal(node)
        if not isTerminal:
            return False
        flag = True
        for consumer in node.info['Consumer']:
            flag = flag and (consumer['power'] >= consumer['config']['c'])
        return flag

    def astar(self):
        Q = PriorityQueue()
        f = {}
        in_path = {}
        trace = {}
        searched_nodes = []
        # searched_edges = []
        for node_id in self.nodes.keys():
            f[node_id] = MAX_VALUE
            in_path[node_id] = False
            trace[node_id] = None
        start_id = "N1"
        f[start_id] = 0

        HeuristicElement.request_state = self.request_state
        Q.put(
            HeuristicElement(
                start_id,
                f[start_id],
                self.nodes[start_id]
            )
        )

        while not Q.empty():
            u: HeuristicElement = Q.get()
            if in_path[u.id]:
                continue
            if self.isFinal(u.node):
                searched_nodes.append(u.id)
                PrintResult(
                    u.id,
                    f[u.id],
                    trace,
                    searched_nodes,
                )
                return

            in_path[u.id] = True
            searched_nodes.append(u.id)
            # if (trace[u.node]): searched_edges.append([trace[u.node], u.node])
            for edge in self.get_edges(u.id):
                v = edge.to_id
                new_cost = f[u.id] + edge.cost
                # new_cost = f[u.id] + 1
                # print(u.id, v, edge.cost, new_cost)
                if (not in_path[v]) and new_cost < f[v]:
                    f[v] = new_cost
                    Q.put(
                        HeuristicElement(
                            v,
                            f[v],
                            self.nodes[v]
                        )
                    )
                    trace[v] = u.id

def main():
    input_file = INPUT_FORMAT.format(name=DOTFILE_NAME)
    G: nx.MultiDiGraph = configuration_graph.read(input_file)

    graph = Graph(G)
    # graph.set_request([150, 100, 90, 250])
    graph.set_request([1,1])
    graph.astar()

main()