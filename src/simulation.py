from src.graph import Drones
from rich import print as rprint
from rich.text import Text

import webcolors


class Simulator():
    def __init__(self, graph, path_finder) -> None:
        self.graph = graph
        self.dijkstra = path_finder
        self.drones = list()
    
    def set_rainbow_zone(self, next_zone):
        colors = ['red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet']
        text_res = Text()
        
        for i, e in enumerate(next_zone):
            color = webcolors.name_to_hex(colors[i % len(colors)])
            text_res.append(e, style=color)

        next_zone_print = text_res
        rprint(next_zone_print, end='')
            
    def set_color_zone(self, next_zone, color_name):
        if color_name.strip() == 'rainbow':
            self.set_rainbow_zone(next_zone)
            return
        try:
            color = webcolors.name_to_hex(color_name)
        except ValueError:
            color = 'white'
        rprint(f"[{color}]{next_zone}[/{color}]", end='')

    def assign_next_zone(self, drone):
        current = drone.current_zone
        if current == self.graph.end.name:
            drone.next_zone = ""
            return
        idx = drone.path_idx
        if idx < len(drone.path):
            next_zone = drone.path[idx][0]
            drone.next_zone = next_zone
            drone.path_idx += 1
        else:
            drone.next_zone = ""

    def create_drones(self):
        for id in range(self.graph.nb_drones):
            drone = Drones()
            drone.id = id + 1
            drone.name = f"D{id + 1}"
            self.drones.append(drone)

    def move_next_zone(self, drone):
        if drone.current_zone == drone.next_zone:
            drone.next_zone = ""
            return

        next_zone = drone.next_zone
        is_restricted = False
        
        if next_zone.startswith('res_conn:'):
            next_zone = next_zone.partition(':')[2]
            is_restricted = True
            
        elif next_zone.startswith('conn:'):
            drone.current_zone = drone.next_zone
            self.assign_next_zone(drone)
            next_zone = drone.next_zone

        if not is_restricted:
            color_name = self.graph.zones[next_zone].color
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

    def start_simulation(self):
        self.create_drones()
        for drone in self.drones:
            path = self.dijkstra.shortest_path()
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
            print()