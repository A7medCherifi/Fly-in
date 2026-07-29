from src.graph import Graph, ZoneType
import heapq


class Pathfinder():
    def __init__(self, graph: Graph):
        self.graph = graph
        self.zones = graph.zones
        self.algo_table = dict()
        self.paths = []

    def __build_algo_table(self):
        for zone in self.zones.values():
            cost = float('inf')
            if zone.name == self.graph.start.name:
                cost = self.graph.get_zone_cost(zone.name)
            self.algo_table.update({
                f"{zone.name}": {
                    "cost": cost,
                    "parent": None
                }
            })

    def get_neighbors(self, name, visited):
        neighbors = []
        connections = self.graph.connections[name]
        for connectinon in connections:
            zone = connectinon.get_next_zone(name)
            if zone.zone_type == ZoneType.BLOCKED:
                continue
            if zone.name in visited:
                continue
            if len(zone.zone_queue) >= zone.max_drones:
                continue
            neighbors.append(zone.name)
        if connections and not neighbors:
            for connectinon in connections:
                zone = connectinon.get_next_zone(name)
                if zone.zone_type == ZoneType.BLOCKED:
                    continue
                if zone.name in visited:
                    continue
                neighbors.append(zone.name)
        return neighbors

    def print_data(self, current_zone):
        zone = self.graph.zones[current_zone]
        print("--------------------")
        print(f"Current Drone: {current_zone}")
        print(f"Max Drones: {zone.max_drones}")
        print(f"Zone queue:\n{zone.zone_queue}\n")
        print("--------------------\n")

    def shortest_path(self, drone):
        # self.create_turn_table()
        visited_zones = set()
        current_zone = self.graph.start
        self.__build_algo_table()
        heap = [
            (self.algo_table[current_zone.name]['cost'], current_zone.name)
        ]
        # print("========================================")
        while heap:
            cost, current_zone = heapq.heappop(heap)
            # self.print_data(current_zone)
            # print(visited_zones)
            if current_zone in visited_zones:
                continue
            visited_zones.add(current_zone)

            if current_zone == self.graph.end.name:
                break

            neighbors = self.get_neighbors(current_zone, visited_zones)
            # print(f"Neibors:\n{neighbors}\n")
            for neighbor in neighbors:
                neighbor_cost = self.graph.get_zone_cost(neighbor)
                new_cost = cost + neighbor_cost
                if new_cost < self.algo_table[neighbor]['cost']:
                    self.algo_table[neighbor]['cost'] = new_cost
                    self.algo_table[neighbor]['parent'] = current_zone
                    heapq.heappush(heap, (new_cost, neighbor))
            # print(heap)
            # print("========================================\n")

        if self.graph.end.name not in visited_zones:
            print("Error: Zone permission denied!")
            exit(1)
        return self.__get_path(drone)

    def __get_path(self, drone):
        path = []
        current = self.graph.end.name
        while current:
            zone = self.graph.zones[current]
            zone.zone_queue.append(drone)
            path.append(current)
            current = self.algo_table[current]['parent']
        return path[::-1]

    # def get_preferred_paths(self):
    #     paths = []
    #     current_zone = self.graph.start
    #     cost = self.graph.get_zone_cost(current_zone.name)
    #     self.paths = [[cost, [current_zone.name]]]

    #     is_first_path = True
    #     first_path_cost = 0
    #     path_counter = 0
    #     while self.paths:
    #         cost, path = heapq.heappop(self.paths)
    #         zone = path[-1]

    #         if not is_first_path:
    #             if cost > first_path_cost or path_counter >= 2:
    #                 break

    #         if zone == self.graph.end.name:
    #             if is_first_path:
    #                 first_path_cost = cost + self.graph.nb_drones
    #                 is_first_path = False
    #             paths.append([cost, path])
    #             path_counter += 1
    #             continue

    #         neighbors = self.graph.get_neighbors(zone)
    #         if not neighbors:
    #             continue

    #         for neighbor in neighbors:
    #             if neighbor.name in path:
    #                 continue
    #             new_path = list(path)
    #             new_path.append(neighbor.name)

    #             neighbor_cost = self.graph.get_zone_cost(zone)
    #             new_cost = neighbor_cost + cost
    #             heapq.heappush(self.paths, [new_cost, new_path])

    #     print("\n============PATHS============\n")
    #     print(len(paths))
    #     print("\n=============================\n")
    #     return paths

    # def __build_algo_table(self):
    #     for zone in self.zones.values():
    #         cost = float('inf')
    #         if zone.name == self.graph.start.name:
    #             cost = self.graph.get_zone_cost(zone.name)
    #         self.algo_table.update({
    #             f"{zone.name}": {
    #                 "cost": cost,
    #                 "parent": None
    #             }
    #         })

    # def shortest_path(self):
    #     visited_zones = set()
    #     current_zone = self.graph.start
    #     self.__build_algo_table()
    #     heap = [
    #         (self.algo_table[current_zone.name]['cost'], current_zone.name)
    #     ]

    #     while heap:
    #         current_cost, current_zone = heapq.heappop(heap)
    #         if current_zone in visited_zones:
    #             continue
    #         visited_zones.add(current_zone)
    #         if self.zones[current_zone].name == self.graph.end.name:
    #             break

    #         neighbors = self.graph.get_neighbors(current_zone)
    #         for neighbor in neighbors:
    #             neighbor_cost = self.graph.get_zone_cost(neighbor.name)
    #             cost = current_cost + neighbor_cost
    #             if cost < self.algo_table[neighbor.name]['cost']:
    #                 self.algo_table[neighbor.name]['cost'] = cost
    #                 self.algo_table[neighbor.name]['parent'] = current_zone
    #                 heapq.heappush(heap, (cost, neighbor.name))

    #     if self.graph.end.name not in visited_zones:
    #         print("Error: Zone permission denied!")
    #         exit(1)
    #     return self.__get_path()

    # def __get_path(self):
    #     path = []
    #     current = self.graph.end.name
    #     while current:
    #         path.append(current)
    #         current = self.algo_table[current]['parent']
    #     return path[::-1]


"""
# Easy Level 2: Simple fork with two paths
nb_drones: 4

start_hub: B 1 0 [color=yellow max_drones=2]
hub: C 2 1 [color=blue]
hub: G 3 1 [color=blue]
hub: X 4 1 [color=blue]
hub: Y 5 1 [color=blue]
hub: D 2 -1 [color=blue]
hub: F 5 -1 [color=blue]
end_hub: E 6 0 [color=red]

connection: B-C
connection: B-D
connection: D-F
connection: F-E
connection: C-G
connection: Y-E
connection: F-G
connection: G-X
connection: X-Y

"""
