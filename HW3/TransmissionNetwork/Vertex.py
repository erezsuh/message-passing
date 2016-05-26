
class Vertex:
    def __init__(self, name: str, observed_value: int=None):
        self.name = name
        self.observed_value = observed_value

    def __eq__(self, other):
        return self.name == other

    def __str__(self):
        return self.name

    def __hash__(self):
        return self.name.__hash__()


