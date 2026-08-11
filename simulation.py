from graph import Drones, Graph
from pathfinding import Pathfinder
from rich import print as rprint
from rich.text import Text

import webcolors   # type: ignore[import-untyped]


class Simulator():
    """
    Runs the drone simulation: creates drones, finds
    paths, and moves them turn by turn
    """

    def __init__(self, graph: Graph, path_finder: Pathfinder) -> None:
        """Set up the simulator with a graph and a pathfinder

        Args:
            graph: The Graph holding zones and connections
            path_finder: The Pathfinder used to compute drone paths
        """
        self.graph: Graph = graph
        self.dijkstra: Pathfinder = path_finder
        self.drones: list[Drones] = list()

    def set_rainbow_zone(self, next_zone: str) -> None:
        """Print a zone name with each letter in a different rainbow color

        Args:
            next_zone: The zone name to print
        """
        colors: list[str] = [
            'red', 'orange', 'yellow', 'green',
            'blue', 'indigo', 'violet'
        ]
        text_res: Text = Text()

        for i, e in enumerate(next_zone):
            color: str = webcolors.name_to_hex(colors[i % len(colors)])
            text_res.append(e, style=color)

        next_zone_print: Text = text_res
        rprint(next_zone_print, end='')

    def set_color_zone(self, next_zone: str, color_name: str) -> None:
        """Print a zone name using its assigned color

        Args:
            next_zone: The zone name to print
            color_name: The color to use for printing
        """
        if color_name == 'rainbow':
            self.set_rainbow_zone(next_zone)
            return
        try:
            color: str = webcolors.name_to_hex(color_name)
        except ValueError:
            color = 'white'
        rprint(f"[{color}]{next_zone}[/{color}]", end='')

    def assign_next_zone(self, drone: Drones) -> None:
        """Set the next zone a drone should move to, based on its path

        Args:
            drone: The drone to update
        """
        current: str = drone.current_zone
        if current == self.graph.end.name:
            drone.next_zone = ""
            return
        idx: int = drone.path_idx
        if idx < len(drone.path):
            next_zone: str = drone.path[idx][0]
            drone.next_zone = next_zone
            drone.path_idx += 1
        else:
            drone.next_zone = ""

    def create_drones(self) -> None:
        """Create all the drones needed for the simulation and store them"""
        for id in range(self.graph.nb_drones):
            drone: Drones = Drones()
            drone.id = id + 1
            drone.name = f"D{id + 1}"
            self.drones.append(drone)

    def move_next_zone(self, drone: Drones) -> None:
        """Move a drone to its next zone and print its movement

        Args:
            drone: The drone to move
        """
        if drone.current_zone == drone.next_zone:
            drone.next_zone = ""
            return

        next_zone: str = drone.next_zone
        is_restricted: bool = False

        if next_zone.startswith('res_conn:'):
            next_zone = next_zone.partition(':')[2]
            is_restricted = True

        elif next_zone.startswith('conn:'):
            next_zone = next_zone.partition(':')[2]

            drone.current_zone = drone.next_zone
            self.assign_next_zone(drone)
            next_zone = drone.next_zone

        if not is_restricted:
            color_name: str = self.graph.zones[next_zone].color
            rprint(drone.name, end='-')
            self.set_color_zone(next_zone, color_name)

        else:
            rprint(drone.name, end='-')
            zone1, _, zone2 = next_zone.partition('-')
            color_name = self.graph.zones[zone1].color
            self.set_color_zone(zone1, color_name)
            print("-", end="")
            color_name = self.graph.zones[zone2].color
            self.set_color_zone(zone2, color_name)

        print(" ", end="")

        drone.current_zone = drone.next_zone
        drone.next_zone = ""

    def start_simulation(self) -> None:
        """Run the full simulation until every drone reaches the end zone."""
        self.create_drones()
        for drone in self.drones:
            path: list[tuple[str, int]] | None = self.dijkstra.shortest_path()
            if not path:
                print(f"Error: Could not find path for {drone.name}")
                exit(1)

            drone.path = path
            self.dijkstra.reserve_path(path)
            drone.current_zone = path[0][0]
            drone.path_idx = 1

        while not all(d.is_finished for d in self.drones):
            for drone in self.drones:
                if drone.is_finished:
                    continue

                if not drone.next_zone:
                    self.assign_next_zone(drone)

                if not drone.next_zone:
                    drone.is_finished = True
                    continue

                self.move_next_zone(drone)

            if not all(d.is_finished for d in self.drones):
                print()
