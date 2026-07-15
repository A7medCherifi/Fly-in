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

    def get_connection(self):
        return {
            'zone1': self.zone1,
            'zone2': self.zone2,
            'max_link_capacity': self.max_link_capacity,
        }


class Graph():
    def __init__(self):
        self.nb_drones = 0
        self.zones: Dict[str, Zone] = {}
        self.connections: Dict[str, List[Connection]] = {}
        self.grid = dict()
        self.start = Zone
        self.end = Zone

    def add_to_zones(self, name, zone: Zone):
        self.zones.update({name: zone})

    def add_to_connections(self, connection: Connection):
        self.connections.append(connection)

    def get_zone(self, name):
        return self.zones.get(name)

    def calculate_cost(self, zone_data):
        cost = 0
        zone_type = zone_data['zone']
        if zone_type == 'normal' or zone_type == 'priority':
            cost += 1
        elif zone_type == 'restricted':
            cost += 2
        else:
            cost = -1
        return cost

    def get_start_zone(self) -> str:
        return self.start

    def get_end_zone(self) -> str:
        return self.end

    def create_grid(self):
        for key, value in self.zones.items():
            zone_data = value.get_zone()
            if zone_data['isstart']:
                self.start = key
            if zone_data['isend']:
                self.end = key
            neighbor = zone_data['neighbor']
            self.grid.update({
                key: {
                    "name": key,
                    "neighbor": neighbor,
                    "metadata": zone_data,
                }
            })
