#!/usr/bin/env python
# coding: utf-8
#
# Day 19: Tractor Beam
#
# https://adventofcode.com/2019/day/19
#
# By Stefan Kruger

from copy import deepcopy
from itertools import count
from intcode import read_program, resume


def is_affected(c, x, y):
    code = deepcopy(c)
    code[1] = 0
    code[2] = 0
    code[3] = [x, y]
    code[4] = []
    resume(code)

    return code[4][0]


def map_tractor_beam(c):
    affected = 0
    for y in range(50):
        for x in range(50):
            affected += is_affected(c, x, y)
    return affected


def fit_square(c, size):
    x = 0
    for y in count(100):
        for dx in count():
            if is_affected(c, x+dx, y):
                x += dx
                if is_affected(c, x + 99, y - 99):
                    return (x, y - 99)
                break


if __name__ == "__main__":
    code = read_program("data/input19.data")
    print(f"Part1: {map_tractor_beam(code)}")
    x, y = fit_square(code, 100)
    print(f"Part2: {x*10_000+y}")
