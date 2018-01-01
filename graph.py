class Graph:

    def __init__(self):
        self.edges = []

    def add_edge(self, v1, v2, weight):
        self.edges.append((v1, v2, weight))
        self.edges.append((v2, v1, weight))

    def remove_edge(self, v1, v2):
        to_delete = []
        for edge in self.edges:
            if (edge[0], edge[1]) == (v1, v2) or (edge[0], edge[1]) == (v2, v1):
                to_delete.append(edge)

        for edge in to_delete:
            self.edges.remove(edge)

    def remove_vertex(self, v):
        to_delete = []
        for edge in self.edges:
            if edge[0] == v or edge[1] == v:
                to_delete.append(edge)

        for edge in to_delete:
            self.edges.remove(edge)

