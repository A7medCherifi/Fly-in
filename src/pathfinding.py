from src.graph import Graph
import heapq


class Pathfinder():
    def __init__(self, graph: Graph):
        self.graph = graph
        self.zones = graph.zones
        self.algo_table = dict()

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

    def shortest_path(self):
        visited_zones = set()
        current_zone = self.graph.start
        self.__build_algo_table()
        heap = [
            (self.algo_table[current_zone.name]['cost'], current_zone.name)
        ]

        while heap:
            current_cost, current_zone = heapq.heappop(heap)
            if current_zone in visited_zones:
                continue
            visited_zones.add(current_zone)
            if self.zones[current_zone].name == self.graph.end.name:
                break

            neighbors = self.graph.get_neighbors(current_zone)
            for neighbor in neighbors:
                neighbor_cost = self.graph.get_zone_cost(neighbor.name)
                cost = current_cost + neighbor_cost
                if cost < self.algo_table[neighbor.name]['cost']:
                    self.algo_table[neighbor.name]['cost'] = cost
                    self.algo_table[neighbor.name]['parent'] = current_zone
                    heapq.heappush(heap, (cost, neighbor.name))

        if self.graph.end.name not in visited_zones:
            print("Error: Zone permission denied!")
            exit(1)
        return self.__get_path()

    def __get_path(self):
        path = []
        current = self.graph.end.name
        while current:
            path.append(current)
            current = self.algo_table[current]['parent']
        return path[::-1]
