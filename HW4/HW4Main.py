from sys import argv
from HW4.Parser.FileParser import FileParser
from HW4.Tests.GraphGenerator import TransmissionNetwork
from HW4.Algorithms.CompleteInferringAlgorithm import CompleteInferringAlgorithm
from HW4.Algorithms.MaximumProbabilityInferenceAlgorithm import MaximumProbabilityInferenceAlgorithm

if len(argv) != 3:
    raise Exception("Invalid args")
option = argv[1]
parser = FileParser(argv[2])
parser.parse()
graph = TransmissionNetwork().graph
if option is 'C':
    algorithm = CompleteInferringAlgorithm(graph, graph.vertices[0], parser.data)
    algorithm.generate_sufficient_statistics()
    algorithm.normalize_sufficient_statistics()
elif option is 'M':
    initial_parameters = [0.5] * len(graph.vertices)
    algorithm = MaximumProbabilityInferenceAlgorithm(graph, graph.vertices[0],
                                                     parser.data, parser.variables)
    algorithm.start(initial_parameters)


    print("bla")
