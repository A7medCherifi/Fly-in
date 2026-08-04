from src.graph import Graph
from src.parsing import Parsing
from src.pathfinding import Pathfinder
from src.simulation import Simulator


def main():
    graph = Graph()
    parsing = Parsing(graph)
    parsing.parse('config.txt')
    exit()
    path_finder = Pathfinder(graph)
    # path_finder.get_preferred_paths()
    simulator = Simulator(graph, path_finder)
    simulator.start_simulation()


if __name__ == "__main__":
    main()
