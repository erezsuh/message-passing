from HW4.TransmissionNetwork.Graph import Graph
from HW4.TransmissionNetwork.Vertex import Vertex
from enum import Enum


class VertexStatus(Enum):
    new = 1
    in_progress = 2
    finished = 3


class GraphTraversal:
    def __init__(self, graph: Graph, root: Vertex):
        self.graph = graph
        self.root = root
        self.parents = {vertex: None for vertex in self.graph.vertices}
        self.vertex_status = {vertex: VertexStatus.new for vertex in self.graph.vertices}

    def traverse(self, vertex):
        if vertex is None:
            vertex = self.root
        self.vertex_status[vertex] = VertexStatus.in_progress
        if vertex is self.root:
            for child in self.graph.get_neighbour_vertices(vertex):
                self.traverse(child)
        else:
            if self.graph.is_leaf(vertex):
                self.parents[vertex] = self.graph.get_neighbour_vertices(vertex)[0]
                self.vertex_status[vertex] = VertexStatus.finished
                return
            else:
                self.parents[vertex] = [v for v in self.graph.get_neighbour_vertices(vertex) if
                                        self.vertex_status[v] is VertexStatus.in_progress][0]
                for child in [v for v in self.graph.get_neighbour_vertices(vertex) if
                              self.vertex_status[v] is VertexStatus.new]:
                    self.traverse(child)
        self.vertex_status[vertex] = VertexStatus.finished
