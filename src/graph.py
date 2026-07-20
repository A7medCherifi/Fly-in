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
        zone_type = self.zones[name].zone_type.value
        # print(f"\n>>>Zone Type: {zone_type.value}\n")
        if zone_type == 'normal':
            cost = 0
        elif zone_type == 'restricted':
            cost = 8
        elif zone_type == 'priority':
            cost = 2

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

    def _get_next_zone(self, visited_nodes, algo_table):
        cost = float('inf')
        next_zone = Zone()
        for name, _ in algo_table.items():
            if name in visited_nodes:
                continue
            zone_cost = algo_table[name]['cost']
            if zone_cost < cost:
                cost = zone_cost
                next_zone = self.zones[name]
        return next_zone

    def shortest_path(self):
        start_zone = self.get_start_zone()
        available_zones = [zone for _, zone in self.zones.items()]
        visited_nodes = []
        current_zone = start_zone
        algo_table = dict()

        for zone in available_zones:
            cost = float('inf')
            if zone.isstart:
                cost = self._get_zone_cost(zone.name)
            algo_table.update({
                f"{zone.name}": {
                    "cost": cost,
                    "parent": None
                }
            })

        len_available = len(available_zones)
        while len(visited_nodes) < len_available:
            print(f"Current zone: {current_zone.name}")
            neighbors = self._get_neighbors(current_zone.name)
            cost = self._get_zone_cost(current_zone.name)
            print(f"Current cost: {cost}")
            # print(f"Neighbors: {neighbors}")
            for neighbor in neighbors:
                # print(f"Neighbor: {neighbor.name}")
                current_cost = algo_table[neighbor.name]['cost']
                # print(f"Cost: {current_cost}")
                neighbor_cost = self._get_zone_cost(neighbor.name)
                print(f"\nNeighbor cost: {neighbor_cost + cost}")
                # print(f"Neighbor Cost: {neighbor_cost}")
                # print()
                if neighbor_cost + cost < current_cost:
                    algo_table[neighbor.name]['cost'] = neighbor_cost + cost
                    algo_table[neighbor.name]['parent'] = current_zone.name
                # print(algo_table[neighbor.name]['cost'])
                # print(algo_table[neighbor.name]['parent'])
            visited_nodes.append(current_zone.name)
            current_zone = self._get_next_zone(visited_nodes, algo_table)
            print(f"\nNext zone: {current_zone.name}")
            print()
        for key, value in algo_table.items():
            print("========================\n")
            print(f"None: {key},\nCost: {value['cost']}\nParent: {value['parent']}\n")
        print("\n========================\n")

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
