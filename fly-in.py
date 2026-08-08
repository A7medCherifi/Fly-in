from graph import Graph
from parsing import Parsing
from pathfinding import Pathfinder
from simulation import Simulator

import argparse


def main() -> None:
    """
    Parse the map file, set up the pathfinder and simulator
    and run the simulation
    """
    argument = argparse.ArgumentParser()
    argument.add_argument("config_text")

    args = argument.parse_args()

    graph: Graph = Graph()
    parsing: Parsing = Parsing(graph)
    parsing.parse(args.config_text)

    try:
        path_finder: Pathfinder = Pathfinder(graph)
        simulator: Simulator = Simulator(graph, path_finder)
        simulator.start_simulation()
    except Exception as e:
        print(f"Error: {e}\n")
        exit(1)


if __name__ == "__main__":
    main()
