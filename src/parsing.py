from src.graph import Connection, Zone, ZoneType


class ParsingError(Exception):
    pass


class Parsing():
    def __init__(self, graph):
        self.line_idx = 0

        self.i = 1
        self.lines = None
        self.zone_type = ZoneType.NORMAL
        self.color = None
        self.max_drones = 1
        self.max_link_capacity = 1
        self.graph = graph

    # ======= Validation =======
    def valid_zone_name(self, name):
        name = name.strip()
        if '-' in name:
            raise ParsingError("Invalid Name!")
        if name in self.graph.zones:
            raise ParsingError("Duplicated zone name!")
        return name

    def valid_coordinates(self, x, y):
        try:
            x = int(x)
            y = int(y)
        except ValueError:
            raise ParsingError("Coordinates should be Integers only!")
        for e in self.graph.zones:
            if self.graph.zones[e].coordinates == (x, y):
                raise ParsingError("Duplicated coordinates are invalid!")
        return (x, y)

    def valid_metadata(self, metadata):
        data = dict()
        zone = color = drones = 0
        array = metadata.split()
        for element in array:
            key, _, value = element.strip().partition('=')
            if '=' in value:
                raise ParsingError("Invalid Metadata Value!")
            if key not in ['zone', 'color', 'max_drones']:
                raise ParsingError("Invalid Metadata Type!")
            if key == 'zone':
                value = ZoneType(value)
                zone += 1
            elif key == 'color':
                if ' ' in value or not value:
                    raise ParsingError("Invalid Color!")
                color += 1
            elif key == 'max_drones':
                try:
                    value = int(value)
                except ValueError:
                    raise ParsingError(
                        "max_drones Should be a Positive Integer!")
                if value <= 0:
                    raise ParsingError("max_drones can't be Negative or 0!")
                drones += 1
            data[key] = value
        if zone > 1 or color > 1 or drones > 1:
            raise ParsingError("Duplicated metadata values!")
        self.zone_type = data.get('zone', ZoneType.NORMAL)
        self.color = data.get('color', None)
        self.max_drones = data.get('max_drones', 1)

    def valid_connection_value(self, values):
        if not values or ' ' in values:
            raise ParsingError("Invalid Connection!")
        data = values.strip().split('-')
        if len(data) != 2:
            raise ParsingError("Invalid Connection!")
        zone1, zone2 = data
        if zone1 not in self.graph.zones:
            raise ParsingError(f"{zone1} not a Zone!")
        if zone2 not in self.graph.zones:
            raise ParsingError(f"{zone2} not a Zone!")
        for c in self.graph.connections:
            if (c.zone1.name == zone1 and c.zone2.name == zone2) or \
              (c.zone1.name == zone2 and c.zone2.name == zone1):
                raise ParsingError("Duplicate connection!")
        return (zone1, zone2)

    def valid_connection_metadata(self, metadata):
        key, _, value = metadata.partition('=')
        if 'max_link_capacity' != key:
            raise ParsingError("Invalid Metadata!")
        try:
            value = int(value)
        except ValueError:
            raise ParsingError("Invalid max_link_capacity Value!")
        if value <= 0:
            raise ParsingError("max_link_capacity Can't be Negative or 0!")
        self.max_link_capacity = int(value)

    # ========= Drones =========
    def nb_drones_parser(self):
        first_line = self.lines[self.line_idx]
        while first_line.strip().startswith('#') or not first_line.strip():
            self.line_idx += 1
            first_line = self.lines[self.line_idx]
        key, _, value = first_line.partition(':')
        if key.strip() != 'nb_drones':
            raise ParsingError("First line should be for 'nb_drones'!")
        if '#' in value:
            value, _, _ = value.partition('#')
        try:
            value = int(value.strip())
        except ValueError:
            raise ParsingError("Invalid Number of Drones!")
        if value <= 0:
            raise ParsingError("nb_drones Can't be Negative or 0!")
        self.graph.nb_drones = value
        self.line_idx += 1

    # ========= Zones =========
    def zone_checker(self):
        isstart = 0
        isend = 0
        i = self.line_idx
        for line in self.lines[i:]:
            if line.strip().startswith('#') or not line.strip():
                self.line_idx += 1
                continue
            key, _, value = line.partition(':')
            if key.strip() == 'start_hub':
                isstart += 1
            elif key.strip() == 'end_hub':
                isend += 1
            elif key.strip() != 'hub':
                break
            self.zone_parser(value.strip(), key)
            self.line_idx += 1
        if isstart != 1 or isend != 1:
            raise ParsingError(
                "Must be one Start hub and End hub!")

    # ------ Parse Zone ------
    def zone_parser(self, line: str, key):
        zone = Zone()
        values = ""
        metadata = ""
        if '[' in line:
            line, _, metadata = line.partition('[')
            if ']' in metadata:
                metadata, _, trash = metadata.partition(']')
                if not metadata.strip():
                    raise ParsingError("Empty Metadata!")
                if trash and not trash.strip().startswith('#'):
                    raise ParsingError("Invalid Input after Metadata!")
            else:
                raise ParsingError("Forget to close Metadata section!")
        elif '#' in line:
            line, _, _ = line.partition('#')
        values = line.strip().split()
        if len(values) != 3:
            raise ParsingError("Invalid Values!")
        name, x, y = values
        name = self.valid_zone_name(name)
        coordinates = self.valid_coordinates(x, y)
        if metadata:
            self.valid_metadata(metadata)
        zone.name = name
        zone.coordinates = coordinates
        zone.zone_type = self.zone_type
        zone.color = self.color
        zone.max_drones = self.max_drones
        if key == 'start_hub':
            zone.isstart = True
            zone.isend = False
        elif key == 'end_hub':
            zone.isstart = False
            zone.isend = True
        else:
            zone.isstart = False
            zone.isend = False
        self.graph.zones[name] = zone
        self.zone_type = ZoneType.NORMAL
        self.color = None
        self.max_drones = 1

    # ========= Connections =========
    def connection_checker(self):
        i = self.line_idx
        for line in self.lines[i:]:
            if line.strip().startswith('#') or not line.strip():
                self.line_idx += 1
                continue
            key, _, value = line.partition(':')
            if key.strip() == 'connection':
                self.connection_parser(value)
            elif key.strip() in ['hub', 'start_hub', 'end_hub']:
                self.zone_checker()
            else:
                raise ParsingError("Invalid line order!")
            self.line_idx += 1

    # ------ Parse Connnection ------
    def connection_parser(self, line):
        connection = Connection()
        values = ""
        metadata = ""
        if '[' in line:
            line, _, metadata = line.partition('[')
            if ']' in metadata:
                metadata, _, trash = metadata.partition(']')
                if not metadata.strip():
                    raise ParsingError("Empty Metadata!")
                if trash and not trash.strip().startswith('#'):
                    raise ParsingError("Invalid Input after Metadata!")
            else:
                raise ParsingError("Forget to close Metadata section!")
        elif '#' in line:
            line, _, _ = line.partition('#')
        values = line.strip()
        name1, name2 = self.valid_connection_value(values)
        if metadata:
            self.valid_connection_metadata(metadata)
        zone1 = self.graph.zones[name1]
        zone2 = self.graph.zones[name2]
        connection.zone1 = zone1
        connection.zone2 = zone2
        connection.max_link_capacity = self.max_link_capacity
        self.graph.connections.append(connection)
        self.max_link_capacity = 1

    def parse(self, file_name: str):
        try:
            with open(file_name, 'r') as f:
                data = f.read()
            self.lines = data.splitlines()
            self.nb_drones_parser()
            self.zone_checker()
            self.connection_checker()
            return
        except FileNotFoundError:
            print("Error: File Not found!\n")
        except PermissionError:
            print("Error: File permission invalid!\n")
        except Exception as e:
            print(f"Error: [line {self.line_idx + 1}] {e}\n")
        exit(1)
