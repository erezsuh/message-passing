from TransmissionNetwork.Graph import Graph
from TransmissionNetwork.Vertex import Vertex
from TransmissionNetwork.Edge import Edge
from Utils import VectorUtils
from enum import Enum
class MessagePassingAlgorithm:
    def __init__(self, graph: Graph, root: Vertex):
        self.graph = graph
        self.root = root
        self.phi = {vertex: [1, 1] for vertex in self.graph.vertices}
        self.messages = {edge: [0, 0] for edge in self.graph.edges}
        self.vertex_status = {vertex: VertexStatus.new for vertex in self.graph.vertices}

    def computeMarginals(self):
        collect_result = self.collect(self.root)
        print(collect_result)
        #distribute(root, None)

    def collect(self, vertex: Vertex) -> float:
        self.vertex_status[vertex] = VertexStatus.in_progress
        if not self.graph.is_leaf(vertex):
            for neighbour_vertex in self.graph.get_neighbour_vertices(vertex):
                if self.vertex_status[neighbour_vertex] is VertexStatus.in_progress:
                    # parent
                    continue
                neighbour_edge = self.graph.get_edge(neighbour_vertex, vertex)
                self.messages[neighbour_edge] = self.collect(neighbour_vertex)
                self.phi[vertex] = VectorUtils.multiply_vectors(self.phi[vertex],
                                                                self.messages[neighbour_edge])
        self.vertex_status[vertex] = VertexStatus.finished
        if vertex is self.root:
            return self.phi[vertex]
        else:
            return self.generate_message(vertex)

    def get_vertex_parent(self, vertex: Vertex) -> Vertex:
        neighbours = self.graph.get_neighbour_vertices(vertex)
        for neighbour in neighbours:
            if self.vertex_status[neighbour] is VertexStatus.in_progress:
                return neighbour

    def generate_message(self, vertex: Vertex):
        parent_vertex = self.get_vertex_parent(vertex)
        parent_edge = self.graph.get_edge(vertex, parent_vertex)
        if vertex.observed_value is not None:
            return self.generate_transmission_distribution(parent_edge, vertex.observed_value)
        else:
            return VectorUtils.addition_vectors(
                VectorUtils.multiply_vectors(self.generate_transmission_distribution(parent_edge, 0),
                                             self.phi[vertex]),
                VectorUtils.multiply_vectors(self.generate_transmission_distribution(parent_edge, 1),
                                             self.phi[vertex]))

    @staticmethod
    def generate_transmission_distribution(edge: Edge, child_value: int):
        if child_value == 0:
            return [1 - edge.flip_probability, edge.flip_probability]
        else:
            return [edge.flip_probability, 1 - edge.flip_probability]

class VertexStatus(Enum):
    new = 1
    in_progress = 2
    finished = 3
