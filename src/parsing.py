from src.graph import Connection, Zone, ZoneType


class ParsingError(Exception):
    pass


class Parsing():
    def __init__(self, graph):
        self.i = 1
        self.lines = None
        self.zone = ZoneType.NORMAL
        self.color = None
        self.max_drones = 1
        self.max_link_capacity = 1
        self.graph = graph

    def valid_name(self, name):
        if not name or ' ' in name or '-' in name:
            raise ParsingError("Invalid Name!")
        return name

    def valid_coordinates(self, x, y):
        x1 = int(x)
        y1 = int(y)
        for e in self.graph.zones:
            if self.graph.zones[e].x == x1 and self.graph.zones[e].y == y1:
                raise ParsingError("Duplicated coordinates are invalid!")
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
            if key == 'color':
                if ' ' in value or not value:
                    raise ParsingError("Invalid Color!")
            if key == 'max_drones':
                if int(value) <= 0:
                    raise ParsingError("Invalid max_drones value!")
                value = int(value)
            data[key] = value
        self.zone = data.get('zone', ZoneType.NORMAL)
        self.color = data.get('color', None)
        self.max_drones = data.get('max_drones', 1)

    def zone_parser(self, line: str):
        key, value = line.split(':')
        value, test, metadata = value.partition('[')
        if metadata and ']' not in metadata:
            raise ParsingError("Invalid Value!")
        if not metadata and test:
            raise ParsingError("Invalid Metadata!")
        if metadata:
            metadata, _, test = metadata.partition(']')
            metadata = metadata.strip()
            if test or not metadata:
                raise ParsingError("Invalid Metadata line")
        values = value.strip().split()
        if len(values) != 3:
            raise ParsingError("Invalid Values!")
        name, x, y = values
        if not name or not x or not y:
            raise ParsingError("Invalid Value!")
        name = self.valid_name(name)
        x, y = self.valid_coordinates(x, y)
        if metadata:
            self.valid_metadata(metadata)
        if self.graph.get_zone(name):
            raise ParsingError("Duplicated Zones!")
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
        isstart = 0
        isend = 0
        for line in self.lines[1:]:
            if line.strip().startswith('#') or not line.strip():
                self.i += 1
                continue
            if line.startswith('start_hub:'):
                self.zone_parser(line)
                isstart += 1
            elif line.startswith('end_hub:'):
                self.zone_parser(line)
                isend += 1
            elif line.startswith('hub:'):
                self.zone_parser(line)
            else:
                break
            self.i += 1
        if isstart != 1 or isend != 1:
            raise ParsingError(
                "Must be one Start hub and End hub!")

    def valid_connection_metadata(self, metadata):
        key, _, value = metadata.partition('=')
        if 'max_link_capacity' != key:
            raise ParsingError("Invalid Metadata!")
        if int(value) <= 0:
            raise ParsingError("Invalid value of mmetadata")
        self.max_link_capacity = int(value)

    def connection_parser(self, line):
        _, value = line.strip().split(':')
        value, test, metadata = value.partition('[')
        if metadata and ']' not in metadata:
            raise ParsingError("Invalid Value!")
        if not metadata and test:
            raise ParsingError("Invalid Metadata!")
        if metadata:
            metadata, _, test = metadata.partition(']')
            metadata = metadata.strip()
            if test or not metadata:
                raise ParsingError("Invalid Metadata line")
        zone1, _, zone2 = value.strip().partition('-')
        if ' ' in zone1 or ' ' in zone2:
            raise ParsingError("Invalid Zone!")
        if not self.graph.get_zone(zone1):
            raise ParsingError("Zone not found!")
        if not self.graph.get_zone(zone2):
            raise ParsingError("Zone not found!")
        if zone1 == zone2:
            raise ParsingError("A zone cannot connect to itself!")
        if metadata:
            self.valid_connection_metadata(metadata)
        for c in self.graph.connections:
            if (c.zone1 == zone1 and c.zone2 == zone2) or \
              (c.zone1 == zone2 and c.zone2 == zone1):
                raise ParsingError("Duplicate connection!")
        connection = Connection(zone1, zone2, self.max_link_capacity)
        self.graph.add_to_connections(connection)
        self.max_link_capacity = 1

    def connection_checker(self):
        for line in self.lines[self.i - 1:]:
            if line.strip().startswith('#') or not line.strip():
                self.i += 1
                continue
            if line.startswith('connection:'):
                self.connection_parser(line)
            else:
                raise ParsingError("Invalid line order!")
            self.i += 1

    def nb_drones_parser(self):
        nb_drones = self.lines[0]
        if not nb_drones.startswith("nb_drones:"):
            raise ParsingError("'nb_drones' Key requied first!")
        else:
            lines = nb_drones.split(':')
            if len(lines) != 2:
                raise ParsingError("should be only Key and Value!")
            _, value = lines
            value = value.strip()
            if int(value) <= 0:
                raise ParsingError("Positive integers only!")
            self.graph.drones.nb_drones = int(value)
        self.i += 1

    def parse(self, file_name: str):
        try:
            with open(file_name, 'r') as f:
                data = f.read()
            self.lines = data.splitlines()
            self.nb_drones_parser()
            self.zone_checker()
            self.connection_checker()
        except FileNotFoundError:
            print(f"Error: [line {self.i}] File Not found!\n")
        except PermissionError:
            print(f"Error: [line {self.i}] File permission invalid!\n")
        except Exception as e:
            print(f"Error: [line {self.i}] {e}\n")
