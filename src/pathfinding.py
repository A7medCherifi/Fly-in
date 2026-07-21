from src.graph import Graph
import heapq


class Pathfinder():
    def __init__(self, graph: Graph):
        self.path = list()
        self.graph = graph
        self.visited = set()
        self.tracker = dict()
        self.queue = []

    def dijkstra(self):
        grid = self.graph.grid
        start_zone = self.graph.get_start_zone()
        end_zone = self.graph.get_end_zone()
        costs = {zone: float('inf') for zone in grid}
        costs[start_zone] = 0

        heapq.heappush(self.queue, [0, 0, start_zone, None])
        while len(self.visited) < len(grid):
            if not self.queue:
                print("Error: Zone permession denied!")
                exit(1)
            cost, _, current, previous = heapq.heappop(self.queue)
            if current in self.visited:
                continue
            self.visited.add(current)
            self.tracker[current] = previous
            if current == end_zone:
                break

            zone = grid[current]
            for neighbor in zone['neighbor']:
                name = neighbor[0]
                neighbor_cost = neighbor[1]
                new_cost = neighbor_cost + cost

                if name in self.visited or neighbor_cost == -1:
                    continue

                if new_cost >= costs[name]:
                    continue
                costs[name] = new_cost
                zone_prefered = 1
                zone_type = grid[name]['metadata']['zone']
                if zone_type == 'priority':
                    zone_prefered = 0

                heapq.heappush(self.queue,
                               [new_cost, zone_prefered, name, current])

        if end_zone not in self.tracker:
            print("Error: Zone permission denied!")
            exit(1)

        self.get_path()
        print(len(self.path))
        return

        # previous = None
        # current = start_zone
        # zone = grid[current]

        # while len(self.visited) < len(grid):
        #     self.visited.add(zone['name'])
        #     if current == end_zone:
        #         self.tracker[zone['name']] = [previous, None]
        #         heapq.heappop(self.queue)
        #         break
        #     for neighbor in zone['neighbor']:
        #         name = neighbor[0]
        #         cost = neighbor[1] + costs[current]
        #         if costs[name] and cost > costs[name]:
        #             continue
        #         costs[name] = cost
        #         zone_prefered = 1
        #         zone_type = grid[name]['metadata']['zone']
        #         if zone_type == 'priority':
        #             zone_prefered = 0
        #         if name in self.visited or cost == -1:
        #             continue
        #         print(f"Current: {current}")
        #         print(f"Next: {name}")
        #         print(f"{neighbor[1]} + {costs[current]} = {cost}")
        #         heapq.heappush(self.queue, [cost, zone_prefered, current,
        #                                     name])
        #         print(f"{self.queue}\n")

        #     if not self.queue:
        #         print("Error: Zone permession denied!")
        #         exit(1)

        #     next = self.queue[0][3]
        #  print(f"\nCurrent Zone: {current} -> {costs[current]} -> {next}")
        #     self.tracker[zone['name']] = [previous, next]
        #     previous = self.queue[0][2]
        #     current = next
        #     heapq.heappop(self.queue)
        #     zone = grid[current]

        # self.get_path()

        # return

    def get_path(self):
        end = self.graph.get_end_zone()
        start = self.graph.get_start_zone()

        self.path.insert(0, end)
        for _ in range(len(self.tracker)):
            previous = self.tracker[end]
            self.path.insert(0, previous)
            if previous == start:
                break
            end = previous

    # def heapify(self, current, neighbor, cost, zone_prefered):
    #     if not self.queue:
    #         self.queue.append([current, neighbor, cost])
    #     elif self.queue[0][2] > cost:
    #         self.queue.insert(0, [current, neighbor, cost])
    #     elif self.queue[0][2] == cost and zone_prefered:
    #         self.queue.insert(0, [current, neighbor, cost])
    #     else:
    #         self.queue.append([current, neighbor, cost])
