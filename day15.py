#!/usr/bin/env python
# coding: utf-8
#
# Day 15: Oxygen System
#
# https://adventofcode.com/2019/day/15
#
# By Stefan Kruger

from collections import deque
from copy import deepcopy
import heapq
from intcode import read_program, resume


def follow_path(state, path):
    state[3] = path
    state[4] = []
    state = resume(state)

    return state


def neighbours(code, pos):

    def newpos(pos, d):
        delta = {1: (0, -1), 2: (0, 1), 3: (-1, 0), 4: (1, 0)}[d]
        return (pos[0] + delta[0], pos[1] + delta[1])

    result = []
    for d in [1, 2, 3, 4]:
        state = follow_path(deepcopy(code), [d])
        response = state[4][0]
        if response == 0:
            continue
        result.append((newpos(pos, d), d, int(response == 2)))

    return result


def unwind(came_from, start, end):
    current = end
    path = []

    while current != start:
        path.append(current)
        try:
            current = came_from[current]
        except KeyError:
            break

    path.append(start)
    path.reverse()

    return path


def breadth_first_search(code, start):
    """
    Save the intcode VM state at each point to make backtracking
    easier.
    """
    frontier = deque([(start, False, code, None)])
    came_from = {start: None}
    target = None

    while frontier:
        current, is_target, state, move = frontier.popleft()

        if is_target:
            target = current

        if move is not None:
            state = follow_path(deepcopy(state), [move])

        for n in neighbours(state, current):
            if n[0] not in came_from:
                frontier.append((n[0], n[2], state, n[1]))
                came_from[n[0]] = current

    return came_from, target


def dijkstra(empties, start, end):

    def ngs(p):
        return (i for i in {
            (p[0] - 1, p[1]),
            (p[0] + 1, p[1]),
            (p[0], p[1] - 1),
            (p[0], p[1] + 1)
            } if i in empties)

    frontier = []
    heapq.heappush(frontier, (0, start))
    came_from = {start: None}
    cost_so_far = {start: 0}

    while frontier:
        cur = heapq.heappop(frontier)[1]

        if cur == end:
            break

        for n in ngs(cur):
            new_cost = cost_so_far[cur] + 1
            if n not in cost_so_far or new_cost < cost_so_far[n]:
                cost_so_far[n] = new_cost
                heapq.heappush(frontier, (new_cost, n))
                came_from[n] = cur

    return came_from


if __name__ == "__main__":
    code = read_program("data/input15.data")

    start = (100, 100)
    came_from, oxyspout = breadth_first_search(code, start)
    path = unwind(came_from, start, oxyspout)
    path_len = len(path)
    print(f"Part1: {path_len-1}")

    empties = set(came_from.keys())

    max_path = 0
    for pos in empties:
        came_from = dijkstra(empties, oxyspout, pos)
        max_path = max(max_path, len(unwind(came_from, oxyspout, pos)))

    print(f"Part2: {max_path - 1}")
