from enum import Enum
from typing import Dict, List


class ZoneType(Enum):
    NORMAL = "normal"
    BLOCKED = "blocked"
    RESTRICTED = "restricted"
    PRIORITY = "priority"


class Drones():
    def __init__(self):
        self.id = id
        self.name = ""
        self.current_zone = ""
        self.is_finished = False
        self.next_zone = ""
        self.path = list()
        self.path_idx = 0


class Zone():
    def __init__(self):
        self.name = ""
        self.coordinates = tuple()
        self.zone_type = ZoneType.NORMAL
        self.color = ""
        self.max_drones = 1


class Connection():
    def __init__(self):
        self.name = ""
        self.zone1 = Zone()
        self.zone2 = Zone()
        self.max_link_capacity = 1

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
        self.turn_table = dict()
        self.conn_table = dict()
        self.start = Zone()
        self.end = Zone()

    def get_zone_cost(self, name):
        cost = 0
        zone_type = self.zones[name].zone_type.value

        if zone_type == 'normal':
            cost = 1
        elif zone_type == 'restricted':
            cost = 2
        elif zone_type == 'priority':
            cost = 1

        return cost
