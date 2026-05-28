from enum import Enum


class ParsingError(Exception):
    pass


class ZoneType(Enum):
    NORMAL = "normal"
    BLOCKED = "blocked"
    RESTRICTED = "restricted"
    PRIORITY = "priority"


class Drones():
    pass


class Zone():
    def __init__(self, name, x, y, zone, color, max_drones, isstart, isend):
        self.name = name
        self.x = x
        self.y = y
        self.isstart = isstart
        self.isend = isend
        self.zone = zone
        self.color = color
        self.max_drones = max_drones


class Graph():
    def __init__(self):
        self.nb_drones = 0
        self.zones = dict()
        self.connections = list()

    def add_to_zones(self, name, zone: Zone):
        self.zones.update({name: zone})

    def add_to_connections(self, connection):
        self.connections.append(connection)

    def get_zone(self, name):
        return self.zones.get(name)


class Connection():
    def __init__(self, zone1, zone2, max_link_capacity):
        self.zone1 = zone1
        self.zone2 = zone2
        self.max_link_capacity = max_link_capacity


class Parsing():
    def __init__(self):
        self.lines = None
        self.nb_drones = None
        self.zone = ZoneType.NORMAL
        self.color = None
        self.max_drones = 1
        self.max_link_capacity = 1
        self.graph = Graph()

    def valid_name(self, name):
        if ' ' in name or '-' in name:
            raise ParsingError("Invalid Name!")

    def valid_coordinates(self, x, y):
        x1 = int(x)
        y1 = int(y)
        return (x1, y1)

    def valid_metadata(self, metadata):
        data = dict()
        array = metadata.split()
        for element in array:
            key, value = element.strip().split('=')
            if key not in ['zone', 'color', 'max_drones']:
                raise ParsingError("Invalid Metadata Type")
            if key == 'zone':
                value = ZoneType(value)
            data[key] = value
        self.zone = data.get('zone', ZoneType.NORMAL)
        self.color = data.get('color', None)
        self.max_drones = data.get('max_drones', 1)

    def zone_parser(self, line: str):
        key, value = line.split(':')
        value, _, metadata = value.partition('[')
        if metadata and ']' not in metadata:
            raise ParsingError("Invalid Value! 0")
        metadata, _, test = metadata.partition(']')
        if test:
            raise ParsingError('Invalid Metadata line')
        value.strip()
        metadata.strip()
        values = value.split()
        if len(values) != 3:
            raise ParsingError("Invalid Values! 1")
        name, x, y = values
        if not name or not x or not y:
            raise ParsingError("Invalid Value! 2")
        self.valid_name(name)
        x, y = self.valid_coordinates(x, y)
        if metadata:
            self.valid_metadata(metadata)
        if key == "start_hub":
            zone = Zone(name, x, y, self.zone, self.color,
                        self.max_drones, True, False)
        elif key == "end_hub":
            zone = Zone(name, x, y, self.zone, self.color,
                        self.max_drones, False, True)
        else:
            zone = Zone(name, x, y, self.zone, self.color,
                        self.max_drones, False, False)
        self.graph.add_to_zones(name, zone)
        self.zone = ZoneType.NORMAL
        self.color = None
        self.max_drones = 1

    def zone_checker(self):
        i = 1
        for line in self.lines[1:]:
            if line.strip().startswith('#') or not line:
                i += 1
                continue
            if line.startswith('start_hub:'):
                self.zone_parser(line)
            elif line.startswith('end_hub:'):
                self.zone_parser(line)
            elif line.startswith('hub:'):
                self.zone_parser(line)
            else:
                break
            i += 1
        return i

    def valid_connection_metadata(self, metadata):
        key, _, value = metadata.partition('=')
        if 'max_link_capacity' != key:
            raise ParsingError("Invalid Metadata!")
        if int(value) <= 0:
            raise ParsingError("Invalid value of mmetadata")
        self.max_link_capacity = int(value)

    def connection_parser(self, line):
        key, _, value = line.strip().partition(':')
        value, _, metadata = value.partition('[')
        if metadata and ']' not in metadata:
            raise ParsingError("Invalid Value! 0")
        metadata, _, test = metadata.partition(']')
        if test:
            raise ParsingError('Invalid Metadata line')
        zone1, _, zone2 = value.strip().partition('-')
        if ' ' in zone1 or ' ' in zone2:
            raise ParsingError("Invalid Zone!")
        if not self.graph.get_zone(zone1):
            raise ParsingError("Zone not found!")
        if not self.graph.get_zone(zone2):
            raise ParsingError("Zone not found!")
        if metadata:
            self.valid_connection_metadata(metadata)
        connection = Connection(zone1, zone2, self.max_link_capacity)
        self.graph.add_to_connections(connection)
        self.max_link_capacity = 1

    def connection_checker(self, i):
        for line in self.lines[i:]:
            if line.strip().startswith('#') or not line:
                continue
            if line.startswith('connection:'):
                self.connection_parser(line)
            else:
                raise ParsingError("Invalid line order!")
            i += 1

    def nb_drones_parser(self):
        nb_drones = self.lines[0]
        if not nb_drones.startswith("nb_drones:"):
            raise ParsingError("'nb_drones' Key requied first!")
        else:
            lines = nb_drones.split(':')
            if len(lines) != 2:
                raise ParsingError("should be only Key and Value!")
            key, value = lines
            value = value.strip()
            if int(value) <= 0:
                raise ParsingError("Positive integers only you bastard!")
            self.nb_drones = value
            self.graph.nb_drones = value

    def parse(self, file_name: str):
        try:
            with open(file_name, 'r') as f:
                data = f.read()
            self.lines = data.splitlines()
            self.nb_drones_parser()
            i = self.zone_checker()
            self.connection_checker(i)
            print("\nEverything went will!")
        except FileNotFoundError:
            print("Error: File Not found!\n")
        except PermissionError:
            print("Error: File permission invalid!\n")
        except Exception as e:
            print(f"Error: {e}\n")


def main():
    parsing = Parsing()
    parsing.parse('test.txt')


if __name__ == "__main__":
    main()
