from HW4.TransmissionNetwork.Graph import Graph
from HW4.TransmissionNetwork.Vertex import Vertex
from HW4.GraphTraversal.GraphTraversal import GraphTraversal

class CompleteInferringAlgorithm:
    def __init__(self, graph: Graph, root: Vertex, data):
        self.graph = graph
        self.data = data
        self.root = root
        self.sufficient_statistics = {edge: [0, 0] for edge in self.graph.edges}
        self.mle = {edge: [0, 0] for edge in self.graph.edges}
        self.graphTraversal = GraphTraversal(graph, root)
        self.graphTraversal.traverse(None)

    def generate_sufficient_statistics(self):
        for data_instance in self.data:
            self.add_data_instance(data_instance)

    def add_data_instance(self, data_instance):
        for vertex in self.graph.vertices:
            if vertex is self.root:
                continue
            parent = self.graphTraversal.parents[vertex]
            edge = self.graph.get_edge(parent, vertex)
            if self.get_data_for_vertex(data_instance, vertex) == self.get_data_for_vertex(data_instance, parent):
                self.sufficient_statistics[edge][0] += 1
            else:
                self.sufficient_statistics[edge][1] += 1

    @staticmethod
    def get_data_for_vertex(data_instance, vertex: Vertex):
        return data_instance[vertex.id]

    def normalize_sufficient_statistics(self):
        for edge in self.sufficient_statistics:
            statistic = self.sufficient_statistics[edge]
            for i in [0, 1]:
                self.mle[edge][i] = float(statistic[i]) / sum(statistic)





