from src.graph import Graph
from src.parsing import Parsing
from src.pathfinding import Pathfinder


def main():
    graph = Graph()
    parsing = Parsing(graph)
    parsing.parse('config.txt')

    path_finder = Pathfinder(graph)
    path_finder.get_all_paths()
    # print(path)


if __name__ == "__main__":
    main()
