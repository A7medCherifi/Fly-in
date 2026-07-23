from src.graph import Drones


class Simulator():
    def __init__(self, graph, paths) -> None:
        self.graph = graph
        self.paths = paths
        self.drones = list()

    def check_zone_availale(self, drone):
        next_id = drone.path_idx + 1
        if next_id == len(drone.path):
            drone.is_finished = True
            return False

        zone = drone.path[next_id]
        if not self.graph.zones[zone].is_available:
            return False
        return True

    def move_next_zone(self, drone):
        previous_id = drone.path_idx
        drone.path_idx += 1
        id = drone.path_idx
        zone = drone.path[id]
        previous_zone = drone.path[previous_id]
        drone.current_zone = zone
        if zone != self.graph.end.name:
            self.graph.zones[zone].is_available = False
        self.graph.zones[previous_zone].is_available = True
        if drone.path_idx == len(drone.path) - 1:
            drone.is_finished = True
        return f"{drone.name}-{zone} "

    def assign_paths_drones(self):
        for id in range(self.graph.nb_drones):
            path = self.paths[id % len(self.paths)]
            name = f"D{id + 1}"
            drone = Drones(id + 1, path[1], name)
            self.drones.append(drone)

    def start_simulation(self):
        self.assign_paths_drones()
        while not all(d.is_finished for d in self.drones):
            moves = ""
            for drone in self.drones:
                if not self.check_zone_availale(drone):
                    continue
                move = self.move_next_zone(drone)
                moves += move
            print(moves)
