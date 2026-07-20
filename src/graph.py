from enum import Enum
from typing import Dict, List


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
        zone_type = self.zones[name].zone_type
        if zone_type == 'normal' or zone_type == 'priority':
            cost += 1
        elif zone_type == 'restricted':
            cost += 2
        else:
            cost = -1

        return cost

    def _get_neighbors(self, name):
        neighbors = []
        for connection in self.connections[name]:
            neighbor_zone = connection.get_next_zone(name)
            if neighbor_zone.zone_type == ZoneType.BLOCKED:
                continue
            neighbors.append(neighbor_zone.name)
        return neighbors

    def shortest_path(self):
        # start_zone = self.get_start_zone()
        available_zones = []

        for _, zone in self.zones.items():
            current_zone = zone
            neighbors = self._get_neighbors(current_zone.name)
            print(f"Current zone: {zone.name} | Neighbors: {neighbors}")
            available_zones.append(neighbors)
            print(f"Available: {available_zones}\n")

    # def calculate_cost(self, zone_data):
    #     cost = 0
    #     zone_type = zone_data['zone']
    #     if zone_type == 'normal' or zone_type == 'priority':
    #         cost += 1
    #     elif zone_type == 'restricted':
    #         cost += 2
    #     else:
    #         cost = -1
    #     return cost

    def get_start_zone(self) -> str:
        for _, zone in self.zones.items():
            if zone.isstart:
                return zone
        return None

    def get_end_zone(self) -> str:
        for _, zone in self.zones.items():
            if zone.isend:
                return zone
        return None

    # def create_grid(self):
    #     for key, value in self.zones.items():
    #         zone_data = value.get_zone()
    #         if zone_data['isstart']:
    #             self.start = key
    #         if zone_data['isend']:
    #             self.end = key
    #         neighbor = zone_data['neighbor']
    #         self.grid.update({
    #             key: {
    #                 "name": key,
    #                 "neighbor": neighbor,
    #                 "metadata": zone_data,
    #             }
    #         })
