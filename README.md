*This project has been created as part of the 42 curriculum by acherifi*

# Fly-in

## Description

Fly-in is a drone routing simulation. The program is built to solve Multi-Agent Path Finding problem (MAPF), which is multi moving entities are moving simultaneously from the start to the end
and we need to make sure there is no bottleneck or they crash on eachother and also make sure that each one of them uses the shortest path possible.

We used a graph network of zones and connections, and drones as the moving entities and simulate the movements from the start zone to the end, using only the fewest moves as possible.

The project is fully object-oriented and does not use any external library for
graph logic (no networkx, no graphlib). All parsing, graph, and pathfinding logic
is implemented from scratch.

## Instructions

### Requirements

- Python >=3.10
- Dependencies: `rich`, `webcolors`

### Install

```bash
make install
```

This installs the project dependencies.

### Run

```bash
make run
```

Or directly:

```bash
python3 fly-in.py <config_file>
```

Example:

```bash
python3 fly-in.py config.txt
```



## Map File Format

The map file describes the number of drones, the zones, and the connections
between them. Example:

```
nb_drones: 5

start_hub: hub 0 0 [color=green]
end_hub: goal 10 10 [color=yellow]
hub: roof1 3 4 [zone=restricted color=red]
hub: roof2 6 2 [zone=normal color=blue]
hub: corridorA 4 3 [zone=priority color=green max_drones=2]
hub: tunnelB 7 4 [zone=normal color=red]
hub: obstacleX 5 5 [zone=blocked color=gray]

connection: hub-roof1
connection: hub-corridorA
connection: roof1-roof2
connection: roof2-goal
connection: corridorA-tunnelB [max_link_capacity=2]
connection: tunnelB-goal
```

Zones can be `normal`, `blocked`, `restricted`, or `priority`. Each zone type has
a different movement cost, and zones or connections can define a maximum number
of drones can go through it at the same time.

## Algorithm Choices and Implementation Strategy

The project is split into four main parts:

- **Parsing (`parsing.py`)**: Reads the map file line by line, validates its
  syntax, and builds the `Graph` object (zones, connections, and metadata). Any
  invalid line raises a clear parsing error with the line number and cause.

- **Graph (`graph.py`)**: Holds the object-oriented data model of the
  simulation: `Zone`, `Connection`, `ZoneType`, `Drones`, and `Graph`. This is a
  simple data structure with no pathfinding logic of its own.

- **Pathfinding (`pathfinding.py`)**: Computes the shortest path for each
  drone using a Dijkstra-like search lying on turns, built with a priority queue (`heapq`) to get the shortest path based on zones cost. The
  search takes into account:
  - the movement cost of each zone type (normal, restricted, priority),
  - zone capacity (`max_drones`),
  - connection capacity (`max_link_capacity`),
  - reservations already made by previous drones, so later drones avoid
    conflicts with earlier ones.

  Each drone's path is reserved right after it is computed, so the next drone's
  found some zones and connections are already reserved for the past drone before it.
  This spreads drones across different paths instead of them all
  taking the exact same route.

- **Simulation (`simulation.py`)**: Moves every drone turn by turn following
  its computed path, prints the movement of each drone, and stops once all
  drones have reached the end zone.

## Visual Representation

The simulation prints each turn's drone movements directly to the terminal,
using the `rich` and `webcolors` libraries to color each zone name according to
its declared color in the map file. This makes it easier to follow which zone
each drone is moving into at a glance. A special `rainbow` color option is also
supported for visual variety.

## Example

Given a small map file `maps/easy1.txt` with two drones and a simple fork, the
program is run as:

```bash
python3 fly-in.py maps/easy/01_linear_path
```

Expected output (turn by turn drone movements):

```
D1-waypoint1 
D1-waypoint2 D2-waypoint1 
D1-goal D2-waypoint2 
D2-goal
```

Each line represents one simulation turn. Each entry follows the format
`D<ID>-<zone>` (or `D<ID>-<connection>` while a drone is still in transit toward
a restricted zone). Drones that do not move during a turn are simply omitted
from that turn's line, and drones are no longer tracked once they reach the end
zone.

## Resources

- [Graphs Explanation](https://www.youtube.com/watch?v=xN5VGzK9_FQ)
- [Fly-In Visualisation](https://fly-in-visualizer-42.vercel.app/)

### AI usage

- Helps with structure this README.
- Helps with docstrings and typehints.
- Helps with Explaining the MAPF problem.