from collections import defaultdict
import heapq
from string import ascii_uppercase


def read_data(filename="data/input20.data"):
    with open(filename) as f:
        return [list(row) for row in f.read().splitlines()]


def portal_tile(data, pos):
    x, y = pos
    if data[y][x - 1] == ".":
        return (x - 1, y)

    if data[y][x + 2] == ".":
        return (x + 2, y)

    if data[y-1][x] == ".":
        return (x, y-1)

    if data[y+2][x] == ".":
        return (x, y + 2)

    raise Exception("Unable to find portal coord")


def make_graph(data):
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
                g[(x, y)].add(n_pos)

    # tie up portals
    connected = defaultdict(set)
    done = set()
    for (x, y) in portals:
        if (x, y) in done:
            continue
        right = (x + 1, y)
        below = (x, y + 1)
        tile = portal_tile(data, (x, y))

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
                connected[name].add(tile)

            done.add(exclude)
        else:
            raise Exception(f"Unable to connect portal: {(x, y)}")

        if len(connected[name]) == 2:
            (a, b) = tuple(connected[name])
            g[a].add(b)
            g[b].add(a)

    return g, external_doors["AA"], external_doors["ZZ"]


def unwind(came_from, start, end):
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
    heapq.heappush(frontier, (0, start))
    came_from = {start: None}
    cost_so_far = {start: 0}

    while frontier:
        cur = heapq.heappop(frontier)[1]

        if cur == end:
            break

        for n in graph[cur]:
            new_cost = cost_so_far[cur] + 1
            if n not in cost_so_far or new_cost < cost_so_far[n]:
                cost_so_far[n] = new_cost
                heapq.heappush(frontier, (new_cost, n))
                came_from[n] = cur

    return came_from


if __name__ == "__main__":
    data = read_data()

    g, start, end = make_graph(data)

    came_from = dijkstra(g, start, end)
    path = unwind(came_from, start, end)

    print(f"Part1: {len(path)}")
