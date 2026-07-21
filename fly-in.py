from src.graph import Graph
from src.parsing import Parsing
# from src.pathfinding import Pathfinder


def main():
    graph = Graph()
    parsing = Parsing(graph)
    parsing.parse('config.txt')
    path = graph.shortest_path()
    print(path)
    # graph.create_grid()
    # path_finder = Pathfinder(graph)
    # path_finder.dijkstra()


if __name__ == "__main__":
    main()
