from HW4.TransmissionNetwork import Vertex


class Edge:
    def __init__(self, source: Vertex, destination: Vertex):
        self.source = source
        self.destination = destination
        self.flip_probability = None

    def contains(self, vertex: Vertex):
        return self.source == vertex or self.destination == vertex

    def __str__(self):
        return "(%s <--> %s)" % (self.source, self.destination)
