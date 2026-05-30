from drones import Drones
from zone import Zone


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
