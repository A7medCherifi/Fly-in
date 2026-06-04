from enum import Enum
from src.drones import Drones


class ZoneType(Enum):
    NORMAL = "normal"
    BLOCKED = "blocked"
    RESTRICTED = "restricted"
    PRIORITY = "priority"


class Zone():
    def __init__(self, name: str, x: int, y: int, zone: ZoneType,
                 color: str, max_drones: int, isstart: bool, isend: bool):
        self.name = name
        self.x = x
        self.y = y
        self.isstart = isstart
        self.isend = isend
        self.zone = zone
        self.color = color
        self.max_drones = max_drones
        self.neighbor = list()
        self.connection = list()

    def get_zone(self):
        return {
            'name': self.name,
            'x': self.x,
            'y': self.y,
            'isstart': self.isstart,
            'isend': self.isend,
            'zone': self.zone.value,
            'color': self.color,
            'max_drones': self.max_drones,
            'neighbor': self.neighbor,
            'connection': self.connection,
        }


class Connection():
    def __init__(self, zone1, zone2, max_link_capacity):
        self.zone1 = zone1
        self.zone2 = zone2
        self.max_link_capacity = max_link_capacity

    def get_connection(self):
        return {
            'zone1': self.zone1,
            'zone2': self.zone2,
            'max_link_capacity': self.max_link_capacity,
        }


class Graph():
    def __init__(self):
        self.drones = Drones()
        self.zones = dict()
        self.connections = list()
        self.grid = dict()
        self.start = ''
        self.end = ''

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
