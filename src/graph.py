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
        }


class Connection():
    def __init__(self, zone1, zone2, max_link_capacity):
        self.zone1 = zone1
        self.zone2 = zone2
        self.max_link_capacity = max_link_capacity

    def get_connections(self):
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

    def add_to_zones(self, name, zone: Zone):
        self.zones.update({name: zone})

    def add_to_connections(self, connection):
        self.connections.append(connection)

    def get_zone(self, name):
        return self.zones.get(name)
