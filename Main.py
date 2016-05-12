from TransmissionNetwork.Graph import Graph
from Tests.GraphGenerator import TransmissionNetwork
from Algorithm.MessagePassing import MessagePassingAlgorithm


def main():
    for g in [TransmissionNetwork(0, 1, 1, 0, 0, 1),
              TransmissionNetwork(0, 0, 1, 0, 0, 1),
              TransmissionNetwork(1, 1, 1, 1, 1, 1)]:
        print("Executing algorithm on %s" % g.graph)
        for root_index in [0, 1, 5]:
            print("Starting from root %s" % g.graph.vertices[root_index])
            algorithm = MessagePassingAlgorithm(g.graph, g.vertices[root_index])
            algorithm.compute_marginals()
            print("Result:")
            algorithm.print_marginals()
            print("---------------------------------------")


main()
