from src.graph import Graph
from src.parsing import Parsing
from src.pathfinding import Pathfinder
from src.simulation import Simulator


def main() -> None:
    graph: Graph = Graph()
    parsing: Parsing = Parsing(graph)
    parsing.parse('config.txt')

    try:
        path_finder: Pathfinder = Pathfinder(graph)
        simulator: Simulator = Simulator(graph, path_finder)
        simulator.start_simulation()
    except Exception as e:
        print(f"Error: {e}\n")
        exit(1)


if __name__ == "__main__":
    main()
