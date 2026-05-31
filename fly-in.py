from src.graph import Graph
from src.parsing import Parsing
from src.pathfinding import Dijkstra


def main():
    graph = Graph()
    parsing = Parsing(graph)
    parsing.parse('config.txt')
    Dijkstra(graph)


if __name__ == "__main__":
    main()
