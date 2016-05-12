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

    def distribute(self, vertex: Vertex):
        self.vertex_status[vertex] = VertexStatus.in_progress
        if vertex is self.root:
            self.marginals[vertex] = self.phi[vertex]
        else:
            vertex_parent = self.get_vertex_parent(vertex)
            edge_parent = self.graph.get_edge(vertex, vertex_parent)
            self.marginals[vertex] = VectorUtils.multiply_vectors(self.phi[vertex],
                                                                  self.collect_messages[edge_parent])
        if not self.graph.is_leaf(vertex):
            for child_vertex in self.get_vertex_children(vertex):
                child_edge = self.graph.get_edge(child_vertex, vertex)
                self.calculate_distribute_message(vertex, child_edge)
                self.distribute(child_vertex)
        self.vertex_status[vertex] = VertexStatus.finished

    def get_vertex_children(self, vertex: Vertex):
        return [neighbour_vertex for neighbour_vertex in self.graph.get_neighbour_vertices(vertex)
                if not self.vertex_status[neighbour_vertex] is VertexStatus.in_progress]

    def get_vertex_parent(self, vertex: Vertex) -> Vertex:
        neighbours = self.graph.get_neighbour_vertices(vertex)
        for neighbour in neighbours:
            if self.vertex_status[neighbour] is VertexStatus.in_progress:
                return neighbour

    def calculate_distribute_message(self, vertex: Vertex, edge: Edge):
        distribution_matrix = self.generate_transmission_distribution_matrix(edge)
        for i in [0, 1]:
            self.distribute_messages[edge][i] = (distribution_matrix[0][i] * self.marginals[vertex][i]) / \
                                                  self.collect_messages[edge][i]

    @staticmethod
    def generate_transmission_distribution_matrix(edge: Edge):
        return [[1 - edge.flip_probability, edge.flip_probability],
                [edge.flip_probability, 1 - edge.flip_probability]]

    def print_marginals(self):
        for vertex in self.graph.vertices:
            print("vertex: %s has marginal %s" %(vertex, self.marginals[vertex]))


class VertexStatus(Enum):
    new = 1
    in_progress = 2
    finished = 3
