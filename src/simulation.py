from src.graph import Drones
import heapq


class Simulator():
    def __init__(self, graph, path_finder) -> None:
        self.graph = graph
        self.dijkstra = path_finder
        self.drones = list()

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
            next_zone = ""

    def create_drones(self):
        for id in range(self.graph.nb_drones):
            drone = Drones()
            drone.id = id + 1
            drone.name = f"D{id + 1}"
            self.drones.append(drone)

    def move_next_zone(self, drone):
        move = ""
        if drone.next_zone and drone.current_zone != drone.next_zone:
            next_zone = drone.next_zone
            if next_zone.startswith('connection:'):
                next_zone = next_zone.split(':')[1]

            move = f"{drone.name}-{next_zone} "

        drone.current_zone = drone.next_zone
        drone.path_idx += 1
        drone.next_zone = ""
        return move

    def start_simulation(self):
        self.create_drones()
        for drone in self.drones:
            path = self.dijkstra.shortest_path(drone)
            if not path:
                print(f"Error: Could not find path for {drone.name}")
                return

            drone.path = path
            self.dijkstra.reserve_path(path)
            drone.current_zone = path[0][0]
            drone.path_idx = 1
            # print("=========================")
            # print(f"Drone: {drone.name}\nPath:")
            # print(*path, sep='\n')
            # print("=========================\n")
        while not all(d.is_finished for d in self.drones):
            moves = ""
            for drone in self.drones:
                if drone.is_finished:
                    continue

                if not drone.next_zone:
                    self.assign_next_zone(drone)

                if not drone.next_zone:
                    drone.is_finished = True
                    continue

                move = self.move_next_zone(drone)
                moves += move
            print(moves)
