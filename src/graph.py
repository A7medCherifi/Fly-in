from enum import Enum
from typing import Dict, List, Optional, Tuple


class ZoneType(Enum):
    NORMAL = "normal"
    BLOCKED = "blocked"
    RESTRICTED = "restricted"
    PRIORITY = "priority"


class Drones():
    def __init__(self) -> None:
        self.id: int = 0
        self.name: str = ""
        self.current_zone: str = ""
        self.is_finished: bool = False
        self.next_zone: str = ""
        self.path: List[Tuple[str, int]] = list()
        self.path_idx: int = 0


class Zone():
    def __init__(self) -> None:
        self.name: str = ""
        self.coordinates: tuple = tuple()
        self.zone_type: ZoneType = ZoneType.NORMAL
        self.color: str = ""
        self.max_drones: int = 1


class Connection():
    def __init__(self) -> None:
        self.name: str = ""
        self.zone1: Zone = Zone()
        self.zone2: Zone = Zone()
        self.max_link_capacity: int = 1

    def get_next_zone(self, name: str) -> Zone:
        if name == self.zone1.name:
            return self.zone2
        return self.zone1



class Graph():
    def __init__(self) -> None:
        self.nb_drones: int = 0
        self.zones: Dict[str, Zone] = {}
        self.connections: Dict[str, List[Connection]] = {}
        self.turn_table: Dict[Tuple[str, int], int] = dict()
        self.conn_table: Dict[Tuple[str, int], int] = dict()
        self.start: Zone = Zone()
        self.end: Zone = Zone()

    def get_zone_cost(self, name: str) -> int:
        cost: int = 0
        zone_type: str = self.zones[name].zone_type.value

        if zone_type == 'normal':
            cost = 1
        elif zone_type == 'restricted':
            cost = 2
        elif zone_type == 'priority':
            cost = 1

        return cost
