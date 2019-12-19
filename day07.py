#!/usr/bin/env python
# coding: utf-8
#
# Day 7: Amplification Circuit
#
# https://adventofcode.com/2019/day/7
#
# By Stefan Kruger

from copy import deepcopy
from itertools import permutations
from intcode import read_program, resume


def run_amplifiers(data, phases):
    amps = [deepcopy(data) for _ in range(5)]

    for phase, amp in zip(phases, amps):
        amp[3].append(phase)
        resume(amp)

    amps[0][3].append(0)
    resume(amps[0])

    while not amps[4][5]:
        for i, amp in enumerate(amps):
            amps[(i + 1) % 5][3].append(amp[4][-1])
            resume(amps[(i + 1) % 5])

    return amps[4][4][-1]


if __name__ == "__main__":
    d = read_program("data/input07.data")
    part1 = max(
        run_amplifiers(d, phases)
        for phases in permutations(range(5))
    )

    print(f"Part1: {part1}")
    part2 = max(
        run_amplifiers(d, phases)
        for phases in permutations(range(5, 10))
    )
    print(f"Part2: {part2}")
