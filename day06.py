#!/usr/bin/env python
# coding: utf-8
#
# Day 6: Universal Orbit Map
#
# https://adventofcode.com/2019/day/6
#
# By Stefan Kruger

from collections import defaultdict, deque


def unwind_path(came_from, start, end):
    current = end
    path = []

    while current != start:
        path.append(current)
        current = came_from[current]
    return path


def breadth_first_search(graph, start, end):
    frontier = deque([start])
    came_from = {start: None}

    while frontier:
        current = frontier.popleft()

        if current == end:
            break

        if current in graph:
            for neighbour in graph[current]:
                if neighbour not in came_from:
                    frontier.append(neighbour)
                    came_from[neighbour] = current

    return unwind_path(came_from, start, end)


def build_graph(data):
    graph = defaultdict(set)
    centres = {}
    for node in data:
        inner, outer = node.split(")")
        graph[inner].add(outer)
        graph[outer].add(inner)
        centres[outer] = inner
    return graph, centres


def path_length(orbits, key, total=0):
    if key == "COM":
        return total
    return path_length(orbits, orbits[key], total+1)


def total_orbits(orbits):
    total = 0
    for key in orbits.keys():
        total += path_length(orbits, key)
    return total


def read_data(filename="data/input06.data"):
    with open(filename) as f:
        return f.read().splitlines()


if __name__ == "__main__":
    g, orbits = build_graph(read_data())
    print(f"Part1: {total_orbits(orbits)}")
    came_from = breadth_first_search(g, "YOU", "SAN")
    print(f"Part2: {len(came_from)-2}")
