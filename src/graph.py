from enum import Enum
from typing import Dict, List
import heapq


class ZoneType(Enum):
    NORMAL = "normal"
    BLOCKED = "blocked"
    RESTRICTED = "restricted"
    PRIORITY = "priority"


class Drones():
    def __init__(self):
        self.nb_drones = 0


class Zone():
    def __init__(self):
        self.name = str
        self.coordinates = tuple()
        self.isstart = bool
        self.isend = bool
        self.zone_type = ZoneType.NORMAL
        self.color = str
        self.max_drones = int
        self.neighbor = list()
        self.connection = list()


class Connection():
    def __init__(self):
        self.name = str
        self.zone1 = Zone()
        self.zone2 = Zone()
        self.max_link_capacity = int

    def get_next_zone(self, name):
        if name == self.zone1.name:
            return self.zone2
        elif name == self.zone2.name:
            return self.zone1
        return None


class Graph():
    def __init__(self):
        self.nb_drones = 0
        self.zones: Dict[str, Zone] = {}
        self.connections: Dict[str, List[Connection]] = {}

    def _get_zone_cost(self, name):
        cost = 0
        zone_type = self.zones[name].zone_type.value

        if zone_type == 'normal':
            cost = 1
        elif zone_type == 'restricted':
            cost = 2
        elif zone_type == 'priority':
            cost = 1

        return cost

    def _get_neighbors(self, name):
        neighbors = []
        connections = self.connections[name]
        for connection in connections:
            neighbor_zone = connection.get_next_zone(name)
            if neighbor_zone.zone_type == ZoneType.BLOCKED:
                continue
            neighbors.append(neighbor_zone)
        return neighbors

    def _get_next_zone(self, visited_zones, algo_table):
        cost = float('inf')
        next_zone = Zone()
        for name, _ in algo_table.items():
            if name in visited_zones:
                continue
            zone_cost = algo_table[name]['cost']
            if zone_cost < cost:
                cost = zone_cost
                next_zone = self.zones[name]
        return next_zone

    def shortest_path(self):
        start_zone = self.get_start_zone()
        end_zone = self.get_end_zone()
        visited_zones = set()
        current_zone = start_zone
        algo_table = dict()

        for zone in self.zones.values():
            cost = float('inf')
            if zone.isstart:
                cost = self._get_zone_cost(zone.name)
            algo_table.update({
                f"{zone.name}": {
                    "cost": cost,
                    "parent": None
                }
            })
        heap = [(algo_table[start_zone.name]['cost'], start_zone.name)]

        while heap:
            current_cost, current_zone = heapq.heappop(heap)
            if current_zone in visited_zones:
                continue
            visited_zones.add(current_zone)
            if self.zones[current_zone].isend:
                break

            neighbors = self._get_neighbors(current_zone)
            for neighbor in neighbors:
                neighbor_cost = self._get_zone_cost(neighbor.name)
                cost = current_cost + neighbor_cost
                if cost < algo_table[neighbor.name]['cost']:
                    algo_table[neighbor.name]['cost'] = cost
                    algo_table[neighbor.name]['parent'] = current_zone
                    heapq.heappush(heap, (cost, neighbor.name))

        if end_zone.name not in visited_zones:
            print("Error: Zone permission denied!")
            exit(1)
        return self._get_path(algo_table)

    def _get_path(self, end_zone, algo_table):
        path = []
        current = end_zone.name
        while current:
            path.append(current)
            current = algo_table[current]['parent']
        return path[::-1]

    def get_start_zone(self) -> Zone:
        for _, zone in self.zones.items():
            if zone.isstart:
                return zone
        return None

    def get_end_zone(self) -> Zone:
        for _, zone in self.zones.items():
            if zone.isend:
                return zone
        return None
