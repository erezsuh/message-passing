
class Vertex:
    def __init__(self, name: str):
        self.name = name

    def __eq__(self, other):
        return self.name == other

    def __str__(self):
        return self.name

    def __hash__(self):
        return self.name.__hash__()


