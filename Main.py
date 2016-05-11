from TransmissionNetwork.Graph import Graph
from TransmissionNetwork.Edge import Edge
from TransmissionNetwork.Vertex import Vertex
from Algorithm.MessagePassing import MessagePassingAlgorithm
def test(dict):
    dict["a"] = 3


def main():
    # vertices = []
    # for i in range(0, 10):
    #     vertices.append(Vertex("X" + str(i + 1)))

    vertices = [Vertex("X1"), Vertex("X2"), Vertex("X3", 0), Vertex("X4", 1), Vertex("X5"),
                Vertex("X6", 1), Vertex("X7", 0), Vertex("X8"), Vertex("X9", 0), Vertex("X10", 1)]

    edges = [Edge(vertices[0], vertices[1], 0.1),
             Edge(vertices[1], vertices[2], 0.1),
             Edge(vertices[1], vertices[3], 0.2),
             Edge(vertices[0], vertices[4], 0.1),
             Edge(vertices[4], vertices[5], 0.1),
             Edge(vertices[4], vertices[6], 0.4),
             Edge(vertices[0], vertices[7], 0.1),
             Edge(vertices[7], vertices[8], 0.5),
             Edge(vertices[7], vertices[9], 0.3)]
    graph = Graph(vertices, edges)
    # for v in graph.vertices:
    #     print("Vertex: %s is a leaf: %s" % (v.name, graph.is_leaf(v)))

    # for v in graph.vertices:
    #     edges = graph.get_neighbour_edges(v)
    #     print("Vertex: %s has edges: %s" % (v.name, ','.join([str(e) for e in edges])))

    # for v in graph.vertices:
    #     vertices = graph.get_neighbour_vertices(v)
    #     print("Vertex: %s has edges: %s" % (v.name, ','.join([str(e) for e in vertices])))

    algorithm = MessagePassingAlgorithm(graph, graph.vertices[0])
    algorithm.computeMarginals()
main()


