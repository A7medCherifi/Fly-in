from enum import Enum


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
