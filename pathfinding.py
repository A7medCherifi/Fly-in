from graph import Graph, ZoneType, Zone, Connection
from typing import Dict, List, Optional, Set, Tuple
import heapq


class Pathfinder():
    """Finds the shortest path for a drone from start to end zone"""

    def __init__(self, graph: Graph) -> None:
        """Set up the pathfinder for a given graph.

        Args:
            graph: The Graph to search paths on.
        """
        self.graph: Graph = graph
        self.zones: Dict[str, Zone] = graph.zones
        self.turn_table: Dict[Tuple[str, int], int] = graph.turn_table
        self.conn_table: Dict[Tuple[str, int], int] = graph.conn_table

    def is_map_possible(self) -> bool:
        """Check if the end zone can be reached from the start zone

        Returns:
            True if a path exists from start to end, False if not.
        """
        start: str = self.graph.start.name
        queue: List[str] = [start]
        visited: Set[str] = set([start])

        if not self.graph.adjacency.get(start, None):
            raise Exception("Start zone dont have a connection!")

        while queue:
            current: str = queue.pop(0)

            if current == self.graph.end.name:
                return True

            for connection in self.graph.adjacency.get(current, []):
                neighbor: Zone = connection.get_next_zone(current)

                if neighbor.zone_type == ZoneType.BLOCKED:
                    continue

                if neighbor.name not in visited:
                    visited.add(neighbor.name)
                    queue.append(neighbor.name)

        return False

    def shortest_path(self) -> Optional[List[Tuple[str, int]]]:
        """Find the shortest path from start to end zone for one drone.

        Returns:
            A list of (zone, turn) path.
        """
        current: str = self.graph.start.name
        visited: Set[Tuple[str, int]] = set()
        turn: int = 0
        cost: float = self.graph.get_zone_cost(current)
        heap: List[Tuple[float, int, str, List[Tuple[str, int]]]] = [
            (cost, turn, current, [(current, turn)])
        ]

        if not self.is_map_possible():
            return None

        while heap:
            cost, turn, current, path = heapq.heappop(heap)
            if current == self.graph.end.name:
                break

            zone_key: Tuple[str, int] = (current, turn)
            if zone_key in visited:
                continue

            visited.add(zone_key)
            connections: List[Connection] = self.graph.adjacency[current]

            for connection in connections:
                neighbor = connection.get_next_zone(current)
                if neighbor.zone_type == ZoneType.BLOCKED:
                    continue

                neighbor_cost: int = self.graph.get_zone_cost(neighbor.name)
                is_restricted: bool = False
                if neighbor_cost == 2:
                    is_restricted = True

                new_turn: int = turn + neighbor_cost
                if is_restricted:
                    is_avai: int = self.turn_table.get(
                        (neighbor.name, turn + 1), 0)
                    if is_avai:
                        continue

                conn_available: bool = True
                conn_key: Tuple[str, int] = (connection.name, turn + 1)
                conn_capcty: int = self.conn_table.get(conn_key, 0)
                if conn_capcty >= connection.max_link_capacity:
                    conn_available = False
                    continue

                if neighbor.name != self.graph.end.name:
                    zone_key = (neighbor.name, new_turn)
                    zone_capacity: int = self.turn_table.get(zone_key, 0)
                    if zone_capacity >= neighbor.max_drones:
                        continue

                priority_zone: float = 0.0
                if neighbor.zone_type == ZoneType.PRIORITY:
                    priority_zone = -0.1

                final_cost: float = new_turn + cost + priority_zone
                new_path: List[Tuple[str, int]] = path.copy()
                if is_restricted:
                    new_path.append((f"res_conn:{connection.name}", turn + 1))

                if conn_available and not is_restricted:
                    new_path.append((f"conn:{connection.name}", turn + 1))

                new_path.append((neighbor.name, new_turn))
                heapq.heappush(heap, (
                    final_cost,
                    new_turn,
                    neighbor.name,
                    new_path
                ))

            next_turn: int = turn + 1
            new_path = path.copy()
            new_path.append((current, next_turn))
            heapq.heappush(heap, (
                cost + 1,
                next_turn,
                current,
                new_path
            ))

        return path

    def reserve_path(self, path: List[Tuple[str, int]]) -> None:
        """Mark a path as used so future drones avoid the same zones
        at spesific turnes.

        Args:
            path: The path to reserve
        """
        for i in range(len(path)):
            zone, turn = path[i]
            if zone.startswith("res_conn:") or zone.startswith("conn:"):
                connection: str = zone.partition(':')[2]
                key: Tuple[str, int] = (connection, turn)
                self.conn_table[key] = self.conn_table.get(key, 0) + 1

            else:
                if zone not in [self.graph.end.name, self.graph.start.name]:
                    key = (zone, turn)
                    self.turn_table[key] = self.turn_table.get(key, 0) + 1
