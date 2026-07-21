from src.graph import Graph
from src.parsing import Parsing
from src.pathfinding import Pathfinder


def main():
    graph = Graph()
    parsing = Parsing(graph)
    parsing.parse('config.txt')
    # path = graph.shortest_path()
    # graph.create_grid()
    path_finder = Pathfinder(graph)
    path = path_finder.shortest_path()
    print(path)


if __name__ == "__main__":
    main()
