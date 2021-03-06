from HW4.TransmissionNetwork import Edge
from HW4.TransmissionNetwork import Vertex


class Graph:
    def __init__(self, vertices, edges) -> None:
        self.vertices = vertices
        self.edges = edges

    def is_leaf(self, vertex: Vertex) -> bool:
        return len(self.get_neighbour_edges(vertex)) == 1

    def get_neighbour_vertices(self, vertex: Vertex):
        neighbour_edges = self.get_neighbour_edges(vertex)
        vertices = set()
        for e in neighbour_edges:
            vertices.add(e.source)
            vertices.add(e.destination)
        vertices.remove(vertex)
        return list(vertices)

    def get_neighbour_edges(self, vertex: Vertex):
        return [e for e in self.edges if e.contains(vertex)]

    def get_edge(self, v1: Vertex, v2: Vertex) -> Edge:
        for e in self.edges:
            if e.contains(v1) and e.contains(v2):
                return e

    def get_vertex_by_id(self, id: int):
        for vertex in self.vertices:
            if vertex.id is id:
                return vertex

    def get_vertex_by_name(self, name: str):
        for vertex in self.vertices:
            if vertex.name == name:
                return vertex
