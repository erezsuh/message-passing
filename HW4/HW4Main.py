from sys import argv
from HW4.Parser.FileParser import FileParser
from HW4.Tests.GraphGenerator import TransmissionNetwork
from HW4.GraphTraversal.GraphTraversal import GraphTraversal

if len(argv) != 3:
    raise Exception("Invalid args")
option = argv[1]
parser = FileParser(argv[2])
parser.parse()

graph = TransmissionNetwork().graph
traversal = GraphTraversal(graph, graph.vertices[0])
traversal.traverse(None)
print("bla")



