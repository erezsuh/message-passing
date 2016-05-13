from TransmissionNetwork.Graph import Graph
from Tests.GraphGenerator import TransmissionNetwork
from Algorithm.MessagePassing import MessagePassingAlgorithm


def main():
    i = 1
    for g in [TransmissionNetwork(0, 1, 1, 0, 0, 1),
              TransmissionNetwork(0, 0, 1, 0, 0, 1),
              TransmissionNetwork(1, 1, 1, 1, 1, 1)]:
        print("Executing algorithm on graph %d" % i)
        i += 1
        for root_index in [0, 1, 5]:
            print("Starting from root %s" % g.graph.vertices[root_index])
            algorithm = MessagePassingAlgorithm(g.graph, g.vertices[root_index])
            algorithm.compute_marginals()
            print("Result:")
            algorithm.print_result()
            print("---------------------------------------")
        print("---------------------------------------")
        print("---------------------------------------")


main()
