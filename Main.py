from Network.Graph import Graph
from Network.Edge import Edge
from Network.Vertex import Vertex


def Main():
    vertices = [Vertex("X1"), Vertex("X2"), Vertex("X3"), Vertex("X4"), Vertex("X5"),
                Vertex("X6"), Vertex("X7"), Vertex("X8"), Vertex("X9"), Vertex("X10")]
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
    print graph

Main()

