from src.graph import Drones
import heapq


class Simulator():
    def __init__(self, graph, path_finder) -> None:
        self.graph = graph
        self.dijkstra = path_finder
        self.drones = list()

    # def create_drones(self):
    #     for id in range(self.graph.nb_drones):
    #         drone = Drones()
    #         drone.id = id + 1
    #         drone.name = f"D{id + 1}"
    #         # drone.current_zone = self.graph.start.name
    #         path = heapq.heappop(self.paths)
    #         drone.path = path
    #         drone.current_zone = path[1][0]
    #         path[0] += 1
    #         heapq.heappush(self.paths, path)
    #         self.drones.append(drone)

    def create_drones(self):
        for id in range(self.graph.nb_drones):
            drone = Drones()
            drone.id = id + 1
            drone.name = f"D{id + 1}"
            self.drones.append(drone)

    def assign_next_zones(self, drone):
        current_zone = drone.current_zone
        drone.visited_zones.append(current_zone)
        if current_zone == self.graph.end.name:
            drone.next_zone = ""
            drone.is_finished = True
            return
        # if not drone.next_zones:
        #     return
        # next_zones = dict(sorted(drone.next_zones.items(), key=lambda e: e[1]))
        # next_zone = list(next_zones)[0]
        drone.path_idx += 1
        id = drone.path_idx
        next_zone = drone.path[id]
        # print(f">>>>>>>>>>>>{next_zone}")
        drone.next_zone = next_zone
        # zone = self.graph.zones[next_zone]
        # zone.zone_queue.append(drone)

    def calculate_cost_path(self, valid_path):
        cost = 0
        for zone in valid_path:
            cost += self.graph.get_zone_cost(zone)
        next_zone = valid_path[0]
        zone_queue = self.graph.zones[next_zone].zone_queue
        if len(zone_queue) > 0:
            zone_type = self.graph.zones[next_zone].zone_type.value
            if zone_type == 'restricted':
                cost += len(zone_queue) * 2
            else:
                cost += len(zone_queue)
        return cost

    def extract_zones_neighbors(self, drone):
        current_zone = drone.current_zone
        for path in self.paths:
            path = path[1]
            if current_zone not in path:
                continue
            idx = path.index(current_zone)
            if current_zone == self.graph.end.name:
                continue
            valid_path = path[idx + 1:]
            next_zone = valid_path[0]
            if next_zone in drone.visited_zones:
                continue
            cost_path = self.calculate_cost_path(valid_path)
            if next_zone not in drone.next_zones:
                drone.next_zones[next_zone] = cost_path
            else:
                if drone.next_zones[next_zone] > cost_path:
                    drone.next_zones[next_zone] = cost_path

    def check_zone_availale(self, drone):
        next_zone = drone.next_zone
        if not next_zone:
            # zone = self.graph.zones[drone.current_zone]
            # if len(zone.zone_queue) > 0:
            #     zone.zone_queue.pop(0)
            drone.is_finished = True
            return False

        if drone.on_connection:
            return True
        zone = self.graph.zones[next_zone]
        if not zone.is_available:
            return False

        if zone.current_drones_count >= zone.max_drones:
            return False

        return True

    def move_next_zone(self, drone):
        move_name = ""
        current_zone = drone.current_zone
        next_zone = drone.next_zone
        zone_type = self.graph.zones[next_zone].zone_type.value
        zone = self.graph.zones[next_zone]

        if zone_type == 'restricted':
            # if drone.on_connection:
            #     drone.on_connection = False

            if not drone.on_connection:
                if zone.is_available:
                    drone.on_connection = True
                    zone.is_available = False
                    actual_next = f"{current_zone}-{next_zone}"
                    if "-" not in current_zone:
                        prev_zone = self.graph.zones[current_zone]
                        prev_zone.is_available = True
                        if prev_zone.current_drones_count > 0:
                            prev_zone.current_drones_count -= 1

                    drone.current_zone = actual_next
                    # drone.next_zone = ""
                    return f"{drone.name}-{actual_next} "
                else:
                    return ""

        if zone.zone_queue and zone.zone_queue[0].name == drone.name:
            zone.zone_queue.pop(0)

        if next_zone != self.graph.end.name:
            zone.is_available = False
            zone.current_drones_count += 1

        if "-" not in current_zone:
            prev_zone = self.graph.zones[current_zone]
            prev_zone.is_available = True
            if prev_zone.current_drones_count > 0:
                prev_zone.current_drones_count -= 1

        drone.current_zone = next_zone
        drone.next_zone = ""
        # drone.next_zones.clear()
        drone.on_connection = False

        return f"{drone.name}-{next_zone} "

    def start_simulation(self):
        self.create_drones()
        for drone in self.drones:
            path = self.dijkstra.shortest_path(drone)
            drone.path = path
            drone.current_zone = path[0]
            print("=========================")
            print(f"Drone: {drone.name}\nPath: {path}\n")
            print("=========================\n")
        exit()
        while not all(d.is_finished for d in self.drones):
            moves = ""
            for drone in self.drones:
                # if i >= 30:
                #     exit()
                # print(drone.name)
                if drone.is_finished:
                    # print("1")
                    continue
                if not drone.next_zone:
                    # print("2")
                    # self.extract_zones_neighbors(drone)
                    self.assign_next_zones(drone)

                if not self.check_zone_availale(drone):
                    # print("3")
                    continue
                move = self.move_next_zone(drone)
                # print("4")
                moves += move
            print(moves)

    # def move_next_zone(self, drone):
    #     previous_id = drone.path_idx
    #     is_connection = False
    #     if drone.current_zone not in drone.path:
    #         previous_id -= 1
    #         is_connection = True
    #     else:
    #         drone.path_idx += 1
    #     id = drone.path_idx
    #     zone = drone.path[id]
    #     zone_type = self.graph.zones[zone].zone_type.value
    #     previous_zone = drone.path[previous_id]
    #     zone_capacity = self.graph.zones[zone].max_drones
    #     zone_count = self.graph.zones[zone].current_drones_count
    #     drone.current_zone = zone
    #     if zone_type == 'restricted' and not is_connection:
    #         if self.graph.zones[zone].is_available:
    #             connection = f"{previous_zone}-{zone}"
    #             drone.current_zone = connection
    #             self.graph.zones[previous_zone].is_available = True
    #             return f"{drone.name}-{connection} "
    #         else:
    #             drone.current_zone = previous_zone
    #             drone.path_idx -= 1
    #     if zone != self.graph.end.name and zone_capacity <= zone_count:
    #         self.graph.zones[zone].is_available = False
    #     else:
    #         self.graph.zones[zone].max_drones += 1

    #     self.graph.zones[previous_zone].is_available = True
    #     if drone.path_idx == len(drone.path) - 1:
    #         drone.is_finished = True
    #     return f"{drone.name}-{zone} "

    # def assign_paths_drones(self):
    #     for id in range(self.graph.nb_drones):
    #         path = self.paths[id % len(self.paths)]
    #         name = f"D{id + 1}"
    #         drone = Drones(id + 1, path[1], name)
    #         self.drones.append(drone)
