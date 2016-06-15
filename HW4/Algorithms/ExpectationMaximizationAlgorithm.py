from HW4.TransmissionNetwork.Graph import Graph
from HW4.TransmissionNetwork.Vertex import Vertex
from HW4.GraphTraversal.GraphTraversal import GraphTraversal
from HW4.Algorithms.CompleteInferringAlgorithm import CompleteInferringAlgorithm

from HW3.Algorithm.MessagePassingAlgorithm import MessagePassingAlgorithm

from decimal import *


class ExpectationMaximizationAlgorithm:
    def __init__(self, graph: Graph, root: Vertex, data, observed_variables):
        self.graph = graph
        self.data = data
        self.root = root
        self.n = {edge: [0, 0] for edge in self.graph.edges}
        self.graphTraversal = GraphTraversal(graph, root)
        self.graphTraversal.traverse(None)
        self.observed_variables = observed_variables
        self.hidden_variables = [vertex.name for
                                 vertex in self.graph.vertices if vertex.name not in self.observed_variables]
        self.x1 = self.graph.get_vertex_by_id(0)
        self.x2 = self.graph.get_vertex_by_id(1)
        self.x3 = self.graph.get_vertex_by_id(2)
        self.x4 = self.graph.get_vertex_by_id(3)
        self.x5 = self.graph.get_vertex_by_id(4)
        self.x6 = self.graph.get_vertex_by_id(5)
        self.x7 = self.graph.get_vertex_by_id(6)
        self.x8 = self.graph.get_vertex_by_id(7)
        self.x9 = self.graph.get_vertex_by_id(8)
        self.x10 = self.graph.get_vertex_by_id(9)

    def start(self, initial_parameters):
        current_parameters = initial_parameters
        previous_data_instance_log_likelihood = 0
        while True:
            s = ""
            self.update_graph_parameters(current_parameters)
            expected_sufficient_statistics = []
            for data_instance in self.data:
                self.update_graph_observed_variables(data_instance)
                mp_algorithm = MessagePassingAlgorithm(self.graph, self.graph.vertices[0], [0.5, 0.5])
                mp_algorithm.compute_marginals()

                expected_sufficient_statistic = {vertex: [[0, 0], [0, 0]] for vertex in self.graph.vertices}
                for vertex in self.graph.vertices:
                    if vertex is self.root:
                        continue
                    parent = self.graphTraversal.parents[vertex]
                    edge = self.graph.get_edge(parent, vertex)
                    for k in [0, 1]:
                        for l in [0, 1]:
                            if k == l:
                                p = 1 - edge.flip_probability
                            else:
                                p = edge.flip_probability
                            expected_sufficient_statistic[vertex][k][l] = (mp_algorithm.marginals[parent][l] * p * mp_algorithm.phi[vertex][k]) \
                                      / (mp_algorithm.collect_messages[edge][l] * mp_algorithm.get_likelihood())
                    expected_sufficient_statistics.append(expected_sufficient_statistic)
            sum_statistics = {vertex: [[0, 0], [0, 0]] for vertex in self.graph.vertices}
            for expected_sufficient_statistic in expected_sufficient_statistics:
                for vertex in expected_sufficient_statistic:
                    for k in [0, 1]:
                        for l in [0, 1]:
                            sum_statistics[vertex][k][l] += expected_sufficient_statistic[vertex][k][l]
            current_parameters = []
            for edge in self.get_ordered_edges():
                if edge.source is self.root:
                    vertex = edge.destination
                elif self.graphTraversal.parents[edge.source] is edge.destination:
                    vertex = edge.source
                else:
                    vertex = edge.destination
                row_sum = sum(sum_statistics[vertex][0]) + sum(sum_statistics[vertex][1])
                current_parameters.append((sum_statistics[vertex][0][1] + sum_statistics[vertex][1][0]) / row_sum)

            s += '\t'.join([str(param) for param in current_parameters])
            # s += '\t\t%s' % current_data_instance_log_likelihood
            # s += '\t%s' % float(likelihood.ln())
            print(s)
            # if abs(current_data_instance_log_likelihood - previous_data_instance_log_likelihood) < 0.001:
            #     break
            # previous_data_instance_log_likelihood = current_data_instance_log_likelihood


    def update_graph_observed_variables(self, data):
        for index, observed_variable in enumerate(self.observed_variables):
            vertex = self.graph.get_vertex_by_name(observed_variable)
            vertex.observed_value = int(data[index])

    def update_graph_parameters(self, parameters):
        for i, edge in enumerate(self.get_ordered_edges()):
            edge.flip_probability = parameters[i]

    def get_ordered_edges(self):
        return [self.graph.get_edge(self.x1, self.x2),
                self.graph.get_edge(self.x2, self.x3),
                self.graph.get_edge(self.x2, self.x4),
                self.graph.get_edge(self.x1, self.x5),
                self.graph.get_edge(self.x5, self.x6),
                self.graph.get_edge(self.x5, self.x7),
                self.graph.get_edge(self.x1, self.x8),
                self.graph.get_edge(self.x8, self.x9),
                self.graph.get_edge(self.x8, self.x10)]

    def calculate_log_likelihood(self):
        likelihood = Decimal(1)
        for data_instance in self.data:
            likelihood *= Decimal(self.calculate_data_instance_likelihood(data_instance))
            # print(likelihood)
            # print(likelihood.ln())
        return float(likelihood.ln())

    def calculate_data_instance_likelihood(self, data_instance):
        data_instance_likelihood = 0.5
        for vertex in self.graph.vertices:
            if vertex is self.root:
                continue
            parent = self.graphTraversal.parents[vertex]
            edge = self.graph.get_edge(parent, vertex)
            if self.get_data_for_vertex(data_instance, vertex) == self.get_data_for_vertex(data_instance, parent):
                data_instance_likelihood *= 1 - edge.flip_probability
            else:
                data_instance_likelihood *= edge.flip_probability
        return data_instance_likelihood