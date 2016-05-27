from HW4.TransmissionNetwork.Vertex import Vertex
from HW4.TransmissionNetwork.Edge import Edge
from HW4.TransmissionNetwork.Graph import Graph


class TransmissionNetwork:
    def __init__(self):
        self.vertices = [Vertex("X1"), Vertex("X2"), Vertex("X3"), Vertex("X4"), Vertex("X5"),
                         Vertex("X6"), Vertex("X7"), Vertex("X8"), Vertex("X9"), Vertex("X10")]
        self.edges = [Edge(self.vertices[0], self.vertices[1]),
                      Edge(self.vertices[1], self.vertices[2]),
                      Edge(self.vertices[1], self.vertices[3]),
                      Edge(self.vertices[0], self.vertices[4]),
                      Edge(self.vertices[4], self.vertices[5]),
                      Edge(self.vertices[4], self.vertices[6]),
                      Edge(self.vertices[0], self.vertices[7]),
                      Edge(self.vertices[7], self.vertices[8]),
                      Edge(self.vertices[7], self.vertices[9])]
        self.graph = Graph(self.vertices, self.edges)
