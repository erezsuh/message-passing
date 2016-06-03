from enum import Enum

from HW3.TransmissionNetwork.Graph import Graph
from HW3.TransmissionNetwork.Vertex import Vertex
from HW3.TransmissionNetwork.Edge import Edge
from HW3.Utils import VectorUtils, MaxUtils


class MostProbableAssignmentAlgorithm:
    def __init__(self, graph: Graph, root: Vertex, root_probability):
        self.graph = graph
        self.root = root
        self.root_probability = root_probability
        self.took_care_of_root_probability = False
        self.phi = {vertex: self.compute_phi(vertex) for vertex in self.graph.vertices}
        self.phi_matrix = {edge: self.compute_phi_matrix(edge) for edge in self.graph.edges}
        self.collect_messages = {edge: [0, 0] for edge in self.graph.edges}
        self.vertex_status = {vertex: VertexStatus.new for vertex in self.graph.vertices}
        self.argmax = {edge: [0, 0] for edge in self.graph.edges}
        self.most_probable_assignment = {vertex: [0, 0] for vertex in self.graph.vertices}

    @staticmethod
    def compute_phi(vertex: Vertex):
        return [1, 1] if vertex.observed_value is None else ([1, 0] if vertex.observed_value is 0 else [0, 1])

    def compute_most_probable_assignment(self):
        self.collect(self.root)
        self.vertex_status = {vertex: VertexStatus.new for vertex in self.graph.vertices}
        self.distribute(self.root)

    def collect(self, vertex: Vertex) -> float:
        self.vertex_status[vertex] = VertexStatus.in_progress
        if not self.is_vertex_leaf(vertex):
            for child_vertex in self.get_vertex_children(vertex):
                child_edge = self.graph.get_edge(child_vertex, vertex)
                self.argmax[child_edge], self.collect_messages[child_edge] = self.collect(child_vertex)
                self.phi[vertex] = VectorUtils.multiply_vectors(self.phi[vertex],
                                                                self.collect_messages[child_edge])
        self.vertex_status[vertex] = VertexStatus.finished
        if vertex is self.root:
            return
        else:
            return self.generate_collect_message_and_argmax(vertex)

    def generate_collect_message_and_argmax(self, vertex: Vertex):
        parent_vertex = self.get_vertex_parent(vertex)
        parent_edge = self.graph.get_edge(vertex, parent_vertex)
        collect_message = [0, 0]
        argmax = [0, 0]
        for i in [0, 1]:
            argmax[i], collect_message[i] = MaxUtils.argmax(VectorUtils.multiply_vectors(
                self.phi_matrix[parent_edge][i], self.phi[vertex]))
        return argmax, collect_message

    def distribute(self, vertex: Vertex):
        self.vertex_status[vertex] = VertexStatus.in_progress
        if vertex is self.root:
            self.most_probable_assignment[vertex] = list(MaxUtils.argmax(self.phi[vertex]))
        else:
            vertex_parent = self.get_vertex_parent(vertex)
            edge_parent = self.graph.get_edge(vertex, vertex_parent)
            most_probable_parent_value = self.most_probable_assignment[vertex_parent][0]
            self.most_probable_assignment[vertex] = [self.argmax[edge_parent][most_probable_parent_value],
                                                     self.collect_messages[edge_parent][most_probable_parent_value]]
        if not self.is_vertex_leaf(vertex):
            for child_vertex in self.get_vertex_children(vertex):
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

    def is_vertex_leaf(self, vertex: Vertex):
        return self.graph.is_leaf(vertex) and len(self.get_vertex_children(vertex)) is 0

    @staticmethod
    def generate_transmission_distribution_matrix(edge: Edge):
        return [[1 - edge.flip_probability, edge.flip_probability],
                [edge.flip_probability, 1 - edge.flip_probability]]

    def compute_phi_matrix(self, edge):
        if (edge.source is self.root or edge.destination is self.root) and not self.took_care_of_root_probability:
            self.took_care_of_root_probability = True

            return [[(1 - edge.flip_probability) * self.root_probability[0],
                     edge.flip_probability * self.root_probability[1]],
                    [edge.flip_probability * self.root_probability[0],
                     (1 - edge.flip_probability) * self.root_probability[1]]]
        else:
            return self.generate_transmission_distribution_matrix(edge)

    def print_result(self):
        for vertex in self.graph.vertices:
            if vertex.observed_value is None:
                print("Max(P({0})) = {1}. P({0}={1}) = {2}".format(vertex, self.most_probable_assignment[vertex][0],
                                                                   self.most_probable_assignment[vertex][1]))
        print("P(X) = %s" % self.most_probable_assignment[Vertex("X1")][1])

class VertexStatus(Enum):
    new = 1
    in_progress = 2
    finished = 3
