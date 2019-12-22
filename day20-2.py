from collections import defaultdict
import heapq
from string import ascii_uppercase


def read_data(filename="data/input20.data"):
    with open(filename) as f:
        return [list(row) for row in f.read().splitlines()]


def level_change(is_internal):
    if is_internal:
        return 1
    return -1


def portal_tile(data, pos):
    x, y = pos
    if data[y][x - 1] == ".":
        # Floor to the left. Are we at near the outer edge?
        return (x - 1, y), x + 2 < len(data[0])    # True == internal

    if data[y][x + 2] == ".":
        # Floor to the right.
        return (x + 2, y), x > 0  # True == internal

    if data[y - 1][x] == ".":
        # Floor above.
        return (x, y - 1), y + 2 < len(data) # True == internal

    if data[y + 2][x] == ".":
        # Floor below.
        return (x, y + 2), y > 0  # True == internal

    raise Exception("Unable to find portal coord")


def make_graph(data):
    """
    Part 2: portals are directional
    """

    g = {}
    portals = []
    external_doors = {}
    for y, row in enumerate(data):
        for x, ch in enumerate(row):
            if ch in " #":
                continue
            if ch == ".":
                g[(x, y)] = set()
            elif ch in ascii_uppercase:
                portals.append((x, y))

    # tie up normal connections
    for (x, y) in g.keys():
        for d in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            n_pos = (x + d[0], y + d[1])
            if n_pos in g:
                g[(x, y)].add((n_pos, 0))

    # tie up portals
    connected = defaultdict(set)
    done = set()
    for (x, y) in portals:
        if (x, y) in done:
            continue
        right = (x + 1, y)
        below = (x, y + 1)
        tile, is_internal = portal_tile(data, (x, y))

        if right in portals or below in portals:
            if right in portals:
                name = data[y][x] + data[y][x + 1]
                exclude = right
            else:
                name = data[y][x] + data[y + 1][x]
                exclude = below

            if name in {"AA", "ZZ"}:
                external_doors[name] = tile
            else:
                connected[name].add((tile, is_internal))

            done.add(exclude)
        else:
            raise Exception(f"Unable to connect portal: {(x, y)}")

        if len(connected[name]) == 2:
            (a, a_is_internal), (b, b_is_internal) = tuple(connected[name])
            assert a_is_internal != b_is_internal

            g[a].add((b, level_change(a_is_internal)))
            g[b].add((a, level_change(b_is_internal)))

    return g, external_doors["AA"], external_doors["ZZ"]


def unwind(came_from, s, e):
    start = (s, 0)
    end = (e, 0)

    current = end
    path = []

    while current != start:
        path.append(current)
        try:
            current = came_from[current]
        except KeyError:
            break

    path.reverse()

    return path


def dijkstra(graph, start, end):

    frontier = []
    heapq.heappush(frontier, (0, (start, 0)))
    came_from = {(start, 0): None}
    cost_so_far = {(start, 0): 0}

    while frontier:
        (cur, level) = heapq.heappop(frontier)[1]

        if (cur, level) == (end, 0):
            break

        for (n, delta) in graph[cur]:
            new_level = level + delta
            if new_level < 0:
                continue
            new_cost = cost_so_far[(cur, level)] + 1
            if (n, new_level) not in cost_so_far or new_cost < cost_so_far[(n, new_level)]:
                cost_so_far[(n, new_level)] = new_cost
                heapq.heappush(frontier, (new_cost, (n, new_level)))
                came_from[(n, new_level)] = (cur, level)

    return came_from


if __name__ == "__main__":
    data = read_data()
    g, start, end = make_graph(data)

    came_from = dijkstra(g, start, end)
    path = unwind(came_from, start, end)

    print(f"Part2: {len(path)}")
