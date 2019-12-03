#!/usr/bin/env python
# coding: utf-8
#
# Advent of Code 2019
#
# Day 3: Crossed Wires
#
# https://adventofcode.com/2019/day/3
#
# By Stefan Kruger

from collections import Counter

def read_data(filename="data/input03.data"):
    with open(filename) as f:
        return [s.split(",") for s in f.readlines()]


def trace_route(route):
    visited = Counter()
    x, y = 0, 0
    for n in route:
        direction, dist = n[:1], int(n[1:])
        for _ in range(dist):
            if direction == "U":
                y += 1
            elif direction == "D":
                y -= 1
            elif direction == "R":
                x += 1
            else:
                x -= 1
            visited[(x, y)] = 1
    return visited


def count_steps(route, pos):
    x, y = 0, 0
    steps = 0
    for n in route:
        direction, dist = n[:1], int(n[1:])
        for _ in range(dist):
            if direction == "U":
                y += 1
            elif direction == "D":
                y -= 1
            elif direction == "R":
                x += 1
            else:
                x -= 1
            steps += 1
            if (x, y) == pos:
                return steps
                
    raise Exception(f"Pos {pos} not visited")


def find_intersections(routes):
    visited = trace_route(routes[0])
    visited.update(trace_route(routes[1]))
    
    best = None
    for p in visited.most_common():
        if p[1] < 2:
            break
        d = abs(p[0][0]) + abs(p[0][1])
        if best is None or d < best:
            best = d
            
    return best, {p[0] for p in visited.most_common() if p[1] > 1}


def shortest_path(routes, intersects):
    mdist = None
    for pos in intersects:
        total = count_steps(routes[0], pos) + count_steps(routes[1], pos)
        if mdist is None or total < mdist:
            mdist = total
    return mdist


if __name__ == "__main__":
    r = read_data()
    best, intersections = find_intersections(r)
    print(f"Part1: {best}")
    print(f"Part2: {shortest_path(r, intersections)}")

