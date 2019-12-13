#!/usr/bin/env python
# coding: utf-8
#
# Day 13: Care Package
#
# https://adventofcode.com/2019/day/13
#
# By Stefan Kruger

from intcode import run
from itertools import zip_longest


def read_data(filename="data/input13.data"):
    with open(filename) as f:
        return f.read()


def chunk(iterator, chunk_size):
    return zip_longest(*[iter(iterator)] * chunk_size)


if __name__ == "__main__":
    program = read_data()
    out = run(program, lambda: 0)
    blocks = sum(1 for item in chunk(out, 3) if item[2] == 2)
    print(blocks)
