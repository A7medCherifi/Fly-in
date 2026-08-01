from src.graph import Graph, ZoneType
import heapq


class Pathfinder():
    def __init__(self, graph: Graph):
        self.graph = graph
        self.zones = graph.zones
        self.algo_table = dict()
        self.paths = []
        self.turn_table = graph.turn_table
        self.conn_table = graph.conn_table

    def __build_algo_table(self):
        pass

    def get_neighbors(self, zone_key):
        pass

    def print_data(self):
        pass

    def is_map_possible(self):
        queue = [self.graph.start.name]
        visited = set([self.graph.start.name])

        while queue:
            current = queue.pop(0)

            if current == self.graph.end.name:
                return True

            for connection in self.graph.connections[current]:
                neighbor = connection.get_next_zone(current)

                if neighbor.zone_type == ZoneType.BLOCKED:
                    continue

                if neighbor.name not in visited:
                    visited.add(neighbor.name)
                    queue.append(neighbor.name)

        return False

    def shortest_path(self, drone):
        current = self.graph.start.name
        visited = set()
        turn = 0
        cost = self.graph.get_zone_cost(current)
        heap = [
            (cost, turn, current, [(current, turn)])
        ]

        if not self.is_map_possible():
            return None

        while heap:
            cost, turn, current, path = heapq.heappop(heap)
            if current == self.graph.end.name:
                return path

            zone_key = (current, turn)
            if zone_key in visited:
                continue

            visited.add(zone_key)
            connections = self.graph.connections[current]

            for connection in connections:
                neighbor = connection.get_next_zone(current)
                if neighbor.zone_type == ZoneType.BLOCKED:
                    continue

                neighbor_cost = self.graph.get_zone_cost(neighbor.name)
                is_restricted = False
                if neighbor_cost == 2:
                    is_restricted = True

                new_turn = turn + neighbor_cost
                if is_restricted:
                    is_avai = self.turn_table.get((neighbor.name, turn + 1), 0)
                    if is_avai:
                        continue

                conn_available = True
                for t in range(turn, new_turn):
                    conn_capcty = self.conn_table.get((connection.name, t), 0)
                    if conn_capcty >= connection.max_link_capacity:
                        conn_available = False
                        break

                if not conn_available:
                    continue

                # conn_capacity = self.conn_table.get(
                # (connection.name, new_turn), 0)
                # if conn_capacity >= connection.max_link_capacity:
                #     continue

                if neighbor.name != self.graph.end.name:
                    zone_capacity = self.turn_table.get(
                        (neighbor.name, new_turn), 0)
                    if zone_capacity >= neighbor.max_drones:
                        continue

                priority_zone = 0.0
                if neighbor.zone_type == ZoneType.PRIORITY:
                    priority_zone = -0.1

                final_cost = new_turn + cost + priority_zone
                new_path = path.copy()
                if is_restricted:
                    new_path.append((f"conn:{connection.name}", turn + 1))

                new_path.append((neighbor.name, new_turn))
                heapq.heappush(heap, (
                    final_cost,
                    new_turn,
                    neighbor.name,
                    new_path
                ))

            next_turn = turn + 1
            zone = self.graph.zones[current]
            if current == self.graph.start.name:
                can_wait = True

            else:
                zone_capacity = self.turn_table.get((current, next_turn), 0)
                if zone_capacity < zone.max_drones:
                    can_wait = True

                else:
                    can_wait = False

            if can_wait:
                new_path = path.copy()
                new_path.append((current, next_turn))
                heapq.heappush(heap, (
                    cost + 1,
                    next_turn,
                    current,
                    new_path
                ))
        return None

    def reserve_path(self, path):
        for i in range(len(path)):
            zone, turn = path[i]
            if zone.startswith("conn:"):
                connection = zone.split(':')[1]
                key = (connection, turn)
                self.conn_table[key] = self.conn_table.get(key, 0) + 1

            else:
                if zone not in [self.graph.end.name, self.graph.start.name]:
                    key = (zone, turn)
                    self.turn_table[key] = self.turn_table.get(key, 0) + 1


"""
# Easy Level 2: Simple fork with two paths
nb_drones: 4

start_hub: B 1 0 [color=yellow max_drones=2]
hub: C 2 1 [color=blue]
hub: G 3 1 [color=blue]
hub: X 4 1 [color=blue]
hub: Y 5 1 [color=blue]
hub: D 2 -1 [color=blue]
hub: F 5 -1 [color=blue]
end_hub: E 6 0 [color=red]

connection: B-C
connection: B-D
connection: D-F
connection: F-E
connection: C-G
connection: Y-E
connection: F-G
connection: G-X
connection: X-Y

"""
