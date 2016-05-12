from TransmissionNetwork.Vertex import Vertex
from TransmissionNetwork.Edge import Edge
from TransmissionNetwork.Graph import Graph


class TransmissionNetwork:
    def __init__(self, x3, x4, x6, x7, x9, x10):
        self.vertices = [Vertex("X1"), Vertex("X2"), Vertex("X3", x3), Vertex("X4", x4), Vertex("X5"),
                         Vertex("X6", x6), Vertex("X7", x7), Vertex("X8"), Vertex("X9", x9), Vertex("X10", x10)]
        self.edges = [Edge(self.vertices[0], self.vertices[1], 0.1),
                      Edge(self.vertices[1], self.vertices[2], 0.1),
                      Edge(self.vertices[1], self.vertices[3], 0.2),
                      Edge(self.vertices[0], self.vertices[4], 0.1),
                      Edge(self.vertices[4], self.vertices[5], 0.1),
                      Edge(self.vertices[4], self.vertices[6], 0.4),
                      Edge(self.vertices[0], self.vertices[7], 0.1),
                      Edge(self.vertices[7], self.vertices[8], 0.5),
                      Edge(self.vertices[7], self.vertices[9], 0.3)]
        self.graph = Graph(self.vertices, self.edges)
