from src.graph import Graph


class Dijkstra():
    def __init__(self, graph: Graph):
        self.path = list()
        self.graph = graph
