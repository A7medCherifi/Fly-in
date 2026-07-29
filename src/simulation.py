from src.graph import Drones
import heapq


class Simulator():
    def __init__(self, graph, path_finder) -> None:
        self.graph = graph
        self.dijkstra = path_finder
        self.drones = list()

    def create_drones(self):
        for id in range(self.graph.nb_drones):
            drone = Drones()
            drone.id = id + 1
            drone.name = f"D{id + 1}"
            self.drones.append(drone)

    def start_simulation(self):
        self.create_drones()
        for drone in self.drones:
            path = self.dijkstra.shortest_path(drone)
            print("=========================")
            print(f"Drone: {drone.name}\nPath: {path}\n")
            print("=========================\n")
        exit()
