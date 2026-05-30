from src.graph import Graph
from src.parsing import Parsing
from src.pathfinding import Dijkstra


def main():
    graph = Graph()
    parsing = Parsing(graph)
    parsing.parse('config.txt')
    dijkstra = Dijkstra(graph)
    dijkstra.printing()


if __name__ == "__main__":
    main()
