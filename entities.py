class Graph:
    vertices = []
    edges = []
    substrings = []

    def __init__(self):
        self.vertices = []
        self.edges = []
        self.substrings = []

    def add_vertex(self, vertex):
        self.vertices.append(vertex)

    def add_edge(self, edge):
        self.edges.append(edge)

    def get_edges_vertex(self, vertex):
        edges = [edge for edge in self.edges if edge.origin == vertex]
        return edges


class Vertex:
    next = []

    def __init__(self, name):
        self.name = name
        self.next = []
        self.inDegree = 0
        self.outDegree = 0
        self.incidentEdges = {}

    def get_unvisited_edges(self):
        edges = [edge for edge, isVisited in self.incidentEdges.items() if isVisited == 0]
        return edges


class Edge:
    def __init__(self, substring, vo, vd):
        self.name = substring
        self.origin = vo
        self.end = vd
