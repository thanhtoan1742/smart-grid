from queue import PriorityQueue
import networkx as nx
import configuration_graph
import functools

INPUT_FORMAT = "../data/dots/{name}.dot"
MAX_VALUE = 2147483647

class Graph:
    def __init__(self, G, adj_edges):
        self.G : nx.MultiDiGraph = G 
        self.adj_edges = adj_edges
    
    def get_nodes(self):
        return self.G.nodes

    def get_detail(self, node):
        return self.G.nodes[node]["grid"]

    def get_consumer_power_list(self, node):
        detail = self.get_detail(node)
        return [cons[1][1] for cons in detail["Consumer"]]
    
    def get_edges(self, node):
        return self.adj_edges[node]

@functools.total_ordering
class Heu_element:
    request_state : list
    def __init__(self, cons_power_list, generated, cost, node):
        self.cons_power_list = cons_power_list
        self.generated = generated
        self.node = node
        self.cost = cost
        self.priority = self.get_priority()

    # def get_priority(self):
    #     priority = 0
    #     for i in range(len(Heu_element.request_state)):
    #         temp = (Heu_element.request_state[i] - self.cons_power_list[i]) / Heu_element.request_state[i]
    #         if temp > 0: priority += temp
    #     return priority

    def get_priority(self):
        priority = 0
        for i in range(len(Heu_element.request_state)):
            temp = (Heu_element.request_state[i] - self.cons_power_list[i]) / Heu_element.request_state[i]
            if temp > 0: priority += temp

        sumlst = sum(Heu_element.request_state)
        if (self.generated <= sumlst):
            priority += (sumlst - self.generated) 
        return priority

    def __lt__(self, other):
        return self.cost + self.priority < other.cost + other.priority

    def __eq__(self, other):
        return self.cost + self.priority == other.cost + other.priority

def isFinal(request_list, power_list):
    flag = True
    for i in range(len(power_list)):
        flag = flag and (request_list[i] <= power_list[i])
    return flag

def PrintResult(u, cost, trace, n_nodes):
    print(u, cost, n_nodes)
    lst = []
    
    while(trace[u]):
        lst.append(u)
        u = trace[u]
    
    lst.append(u)
    lst.reverse()
    print(lst)

def astar(graph: Graph, request_state):
    Q = PriorityQueue()
    f = {}
    in_path = {}
    trace = {}
    for node in graph.get_nodes():
        f[node] = MAX_VALUE
        in_path[node] = False
        trace[node] = None
    start = 'N1'
    f[start] = 0

    
    Heu_element.request_state = request_state
    Q.put(Heu_element(graph.get_consumer_power_list(start), graph.get_detail(start)["Generated"][0][1],0, start))

    while not Q.empty():
        u: Heu_element = Q.get()
        if (in_path[u.node]):
            continue
        if (isFinal(request_state, u.cons_power_list)):
            n_nodes = 0
            for key, item in in_path.items():
                if item == True: n_nodes += 1
            PrintResult(u.node, f[u.node], trace, n_nodes)
            return
        
        in_path[u.node] = True
        for edge in graph.get_edges(u.node):
            v = edge["to"]
            new_cost = f[u.node] + 1
            if ((not in_path[v]) and new_cost < f[v]):
                f[v] = new_cost
                Q.put(Heu_element(graph.get_consumer_power_list(v),graph.get_detail(v)["Generated"][0][1], f[v], v))
                trace[v] = u.node

def configuration_4_astar():
    name = "test"
    input_file = INPUT_FORMAT.format(name=name)
    G: nx.MultiDiGraph = configuration_graph.read(input_file)

    adj_edges = {}
    for edge in G.edges:
        u = edge[0]
        if (u not in adj_edges): adj_edges[u] = []
        adj_edges[u] = adj_edges[u] + [{
            "to": edge[1],
            "info": G.edges[edge]["grid"]
        }]

    request_state = [100, 800, 450]

    graph = Graph(G, adj_edges)
    astar(graph, request_state)

configuration_4_astar()
