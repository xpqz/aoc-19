#!/usr/bin/env python
# coding: utf-8
#
# Day 10: Monitoring Station
#
# https://adventofcode.com/2019/day/10
#
# By Stefan Kruger

from collections import deque
from math import atan2, degrees, hypot
import itertools


def read_data(filename="data/input10.data"):
    with open(filename) as f:
        return f.read().splitlines()


def asteroids(rows):
    a = set()
    for y, row in enumerate(rows):
        for x, s in enumerate(list(row)):
            if s != ".":
                a.add((x, y))
    return a


def angle(a, b):
    return (360 + 90 + degrees(atan2(b[1] - a[1], b[0] - a[0]))) % 360


def get_visible(g, start):
    nodes = [
        (angle(start, end), hypot(end[0] - start[0], end[1] - start[1]), end)
        for end in g
        if end != start
    ]
    return [
        list(group)[0]
        for _, group in (itertools.groupby(sorted(nodes), lambda x: x[0]))
    ]


def find_best(g):
    return max([(len(get_visible(g, a)), a) for a in g], key=lambda x: x[0])


def engage_laser(g, monitor_astr):
    zapped = 1
    while len(g) > 2:
        visibles = deque(get_visible(g, monitor_astr))
        while len(visibles) > 1:
            ang, dist, n = visibles.popleft()
            if zapped == 200:
                return n
            g.remove(n)
            zapped += 1


if __name__ == "__main__":
    data = read_data()
    g = asteroids(data)

    viz_count, monitor_astr = find_best(g)
    print(f"Part1: {viz_count}")

    zapped = engage_laser(g, monitor_astr)
    print(f"Part2: {zapped[0]*100+zapped[1]}")
