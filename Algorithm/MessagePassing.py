from TransmissionNetwork.Graph import Graph

def computeMarginals(graph, root):
    collect_result = collect(graph, root)
    distribute(root, None)


def collect(graph: Graph , v, phi, m):
    if graph.is_leaf(v):
        phi[v] = 1
    else:
        for child in graph.get_neighbours(v):
            m[child, v] = collect(graph, child, phi, m)
            phi[v] = phi[v] * m[child, v]
    if graph.is_root(v):
        return phi[v]
    else:
        u = graph.get_parent(v)
        sum = 0
        for value in v.values:
            sum += graph.get_edge(v, u)