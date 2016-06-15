from os.path import isfile


class FileParser:
    def __init__(self, file_path):
        self.file_path = file_path
        if not isfile(self.file_path):
            raise Exception("File not existing")
        self.raw_data = None
        self.data = []
        self.variables = []

    def parse(self):
        with open(self.file_path, 'r') as f:
            self.raw_data = f.read()
        lines = [line for line in self.raw_data.split('\n') if line]
        self.variables.extend([x for x in lines[0].split('\t') if x])
        for line in lines[1:]:
            self.data.append([x for x in line.split('\t') if x])
