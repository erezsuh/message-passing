from HW4.TransmissionNetwork.Graph import Graph
from HW4.TransmissionNetwork.Vertex import Vertex
from HW4.GraphTraversal.GraphTraversal import GraphTraversal
from HW4.Algorithms.CompleteInferringAlgorithm import CompleteInferringAlgorithm

from HW3.Algorithm.MostProbableAssignmentAlgorithm import MostProbableAssignmentAlgorithm
from HW3.Algorithm.MessagePassingAlgorithm import MessagePassingAlgorithm

from decimal import *
from copy import deepcopy

class ExpectationMaximizationAlgorithm:
    def __init__(self, graph: Graph, root: Vertex, data, observed_variables):
        self.graph = graph
        self.data = data
        self.root = root
        self.model_parameters = {edge: 0 for edge in self.graph.edges}
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
            complete_data = []
            s = ""
            self.update_graph_parameters(current_parameters)
            for data_instance in self.data:
                self.reset_hidden_variables()
                self.update_graph_observed_variables(data_instance)
                mp_algorithm = MostProbableAssignmentAlgorithm(self.graph, self.graph.vertices[0], [0.5, 0.5])
                mp_algorithm.compute_most_probable_assignment()
                self.update_graph_hidden_variables(mp_algorithm.most_probable_assignment)
                complete_data.append([vertex.observed_value for vertex in self.graph.vertices])

            ci_algorithm = CompleteInferringAlgorithm(self.graph, self.root, complete_data)
            ci_algorithm.generate_sufficient_statistics()
            current_data_instance_log_likelihood = ci_algorithm.calculate_log_likelihood()
            s += '\t'.join([str(edge.flip_probability) for edge in self.get_ordered_edges()])
            s += '\t\t%s' % current_data_instance_log_likelihood
            s += '\t%s' % self.calculate_log_likelihood()
            print(s)
            if abs(current_data_instance_log_likelihood - previous_data_instance_log_likelihood) < 0.001:
                break
            previous_data_instance_log_likelihood = current_data_instance_log_likelihood
            ci_algorithm.update_graph_flip_probabilities()
            current_parameters = []
            for edge in self.get_ordered_edges():
                current_parameters.append(edge.flip_probability)

    def update_graph_observed_variables(self, data):
        for index, observed_variable in enumerate(self.observed_variables):
            vertex = self.graph.get_vertex_by_name(observed_variable)
            vertex.observed_value = int(data[index])

    def update_graph_hidden_variables(self, most_probable_assignment):
        for hidden_variable in self.hidden_variables:
            vertex = self.graph.get_vertex_by_name(hidden_variable)
            vertex.observed_value = int(most_probable_assignment[vertex][0])

    def reset_hidden_variables(self):
        for hidden_variable in self.hidden_variables:
            vertex = self.graph.get_vertex_by_name(hidden_variable)
            vertex.observed_value = None

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
        getcontext().prec = 1000
        likelihood = Decimal(1)
        for data_instance in self.data:
            likelihood *= Decimal(self.calculate_data_instance_likelihood(data_instance))
            # print(likelihood)
            # print(likelihood.ln())
        return float(likelihood.ln())

    def calculate_data_instance_likelihood(self, data_instance):
        graph_copy = deepcopy(self.graph)
        for vertex in graph_copy.vertices:
            if vertex.name in self.observed_variables:
                vertex.observed_value = self.get_data_for_vertex(data_instance, vertex)
            else:
                vertex.observed_value = None
        mp_algorithm = MessagePassingAlgorithm(graph_copy, self.root, [0.5, 0.5])
        mp_algorithm.compute_marginals()
        return sum(mp_algorithm.marginals[mp_algorithm.root])



    def get_data_for_vertex(self, data_instance, vertex: Vertex):
        for i, observed_variable in enumerate(self.observed_variables):
            if observed_variable == vertex.name:
                return int(data_instance[i])
        raise Exception("not found")
