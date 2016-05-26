from sys import argv
from HW4.Parser.FileParser import FileParser
if len(argv) != 3:
    raise Exception("Invalid args")
option = argv[1]
parser = FileParser(argv[2])
parser.parse()
print("Hello")





