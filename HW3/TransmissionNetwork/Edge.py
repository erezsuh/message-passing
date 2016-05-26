from HW3.TransmissionNetwork import Vertex


class Edge:
    def __init__(self, source: Vertex, destination: Vertex, flip_probability: float):
        self.source = source
        self.destination = destination
        self.flip_probability = flip_probability

    def contains(self, vertex: Vertex):
        return self.source == vertex or self.destination == vertex

    def __str__(self):
        return "(%s <--> %s)" % (self.source, self.destination)
