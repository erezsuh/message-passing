from TransmissionNetwork.Graph import Graph
from Tests.GraphGenerator import TransmissionNetwork
from Algorithm.MessagePassingAlgorithm import MessagePassingAlgorithm
from Algorithm.MostProbableAssignmentAlgorithm import MostProbableAssignmentAlgorithm

def main():
    i = 1
    for g in [TransmissionNetwork(0, 1, 1, 0, 0, 1),
              TransmissionNetwork(0, 0, 1, 0, 0, 1),
              TransmissionNetwork(1, 1, 1, 1, 1, 1)]:
        print("Executing algorithm on graph %d" % i)
        i += 1
        for root_index in [0, 1, 5]:
            print("Starting from root %s" % g.graph.vertices[root_index])
            marginal_algorithm = MessagePassingAlgorithm(g.graph, g.vertices[root_index], [0.5, 0.5])
            marginal_algorithm.compute_marginals()
            print("Results for marginals:")
            marginal_algorithm.print_result()
            print("End of marginals")
            print()
            print()
            print()
            most_probable_algorithm = MostProbableAssignmentAlgorithm(g.graph, g.vertices[0], [0.5, 0.5])
            most_probable_algorithm.compute_most_probable_assignment()
            print("Results for most probable assignment:")
            most_probable_algorithm.print_result()
            print("End of most probable assignment")
            print("---------------------------------------")
            print()
            print()
            print()
            print()
            print()
        print("---------------------------------------")
    return


main()
