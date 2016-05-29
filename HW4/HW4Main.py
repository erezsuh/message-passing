from sys import argv
from HW4.Parser.FileParser import FileParser
from HW4.Tests.GraphGenerator import TransmissionNetwork
from HW4.CompleteInferring.CompleteInferringAlgorithm import CompleteInferringAlgorithm

if len(argv) != 3:
    raise Exception("Invalid args")
option = argv[1]
parser = FileParser(argv[2])
parser.parse()

graph = TransmissionNetwork().graph
algorithm = CompleteInferringAlgorithm(graph, graph.vertices[0], parser.data)
algorithm.generate_sufficient_statistics()
algorithm.normalize_sufficient_statistics()




print("bla")
