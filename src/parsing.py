from src.graph import Connection, Graph, Zone, ZoneType
from typing import Any, Dict, List, Optional, Tuple


class ParsingError(Exception):
    pass


class Parsing():
    def __init__(self, graph: Graph) -> None:
        self.line_idx: int = 0

        self.i: int = 1
        self.lines: Optional[List[str]] = list()
        self.zone_type: ZoneType = ZoneType.NORMAL
        self.color: str = "white"
        self.max_drones: int = 1
        self.max_link_capacity: int = 1
        self.graph: Graph = graph
        self.connections: int = 0

    # ======= Validation =======
    def valid_zone_name(self, name: str) -> str:
        name = name.strip()
        if '-' in name:
            raise ParsingError("Invalid Name!")
        if name in self.graph.zones:
            raise ParsingError("Duplicated zone name!")
        return name

    def valid_coordinates(self, x: str, y: str) -> Tuple[int, int]:
        try:
            x1: int = int(x)
            y1: int = int(y)
        except ValueError:
            raise ParsingError("Coordinates should be Integers only!")
        for z in self.graph.zones:
            if self.graph.zones[z].coordinates == (x1, y1):
                raise ParsingError("Duplicated coordinates are invalid!")
        return (x1, y1)

    def valid_metadata(self, metadata: str) -> None:
        data: Dict[str, Any] = dict()
        zone = color = drones = 0
        array: List[str] = metadata.split()
        for element in array:
            value: Any = ""
            key, _, value = element.strip().partition('=')
            if '=' in value or ']' in value:
                raise ParsingError(f"Invalid Metadata Value {value}!")
            if key not in ['zone', 'color', 'max_drones']:
                raise ParsingError("Invalid Metadata Type!")
            if key == 'zone':
                value = ZoneType(value)
                zone += 1
            elif key == 'color':
                if not value:
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
        self.color = data.get('color', 'white')
        self.max_drones = data.get('max_drones', 1)

    def valid_connection_value(self, values: str) -> Tuple[str, str]:
        if not values or ' ' in values:
            raise ParsingError("Invalid Connection!")
        data: List[str] = values.strip().split('-')
        if len(data) != 2:
            raise ParsingError("Invalid Connection!")
        zone1, zone2 = data
        if zone1 not in self.graph.zones:
            raise ParsingError(f"{zone1} not a Zone!")
        if zone2 not in self.graph.zones:
            raise ParsingError(f"{zone2} not a Zone!")
        if zone1 in self.graph.connections:
            for c in self.graph.connections[zone1]:
                if c.zone1.name == zone2 or c.zone2.name == zone2:
                    raise ParsingError("Duplicate connection!")
        return (zone1.strip(), zone2.strip())

    def valid_connection_metadata(self, metadata: str) -> None:
        value: Any = ""
        key, _, value = metadata.partition('=')
        size: List[str] = metadata.split()
        if len(size) > 1:
            raise ParsingError("only max_link_capacity key valid")
        if 'max_link_capacity' != key:
            raise ParsingError("Invalid Metadata!")
        try:
            value = int(value)
        except ValueError:
            raise ParsingError("Invalid max_link_capacity Value!")
        if value <= 0:
            raise ParsingError("max_link_capacity Can't be Negative or 0!")
        self.max_link_capacity = int(value)

    def check_start_end(self) -> None:
        start: str = self.graph.start.name
        end: str = self.graph.end.name
        if not start:
            raise ParsingError("There is not start hub, invalid graph!")
        if not end:
            raise ParsingError("There is not end hub, invalid graph!")

    # ========= Drones =========
    def nb_drones_parser(self) -> None:
        first_line: str = self.lines[self.line_idx]
        while first_line.strip().startswith('#') or not first_line.strip():
            self.line_idx += 1
            first_line = self.lines[self.line_idx]
        value: Any = ""
        key, _, value = first_line.partition(':')
        if key.strip() != 'nb_drones':
            raise ParsingError("First line should be for 'nb_drones'! should be: nb_drones: <int>")
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
    def zone_checker(self) -> None:
        i: int = self.line_idx
        for line in self.lines[i:]:
            if line.strip().startswith('#') or not line.strip():
                self.line_idx += 1
                continue
            key, _, value = line.partition(':')
            if key.strip() == 'nb_drones':
                raise ParsingError("Duplicated nb_drones rule!")
            if key.strip().startswith("connection"):
                break
            if key.strip() not in ['hub', 'end_hub', 'start_hub']:
                raise ParsingError("Invalid rule name! should be hub: <zone> <x> <y>")
            if not value.startswith(' '):
                raise ParsingError("You should seperate zone from the rule!")
            self.zone_parser(value.strip(), key)
            self.line_idx += 1

    # ------ Parse Zone ------
    def zone_parser(self, line: str, key: str) -> None:
        zone: Zone = Zone()
        if '#' in line:
            line, _, _ = line.partition('#')
        values: List[str] = line.strip().split()
        if len(values) < 3:
            raise ParsingError(f"Invalid Values of {key}, Should be <zone> <x> <y>!")
        name, x, y = values[0], values[1], values[2]
        name = self.valid_zone_name(name)
        coordinates: Tuple[int, int] = self.valid_coordinates(x, y)
        metadata: str = ""
        if len(values) > 3:
            metadata = " ".join(values[3:])
            if '[' in metadata:
                metadata = metadata.partition('[')[2]
                if ']' in metadata:
                    metadata, _, trash = metadata.rpartition(']')
                    if not metadata.strip():
                        raise ParsingError("Empty Metadata!")
                    if trash and not trash.strip().startswith('#'):
                        raise ParsingError("Invalid Input after Metadata closed!")
                else:
                    raise ParsingError("Forget to close Metadata section!")
            else:
                raise ParsingError("Invalid Metadata, should be inside of [...]!")

        if metadata:
            self.valid_metadata(metadata)
        zone.name = name
        zone.coordinates = coordinates
        zone.zone_type = self.zone_type
        zone.color = self.color
        zone.max_drones = self.max_drones
        if key.strip() == 'start_hub':
            if self.graph.start.name:
                raise ParsingError("Start hub is duplicated!")
            if zone.zone_type.value == 'blocked':
                raise ParsingError("Start hub can't be Blocked!")
            self.graph.start = zone
        elif key.strip() == 'end_hub':
            if self.graph.end.name:
                raise ParsingError("End hub is duplicated!")
            if zone.zone_type.value == 'blocked':
                raise ParsingError("End hub can't be Blocked!")
            self.graph.end = zone
        self.graph.zones[name] = zone
        self.zone_type = ZoneType.NORMAL
        self.color = "white"
        self.max_drones = 1

    # ========= Connections =========
    def connection_checker(self) -> None:
        i: int = self.line_idx
        for line in self.lines[i:]:
            if line.strip().startswith('#') or not line.strip():
                self.line_idx += 1
                continue
            key, _, value = line.partition(':')
            if key.strip() == 'connection':
                self.connections += 1
                if not value.startswith(' '):
                    raise ParsingError("You should seperate connection from the rule!")
                self.connection_parser(value)
            elif key.strip() in ['hub', 'start_hub', 'end_hub']:
                self.zone_checker()
            elif key.strip() == 'nb_drones':
                raise ParsingError("Duplicated nb_drones rule!")
            else:
                raise ParsingError("Invalid rule name! should be: connection: <connection>")
            self.line_idx += 1

    # ------ Parse Connnection ------
    def connection_parser(self, line: str) -> None:
        connection: Connection = Connection()
        if '#' in line:
            line, _, _ = line.partition('#')
        metadata: str = ""
        values: List[str] = line.strip().split()
        if len(values) < 1:
            raise ParsingError("Invalid connection, Should be <connection>!")
        name1, name2 = self.valid_connection_value(values[0])
        if len(values) > 1:
            metadata = ' '.join(values[1:])
            if '[' in metadata:
                metadata = metadata.partition('[')[2]
                if ']' in metadata:
                    metadata, _, trash = metadata.partition(']')
                    if not metadata.strip():
                        raise ParsingError("Empty Metadata!")
                    if trash and not trash.strip().startswith('#'):
                        raise ParsingError("Invalid Input after Metadata closed!")
                else:
                    raise ParsingError("Forget to close Metadata section!")
            else:
                raise ParsingError("Invalid Metadata, should be inside of [...]!")

        if metadata:
            self.valid_connection_metadata(metadata)
        zone1: Zone = self.graph.zones[name1]
        zone2: Zone = self.graph.zones[name2]
        connection.name = f"{name1}-{name2}"
        connection.zone1 = zone1
        connection.zone2 = zone2
        connection.max_link_capacity = self.max_link_capacity
        if name1 not in self.graph.connections:
            self.graph.connections[name1] = []
        if name2 not in self.graph.connections:
            self.graph.connections[name2] = []

        self.graph.connections[name1].append(connection)
        self.graph.connections[name2].append(connection)
        self.max_link_capacity = 1

    def parse(self, file_name: str) -> None:
        try:
            with open(file_name, 'r') as f:
                data: str = f.read()
            if not data.strip():
                raise ParsingError("Empty File!")
            self.lines = data.splitlines()
            self.nb_drones_parser()
            self.zone_checker()
            self.connection_checker()
            self.check_start_end()
            if self.connections < 1:
                raise ParsingError("Must be at least a connection!")
        except FileNotFoundError:
            print("Error: File Not found!\n")
            exit(1)
        except PermissionError:
            print("Error: File permission invalid!\n")
            exit(1)
        except (Exception, ParsingError) as e:
            print(f"Error: [line {self.line_idx + 1}] {e}\n")
            exit(1)
