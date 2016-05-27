from HW4.TransmissionNetwork.Graph import Graph
from HW4.TransmissionNetwork.Vertex import Vertex


class CompleteInferring:
    def __init__(self, graph: Graph, root: Vertex, number_of_variables: int, data):
        self.graph = graph
        self.data = data
        self.root = root
        self.number_of_variables = number_of_variables
        self.sufficient_statistics = {}
        self.model_parameters = {edge: 0 for edge in self.graph.edges}

    def generate_sufficient_statistics(self):
        for data_instance in self.data:
            self.add_data_instance(data_instance)

    def add_data_instance(self, data_instance):
        pass

    def a(self):
        for vertex in self.graph.vertices:
            parents = self.graph.get



