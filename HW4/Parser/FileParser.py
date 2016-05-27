from os.path import join, isfile


class FileParser:
    def __init__(self, file_name):
        self.base_dir = 'e:\Projects\IDC\ProbabilisticModels\HW4\ex4-data'
        self.file_name = file_name
        self.file_path = join(self.base_dir, file_name)
        if not isfile(self.file_path):
            raise Exception("File not existing")
        self.raw_data = None
        self.data = []
        self.number_of_variables = 0

    def parse(self):
        with open(self.file_path, 'r') as f:
            self.raw_data = f.read()
        lines = [line for line in self.raw_data.split('\n') if line]
        self.number_of_variables = len(lines[0])
        for line in lines[1:]:
            self.data.append([x for x in line.split('\t') if x])
