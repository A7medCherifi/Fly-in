from graph import Graph
from parsing import Parsing
from pathfinding import Pathfinder
from simulation import Simulator
import sys


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Invalid arguments, program only takes config file as argument!")
        exit(1)


    graph: Graph = Graph()
    parsing: Parsing = Parsing(graph)
    parsing.parse(sys.argv[1])

    try:
        path_finder: Pathfinder = Pathfinder(graph)
        simulator: Simulator = Simulator(graph, path_finder)
        simulator.start_simulation()
    except Exception as e:
        print(f"Error: {e}\n")
        exit(1)
