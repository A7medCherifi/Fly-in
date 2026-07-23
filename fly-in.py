from src.graph import Graph
from src.parsing import Parsing
from src.pathfinding import Pathfinder
from src.simulation import Simulator


def main():
    graph = Graph()
    parsing = Parsing(graph)
    parsing.parse('config.txt')

    path_finder = Pathfinder(graph)
    paths = path_finder.get_preferred_paths()
    simulator = Simulator(graph, paths)
    simulator.start_simulation()


if __name__ == "__main__":
    main()
