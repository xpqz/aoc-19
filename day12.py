#!/usr/bin/env python
# coding: utf-8
#
# Day 12: The N-Body Problem
#
# https://adventofcode.com/2019/day/12
#
# By Stefan Kruger


from dataclasses import dataclass
from math import gcd
import re
from typing import Tuple


def cmp(b, a):
    return (a > b) - (a < b)


def lcm(x, y):
    return (x * y) // gcd(x, y)


@dataclass(frozen=True)
class Moon:
    position: Tuple[int, int, int]
    velocity: Tuple[int, int, int]

    def gravity(self, moon):
        return tuple([cmp(self.position[i], moon.position[i]) for i in [0, 1, 2]])

    def apply_gravity(self, dv):
        p = list(self.position)
        v = list(self.velocity)
        for i in [0, 1, 2]:
            v[i] += dv[i]
            p[i] += v[i]
        return Moon(position=tuple(p), velocity=tuple(v))

    def total_energy(self):
        return (
            sum([abs(i) for i in self.position]) *
            sum([abs(i) for i in self.velocity])
        )


def make_moons(data):
    positions = [
        [int(s) for s in re.findall(r'-?\d+', line)]
        for line in data
    ]

    return [
        Moon(position=p, velocity=(0, 0, 0))
        for p in positions
    ]


def apply_forces(moons):
    gravities = []
    for j, n in enumerate(moons):
        new_gravity = [0, 0, 0]
        for i, m in enumerate(moons):
            if j == i:
                continue
            g = n.gravity(m)
            for k in [0, 1, 2]:
                new_gravity[k] += g[k]
        gravities.append(new_gravity)

    return [
        m.apply_gravity(gravities[i])
        for i, m in enumerate(moons)
    ]


def find_periods(data):
    moons = make_moons(data)
    start_states = [
        tuple((m.position[i] for m in moons))
        for i in [0, 1, 2]
    ]
    periods = [-1, -1, -1]
    for i in range(1, 300_000):
        states = [
            tuple((m.position[i] for m in moons))
            for i in [0, 1, 2]
        ]

        if i > 1:
            for ii, st in enumerate(states):
                if periods[ii] == -1 and start_states[ii] == st:
                    periods[ii] = i
            if -1 not in periods:
                return periods

        moons = apply_forces(moons)


def find_energy(data, iterations):
    moons = make_moons(data)
    for i in range(1, iterations+1):
        moons = apply_forces(moons)
    return sum([m.total_energy() for m in moons])


if __name__ == "__main__":
    data = [
        "<x=-15, y=1, z=4>",
        "<x=1, y=-10, z=-8>",
        "<x=-5, y=4, z=9>",
        "<x=4, y=6, z=-2>"
    ]

    print(f"Part1: {find_energy(data, 1000)}")

    # Key insight: x, y and z are independent and periodic (or there would be no solution).
    # Find the common period

    periods = find_periods(data)
    steps = lcm(lcm(periods[0], periods[1]), periods[2])

    print(f"Part2: {steps}")
