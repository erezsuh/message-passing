from TransmissionNetwork.Graph import Graph
from TransmissionNetwork.Vertex import Vertex
from TransmissionNetwork.Edge import Edge
from Utils import VectorUtils
from enum import Enum
from pickle import dump


class MessagePassingAlgorithm:
    def __init__(self, graph: Graph, root: Vertex):
        self.graph = graph
        self.root = root
        self.phi = {vertex: [1, 1] for vertex in self.graph.vertices}
        self.collect_messages = {edge: [0, 0] for edge in self.graph.edges}
        self.distribute_messages = {edge: [0, 0] for edge in self.graph.edges}
        self.vertex_status = {vertex: VertexStatus.new for vertex in self.graph.vertices}
        self.marginals = {vertex: [1, 1] for vertex in self.graph.vertices}

    def compute_marginals(self):
        self.collect(self.root)
        self.vertex_status = {vertex: VertexStatus.new for vertex in self.graph.vertices}
        self.distribute(self.root)

    def collect(self, vertex: Vertex) -> float:
        self.vertex_status[vertex] = VertexStatus.in_progress
        if self.graph.is_leaf(vertex):
            self.phi[vertex] = [1, 0] if vertex.observed_value is 0 else [0, 1]
        else:
            for child_vertex in self.get_vertex_children(vertex):
                child_edge = self.graph.get_edge(child_vertex, vertex)
                self.collect_messages[child_edge] = self.collect(child_vertex)
                self.phi[vertex] = VectorUtils.multiply_vectors(self.phi[vertex],
                                                                self.collect_messages[child_edge])
        self.vertex_status[vertex] = VertexStatus.finished
        if vertex is self.root:
            return self.phi[vertex]
        else:
            return self.generate_collect_message(vertex)

    def generate_collect_message(self, vertex: Vertex):
        parent_vertex = self.get_vertex_parent(vertex)
        parent_edge = self.graph.get_edge(vertex, parent_vertex)
        return VectorUtils.multiply_matrix_and_vector(self.generate_transmission_distribution_matrix(parent_edge),
                                             self.phi[vertex])
        # if vertex.observed_value is not None:
        #     return self.generate_transmission_distribution(parent_edge, vertex.observed_value)
        # else:
        #     return VectorUtils.addition_vectors(self.generate_collect_multiplication_vector(vertex, parent_edge, 0),
        #                                         self.generate_collect_multiplication_vector(vertex, parent_edge, 1))

    def distribute(self, vertex: Vertex):
        if vertex is self.root:
            self.marginals[vertex] = self.phi[vertex]
        else:
            self.marginals[vertex] = VectorUtils.multiply_vectors(self.phi[vertex],
                                                                  self.collect_messages[vertex])
        if not self.graph.is_leaf(vertex):
            for child_vertex in self.get_vertex_children(vertex):
                child_edge = self.graph.get_edge(child_vertex, vertex)
                self.distribute_messages[child_edge] = VectorUtils.addition_vectors(
                    self.generate_distribute_message(vertex, child_edge, 0),
                    self.generate_distribute_message(vertex, child_edge, 1))

    def get_vertex_children(self, vertex: Vertex):
        return [neighbour_vertex for neighbour_vertex in self.graph.get_neighbour_vertices(vertex)
                if not self.vertex_status[neighbour_vertex] is VertexStatus.in_progress]

    def get_vertex_parent(self, vertex: Vertex) -> Vertex:
        neighbours = self.graph.get_neighbour_vertices(vertex)
        for neighbour in neighbours:
            if self.vertex_status[neighbour] is VertexStatus.in_progress:
                return neighbour

    def generate_collect_multiplication_vector(self, vertex: Vertex, edge: Edge, child_value: int):
        return VectorUtils.multiply_vectors(self.generate_transmission_distribution(edge, child_value),
                                            [self.phi[vertex][child_value], self.phi[vertex][child_value]])

    def generate_distribute_message(self, vertex: Vertex, child_edge: Edge, child_value):
        multiplication_vector = VectorUtils.multiply_vectors(
            self.generate_transmission_distribution(child_edge, child_value), self.phi[vertex])
        return VectorUtils.devide_vectors(multiplication_vector, self.collect_messages[child_edge])

    @staticmethod
    def generate_transmission_distribution(edge: Edge, child_value: int):
        if child_value == 0:
            return [1 - edge.flip_probability, edge.flip_probability]
        else:
            return [edge.flip_probability, 1 - edge.flip_probability]

    @staticmethod
    def generate_transmission_distribution_matrix(edge: Edge):
        return [[1 - edge.flip_probability, edge.flip_probability],
                [edge.flip_probability, 1 - edge.flip_probability]]


class VertexStatus(Enum):
    new = 1
    in_progress = 2
    finished = 3
